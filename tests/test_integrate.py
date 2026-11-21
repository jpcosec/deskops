"""`deskops integrate` against real git, a real desk and a bare remote in tmp_path."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from tests.activation_receipts import accept_receipts

ROOT = Path(__file__).resolve().parents[1]
TASK = "task-foo"
BRANCH = "main"


def _git(cwd: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=cwd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _cli(root: Path, *argv: str, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    full_env = {k: v for k, v in os.environ.items() if not k.startswith("DESKOPS_")}
    full_env["PYTHONPATH"] = str(ROOT) + os.pathsep + full_env.get("PYTHONPATH", "")
    full_env.update(env or {})
    result = subprocess.run([sys.executable, "-m", "deskops", *argv], cwd=root, capture_output=True, text=True, env=full_env)
    if check:
        assert result.returncode == 0, result.stderr or result.stdout
    return result


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _configure(root: Path, suite: list[str] | None = None, **extra: object) -> None:
    config_path = root / "desk" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["queue_min_available_gb"] = 0
    config["queue_max_psi_avg60"] = 101
    config["integrate"] = {
        "remote_url": str(root.parent / "remote.git"),
        "branch": BRANCH,
        "suite": suite or ["sh", "-c", "exit 0"],
        **extra,
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")


def _build(tmp_path: Path) -> tuple[Path, Path]:
    """Build once (slow: real `deskops init` and lifecycle): (unclosed snapshot, closed repo), each with its remote."""
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", BRANCH)
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _write(root / "seed.txt", "seed\n")
    _git(root, "add", "seed.txt")
    _git(root, "commit", "-q", "-m", "seed")
    _cli(root, "init", str(root))
    _cli(
        root, "add", "atom", "--root", str(root), "--title", "Integrate evidence", "--five-wh-one-plus", "what",
        "--answer", "The integration is exercised against a bare remote.",
    )
    _cli(
        root, "add", "task", "--root", str(root),
        json.dumps({"id": TASK, "title": "Foo", "goal": "g", "scope": "s", "implementation_path": "i",
                    "done_when": "d", "validation": ["pytest"], "task_type": "task.code"}),
    )
    accept_receipts(root, TASK)
    _write(root / "tests" / "test_smoke.py", "def test_smoke():\n    assert True\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    remote = tmp_path / "remote.git"
    _git(tmp_path, "init", "-q", "--bare", "-b", BRANCH, str(remote))
    _git(root, "push", "-q", str(remote), f"HEAD:{BRANCH}")

    _cli(root, "advance", "task", TASK, "--root", str(root))
    _cli(root, "advance", "task", TASK, "--root", str(root))
    _write(root / "feature.py", "VALUE = 1\n")
    _git(root, "add", "feature.py")
    _git(root, "commit", "-q", "-m", "feature")
    code = _git(root, "rev-parse", "HEAD")
    _cli(
        root, "edit", "task", TASK, "references",
        json.dumps(["desk/atoms/atom-integrate-evidence.md", "pytest tests/test_smoke.py::test_smoke", code]),
        "--root", str(root),
    )
    _cli(root, "edit", "task", TASK, "files", json.dumps(["desk/atoms/atom-integrate-evidence.md"]), "--root", str(root))
    unclosed = tmp_path.parent / (tmp_path.name + "-unclosed")
    shutil.copytree(tmp_path, unclosed, symlinks=True)
    _cli(root, "closeout", "verify", "--root", str(root), "--task", TASK, check=False)
    _cli(
        root, "closeout", "commit", "--root", str(root), "--task", TASK, "--no-run",
        "--reason", "integrate test", "--paths", "desk", ".sldb",
    )
    return unclosed, tmp_path


@pytest.fixture(scope="module")
def _templates(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, Path]:
    return _build(tmp_path_factory.mktemp("integrate-template"))


def _copy(template: Path, tmp_path: Path) -> Path:
    for name in ("repo", "remote.git"):
        shutil.copytree(template / name, tmp_path / name, symlinks=True)
    root = tmp_path / "repo"
    _configure(root)
    return root


@pytest.fixture
def closed(_templates: tuple[Path, Path], tmp_path: Path) -> Path:
    return _copy(_templates[1], tmp_path)


@pytest.fixture
def unclosed(_templates: tuple[Path, Path], tmp_path: Path) -> Path:
    return _copy(_templates[0], tmp_path)


def _integrate(root: Path, *extra: str, tmpdir: Path | None = None) -> subprocess.CompletedProcess[str]:
    tmp = tmpdir or root.parent / "tmpdir"
    tmp.mkdir(exist_ok=True)
    return _cli(root, "integrate", "--task", TASK, "--root", ".", *extra, env={"TMPDIR": str(tmp)}, check=False)


def _remote_head(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "-q", BRANCH], cwd=root.parent / "remote.git", capture_output=True, text=True
    )
    return result.stdout.strip() or None


def _find(root: Path, subject: str) -> str:
    return _git(root, "log", "-1", "--format=%H", "--fixed-strings", f"--grep={subject}")


def _leftovers(root: Path) -> list[str]:
    return sorted(p.name for p in (root.parent / "tmpdir").iterdir())


def _events(root: Path) -> list[str]:
    return (root / "runs" / "hooks" / "events.log").read_text(encoding="utf-8").splitlines()


def test_green_gates_push_code_and_tip(closed: Path, tmp_path: Path) -> None:
    root = closed
    tip = _git(root, "rev-parse", "HEAD")
    assert _git(root, "log", "-1", "--format=%s") == f"closeout: {TASK}"
    code = _find(root, "feature")
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == f"integrado {code[:12]} {tip[:12]} en {BRANCH}"
    assert _remote_head(root) == tip
    remote = root.parent / "remote.git"
    assert _git(remote, "merge-base", "--is-ancestor", code, tip) == ""
    assert _events(root)[-1].endswith(f" {TASK} integrate ok {tip[:12]}")
    assert (root / "runs" / "queue" / "logs" / f"integrate-{TASK}.log").exists()
    assert _leftovers(root) == []


def test_task_from_env_is_equivalent(closed: Path, tmp_path: Path) -> None:
    root = closed
    tmp = tmp_path / "tmpdir"
    tmp.mkdir()
    result = _cli(root, "integrate", "--task-from-env", "--root", ".", env={"DESKOPS_TASK_ID": TASK, "TMPDIR": str(tmp)}, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.startswith("integrado ")
    assert _remote_head(root) == _git(root, "rev-parse", "HEAD")


def test_dry_run_leaves_the_remote_and_prints_both_pushes(closed: Path, tmp_path: Path) -> None:
    root = closed
    before = _remote_head(root)
    tip = _git(root, "rev-parse", "HEAD")
    code = _find(root, "feature")
    tools = tmp_path / "tools"
    _git(tmp_path, "clone", "-q", str(root.parent / "remote.git"), str(tools))
    tools_before = _git(tools, "rev-parse", "HEAD")
    _configure(root, tools_checkout=str(tools))
    result = _integrate(root, "--dry-run")
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"git push origin {code}:{BRANCH}" in result.stdout
    assert f"git push origin {tip}:{BRANCH}" in result.stdout
    assert result.stdout.index(code) < result.stdout.index(tip)
    assert _remote_head(root) == before
    assert _git(tools, "rev-parse", "HEAD") == tools_before
    assert _leftovers(root) == []


def test_tools_checkout_follows_the_remote_after_push(closed: Path, tmp_path: Path) -> None:
    root = closed
    tools = tmp_path / "tools"
    _git(tmp_path, "clone", "-q", str(root.parent / "remote.git"), str(tools))
    _configure(root, tools_checkout=str(tools))
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(tools, "rev-parse", "HEAD") == _git(root, "rev-parse", "HEAD")


def test_failing_suite_stops_before_any_push(closed: Path, tmp_path: Path) -> None:
    root = closed
    before = _remote_head(root)
    _configure(root, suite=["sh", "-c", "echo roto; exit 1"])
    result = _integrate(root)
    assert result.returncode == 1
    assert "fallo: suite: " in result.stdout
    assert _remote_head(root) == before
    assert "roto" in (root / "runs" / "queue" / "logs" / f"integrate-{TASK}.log").read_text(encoding="utf-8")
    assert " integrate fallo:suite " in _events(root)[-1]
    assert _leftovers(root) == []


def test_suite_timeout_is_reported(closed: Path, tmp_path: Path) -> None:
    root = closed
    _configure(root, suite=["sh", "-c", "sleep 30"], suite_timeout=1)
    result = _integrate(root)
    assert result.returncode == 1
    assert "fallo: suite: timeout tras 1 s" in result.stdout


def test_suite_runs_under_the_declared_lock_with_pythonpath_of_the_copy(closed: Path, tmp_path: Path) -> None:
    root = closed
    probe = tmp_path / "probe.txt"
    lock = tmp_path / "locks" / "tests.lock"
    _configure(root, suite=["sh", "-c", f'echo "$PYTHONPATH" > {probe}'], tests_lock=str(lock))
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert lock.exists()
    assert probe.read_text(encoding="utf-8").strip().startswith(str(tmp_path / "tmpdir"))


def test_range_touching_only_desk_does_not_run_the_suite(closed: Path, tmp_path: Path) -> None:
    root = closed
    # The remote already has the code commit: what is left to publish is only the closeout (desk, .sldb, runs).
    code = _find(root, "feature")
    _git(root, "push", "-q", str(root.parent / "remote.git"), f"{code}:{BRANCH}")
    _configure(root, suite=["sh", "-c", "exit 1"])
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "integrado " in result.stdout
    assert not (root / "runs" / "queue" / "logs" / f"integrate-{TASK}.log").exists()


def test_code_already_behind_origin_main_is_not_pushed(closed: Path, tmp_path: Path) -> None:
    root = closed
    tip = _git(root, "rev-parse", "HEAD")
    code = _find(root, "feature")
    # origin/main is ahead of the code commit (it holds a descendant): pushing code:main would be non-fast-forward.
    # Rebuild the tip on top of an extra empty commit that the remote already has.
    extra = _git(root, "commit-tree", f"{code}^{{tree}}", "-p", code, "-m", "other task tip")
    tip = _git(root, "commit-tree", f"{tip}^{{tree}}", "-p", extra, "-m", f"closeout: {TASK}")
    _git(root, "reset", "-q", "--hard", tip)
    _configure(root)
    _git(root, "push", "-q", str(root.parent / "remote.git"), f"{extra}:{BRANCH}")
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"código ya en origin: {code[:12]}" in result.stdout
    assert result.stdout.strip().splitlines()[-1] == f"integrado {code[:12]} {tip[:12]} en {BRANCH}"
    assert _remote_head(root) == tip


def test_a_tip_that_is_not_fast_forward_fails(closed: Path, tmp_path: Path) -> None:
    root = closed
    side = tmp_path / "side"
    _git(tmp_path, "clone", "-q", str(root.parent / "remote.git"), str(side))
    _git(side, "config", "user.email", "o@example.com")
    _git(side, "config", "user.name", "Other")
    _git(side, "commit", "-q", "--allow-empty", "-m", "elsewhere")
    _git(side, "push", "-q", "origin", f"HEAD:{BRANCH}")
    before = _remote_head(root)
    result = _integrate(root)
    assert result.returncode == 1
    assert "fallo: fast-forward" in result.stdout
    assert _remote_head(root) == before
    assert _leftovers(root) == []


def test_a_store_path_missing_in_the_commit_fails(closed: Path, tmp_path: Path) -> None:
    root = closed
    store_path = root / ".sldb" / "store.yaml"
    store = yaml.safe_load(store_path.read_text(encoding="utf-8"))
    store["links"] = [*store.get("links", []), {"name": "ghost", "path": "ghost/absent.yaml"}]
    store_path.write_text(yaml.safe_dump(store, sort_keys=False), encoding="utf-8")
    _git(root, "add", ".sldb/store.yaml")
    _git(root, "commit", "-q", "--amend", "--no-edit")
    before = _remote_head(root)
    result = _integrate(root)
    assert result.returncode == 1
    assert "fallo: store: " in result.stdout and "ghost/absent.yaml" in result.stdout
    assert _remote_head(root) == before


def test_an_unclosed_task_exits_2(unclosed: Path, tmp_path: Path) -> None:
    root = unclosed
    result = _integrate(root)
    assert result.returncode == 2
    assert "no esta cerrada" in result.stdout
    assert not (root / "runs" / "hooks" / "events.log").exists()


def test_a_closed_task_without_code_commit_exits_2(unclosed: Path, tmp_path: Path) -> None:
    root = unclosed
    _cli(root, "edit", "task", TASK, "references", json.dumps(["desk/atoms/atom-integrate-evidence.md"]), "--root", str(root))
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "refs")
    _git(root, "commit", "-q", "--allow-empty", "-m", f"closeout: {TASK}")
    _git(root, "rm", "-q", "-f", f"desk/tasks/{TASK}.md")
    _git(root, "commit", "-q", "--amend", "--no-edit")
    result = _integrate(root)
    assert result.returncode == 2
    assert "falta el commit de codigo en references" in result.stdout


def test_missing_integrate_field_exits_2(closed: Path, tmp_path: Path) -> None:
    root = closed
    config_path = root / "desk" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    del config["integrate"]
    config_path.write_text(json.dumps(config), encoding="utf-8")
    result = _integrate(root)
    assert result.returncode == 2
    assert "falta el campo integrate en desk/config.json" in result.stdout


@pytest.mark.parametrize(
    "argv, env",
    [
        ([], {}),
        (["--task", TASK, "--task-from-env"], {"DESKOPS_TASK_ID": TASK}),
        (["--task-from-env"], {"DESKOPS_TASK_ID": ""}),
    ],
)
def test_task_selection_errors_exit_2(closed: Path, argv: list[str], env: dict[str, str]) -> None:
    root = closed
    result = _cli(root, "integrate", *argv, "--root", ".", env=env, check=False)
    assert result.returncode == 2, result.stdout + result.stderr


def test_memory_gate_fails_the_first_step(closed: Path, tmp_path: Path) -> None:
    root = closed
    config_path = root / "desk" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["queue_min_available_gb"] = 100000
    config_path.write_text(json.dumps(config), encoding="utf-8")
    result = _integrate(root)
    assert result.returncode == 1
    assert "fallo: memoria: " in result.stdout
    assert _remote_head(root) != _git(root, "rev-parse", "HEAD")
    assert _leftovers(root) == []


def test_push_env_reaches_the_push_commands(closed: Path, tmp_path: Path) -> None:
    root = closed
    hooks = tmp_path / "remote.git" / "hooks"
    marker = tmp_path / "marker.txt"
    hook = hooks / "pre-receive"
    hook.write_text(f'#!/bin/sh\necho "$INTEGRATE_MARK" >> {marker}\n', encoding="utf-8")
    hook.chmod(0o755)
    _configure(root, push_env={"INTEGRATE_MARK": "visible"})
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert marker.read_text(encoding="utf-8").split() == ["visible", "visible"]


def test_a_tip_already_on_the_remote_is_a_noop(closed: Path, tmp_path: Path) -> None:
    root = closed
    tip = _git(root, "rev-parse", "HEAD")
    first = _integrate(root)
    assert first.returncode == 0, first.stdout + first.stderr
    second = _integrate(root)
    assert second.returncode == 0, second.stdout + second.stderr
    assert second.stdout.strip() == f"ya integrado: {tip[:12]}"
    assert _remote_head(root) == tip
    assert _events(root)[-1].endswith(f" {TASK} integrate ya-integrado {tip[:12]}")
    assert _leftovers(root) == []


def _dangling_closeout(root: Path) -> str:
    """Amend the closeout commit so it carries a task with a dangling file reference; returns the tip."""
    other = {"id": "task-old", "title": "Old", "goal": "g", "scope": "s", "implementation_path": "i",
             "done_when": "d", "validation": ["pytest"], "task_type": "task.code"}
    _cli(root, "add", "task", "--root", str(root), json.dumps(other))
    _cli(root, "edit", "task", "task-old", "files", json.dumps(["desk/ghost-absent.md"]), "--root", str(root))
    _git(root, "add", "desk", ".sldb")
    _git(root, "commit", "-q", "--amend", "--no-edit")
    return _git(root, "rev-parse", "HEAD")


def test_tip_extends_over_later_desk_only_commits(closed: Path, tmp_path: Path) -> None:
    root = closed
    tip = _dangling_closeout(root)
    before = _remote_head(root)
    failed = _integrate(root)
    assert failed.returncode == 1 and "fallo: graph" in failed.stdout
    assert _remote_head(root) == before
    _cli(root, "edit", "task", "task-old", "files", json.dumps([]), "--root", str(root))
    _git(root, "add", "desk", ".sldb")
    _git(root, "commit", "-q", "-m", "desk: retire dangling reference")
    head = _git(root, "rev-parse", "HEAD")
    assert head != tip
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"tip extendido a {head[:12]}: solo commits de desk" in result.stdout
    assert _remote_head(root) == head


def _remote_code_commit(root: Path) -> None:
    """Another person pushes a code commit to the bare remote."""
    other = root.parent / "other"
    _git(root.parent, "clone", "-q", str(root.parent / "remote.git"), str(other))
    _write(other / "src" / "remote_code.py", "R = 1\n")
    _git(other, "add", "src/remote_code.py")
    _git(other, "commit", "-q", "-m", "remote code")
    _git(other, "push", "-q", "origin", f"HEAD:{BRANCH}")


def test_tip_extends_over_a_merge_of_the_remote_branch(closed: Path, tmp_path: Path) -> None:
    root = closed
    _dangling_closeout(root)
    _remote_code_commit(root)
    _git(root, "fetch", "-q", str(root.parent / "remote.git"), BRANCH)
    _git(root, "merge", "-q", "--no-ff", "-m", "merge remote", "FETCH_HEAD")
    _cli(root, "edit", "task", "task-old", "files", json.dumps([]), "--root", str(root))
    _git(root, "add", "desk", ".sldb")
    _git(root, "commit", "-q", "-m", "desk: retire dangling reference")
    head = _git(root, "rev-parse", "HEAD")
    result = _integrate(root, "--dry-run")
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"tip extendido a {head[:12]}: solo commits de desk" in result.stdout
    assert "fast-forward" not in result.stdout


def test_tip_stays_when_a_local_code_commit_follows_a_remote_merge(closed: Path, tmp_path: Path) -> None:
    root = closed
    _dangling_closeout(root)
    _remote_code_commit(root)
    _git(root, "fetch", "-q", str(root.parent / "remote.git"), BRANCH)
    _git(root, "merge", "-q", "--no-ff", "-m", "merge remote", "FETCH_HEAD")
    _write(root / "src" / "local_code.py", "L = 1\n")
    _git(root, "add", "src/local_code.py")
    _git(root, "commit", "-q", "-m", "local code")
    result = _integrate(root, "--dry-run")
    assert "tip extendido" not in result.stdout


def test_tip_stays_at_closeout_when_a_later_commit_touches_code(closed: Path, tmp_path: Path) -> None:
    root = closed
    tip = _dangling_closeout(root)
    _write(root / "src" / "later.py", "X = 1\n")
    _git(root, "add", "src/later.py")
    _git(root, "commit", "-q", "-m", "later code")
    result = _integrate(root)
    assert "tip extendido" not in result.stdout
    assert result.returncode == 1 and "fallo: graph" in result.stdout
    assert _remote_head(root) != tip

"""`deskops dispatch {start|reap}` against a fake scion executable and a throwaway desk."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]

FAKE_SCION = """#!{python}
import json, os, sys
with open(os.environ["FAKE_SCION_LOG"], "a") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
if sys.argv[1:2] == ["list"]:
    with open(os.environ["FAKE_SCION_LIST"]) as handle:
        sys.stdout.write(handle.read())
if sys.argv[1:2] == ["stop"] and sys.argv[2:3] == [os.environ.get("FAKE_SCION_FAIL_STOP")]:
    sys.exit(9)
sys.exit(int(os.environ.get("FAKE_SCION_START_CODE", "0")) if sys.argv[1:2] == ["start"] else 0)
"""


class Env:
    def __init__(self, tmp_path: Path, root: Path) -> None:
        self.root = root
        self.log = tmp_path / "scion.log"
        self.listing = tmp_path / "list.json"
        self.listing.write_text("[]")
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        scion = bin_dir / "scion"
        scion.write_text(FAKE_SCION.format(python=sys.executable))
        scion.chmod(0o755)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("DESKOPS_")}
        self.env["PATH"] = f"{bin_dir}{os.pathsep}{self.env['PATH']}"
        self.env["PYTHONPATH"] = str(ROOT) + os.pathsep + self.env.get("PYTHONPATH", "")
        self.env["FAKE_SCION_LOG"] = str(self.log)
        self.env["FAKE_SCION_LIST"] = str(self.listing)
        self.scion_tmp = tmp_path / "pytest-of-scion"
        self.env["DESKOPS_SCION_PYTEST_TMP"] = str(self.scion_tmp)

    def cli(self, *argv: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "deskops", *argv, "--root", "."],
            cwd=self.root, capture_output=True, text=True, env=self.env,
        )

    def calls(self) -> list[list[str]]:
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def agents(self, *items: dict) -> None:
        self.listing.write_text(json.dumps(list(items)))


def _role_config(role: str, **extra) -> dict:
    return {"role": role, "harness": "claude", "model_alias": "medium", "harness_auth": "oauth-token", **extra}


@pytest.fixture
def env(lifecycle_desk: Path, tmp_path: Path) -> Env:
    root = lifecycle_desk
    e = Env(tmp_path, root)
    for sub in ("src/deskops", "sldbsrc/sldb"):
        (tmp_path / sub).mkdir(parents=True)
    context = tmp_path / "context.json"
    context.write_text(json.dumps({
        "project": "proj", "workspace_root": str(tmp_path), "desk_root": str(root),
        "source_root": str(tmp_path / "src"), "sldb_root": str(tmp_path / "sldbsrc"),
    }))
    for name in ("disp-executor", "disp-tester"):
        added = e.cli("add", "role", "--name", name, "--kind", "claude", "--description", f"{name}.", "--body", f"# {name}\n")
        assert added.returncode == 0, added.stdout + added.stderr
    added = e.cli("add", "runtime-profile", "--title", "Claude on Scion", "--kind", "claude",
                  "--binary", "claude", "--status", "active", "--tools-flag=--allowedTools")
    assert added.returncode == 0, added.stdout + added.stderr
    added = e.cli("add", "task", "--title", "Dispatch me", "--goal", "g", "--scope", "s",
                  "--validation", "pytest", "--task-type", "task.code")
    assert added.returncode == 0, added.stdout + added.stderr
    config = {
        "project_identity": "dispatch-test",
        "queue_min_available_gb": 0,
        "queue_max_psi_avg60": 1000,
        "dispatch": {
            "project": "proj", "workspace": str(tmp_path), "templates_dir": str(tmp_path / "templates"),
            "context_file": str(context),
            "roles": {
                "executor": _role_config("role-disp-executor", env_config=str(tmp_path / "env.yaml")),
                "tester": _role_config("disp-tester"),
            },
        },
    }
    (root / "desk" / "config.json").write_text(json.dumps(config))
    subprocess.run(["git", "checkout", "-q", "-B", "main"], cwd=root, check=True)
    return e


TASK = "task-dispatch-me"


def _start_call(env: Env) -> list[str]:
    return next(c for c in env.calls() if c[0] == "start")


def test_start_executor(env: Env, tmp_path: Path) -> None:
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    start = _start_call(env)
    name = start[1]
    assert name.startswith("deskops-e-")
    run_dir = f"runs/subagents/exec-{name}"
    assert result.stdout.strip() == f"agente {name} run_dir {run_dir}"
    assert env.calls()[0] == ["list", "--project", "proj", "--format", "json"]
    assert ["templates", "sync", str((tmp_path / "templates" / "disp-executor").resolve()), "--project", "proj"] in env.calls()
    prompt_file = (env.root / run_dir / "prompt.md").resolve()
    assert start[2] == (
        f"Tu encargo esta en el archivo {prompt_file}. "
        "Lee el archivo completo antes de empezar y luego cumple el encargo que describe."
    )
    assert start[3:9] == ["--type", "disp-executor", "--project", "proj", "--workspace", str(tmp_path)]
    assert "--harness-auth" in start and "oauth-token" in start
    materialized = tmp_path / "templates" / "disp-executor" / "scion-env.yaml"
    assert materialized.is_file()
    assert start[start.index("--config") + 1] == str(materialized)
    assert start.index("--config") == start.index("--workspace") + 2
    assert "deskops.role=executor" in start and f"deskops.task_id={TASK}" in start
    assert (tmp_path / "templates" / "disp-executor" / "scion-agent.yaml").is_file()
    assert (env.root / run_dir / "run.md").is_file()
    text = prompt_file.read_text()
    assert TASK in text and "# Dispatch me" in text


def test_start_syncs_the_template_by_path_in_a_desk_with_its_own_scion(env: Env, tmp_path: Path) -> None:
    (env.root / ".scion").mkdir()
    (env.root / ".scion" / "settings.yaml").write_text("hub:\n  enabled: true\n")
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    target = (tmp_path / "templates" / "disp-executor").resolve()
    assert ["templates", "sync", str(target), "--project", "proj"] in env.calls()
    assert _start_call(env)[3:5] == ["--type", "disp-executor"]


def test_start_tester_run_dir_has_testing_suffix(env: Env, tmp_path: Path) -> None:
    result = env.cli("dispatch", "start", "tester", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    start = _start_call(env)
    name = start[1]
    assert name.startswith("deskops-t-") and not name.endswith("-testing")
    run_dir = f"runs/subagents/exec-{name}-testing"
    assert result.stdout.strip() == f"agente {name} run_dir {run_dir}"
    assert start[start.index("--config") + 1] == str(tmp_path / "templates" / "disp-tester" / "scion-env.yaml")
    assert (env.root / run_dir / "prompt.md").is_file() and (env.root / run_dir / "run.md").is_file()
    assert ["templates", "sync", str((tmp_path / "templates" / "disp-tester").resolve()), "--project", "proj"] in env.calls()
    assert (tmp_path / "templates" / "disp-tester").is_dir()


def _set_config(env: Env, **fields) -> None:
    path = env.root / "desk" / "config.json"
    data = json.loads(path.read_text())
    data.update(fields)
    path.write_text(json.dumps(data))


def test_start_launches_while_another_task_agent_is_running(env: Env) -> None:
    env.agents({"name": "other-agent", "phase": "running"}, {"name": "old", "phase": "stopped"})
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert any(call[0] == "start" for call in env.calls())


def test_start_refuses_when_the_task_already_has_a_running_agent(env: Env) -> None:
    first = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert first.returncode == 0, first.stdout + first.stderr
    name = _start_call(env)[1]
    env.log.unlink()
    env.agents({"name": name, "phase": "running"})
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 3
    assert f"ocupado: la tarea ya tiene agente {name}" in result.stdout
    assert all(call[0] == "list" for call in env.calls())


def test_start_refuses_when_memory_is_under_the_gate(env: Env) -> None:
    _set_config(env, queue_min_available_gb=100000)
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 3
    assert "ocupado: memoria disponible" in result.stdout
    assert not any(call[0] == "start" for call in env.calls())


def test_attempts_then_no_more(env: Env) -> None:
    first = env.cli("dispatch", "start", "executor", "--task", TASK)
    second = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert first.returncode == 0 and second.returncode == 0
    names = [c[1] for c in env.calls() if c[0] == "start"]
    assert len(names) == 2 and names[1] == names[0] + "-a2"
    third = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert third.returncode == 5
    assert third.stdout.strip() == f"sin intentos: {TASK} executor"
    assert len([c for c in env.calls() if c[0] == "start"]) == 2


def test_start_returns_scion_start_exit_code(env: Env) -> None:
    env.env["FAKE_SCION_START_CODE"] = "7"
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 7 and "agente deskops-e-" in result.stdout


def test_reap(env: Env) -> None:
    labels = lambda role: {"deskops.task_id": TASK, "deskops.role": role}  # noqa: E731
    summary_dir = env.root / "runs" / "subagents" / "exec-deskops-t-aaa-testing"
    summary_dir.mkdir(parents=True)
    (summary_dir / "result-summary.md").write_text("done")
    env.agents(
        {"name": "deskops-e-phase", "phase": "stopped", "activity": "idle", "labels": labels("executor")},
        {"name": "deskops-e-act", "phase": "running", "activity": "blocked", "labels": labels("executor")},
        {"name": "deskops-t-aaa", "phase": "running", "activity": "working", "labels": labels("tester")},
        {"name": "deskops-e-live", "phase": "running", "activity": "working", "labels": labels("executor")},
        {"name": "unrelated", "phase": "stopped", "labels": {"deskops.task_id": "task-other", "deskops.role": "executor"}},
    )
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 4, result.stdout + result.stderr
    assert result.stdout.splitlines() == [
        "deskops-e-phase executor phase:stopped",
        "deskops-e-act executor activity:blocked",
        "deskops-t-aaa tester result-summary",
        "deskops-e-live executor vivo",
    ]
    calls = env.calls()
    for name in ("deskops-e-phase", "deskops-e-act", "deskops-t-aaa"):
        assert ["stop", name, "--project", "proj"] in calls
        assert ["delete", name, "--project", "proj", "--yes"] in calls
    assert not any(len(c) > 1 and c[1] in ("deskops-e-live", "unrelated") for c in calls)


def test_reap_all_finished_exits_zero(env: Env) -> None:
    env.agents({"name": "deskops-e-x", "phase": "stopped", "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}})
    assert env.cli("dispatch", "reap", "--task", TASK).returncode == 0


def test_reap_after_the_task_was_deleted(env: Env) -> None:
    (env.root / "desk" / "tasks" / f"{TASK}.md").unlink()
    env.agents({"name": "deskops-e-x", "phase": "stopped", "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}})
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert ["delete", "deskops-e-x", "--project", "proj", "--yes"] in env.calls()


def test_reap_scion_error_continues_and_fails(env: Env) -> None:
    labels = {"deskops.task_id": TASK, "deskops.role": "executor"}
    env.env["FAKE_SCION_FAIL_STOP"] = "deskops-e-bad"
    env.agents(
        {"name": "deskops-e-bad", "phase": "stopped", "labels": labels},
        {"name": "deskops-e-ok", "phase": "stopped", "labels": labels},
    )
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode != 0
    assert result.stdout.splitlines() == ["deskops-e-bad executor error:9", "deskops-e-ok executor phase:stopped"]
    assert ["delete", "deskops-e-ok", "--project", "proj", "--yes"] in env.calls()


def test_executor_prompt_asks_for_named_commit_with_task_id(env: Env) -> None:
    assert env.cli("dispatch", "start", "executor", "--task", TASK).returncode == 0
    name = _start_call(env)[1]
    text = (env.root / f"runs/subagents/exec-{name}/prompt.md").read_text()
    assert f"Task-Id: {TASK}" in text and "uno por uno" in text
    assert "git add -A" in text and "git stash" in text and "deskops advance task" in text
    assert "--grep" not in text


def test_tester_prompt_runs_only_touched_tests(env: Env) -> None:
    assert env.cli("dispatch", "start", "tester", "--task", TASK).returncode == 0
    name = _start_call(env)[1]
    text = (env.root / f"runs/subagents/exec-{name}-testing/prompt.md").read_text()
    assert f'git log -1 --format=%H --grep "Task-Id: {TASK}"' in text
    assert "git show --name-only" in text and "TMPDIR=/tmp" in text
    assert "PASA o FALLA" in text and "integrate en el host" in text


@pytest.mark.parametrize("argv", [("start", "executor"), ("start", "tester"), ("reap",)])
def test_without_dispatch_config_exits_2(env: Env, argv: tuple[str, ...]) -> None:
    (env.root / "desk" / "config.json").write_text(json.dumps({"project_identity": "x"}))
    result = env.cli("dispatch", *argv, "--task", TASK)
    assert result.returncode == 2
    assert "falta el campo dispatch en desk/config.json" in result.stdout + result.stderr
    assert env.calls() == []


@pytest.fixture
def roleless(env: Env, tmp_path: Path) -> Env:
    """A task desk without roles; its dispatch config takes them from the `env` desk."""
    import shutil

    taskdesk = tmp_path / "taskdesk"
    shutil.copytree(env.root, taskdesk, ignore=shutil.ignore_patterns("roles"))
    assert not (taskdesk / "desk" / "roles").exists()
    config = json.loads((env.root / "desk" / "config.json").read_text())
    config["project_identity"] = "taskdesk-identity"
    config["dispatch"]["roles_root"] = str(env.root)
    (taskdesk / "desk" / "config.json").write_text(json.dumps(config))
    env.root = taskdesk
    return env


def test_start_takes_roles_from_roles_root(roleless: Env, tmp_path: Path) -> None:
    result = roleless.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    start = _start_call(roleless)
    name = start[1]
    run_dir = f"runs/subagents/exec-{name}"
    assert start[3:5] == ["--type", "disp-executor"]
    assert (tmp_path / "templates" / "disp-executor" / "scion-agent.yaml").is_file()
    assert "taskdesk-identity" in (tmp_path / "templates" / "disp-executor" / "agents.md").read_text()
    assert (roleless.root / run_dir / "run.md").is_file()
    assert (roleless.root / run_dir / "prompt.md").is_file()


def test_roles_root_relative_resolves_against_task_root(roleless: Env, tmp_path: Path) -> None:
    path = roleless.root / "desk" / "config.json"
    config = json.loads(path.read_text())
    config["dispatch"]["roles_root"] = "../repo"
    path.write_text(json.dumps(config))
    result = roleless.cli("dispatch", "start", "tester", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _start_call(roleless)[3:5] == ["--type", "disp-tester"]


def test_start_without_roles_root_and_without_roles_fails(roleless: Env) -> None:
    path = roleless.root / "desk" / "config.json"
    config = json.loads(path.read_text())
    del config["dispatch"]["roles_root"]
    path.write_text(json.dumps(config))
    result = roleless.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode != 0
    assert not any(c[0] == "start" for c in roleless.calls())


def test_reap_works_on_a_desk_without_roles(roleless: Env) -> None:
    roleless.agents({"name": "deskops-e-x", "phase": "stopped", "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}})
    result = roleless.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert ["stop", "deskops-e-x", "--project", "proj"] in roleless.calls()


def _set_quick_gates(env: Env, gates: list[str] | None) -> None:
    path = env.root / "desk" / "config.json"
    config = json.loads(path.read_text())
    if gates is not None:
        config["dispatch"]["quick_gates"] = gates
    path.write_text(json.dumps(config))


@pytest.mark.parametrize("role", ["executor", "tester"])
def test_prompts_require_quick_gates_when_declared(env: Env, role: str) -> None:
    _set_quick_gates(env, ["bash", "tools/check.sh", "--fast"])
    assert env.cli("dispatch", "start", role, "--task", TASK).returncode == 0
    name = _start_call(env)[1]
    suffix = "-testing" if role == "tester" else ""
    text = (env.root / f"runs/subagents/exec-{name}{suffix}/prompt.md").read_text()
    assert "bash tools/check.sh --fast" in text
    assert ("rc 0 antes de commitear" if role == "executor" else "veredicto es FALLA") in text


@pytest.mark.parametrize("role", ["executor", "tester"])
def test_prompts_without_quick_gates_do_not_mention_them(env: Env, role: str) -> None:
    _set_quick_gates(env, None)
    assert env.cli("dispatch", "start", role, "--task", TASK).returncode == 0
    name = _start_call(env)[1]
    suffix = "-testing" if role == "tester" else ""
    text = (env.root / f"runs/subagents/exec-{name}{suffix}/prompt.md").read_text()
    assert "Gates rapidos" not in text


# --- worktree por ejecutor ---------------------------------------------------


def _git(cwd: Path, *argv: str) -> str:
    done = subprocess.run(["git", *argv], cwd=cwd, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    return done.stdout.strip()


def _start_executor(env: Env, task: str = TASK) -> str:
    result = env.cli("dispatch", "start", "executor", "--task", task)
    assert result.returncode == 0, result.stdout + result.stderr
    return next(c for c in reversed(env.calls()) if c[0] == "start")[1]


def _commit_in(worktree: Path, filename: str, text: str) -> str:
    (worktree / filename).write_text(text)
    _git(worktree, "add", filename)
    _git(worktree, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", f"add {filename}")
    return _git(worktree, "rev-parse", "HEAD")


def _finished(env: Env, *names: str) -> None:
    env.agents(*({"name": n, "phase": "stopped", "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}} for n in names))


def test_start_executor_creates_own_worktree_and_branch(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    assert worktree.is_dir()
    assert _git(worktree, "rev-parse", "--abbrev-ref", "HEAD") == f"deskops/{name}"
    assert _git(worktree, "rev-parse", "HEAD") == _git(env.root, "rev-parse", "main")
    assert ".worktrees/" in (env.root / ".git" / "info" / "exclude").read_text().splitlines()
    assert ".worktrees" not in _git(env.root, "status", "--short")
    prompt = (env.root / f"runs/subagents/exec-{name}" / "prompt.md").read_text()
    assert f"{worktree}" in prompt and f"deskops/{name}" in prompt


def test_start_tester_has_no_worktree(env: Env) -> None:
    assert env.cli("dispatch", "start", "tester", "--task", TASK).returncode == 0
    assert not (env.root / ".worktrees").exists()


def test_start_tester_waits_while_the_executor_branch_is_not_integrated(env: Env) -> None:
    name = _start_executor(env)
    _commit_in(env.root / ".worktrees" / name, "one.txt", "1")
    _finished(env, name)
    result = env.cli("dispatch", "start", "tester", "--task", TASK)
    assert result.returncode == 3, result.stdout + result.stderr
    assert f"en espera: la rama deskops/{name} de la tarea no está integrada" in result.stdout
    assert not any(c[0] == "start" and c[1].startswith("deskops-t-") for c in env.calls())
    assert env.cli("dispatch", "reap", "--task", TASK).returncode == 0
    assert env.cli("dispatch", "start", "tester", "--task", TASK).returncode == 0


def test_start_tester_launches_when_the_executor_branch_has_no_new_commits(env: Env) -> None:
    name = _start_executor(env)
    _finished(env, name)
    assert env.cli("dispatch", "start", "tester", "--task", TASK).returncode == 0


def test_start_refuses_when_checkout_is_not_on_base_branch(env: Env) -> None:
    _git(env.root, "checkout", "-q", "-b", "other")
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 8 and "no en 'main'" in result.stdout
    assert not any(c[0] == "start" for c in env.calls())


def test_start_scion_failure_removes_the_worktree(env: Env) -> None:
    env.env["FAKE_SCION_START_CODE"] = "7"
    assert env.cli("dispatch", "start", "executor", "--task", TASK).returncode == 7
    assert not list((env.root / ".worktrees").glob("*"))
    assert "deskops/" not in _git(env.root, "branch", "--list")


def test_two_executors_do_not_share_tree_or_index(env: Env) -> None:
    add = env.cli("add", "task", "--title", "Second", "--goal", "g", "--scope", "s",
                  "--validation", "pytest", "--task-type", "task.code")
    assert add.returncode == 0, add.stdout + add.stderr
    first = _start_executor(env)
    second = _start_executor(env, "task-second")
    assert first != second
    one, two = env.root / ".worktrees" / first, env.root / ".worktrees" / second
    _commit_in(one, "one.txt", "1")
    (two / "dirty.txt").write_text("x")
    assert not (two / "one.txt").exists() and not (one / "dirty.txt").exists()
    assert _git(two, "status", "--short") == "?? dirty.txt"
    assert _git(env.root, "branch", "--list", "deskops/*").count("deskops/") == 2


def test_reap_fast_forwards_commit_and_removes_worktree(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    sha = _commit_in(worktree, "one.txt", "1")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(env.root, "rev-parse", "main") == sha
    assert not worktree.exists()
    assert _git(env.root, "branch", "--list", "deskops/*") == ""


def test_reap_cherry_picks_only_the_task_commit(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    _commit_in(worktree, "mine.txt", "m")
    (env.root / "other.txt").write_text("o")
    _git(env.root, "add", "other.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "main moved")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(env.root, "show", "--name-only", "--format=", "main") == "mine.txt"
    assert (env.root / "other.txt").is_file()
    assert not worktree.exists()


def test_reap_conflict_aborts_and_keeps_worktree(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    _commit_in(worktree, "same.txt", "mine")
    (env.root / "same.txt").write_text("theirs")
    _git(env.root, "add", "same.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "main same")
    before = _git(env.root, "rev-parse", "main")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 8 and "conflicto" in result.stdout
    assert _git(env.root, "rev-parse", "main") == before
    assert worktree.is_dir() and f"deskops/{name}" in _git(env.root, "branch", "--list", "deskops/*")
    assert not (env.root / ".git" / "CHERRY_PICK_HEAD").exists()


def test_start_commits_the_rundoc_so_reap_brings_an_executor_commit_touching_the_store(env: Env) -> None:
    _git(env.root, "add", ".sldb", "desk")
    _git(env.root, "commit", "-q", "-m", "desk")
    (env.root / "unrelated.txt").write_text("dirty")  # foreign dirty work must stay uncommitted
    name = _start_executor(env)
    assert _git(env.root, "status", "--short", "--", ".sldb") == ""
    assert _git(env.root, "log", "-1", "--format=%s%n%b", "--", ".sldb").splitlines()[0] == f"run: {name}"
    assert "[skip ci]" in _git(env.root, "log", "-1", "--format=%B")
    assert _git(env.root, "status", "--short", "unrelated.txt") == "?? unrelated.txt"
    worktree = env.root / ".worktrees" / name
    index = worktree / ".sldb/core/store_index.yaml"
    index.write_text(index.read_text() + "\n# executor sync\n")
    _git(worktree, "add", ".sldb/core/store_index.yaml")
    _git(worktree, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "sync store")
    (env.root / "main.txt").write_text("m")
    _git(env.root, "add", "main.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "main moved")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "executor sync" in (env.root / ".sldb/core/store_index.yaml").read_text()
    assert not worktree.exists()


def test_start_commits_the_run_md_with_the_rundoc_and_the_store_gate_passes(env: Env) -> None:
    from deskops.integrate import _collect_paths

    _git(env.root, "add", ".sldb", "desk", "sldb")
    _git(env.root, "commit", "-q", "-m", "desk")
    name = _start_executor(env)
    run_md = f"runs/subagents/exec-{name}/run.md"
    files = _git(env.root, "show", "--name-only", "--format=%s", "HEAD").splitlines()
    assert files[0] == f"run: {name}"
    assert run_md in files and any("RunDoc/run-" in f for f in files)
    store = yaml.safe_load(_git(env.root, "show", "HEAD:.sldb/store.yaml"))
    for path in _collect_paths(store):
        if not path.startswith("../"):
            _git(env.root, "cat-file", "-e", f"HEAD:{path.rstrip('/') or '.'}")


def test_reap_names_the_files_when_local_changes_block_the_pick(env: Env) -> None:
    _git(env.root, "add", ".sldb", "desk")
    _git(env.root, "commit", "-q", "-m", "desk")
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    _commit_in(worktree, "shared.txt", "mine")
    (env.root / "main.txt").write_text("m")
    _git(env.root, "add", "main.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "main moved")
    (env.root / "shared.txt").write_text("local")
    _git(env.root, "add", "shared.txt")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 8 and "shared.txt" in result.stdout and "commitea" in result.stdout


def test_reap_names_the_files_under_a_spanish_locale(env: Env) -> None:
    env.env.update({"LANG": "es_ES.UTF-8", "LC_ALL": "es_ES.UTF-8", "LANGUAGE": "es"})
    test_reap_names_the_files_when_local_changes_block_the_pick(env)


def test_start_untracks_a_stale_rundoc_whose_run_dir_is_missing(env: Env) -> None:
    import shutil

    name = _start_executor(env)
    _git(env.root, "worktree", "remove", "--force", str(env.root / ".worktrees" / name))
    _git(env.root, "branch", "-D", f"deskops/{name}")
    shutil.rmtree(env.root / f"runs/subagents/exec-{name}")  # RunDoc stays tracked in the store
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (env.root / f"runs/subagents/exec-{name}/run.md").is_file()
    assert [c[1] for c in env.calls() if c[0] == "start"] == [name, name]


def test_reap_brings_the_commit_made_on_top_of_a_run_commit_made_in_main(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    (env.root / "marker.txt").write_text("r")  # the 'run:' commit made in main after the branch was created
    _git(env.root, "add", "marker.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", f"run: {name}")
    _git(worktree, "merge", "--ff-only", "-q", "main")  # the executor's commit sits on top of it ...
    (worktree / "marker.txt").write_text("r2")
    _git(worktree, "add", "marker.txt")
    _git(worktree, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "mine", "-m", "Task-Id: t")
    # ... and another main commit repeats its patch, so `--cherry-pick` would count it as already in main
    (env.root / "marker.txt").write_text("r2")
    _git(env.root, "add", "marker.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "same patch")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "integrado 1 commit(s)" in result.stdout
    assert "Task-Id: t" in _git(env.root, "log", "--format=%B", "main")
    assert not worktree.exists()


def test_reap_keeps_the_branch_when_no_commit_is_counted_but_the_tip_is_not_in_main(env: Env, monkeypatch) -> None:
    from deskops import dispatch

    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    sha = _commit_in(worktree, "mine.txt", "m")
    real = dispatch._git

    def blind(root, *args):  # a miscount: rev-list reports nothing pending
        if args[:1] == ("rev-list",) and "--count" not in args:
            return subprocess.CompletedProcess(args, 0, "", "")
        return real(root, *args)

    monkeypatch.setattr(dispatch, "_git", blind)
    code, message = dispatch._integrate_branch(env.root, name)
    assert code == 8 and f"deskops/{name}" in message and sha in message
    assert worktree.is_dir() and f"deskops/{name}" in _git(env.root, "branch", "--list", "deskops/*")


def test_reap_waits_while_the_worktree_has_uncommitted_changes(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    (worktree / "late.txt").write_text("not committed yet")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 3, result.stdout + result.stderr
    assert f"en espera: el worktree de {name} tiene cambios sin commitear" in result.stdout
    assert (worktree / "late.txt").read_text() == "not committed yet"
    assert f"deskops/{name}" in _git(env.root, "branch", "--list", "deskops/*")
    assert not any(c[0] == "delete" for c in env.calls())
    _git(worktree, "add", "late.txt")
    sha = _commit_in(worktree, "other.txt", "o")
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(env.root, "rev-parse", "main") == sha and (env.root / "late.txt").is_file()
    assert not worktree.exists()


def test_reap_waits_while_the_executor_is_alive(env: Env) -> None:
    name = _start_executor(env)
    (env.root / "runs" / "subagents" / f"exec-{name}" / "result-summary.md").write_text("done")
    env.agents({"name": name, "phase": "running", "activity": "working", "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}})
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 3, result.stdout + result.stderr
    assert f"en espera: {name} sigue vivo" in result.stdout
    assert (env.root / ".worktrees" / name).is_dir()
    assert not any(c[0] in ("stop", "delete") for c in env.calls())


def test_reap_in_pr_mode_brings_commits_to_the_task_branch_not_the_base(env: Env) -> None:
    _set_config(env, integrate={"remote_url": "unused", "branch": "main", "suite": ["true"], "mode": "pr"})
    name = _start_executor(env)
    base_sha = _git(env.root, "rev-parse", "main")  # start commits the RunDoc on the base
    worktree = env.root / ".worktrees" / name
    sha = _commit_in(worktree, "one.txt", "1")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(env.root, "rev-parse", "main") == base_sha
    assert _git(env.root, "rev-parse", f"task/{TASK}") == sha
    assert _git(env.root, "rev-parse", "--abbrev-ref", "HEAD") == f"task/{TASK}"
    assert not worktree.exists()


@pytest.mark.parametrize("role", ["executor", "tester"])
def test_prompt_sets_pytest_basetemp_in_container_tmp(env: Env, role: str) -> None:
    assert env.cli("dispatch", "start", role, "--task", TASK).returncode == 0
    name = _start_call(env)[1]
    suffix = "-testing" if role == "tester" else ""
    text = (env.root / f"runs/subagents/exec-{name}{suffix}/prompt.md").read_text()
    assert "Temporales de pytest" in text
    assert f'PYTEST_ADDOPTS="--basetemp=/tmp/pytest-{name}"' in text


def _reap_in_process(env: Env, monkeypatch, scion_tmp: Path) -> int:
    from deskops import dispatch

    for key in ("PATH", "FAKE_SCION_LOG", "FAKE_SCION_LIST"):
        monkeypatch.setenv(key, env.env[key])
    monkeypatch.setenv("DESKOPS_SCION_PYTEST_TMP", str(scion_tmp))
    return dispatch.reap(env.root, TASK)


def test_reap_cleans_scion_pytest_tmp_when_no_agent_is_alive(env: Env, monkeypatch, tmp_path: Path, capsys) -> None:
    scion_tmp = tmp_path / "pytest-of-scion"
    (scion_tmp / "pytest-0").mkdir(parents=True)
    env.agents({"name": "deskops-t-x", "phase": "stopped", "labels": {"deskops.task_id": TASK, "deskops.role": "tester"}})
    assert _reap_in_process(env, monkeypatch, scion_tmp) == 0
    assert not scion_tmp.exists()
    assert f"limpieza: {scion_tmp}" in capsys.readouterr().out


def test_reap_keeps_scion_pytest_tmp_while_an_agent_runs(env: Env, monkeypatch, tmp_path: Path, capsys) -> None:
    scion_tmp = tmp_path / "pytest-of-scion"
    (scion_tmp / "pytest-0").mkdir(parents=True)
    env.agents(
        {"name": "deskops-t-x", "phase": "stopped", "labels": {"deskops.task_id": TASK, "deskops.role": "tester"}},
        {"name": "other", "phase": "running", "activity": "working", "labels": {"deskops.task_id": "task-other", "deskops.role": "executor"}},
    )
    _reap_in_process(env, monkeypatch, scion_tmp)
    assert scion_tmp.is_dir()
    assert "limpieza" not in capsys.readouterr().out


# --- reap encola el tester tras integrar --------------------------------------


def _declare_tester_job(env: Env) -> None:
    _set_config(env, queue_jobs={"dispatch-tester": {"run": ["true"], "timeout": 60}})


def _pending_testers(env: Env) -> list[dict]:
    folder = env.root / "runs" / "queue" / "pending"
    jobs = [json.loads(p.read_text()) for p in sorted(folder.glob("*.json"))] if folder.is_dir() else []
    return [j for j in jobs if j["kind"] == "dispatch-tester" and j["task_id"] == TASK]


def test_reap_enqueues_the_tester_after_integrating_the_executor(env: Env) -> None:
    _declare_tester_job(env)
    name = _start_executor(env)
    _commit_in(env.root / ".worktrees" / name, "one.txt", "1")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "encolado: dispatch-tester" in result.stdout
    assert len(_pending_testers(env)) == 1


def test_reap_does_not_duplicate_a_pending_tester(env: Env) -> None:
    _declare_tester_job(env)
    from deskops import queue

    queue.enqueue(env.root, "dispatch-tester", TASK, "execution->testing")
    name = _start_executor(env)
    _commit_in(env.root / ".worktrees" / name, "one.txt", "1")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "encolado" not in result.stdout
    assert len(_pending_testers(env)) == 1


def test_reap_does_not_enqueue_the_tester_when_integration_fails(env: Env) -> None:
    _declare_tester_job(env)
    name = _start_executor(env)
    _commit_in(env.root / ".worktrees" / name, "same.txt", "mine")
    (env.root / "same.txt").write_text("theirs")
    _git(env.root, "add", "same.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "main same")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 8
    assert _pending_testers(env) == []

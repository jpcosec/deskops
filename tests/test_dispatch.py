"""`deskops dispatch {start|reap}` against a fake scion executable and a throwaway desk."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

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
    assert ["templates", "sync", "disp-executor", "--project", "proj"] in env.calls()
    prompt_file = (env.root / run_dir / "prompt.md").resolve()
    assert start[2] == (
        f"Tu encargo esta en el archivo {prompt_file}. "
        "Lee el archivo completo antes de empezar y luego cumple el encargo que describe."
    )
    assert start[3:9] == ["--type", "disp-executor", "--project", "proj", "--workspace", str(tmp_path)]
    assert "--harness-auth" in start and "oauth-token" in start
    assert start[start.index("--config") + 1] == str(tmp_path / "env.yaml")
    assert "deskops.role=executor" in start and f"deskops.task_id={TASK}" in start
    assert (tmp_path / "templates" / "disp-executor" / "scion-agent.yaml").is_file()
    assert (env.root / run_dir / "run.md").is_file()
    text = prompt_file.read_text()
    assert TASK in text and "# Dispatch me" in text


def test_start_tester_run_dir_has_testing_suffix(env: Env, tmp_path: Path) -> None:
    result = env.cli("dispatch", "start", "tester", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    start = _start_call(env)
    name = start[1]
    assert name.startswith("deskops-t-") and not name.endswith("-testing")
    run_dir = f"runs/subagents/exec-{name}-testing"
    assert result.stdout.strip() == f"agente {name} run_dir {run_dir}"
    assert "--config" not in start
    assert (env.root / run_dir / "prompt.md").is_file() and (env.root / run_dir / "run.md").is_file()
    assert ["templates", "sync", "disp-tester", "--project", "proj"] in env.calls()
    assert (tmp_path / "templates" / "disp-tester").is_dir()


def test_start_refuses_when_an_agent_is_running(env: Env) -> None:
    env.agents({"name": "other-agent", "phase": "running"}, {"name": "old", "phase": "stopped"})
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 3 and "ocupado: other-agent" in result.stdout
    assert all(call[0] == "list" for call in env.calls())


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

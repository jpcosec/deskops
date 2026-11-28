"""`deskops dispatch {start|reap}` with ``dispatch.runtime: paseo``, against a fake paseo executable."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from deskops.config import DispatchConfig
from deskops.runtime import paseo

from tests.test_dispatch import TASK, Env

FAKE_PASEO = """#!{python}
import json, os, sys
with open(os.environ["FAKE_PASEO_LOG"], "a") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
if sys.argv[1:2] == ["ls"]:
    with open(os.environ["FAKE_PASEO_LIST"]) as handle:
        sys.stdout.write(handle.read())
if sys.argv[1:2] == ["run"]:
    sys.stderr.write("Created workspace wks_1 - x\\n")
    if os.environ.get("FAKE_PASEO_FAIL") == "run":
        sys.exit(7)
    sys.stdout.write(json.dumps({{"agentId": "id-1", "status": "running"}}))
if sys.argv[1:2] == ["delete"] and sys.argv[2:3] == [os.environ.get("FAKE_PASEO_FAIL_DELETE")]:
    sys.exit(9)
"""


class PaseoEnv(Env):
    def __init__(self, tmp_path: Path, root: Path) -> None:
        super().__init__(tmp_path, root)
        self.paseo_log = tmp_path / "paseo.log"
        self.paseo_list = tmp_path / "paseo-list.json"
        self.paseo_list.write_text("[]")
        fake = tmp_path / "bin" / "paseo"
        fake.write_text(FAKE_PASEO.format(python=sys.executable))
        fake.chmod(0o755)
        self.env["FAKE_PASEO_LOG"] = str(self.paseo_log)
        self.env["FAKE_PASEO_LIST"] = str(self.paseo_list)

    def paseo_calls(self) -> list[list[str]]:
        if not self.paseo_log.exists():
            return []
        return [json.loads(line) for line in self.paseo_log.read_text().splitlines()]

    def paseo_agents(self, *items: dict) -> None:
        self.paseo_list.write_text(json.dumps(list(items)))


@pytest.fixture
def penv(lifecycle_desk: Path, tmp_path: Path) -> PaseoEnv:
    root = lifecycle_desk
    e = PaseoEnv(tmp_path, root)
    for name in ("disp-executor", "disp-tester"):
        added = e.cli("add", "role", "--name", name, "--kind", "pi", "--description", f"{name}.", "--body", f"# {name}\n\nRegla del rol {name}.\n")
        assert added.returncode == 0, added.stdout + added.stderr
    added = e.cli("add", "task", "--title", "Dispatch me", "--goal", "g", "--scope", "s",
                  "--validation", "pytest", "--task-type", "task.code")
    assert added.returncode == 0, added.stdout + added.stderr
    config = {
        "project_identity": "dispatch-test",
        "queue_min_available_gb": 0,
        "queue_max_psi_avg60": 1000,
        "dispatch": {
            "runtime": "paseo",
            "roles": {
                "executor": {"role": "role-disp-executor", "provider": "claude", "mode": "bypass"},
                "tester": {"role": "disp-tester", "provider": "pi"},
            },
        },
    }
    (root / "desk" / "config.json").write_text(json.dumps(config))
    subprocess.run(["git", "checkout", "-q", "-B", "main"], cwd=root, check=True)
    return e


def _run_call(env: PaseoEnv) -> list[str]:
    return next(c for c in env.paseo_calls() if c[0] == "run")


def _opt(argv: list[str], flag: str) -> str:
    return argv[argv.index(flag) + 1]


def test_start_executor_runs_paseo_in_its_worktree(penv: PaseoEnv) -> None:
    result = penv.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    run = _run_call(penv)
    name = _opt(run, "--title")
    assert name.startswith("deskops-e-")
    run_dir = f"runs/subagents/exec-{name}"
    assert result.stdout.strip() == f"agente {name} run_dir {run_dir}"
    assert penv.calls() == []  # scion is never called
    assert penv.paseo_calls()[0] == ["ls", "--global", "--all", "--json"]
    assert run[:3] == ["run", "--no-wait", "--json"]
    assert _opt(run, "--provider") == "claude" and _opt(run, "--mode") == "bypass"
    assert "--model" not in run
    worktree = penv.root / ".worktrees" / name
    assert _opt(run, "--cwd") == str(worktree) and worktree.is_dir()
    assert "deskops.role=executor" in run and f"deskops.task_id={TASK}" in run
    prompt_file = (penv.root / run_dir / "prompt.md").resolve()
    assert run[-1].startswith(f"Tu encargo esta en el archivo {prompt_file}.")
    text = prompt_file.read_text()
    assert text.startswith("# Tu rol")
    assert "Regla del rol disp-executor." in text
    assert f"Tu run_dir es `{run_dir}`" in text and f"deskops advance task {TASK}" in text
    assert "contenedor" not in text and "/tmp/ws-venv" not in text
    assert (penv.root / run_dir / "run.md").is_file()
    assert not (penv.root.parent / "templates").exists()


def test_start_tester_runs_in_the_main_checkout(penv: PaseoEnv) -> None:
    result = penv.cli("dispatch", "start", "tester", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    run = _run_call(penv)
    assert _opt(run, "--provider") == "pi" and "--mode" not in run
    assert _opt(run, "--cwd") == str(penv.root)
    text = (penv.root / f"runs/subagents/exec-{_opt(run, '--title')}-testing" / "prompt.md").read_text()
    assert "PASA o FALLA" in text and "deskops advance task" not in text


def test_start_failure_gives_the_attempt_back(penv: PaseoEnv) -> None:
    penv.env["FAKE_PASEO_FAIL"] = "run"
    result = penv.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 7, result.stdout + result.stderr
    assert "paseo start fallo (7)" in result.stdout and "reintentable" in result.stdout
    assert not any((penv.root / "runs" / "subagents").glob("exec-deskops-e-*"))
    assert not any((penv.root / ".worktrees").glob("deskops-e-*"))


def test_start_busy_when_the_task_has_a_running_agent(penv: PaseoEnv) -> None:
    penv.cli("dispatch", "start", "executor", "--task", TASK)
    name = _opt(_run_call(penv), "--title")
    penv.paseo_agents({"id": "id-1", "name": name, "status": "running", "labels": {}})
    result = penv.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 3 and f"ocupado: la tarea ya tiene agente {name}" in result.stdout


def test_reap_deletes_finished_agents_by_id(penv: PaseoEnv) -> None:
    labels = lambda role: {"deskops.task_id": TASK, "deskops.role": role}  # noqa: E731
    penv.paseo_agents(
        {"id": "id-idle", "name": "deskops-t-idle", "status": "idle", "labels": labels("tester")},
        {"id": "id-closed", "name": "deskops-t-closed", "status": "closed", "labels": labels("tester")},
        {"id": "id-live", "name": "deskops-t-live", "status": "running", "labels": labels("tester")},
        {"id": "id-other", "name": "deskops-t-other", "status": "idle", "labels": {"deskops.task_id": "task-x"}},
    )
    result = penv.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 4, result.stdout + result.stderr
    assert result.stdout.splitlines() == [
        "deskops-t-idle tester activity:completed",
        "deskops-t-closed tester phase:stopped",
        "deskops-t-live tester vivo",
    ]
    deletes = [c for c in penv.paseo_calls() if c[0] == "delete"]
    assert deletes == [["delete", "id-idle", "--json"], ["delete", "id-closed", "--json"]]


def test_reap_integrates_the_executor_branch(penv: PaseoEnv) -> None:
    assert penv.cli("dispatch", "start", "executor", "--task", TASK).returncode == 0
    name = _opt(_run_call(penv), "--title")
    worktree = penv.root / ".worktrees" / name
    (worktree / "hecho.txt").write_text("ok\n")
    subprocess.run(["git", "add", "hecho.txt"], cwd=worktree, check=True)
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "hecho"], cwd=worktree, check=True)
    penv.paseo_agents({"id": "id-1", "name": name, "status": "idle",
                       "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}})
    result = penv.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"{name} integrado 1 commit(s) de deskops/{name} en main" in result.stdout
    assert (penv.root / "hecho.txt").is_file() and not worktree.exists()


def test_reap_delete_error_fails(penv: PaseoEnv) -> None:
    penv.env["FAKE_PASEO_FAIL_DELETE"] = "id-1"
    penv.paseo_agents({"id": "id-1", "name": "deskops-t-x", "status": "idle",
                       "labels": {"deskops.task_id": TASK, "deskops.role": "tester"}})
    result = penv.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 6 and "deskops-t-x tester error:9" in result.stdout


def test_config_requires_the_fields_of_its_runtime() -> None:
    roles = {"executor": {"role": "e", "provider": "pi"}, "tester": {"role": "t", "provider": "pi"}}
    assert DispatchConfig.model_validate({"runtime": "paseo", "roles": roles}).project is None
    with pytest.raises(ValidationError, match="roles.tester.provider"):
        DispatchConfig.model_validate({"runtime": "paseo", "roles": {**roles, "tester": {"role": "t"}}})
    with pytest.raises(ValidationError, match="project"):
        DispatchConfig.model_validate({"roles": roles})  # scion is the default runtime


def test_paseo_helpers() -> None:
    assert paseo.parse_json('aviso\n[{"id": "a"}]') == [{"id": "a"}]
    assert paseo.normalize({"id": "a", "name": "n", "status": "idle", "labels": {"k": "v"}}) == {
        "id": "a", "name": "n", "phase": "running", "activity": "completed", "labels": {"k": "v"}, "status": "idle",
    }
    with pytest.raises(ValueError):
        paseo.run_argv("n", " ", cwd="/", provider="pi", labels={})

"""`deskops queue {add|run|list}` against real commands in a throwaway desk."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _cli(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    full_env = {k: v for k, v in os.environ.items() if not k.startswith("DESKOPS_")}
    full_env.update(env or {})
    full_env["PYTHONPATH"] = str(ROOT) + os.pathsep + full_env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv],
        cwd=root, capture_output=True, text=True, env=full_env,
    )


def _configure(root: Path, jobs: dict, **extra) -> None:
    config = {"project_identity": "queue-test", "queue_jobs": jobs, "queue_min_available_gb": 0,
              "queue_max_psi_avg60": 101, **extra}
    (root / "desk" / "config.json").write_text(json.dumps(config), encoding="utf-8")


def _queue(root: Path, state: str) -> list[Path]:
    return sorted((root / "runs" / "queue" / state).glob("*.json"))


def _add(root: Path, kind: str, task: str = "task-a") -> str:
    result = _cli(root, "queue", "add", kind, "--task", task, "--transition", "t->u", "--root", ".")
    assert result.returncode == 0, result.stderr or result.stdout
    return result.stdout.strip()


def _sh(script: str, timeout: int | None = None) -> dict:
    job: dict = {"run": ["sh", "-c", script]}
    if timeout is not None:
        job["timeout"] = timeout
    return job


@pytest.fixture
def desk(lifecycle_desk: Path) -> Path:
    return lifecycle_desk


def test_add_declared_and_undeclared(desk: Path) -> None:
    _configure(desk, {"suite": _sh("true")})
    job_id = _add(desk, "suite")
    files = _queue(desk, "pending")
    assert [f.stem for f in files] == [job_id]
    data = json.loads(files[0].read_text())
    assert data["id"] == job_id and data["kind"] == "suite" and data["task_id"] == "task-a"
    assert data["transition"] == "t->u" and data["enqueued_at"]
    bad = _cli(desk, "queue", "add", "nope", "--task", "x", "--root", ".")
    assert bad.returncode == 2 and "suite" in bad.stdout + bad.stderr


def test_add_reads_environment(desk: Path) -> None:
    _configure(desk, {"suite": _sh("true")})
    env = {"DESKOPS_TASK_ID": "task-env", "DESKOPS_TRANSITION": "a->b"}
    result = _cli(desk, "queue", "add", "suite", "--root", ".", env=env)
    assert result.returncode == 0, result.stderr
    data = json.loads(_queue(desk, "pending")[0].read_text())
    assert data["task_id"] == "task-env" and data["transition"] == "a->b"
    assert _cli(desk, "queue", "add", "suite", "--root", ".").returncode == 2


def test_run_success_writes_log_with_variables(desk: Path) -> None:
    _configure(desk, {"suite": _sh(
        'echo hello; echo "$DESKOPS_ROOT|$DESKOPS_TASK_ID|$DESKOPS_TRANSITION|$DESKOPS_JOB_ID|$DESKOPS_JOB_KIND"; pwd')})
    job_id = _add(desk, "suite")
    result = _cli(desk, "queue", "run", "--root", ".")
    assert result.returncode == 0, result.stderr
    assert not _queue(desk, "pending") and not _queue(desk, "running")
    data = json.loads(_queue(desk, "done")[0].read_text())
    assert data["exit_code"] == 0 and data["started_at"] and data["ended_at"]
    log = Path(data["log"]).read_text()
    assert "hello" in log
    assert f"{desk.resolve()}|task-a|t->u|{job_id}|suite" in log
    assert str(desk.resolve()) in log.splitlines()[-1]


def test_run_failure_goes_to_failed_with_inbox_note(desk: Path) -> None:
    _configure(desk, {"suite": _sh("echo boom; exit 3")})
    _add(desk, "suite")
    result = _cli(desk, "queue", "run", "--root", ".")
    assert result.returncode == 1
    data = json.loads(_queue(desk, "failed")[0].read_text())
    assert data["exit_code"] == 3
    notes = list((desk / "desk" / "inbox").glob("*.md"))
    assert len(notes) == 1
    text = notes[0].read_text()
    assert data["log"] in text and "queue: " in text


def test_timeout_fails_job(desk: Path) -> None:
    _configure(desk, {"slow": _sh("sleep 30", timeout=1)})
    _add(desk, "slow")
    result = _cli(desk, "queue", "run", "--root", ".")
    assert result.returncode == 1
    data = json.loads(_queue(desk, "failed")[0].read_text())
    assert data["timeout"] is True


def test_waits_when_memory_is_short(desk: Path) -> None:
    _configure(desk, {"suite": _sh("true")}, queue_min_available_gb=10**9)
    _add(desk, "suite")
    result = _cli(desk, "queue", "run", "--root", ".")
    assert result.returncode == 0
    assert "en espera" in result.stdout
    assert len(_queue(desk, "pending")) == 1 and not _queue(desk, "done")


def test_concurrent_runs_execute_once(desk: Path) -> None:
    marker = desk / "marker.txt"
    _configure(desk, {"slow": _sh(f"echo x >> {marker}; sleep 2")})
    _add(desk, "slow")
    argv = [sys.executable, "-m", "deskops", "queue", "run", "--root", "."]
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    procs = [subprocess.Popen(argv, cwd=desk, env=env, stdout=subprocess.PIPE, text=True) for _ in range(2)]
    outs = [p.communicate(timeout=60)[0] for p in procs]
    assert [p.returncode for p in procs] == [0, 0]
    assert sum("ocupado" in o for o in outs) == 1
    assert marker.read_text().count("x") == 1
    assert len(_queue(desk, "done")) == 1


def test_run_all_drains_in_order(desk: Path) -> None:
    order = desk / "order.txt"
    _configure(desk, {"a": _sh(f'echo "$DESKOPS_TASK_ID" >> {order}')})
    _add(desk, "a", "task-1")
    _add(desk, "a", "task-2")
    # distinct names even within one second
    result = _cli(desk, "queue", "run", "--all", "--root", ".")
    assert result.returncode == 0, result.stderr
    assert order.read_text().split() == ["task-1", "task-2"]
    assert len(_queue(desk, "done")) == 2 and not _queue(desk, "pending")


def test_interrupted_running_job_is_failed(desk: Path) -> None:
    _configure(desk, {"suite": _sh("true")})
    (desk / "runs" / "queue" / "running").mkdir(parents=True)
    job = {"id": "20260101T000000Z-suite-task-a", "kind": "suite", "task_id": "task-a",
           "transition": "", "enqueued_at": "2026-01-01T00:00:00Z"}
    (desk / "runs" / "queue" / "running" / f"{job['id']}.json").write_text(json.dumps(job))
    result = _cli(desk, "queue", "run", "--root", ".")
    assert result.returncode == 0, result.stderr
    data = json.loads(_queue(desk, "failed")[0].read_text())
    assert data["interrupted"] is True and data["exit_code"] is None
    assert not _queue(desk, "running")
    assert len(list((desk / "desk" / "inbox").glob("*.md"))) == 1


def test_list_json_has_four_states(desk: Path) -> None:
    _configure(desk, {"suite": _sh("true")})
    _add(desk, "suite")
    result = _cli(desk, "queue", "list", "--root", ".", "--format", "json")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert set(data) == {"pending", "running", "done", "failed"}
    assert len(data["pending"]) == 1
    text = _cli(desk, "queue", "list", "--root", ".")
    assert text.returncode == 0 and "pending (1)" in text.stdout


@pytest.mark.parametrize("argv", [("queue", "--help"), ("queue", "add", "--help"),
                                  ("queue", "run", "--help"), ("queue", "list", "--help")])
def test_help_exits_zero(desk: Path, argv: tuple[str, ...]) -> None:
    assert _cli(desk, *argv).returncode == 0

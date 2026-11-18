"""Host job queue: `deskops queue {add|run|list}`.

Post-hooks that run inside a container enqueue heavy jobs (full suite,
integration, push) as JSON files under ``<root>/runs/queue``; a runner on the
host takes them one at a time. A state change is an ``os.replace`` between the
state folders, so a job is always in exactly one of them.
"""

from __future__ import annotations

import contextlib
import fcntl
import io
import json
import os
import signal
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterator

from deskops.cli.render import render
from deskops.config import DeskConfig
from deskops.errors import UsageError

STATES = ("pending", "running", "done", "failed")
LOCK_NAME = "run.lock"
_MEMINFO = Path("/proc/meminfo")
_PRESSURE = Path("/proc/pressure/memory")


def queue_dir(root: Path) -> Path:
    return root / "runs" / "queue"


def _ensure_dirs(queue: Path) -> None:
    for name in (*STATES, "logs"):
        (queue / name).mkdir(parents=True, exist_ok=True)


def _load_config(root: Path) -> DeskConfig:
    return DeskConfig.load(root / "desk")


def _write_job(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def _read_job(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def enqueue(root: Path, kind: str, task_id: str | None, transition: str | None) -> str:
    config = _load_config(root)
    if kind not in config.queue_jobs:
        declared = ", ".join(sorted(config.queue_jobs)) or "(none)"
        raise UsageError(f"Unknown queue job kind '{kind}'. Declared kinds: {declared}")
    task_id = (task_id or os.environ.get("DESKOPS_TASK_ID", "")).strip()
    if not task_id:
        raise UsageError("queue add needs --task or DESKOPS_TASK_ID.")
    transition = (transition if transition is not None else os.environ.get("DESKOPS_TRANSITION", "")).strip()

    queue = queue_dir(root)
    _ensure_dirs(queue)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    while True:
        job_id = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{kind}-{task_id}"
        path = queue / "pending" / f"{job_id}.json"
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        except FileExistsError:
            now = now + timedelta(seconds=1)
            continue
        os.close(fd)
        break
    _write_job(
        path,
        {
            "id": job_id,
            "kind": kind,
            "task_id": task_id,
            "transition": transition,
            "enqueued_at": now.isoformat().replace("+00:00", "Z"),
        },
    )
    return job_id



def _jobs(queue: Path, state: str) -> list[Path]:
    folder = queue / state
    return sorted(folder.glob("*.json")) if folder.is_dir() else []


def _memory_state() -> tuple[float | None, float | None]:
    """(MemAvailable in GB, memory PSI some avg60); None when unreadable."""
    available = None
    try:
        for line in _MEMINFO.read_text(encoding="utf-8").splitlines():
            if line.startswith("MemAvailable:"):
                available = int(line.split()[1]) / (1024 * 1024)
                break
    except (OSError, ValueError, IndexError):
        pass
    avg60 = None
    try:
        for line in _PRESSURE.read_text(encoding="utf-8").splitlines():
            if line.startswith("some "):
                for part in line.split()[1:]:
                    if part.startswith("avg60="):
                        avg60 = float(part.split("=", 1)[1])
    except (OSError, ValueError):
        pass
    return available, avg60


def wait_reason(config: DeskConfig) -> str | None:
    available, avg60 = _memory_state()
    if available is not None and available < config.queue_min_available_gb:
        return f"memoria disponible {available:.1f} GB < minimo {config.queue_min_available_gb} GB"
    if avg60 is not None and avg60 >= config.queue_max_psi_avg60:
        return f"presion de memoria avg60 {avg60:.2f} >= maximo {config.queue_max_psi_avg60:g}"
    return None


def _notify_failure(root: Path, job: dict[str, Any], *, interrupted: bool) -> None:
    """Leave an inbox note with the function behind `deskops message send`."""
    from deskops.cli.commands.message import MessageCLI

    if interrupted:
        body = f"Trabajo {job['id']} interrumpido. Tipo: {job['kind']}. Tarea: {job['task_id']}."
    else:
        code = "timeout" if job.get("timeout") else job.get("exit_code")
        body = (
            f"Tipo: {job['kind']}. Tarea: {job['task_id']}. "
            f"Codigo de salida: {code}. Log: {job.get('log')}"
        )
    args = SimpleNamespace(
        title=f"queue: {job['id']}",
        message=body,
        kind="unclear",
        root=str(root),
        desk_root=None,
        repo=None,
        store=None,
        pythonpath=None,
        sender=None,
        format="json",
    )
    cwd = os.getcwd()
    try:
        os.chdir(root)
        with contextlib.redirect_stdout(io.StringIO()):
            MessageCLI()._deliver_note(args)
    except Exception as exc:  # the job already failed; a lost note must not hide that
        print(f"Warning: could not leave the inbox note for {job['id']}: {exc}", file=sys.stderr)
    finally:
        os.chdir(cwd)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _recover_interrupted(root: Path, queue: Path) -> None:
    for path in _jobs(queue, "running"):
        job = _read_job(path)
        job.update({"ended_at": _now(), "exit_code": None, "interrupted": True})
        _write_job(path, job)
        os.replace(path, queue / "failed" / path.name)
        _notify_failure(root, job, interrupted=True)


def _execute(root: Path, queue: Path, config: DeskConfig, path: Path) -> bool:
    """Run one pending job; True when it succeeded."""
    running = queue / "running" / path.name
    os.replace(path, running)
    job = _read_job(running)
    spec = config.queue_jobs.get(job["kind"])
    log_path = queue / "logs" / f"{job['id']}.log"
    job["started_at"] = _now()
    job["log"] = str(log_path)
    code: int | None = None
    if spec is None:
        log_path.write_text(f"queue kind '{job['kind']}' is no longer declared in queue_jobs\n", encoding="utf-8")
        code = 127
    else:
        env = dict(os.environ)
        env.update(
            DESKOPS_ROOT=str(root),
            DESKOPS_TASK_ID=job["task_id"],
            DESKOPS_TRANSITION=job.get("transition", ""),
            DESKOPS_JOB_ID=job["id"],
            DESKOPS_JOB_KIND=job["kind"],
        )
        with log_path.open("wb") as log:
            try:
                proc = subprocess.Popen(
                    spec.run, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL, start_new_session=True,
                )
            except OSError as exc:
                log.write(f"cannot start {spec.run}: {exc}\n".encode())
                code = 127
            else:
                try:
                    code = proc.wait(timeout=spec.timeout)
                except subprocess.TimeoutExpired:
                    with contextlib.suppress(ProcessLookupError):
                        os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
                    job["timeout"] = True
                    code = None
    job["ended_at"] = _now()
    if not job.get("timeout"):
        job["exit_code"] = code
    ok = code == 0
    _write_job(running, job)
    os.replace(running, queue / ("done" if ok else "failed") / path.name)
    if not ok:
        _notify_failure(root, job, interrupted=False)
    return ok


@contextlib.contextmanager
def _try_lock(queue: Path) -> Iterator[bool]:
    with (queue / LOCK_NAME).open("a+") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def run_queue(root: Path, run_all: bool) -> int:
    queue = queue_dir(root)
    _ensure_dirs(queue)
    config = _load_config(root)
    with _try_lock(queue) as locked:
        if not locked:
            print("ocupado: otro queue run en curso")
            return 0
        _recover_interrupted(root, queue)
        while True:
            pending = _jobs(queue, "pending")
            if not pending:
                print("sin trabajos")
                return 0
            reason = wait_reason(config)
            if reason:
                print(f"en espera: {reason}")
                return 0
            path = pending[0]
            print(f"ejecutando {path.stem}")
            if not _execute(root, queue, config, path):
                print(f"fallo {path.stem}")
                return 1
            print(f"listo {path.stem}")
            if not run_all:
                return 0


def list_jobs(root: Path) -> dict[str, list[dict[str, Any]]]:
    queue = queue_dir(root)
    result: dict[str, list[dict[str, Any]]] = {}
    for state in STATES:
        items = []
        for path in _jobs(queue, state):
            job = _read_job(path)
            job["state"] = state
            items.append(job)
        result[state] = items
    return result


class QueueCLI:
    """`deskops queue {add|run|list}`; the subcommand is required."""

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        cmd = args.queue_command
        if cmd == "add":
            print(enqueue(root, args.kind, args.task, args.transition))
            return 0
        if cmd == "run":
            return run_queue(root, bool(args.all))
        if cmd == "list":
            return render(list_jobs(root), args.format, _format_list)
        raise UsageError(f"Unknown queue command: {cmd}")


def _format_list(data: dict[str, list[dict[str, Any]]]) -> str:
    lines: list[str] = []
    for state in STATES:
        lines.append(f"{state} ({len(data[state])})")
        for job in data[state]:
            extra = ""
            if state in ("done", "failed"):
                extra = " | timeout" if job.get("timeout") else f" | exit {job.get('exit_code')}"
            lines.append(f"  {job['id']} | {job['kind']} | {job['task_id']}{extra}")
    return "\n".join(lines)

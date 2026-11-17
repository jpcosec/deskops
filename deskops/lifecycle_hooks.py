"""Run the post-hooks of a lifecycle transition (``attributes.hooks`` of its RelationDoc).

``deskops advance task`` calls ``run_hooks`` after it persisted the transition. Hooks are
commands (argument lists, no shell) run in order from the desk root with ``DESKOPS_ROOT``,
``DESKOPS_TASK_ID``, ``DESKOPS_TRANSITION``, ``DESKOPS_FROM_NODE`` and ``DESKOPS_TO_NODE`` in
their environment. One log per advance, ``runs/hooks/<task id>/<relation_type>-<AAAAMMDDTHHMMSSZ>.log``,
records each hook that ran: its name, arguments, result and standard output and error.
The first hook that exits non-zero or exceeds its timeout stops the chain.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
import os
from pathlib import Path
import subprocess

from deskops.lifecycle import Hook
from deskops.lifecycle import Transition

HOOKS_RUNS_DIR = Path("runs") / "hooks"


@dataclass(frozen=True, slots=True)
class HookFailure:
    hook: str
    #: The exit code, or None when the hook ran out of time.
    exit_code: int | None
    timeout: int
    log: str

    @property
    def outcome(self) -> str:
        return f"timeout tras {self.timeout} s" if self.exit_code is None else f"codigo de salida {self.exit_code}"

    def finding(self, relation_type: str) -> str:
        """The error finding ``deskops advance`` prints (``finding_line`` format)."""
        return f"error: [lifecycle/hook-failed] {relation_type}: hook '{self.hook}' fallo: {self.outcome}; log: {self.log}"


def log_path(task_id: str, relation_type: str, now: datetime | None = None) -> Path:
    stamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    return HOOKS_RUNS_DIR / task_id / f"{relation_type}-{stamp}.log"


def _text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    return value.decode("utf-8", "replace") if isinstance(value, bytes) else value


def run_hooks(root: Path, task_id: str, transition: Transition, target: str, hooks: tuple[Hook, ...]) -> HookFailure | None:
    """Run ``hooks`` in order; None when all succeed, else the failure of the first that did not."""
    if not hooks:
        return None
    root = root.resolve()
    rel_log = log_path(task_id, transition.relation_type)
    log = root / rel_log
    log.parent.mkdir(parents=True, exist_ok=True)
    env = {
        **os.environ,
        "DESKOPS_ROOT": str(root),
        "DESKOPS_TASK_ID": task_id,
        "DESKOPS_TRANSITION": transition.relation_type,
        "DESKOPS_FROM_NODE": transition.source,
        "DESKOPS_TO_NODE": target,
    }
    with log.open("w", encoding="utf-8") as handle:
        for hook in hooks:
            exit_code: int | None
            stdout = stderr = ""
            try:
                done = subprocess.run(list(hook.run), cwd=root, env=env, capture_output=True, timeout=hook.timeout, check=False)
                exit_code, stdout, stderr = done.returncode, _text(done.stdout), _text(done.stderr)
                result = f"exit {exit_code}"
            except subprocess.TimeoutExpired as exc:
                exit_code, stdout, stderr = None, _text(exc.stdout), _text(exc.stderr)
                result = f"timeout tras {hook.timeout} s"
            except OSError as exc:
                exit_code, stderr = 127, f"{exc}\n"
                result = f"exit {exit_code}"
            handle.write(f"== hook {hook.name}\nrun: {list(hook.run)}\nresult: {result}\n--- stdout\n{stdout}\n--- stderr\n{stderr}\n")
            handle.flush()
            if exit_code != 0:
                return HookFailure(hook.name, exit_code, hook.timeout, rel_log.as_posix())
    return None

"""Wake the desk's scion identity when work (an inbox note) reaches it."""

from __future__ import annotations

import subprocess
from pathlib import Path

from deskops.config import DeskConfig
from deskops import queue

WAKE_TIMEOUT = 60
WAKE_JOB_KIND = "wake-identity"


def wake_identity(root: Path, note_name: str) -> str | None:
    """Wake the identity of the desk at ``root``; None when it has nothing to wake.

    Returns "despertado", "fallo: <rc>" or "bloqueado: <motivo>".
    """
    config = DeskConfig.load(Path(root) / "desk")
    identity = config.identity
    if identity is None or not identity.wake:
        return None
    reason = queue.wait_reason(config)
    if reason:
        return f"bloqueado: {reason}"
    markers = {"agent": identity.agent, "project": identity.scion_project, "note": note_name}
    argv = [_fill(part, markers) for part in identity.command]
    try:
        completed = subprocess.run(
            argv, stdin=subprocess.DEVNULL, capture_output=True, timeout=WAKE_TIMEOUT, check=False
        )
    except subprocess.TimeoutExpired:
        return "fallo: timeout"
    except OSError as exc:
        return f"fallo: {exc}"
    return "despertado" if completed.returncode == 0 else f"fallo: {completed.returncode}"


def _fill(part: str, markers: dict[str, str]) -> str:
    for key, value in markers.items():
        part = part.replace("{" + key + "}", value)
    return part

"""Paseo runtime for `deskops dispatch`: the agents run as processes of the local paseo daemon.

Paseo (https://paseo.sh) launches the provider CLI (pi, claude, codex...) on the host, in the cwd it is
given, and keeps the conversation: an idle agent's process is released after an hour and the next
message resumes it. There are no templates and no container: the role's instructions travel in the
prompt file, and the executor's isolation is its git worktree.

Every call to paseo goes through ``dispatch._paseo``; this module only builds argv and reads JSON.
"""

from __future__ import annotations

import json
from typing import Any

# paseo agent status -> the (phase, activity) pair dispatch already reasons about
_STATUS = {
    "running": ("running", ""),
    "initializing": ("running", ""),
    "idle": ("running", "completed"),  # the turn ended: the agent is done with its task
    "closed": ("stopped", "stopped"),  # the process was released (idle cleanup or daemon restart)
    "error": ("error", "error"),
}


def run_argv(
    name: str,
    prompt: str,
    *,
    cwd: str,
    provider: str,
    labels: dict[str, str],
    model: str | None = None,
    mode: str | None = None,
) -> list[str]:
    """`paseo run` for one deterministic agent identity, detached (``--no-wait``), JSON out."""
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    argv = ["paseo", "run", "--no-wait", "--json", "--title", name, "--provider", provider, "--cwd", cwd]
    if model:
        argv += ["--model", model]
    if mode:
        argv += ["--mode", mode]
    for key, value in labels.items():
        argv += ["--label", f"{key}={value}"]
    return [*argv, prompt]


def list_argv() -> list[str]:
    """Every agent of the daemon, in any directory and archived too (the name is the identity)."""
    return ["paseo", "ls", "--global", "--all", "--json"]


def delete_argv(agent_id: str) -> list[str]:
    """Interrupt the agent if it is running, then delete it."""
    return ["paseo", "delete", agent_id, "--json"]


def parse_json(stdout: str) -> Any:
    """The JSON document of a paseo command (paseo may print notices before it)."""
    text = stdout or ""
    starts = [i for i in (text.find("["), text.find("{")) if i >= 0]
    if not starts:
        raise ValueError("paseo no devolvio JSON")
    return json.loads(text[min(starts):])


def normalize(agent: dict[str, Any]) -> dict[str, Any]:
    """A paseo agent as the scion-shaped dict dispatch reads: name, phase, activity, labels, id."""
    status = str(agent.get("status", ""))
    phase, activity = _STATUS.get(status, (status or "unknown", ""))
    return {
        "id": str(agent.get("id") or agent.get("agentId") or ""),
        "name": str(agent.get("name") or agent.get("title") or ""),
        "phase": phase,
        "activity": activity,
        "labels": dict(agent.get("labels") or {}),
        "status": status,
    }

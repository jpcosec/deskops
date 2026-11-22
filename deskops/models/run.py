from pydantic import Field
from pydantic import field_validator

from sldb import StructuredNLDoc


class RunDoc(StructuredNLDoc):
    """One supervised agent execution: one RunDoc per attempt.

    Writers. ``deskops.runtime.scion.record_scion_run`` (runtime template and
    ``deskops dispatch start``) creates the RunDoc at ``<run_dir>/run.md`` with
    outcome ``in_progress`` and ``intent_at`` set: intent, not proof of start.
    ``confirm_scion_dispatch`` sets ``dispatch_confirmed_at`` once the agent is
    observed in Scion. ``deskops closeout commit --run-dir`` updates the RunDoc
    whose ``run_dir`` matches (outcome, commit_sha, ended_at); ``resolved-by``
    and ``--no-run`` have no run dir and never touch a RunDoc.

    Id format: ``run-<agent_slug>`` for attempt 1 and ``run-<agent_slug>-a2``
    for attempt 2, like the child name in the dispatch contract of
    ``desk/roles/deskops-supervisor.md``. The attempt comes from the
    ``deskops.attempt`` label of the dispatch; there is no counter, and a retry
    never overwrites the earlier RunDoc. ``external_ref`` is
    ``scion://agent/<slug>``. Scion's API does not expose the execution run id
    (``Agent.RunID``/``PreviousRunIDs`` are ``json:"-"``), so only this internal
    identity is used. Documents written before ``intent_at``,
    ``dispatch_confirmed_at`` and ``external_ref`` existed read with them empty.
    """

    __references__ = ["task_id", "role_id"]
    __semantics__ = {"type": ["workflow", "run"], "workspace": ["desk", "runs"]}
    __template__ = """---
# run-xxx
id: ⸢rev•id⸥
# Task identifier this run executed against
task_id: ⸢rev•task_id⸥
# Role identifier dispatched for this run
role_id: ⸢rev•role_id⸥
# Runtime binary identifier, matching RuntimeProfileDoc.kind
kind: ⸢rev•kind⸥
# Run evidence directory, relative to the project root
run_dir: ⸢rev•run_dir⸥
# Herdr pane identifier, empty if not recorded
herdr_pane_id: ⸢rev•herdr_pane_id⸥
# Session/transcript file path, relative to the project root
session_path: ⸢rev•session_path⸥
# SHA-256 digest of the session file
session_sha256: ⸢rev•session_sha256⸥
# ISO 8601 start timestamp
started_at: ⸢rev•started_at⸥
# ISO 8601 timestamp when the dispatch intent was recorded
intent_at: ⸢rev•intent_at⸥
# ISO 8601 timestamp when the agent was observed in Scion, empty until then
dispatch_confirmed_at: ⸢rev•dispatch_confirmed_at⸥
# External reference, e.g. scion://agent/<slug>
external_ref: ⸢rev•external_ref⸥
# ISO 8601 end timestamp, empty while in progress
ended_at: ⸢rev•ended_at⸥
# in_progress | success | failure | aborted
outcome: ⸢rev•outcome⸥
# Closeout commit hash, empty until closeout completes
commit_sha: ⸢rev•commit_sha⸥
# e.g. system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what this run attempted and its result._

⸢rev•summary⸥
""".strip()

    id: str = Field(description="Stable run identifier, 'run-<agent_slug>' for attempt 1, 'run-<agent_slug>-a2' for attempt 2.")
    title: str = Field(description="Short human-readable label for the run.")
    summary: str = Field(description="Short summary of what this run attempted and its result.")
    task_id: str = Field(description="TaskDoc identifier this run executed against.")
    role_id: str = Field(description="RoleDoc identifier that was dispatched for this run.")
    kind: str = Field(description="Runtime binary identifier used for this run, matching RuntimeProfileDoc.kind.")
    run_dir: str = Field(description="Path to the run evidence directory under runs/subagents/, relative to the project root.")
    herdr_pane_id: str = Field(
        default="", description="Herdr pane identifier the agent ran in; empty if not recorded or the pane no longer exists."
    )
    session_path: str = Field(
        default="", description="Path to the session/transcript file produced by the runtime, relative to the project root."
    )
    session_sha256: str = Field(
        default="",
        description="SHA-256 digest of the session file at the time it was last recorded, matching the closeout commit trailer.",
    )
    started_at: str = Field(description="ISO 8601 timestamp when the run started.")
    intent_at: str = Field(default="", description="ISO 8601 timestamp when the runtime template recorded the dispatch intent.")
    dispatch_confirmed_at: str = Field(
        default="", description="ISO 8601 timestamp when the agent was observed in Scion; empty until confirmed."
    )
    external_ref: str = Field(default="", description="External reference of the run, e.g. 'scion://agent/<slug>'.")
    ended_at: str = Field(default="", description="ISO 8601 timestamp when the run ended; empty while the run is in progress.")
    outcome: str = Field(default="in_progress", description="Run outcome: in_progress, success, failure, or aborted.")
    commit_sha: str = Field(
        default="", description="Git commit hash of the closeout commit linked to this run; empty until closeout completes."
    )
    tags: list[str] = Field(
        default_factory=list, description="Semantic tags placed at the end, using namespaced forms such as 'system:deskops'."
    )

    @field_validator("intent_at", "dispatch_confirmed_at", "external_ref", mode="before")
    @classmethod
    def _absent_means_empty(cls, value: object) -> object:
        """RunDocs written before these fields existed read them as empty, not as a validation error."""
        return "" if value is None else value

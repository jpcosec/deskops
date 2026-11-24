from typing import Literal, Optional

from pydantic import Field, field_validator

from sldb import StructuredNLDoc


class InboxNoteDoc(StructuredNLDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "inbox-note-{slug}",
        "status_default": "open",
        "tags": [],
    }
    __semantics__ = {
        "type": ["desk", "inbox-note"],
        "workspace": ["desk", "inbox"],
    }
    __template__ = """---
# unclear | suggestion
kind: ⸢rev•kind⸥
# e.g., other_repo
sender_project: ⸢optrev•sender_project⸥
# e.g., target_repo
target_project: ⸢optrev•target_project⸥
# ISO 8601 timestamp
created_at: ⸢rev•created_at⸥
# open | closed
status: ⸢rev•status⸥
# project identity that acknowledged the note
acknowledged_by: ⸢optrev•acknowledged_by⸥
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: ⸢optrev•acknowledged_at⸥
# why the note was acknowledged; empty when no reason was given
ack_reason: ⸢optrev•ack_reason⸥
# conversation thread/message the note came from, e.g. #hilo/1234
conversation_ref: ⸢optrev•conversation_ref⸥
---

# ⸢rev•title⸥

_Describe the incoming message with enough evidence to triage._

⸢rev,markdown•body⸥
"""

    kind: Literal["unclear", "suggestion"] = Field(
        description="Inbox note type indicating unresolved confusion or an improvement proposal."
    )
    sender_project: Optional[str] = Field(
        default=None,
        description="Project that sent the inbox message, resolved from the repo registry when possible."
    )
    target_project: Optional[str] = Field(
        default=None,
        description="Project the inbox note targets, resolved from the shared desk identity contract."
    )
    created_at: str = Field(description="Timestamp for when the inbox note was created.")
    status: Literal["open", "closed"] = Field(
        description="Whether the inbox note is still open or already handled."
    )
    acknowledged_by: Optional[str] = Field(
        default=None,
        description="Project identity that acknowledged and closed the inbox note."
    )
    acknowledged_at: Optional[str] = Field(
        default=None,
        description="Timestamp for when the inbox note was acknowledged and closed."
    )
    ack_reason: str = Field(
        default="",
        description="Why the inbox note was acknowledged, recorded by `deskops message ack --reason`; empty when none was given."
    )

    conversation_ref: Optional[str] = Field(
        default=None,
        description='Optional conversation reference in the form "<thread>/<message id>" or just "<thread>" (e.g. "#acuerdos-sldb1/1234"); empty is not written.',
    )

    @field_validator("conversation_ref", mode="before")
    @classmethod
    def _blank_conversation_ref_is_absent(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value.strip() if isinstance(value, str) else value

    @field_validator("ack_reason", mode="before")
    @classmethod
    def _absent_ack_reason_is_empty(cls, value: object) -> object:
        # A note written before ack_reason existed has no such key and reads as ''.
        return "" if value is None else value

    title: str = Field(description="Inbox note title shown as the H1 heading.")
    body: str = Field(description="Markdown body describing the question or suggestion in detail.")

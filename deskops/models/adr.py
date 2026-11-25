"""``atom.adr``: an accepted architecture decision is an atom that answers *why*.

An atom type is a model, like a task type (``task_types.py``): ``AtomAdrDoc`` extends
``AtomDoc`` and only *adds* (``AtomDoc``, its contract and its hash do not change), and
``ATOM_TYPE_MODELS`` maps the type name to the model the way ``TASK_TYPE_MODELS`` does.

A decision still pending is not an atom: it is a ``task.decision`` that closes citing the
``atom.adr``. The rules that guard the type are ``RuleDoc`` seeds in ``deskops/data/rules/``
(``rule-adr-*``), not Python here:

- ``rule-adr-owner-receipt``: an ADR carries an accepted, intact ``owner`` review receipt
  whose subject is the ADR (``deskops review record --kind owner``; only JP disposes it).
- ``rule-adr-supersedes``: no ``accepted`` ADR has a *full* ``supersedes`` pointing at it
  from another ``accepted`` ADR. A partial replacement (``partial_supersedes``, with the
  section it replaces in ``superseded_section``) leaves the earlier ADR ``accepted``.

``supersedes`` and ``partial_supersedes`` are reference fields because a rule walks edges
(``^supersedes``) and cannot read a ``RelationDoc``'s attributes; ``deskops add atom
--supersedes`` also records the ``supersedes`` ``RelationDoc`` (``section`` as attribute) for
the graph. What the ADR applies to goes in ``references`` (the common pointers field does not
exist yet on ``AtomDoc``; the day it does, ``references`` is what moves there).
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from .atom import AtomDoc, AtomQuestion, check_slug_id

ADR_TYPE = "atom.adr"
ADR_STATUSES = ("accepted", "superseded")


class AtomAdrDoc(AtomDoc):
    """``atom.adr``: the decision as the answer to *why*, with context, consequences and what it replaces."""

    __artifact__ = {
        "id_pattern": "atom-{slug}",
        "status_default": "accepted",
        "tags": ["system:deskops", "topic:atoms"],
    }
    # Editing the status or the replaced ADRs is the effect of a later decision, not a change of
    # this one: only the decision itself is what the owner receipt is anchored to.
    __contract__ = ["title", "answer", "context", "consequences", "decided_on", "decided_by"]
    __references__ = ["supersedes", "partial_supersedes"]
    __reference_models__ = {"supersedes": ["AtomAdrDoc"], "partial_supersedes": ["AtomAdrDoc"]}
    __template__ = """---
id: ⸢rev•id⸥
atom_type: ⸢optrev•atom_type⸥
status: ⸢optrev•status⸥
five_wh_one_plus: ⸢optrev•five_wh_one_plus⸥
decided_on: ⸢rev•decided_on⸥
decided_by: ⸢rev•decided_by⸥
supersedes: ⸢optrev,list•supersedes⸥
partial_supersedes: ⸢optrev,list•partial_supersedes⸥
superseded_section: ⸢optrev•superseded_section⸥
references: ⸢optrev,list•references⸥
pointers: ⸢optrev,list•pointers⸥
tags: ⸢optrev,list•tags⸥
provenance: ⸢optrev•provenance⸥
conversation_ref: ⸢optrev•conversation_ref⸥
---

# ⸢rev•title⸥

## Context

⸢rev•context⸥

## Decision

⸢rev•answer⸥

## Consequences

⸢rev•consequences⸥

## Alternatives

⸢optrev•alternatives⸥
""".strip()

    atom_type: Literal["atom.adr"] = Field(
        default="atom.adr",
        description="Atom type; fixed to 'atom.adr' for this model.",
    )
    status: Literal["accepted", "superseded"] = Field(
        default="accepted",
        description="'accepted' while in force; 'superseded' once an accepted ADR replaces it in full.",
    )
    five_wh_one_plus: AtomQuestion = Field(
        default=AtomQuestion.WHY,
        description="An ADR answers why; the decision is the answer.",
    )
    decided_on: str = Field(description="Date of the decision, YYYY-MM-DD.", pattern=r"^\d{4}-\d{2}-\d{2}$")
    decided_by: str = Field(description="Who made the decision (the owner who disposes the receipt).")
    context: str = Field(description="The forces and the situation that made the decision necessary.")
    consequences: str = Field(description="What the decision makes easier, harder or impossible.")
    alternatives: str | None = Field(default=None, description="Optional: what was considered and discarded.")
    supersedes: list[str] = Field(
        default_factory=list,
        description="Ids of the ADRs this one replaces in full; each becomes 'superseded'.",
    )
    partial_supersedes: list[str] = Field(
        default_factory=list,
        description="Ids of the ADRs this one replaces only in a section; each stays 'accepted'.",
    )
    superseded_section: str | None = Field(
        default=None,
        description="With partial_supersedes: the section of the earlier ADR this one replaces.",
    )
    references: list[str] = Field(
        default_factory=list,
        description="What the decision applies to: files, documents, repositories or tasks.",
    )

    @field_validator("answer", "context", "consequences", mode="before")
    @classmethod
    def _text_not_blank(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            raise ValueError("an ADR section cannot be blank")
        return value

    @field_validator("supersedes", "partial_supersedes", mode="before")
    @classmethod
    def _replaced_ids_are_atoms(cls, value: object) -> object:
        if isinstance(value, list):
            for item in value:
                check_slug_id(item, "atom-", "atom")
        return value


#: Atom type name -> model class, as ``TASK_TYPE_MODELS`` is for tasks. ``AtomDoc`` itself is
#: the untyped atom and is not listed.
ATOM_TYPE_MODELS: dict[str, type[AtomDoc]] = {
    ADR_TYPE: AtomAdrDoc,
}

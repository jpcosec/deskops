FILE:desk/tasks/task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt.md
---
sldb:
  by: agent
  at: '2026-11-23T04:38:53Z'
  authority: generated
  via: create_document
id: task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261123-024325-suggestion-campo-propio-para-la-referencia-de-conversacion-scion-en-atoms-y-notas.md
depends_on: []
pills: []
files:
- deskops/models/atom.py
- deskops/models/inbox.py
- deskops/cli/commands/atoms.py
- deskops/cli/commands/message.py
- tests/test_atoms_cli.py
- tests/test_message_cli.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# AtomDoc e InboxNoteDoc ganan conversation_ref, add atom y message send aceptan --conv y list atoms filtra por --conv

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-024325 (hilo #acuerdos-sldb1 del proyecto scion wf-desks, encargo de JP vía scion-coordination): hoy la referencia conv/#hilo de un acuerdo va en --provenance y en el texto del atom (así lo hace /mnt/ssd/proyectos/wf-desks/bin/desk-prompt.sh), y no se pueden listar los acuerdos de una conversación. Se pide un campo propio.

## Goal

_Describe the concrete result this task must produce._

(1) AtomDoc (deskops/models/atom.py) e InboxNoteDoc (deskops/models/inbox.py) ganan conversation_ref: str | None (por defecto None), con la forma "<hilo>/<id de mensaje>" o solo "<hilo>" (por ejemplo "#acuerdos-sldb1/1234"); vacío no se escribe. (2) deskops add atom --conv <ref> y deskops message send --conv <ref> lo llenan. (3) deskops list atoms --conv <hilo> lista solo los atoms cuyo conversation_ref es ese hilo o empieza por "<hilo>/"; con --format json incluye el campo. (4) deskops add atom con un --conv que ya tiene otro atom avisa en stderr "ya existe <atom id> con conversation_ref <ref>" y no crea un duplicado (sale con código 1).

## Scope

_State what is in scope and what is out of scope._

Entra: los dos modelos, deskops/cli/commands/atoms.py, deskops/cli/commands/message.py, los goldens de contrato y de ayuda, sldb models update de los dos modelos en el store del desk, tests/test_atoms_cli.py y tests/test_message_cli.py. No entra: un verbo nuevo add agreement (el campo cubre el pedido), migrar los atoms viejos que tienen la referencia en provenance.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_atoms_cli.py: test_add_atom_with_conv_writes_conversation_ref, test_list_atoms_filters_by_conv, test_add_atom_refuses_duplicate_conv. p2: test en tests/test_message_cli.py: test_send_with_conv_writes_conversation_ref. p3: implementar. p4: goldens y sldb models update AtomDoc e InboxNoteDoc en .sldb. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_atoms_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los cuatro tests nuevos pasan, deskops doctor --root . no suma errores por los atoms e inbox existentes (que no traen el campo), y sldb stores check --store .sldb no suma errores nuevos.

FILE:deskops/models/atom.py
from enum import StrEnum
import re
from typing import Annotated

from pydantic import Field, field_validator

from sldb import StructuredNLDoc

from .crossroad import check_domain_path

ATOM_TAG_PATTERN = r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$"
# The value is dot-separated segments, none empty (no ``a..b``, ``a.`` or ``.a``): sldb's
# ``tag_folder`` refuses an empty segment (CC35d H3) and deskops derives atom folders with it.
# Checked by ``check_atom_tags`` and not in the field's schema pattern, so the model contract
# (its hash, which every store records) stays the same.
ATOM_TAG_SEGMENTS_PATTERN = r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_-]*(\.[a-z0-9_-]+)*$"
DOMAIN_NAMESPACE = "domain"
_ATOM_TAG = re.compile(ATOM_TAG_PATTERN)
_ATOM_TAG_SEGMENTS = re.compile(ATOM_TAG_SEGMENTS_PATTERN)


class AtomQuestion(StrEnum):
    WHAT = "what"
    WHY = "why"
    HOW = "how"
    HOW_NOT = "how_not"
    WHEN = "when"
    WHERE = "where"
    FOR_WHOM = "for_whom"


AtomTag = Annotated[
    str,
    Field(
        pattern=ATOM_TAG_PATTERN,
        description="Namespaced semantic tag in the form namespace:value.",
    ),
]


def check_slug_id(value: object, prefix: str, label: str) -> object:
    """``<prefix><slug>``, where the slug is already in slug form. Anything else is left to pydantic."""
    if not isinstance(value, str):
        return value
    # Lazy: doc_access imports the models, and the slug form is defined once, there.
    from deskops.doc_access import slug_form

    slug = value.removeprefix(prefix)
    if not value.startswith(prefix) or not slug or slug != slug_form(slug):
        raise ValueError(f"{label} id must follow slug convention {prefix}<slug>: {value}")
    return value


def check_atom_tags(tags: object) -> object:
    """Each tag is ``namespace:value``; each ``domain:`` value is a domain path (its own, more
    specific message), and any other value has no empty dot segment. Anything that is not a list
    of strings is left to pydantic."""
    if not isinstance(tags, list):
        return tags
    for tag in tags:
        if not isinstance(tag, str):
            continue
        if _ATOM_TAG.fullmatch(tag) is None:
            raise ValueError(f"Invalid atom tag '{tag}'. Expected namespace:value.")
        namespace, value = tag.split(":", 1)
        if namespace == DOMAIN_NAMESPACE:
            check_domain_path(value)
        elif _ATOM_TAG_SEGMENTS.fullmatch(tag) is None:
            raise ValueError(
                f"Invalid atom tag '{tag}': the value has an empty segment; separate non-empty segments with single dots."
            )
    return tags


def domain_paths(tags: list[str]) -> list[str]:
    """Values of the ``domain:`` tags, in order."""
    values: list[str] = []
    for tag in tags:
        match = _ATOM_TAG.fullmatch(str(tag))
        if match is not None and str(tag).split(":", 1)[0] == DOMAIN_NAMESPACE:
            values.append(str(tag).split(":", 1)[1])
    return values


class AtomDoc(StructuredNLDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "atom-{slug}",
        "status_default": None,
        "tags": ["system:deskops", "topic:atoms"],
    }
    __semantics__ = {
        "type": ["knowledge", "atom"],
        "workspace": ["desk", "atoms"],
    }
    __template__ = """---
id: ⸢rev•id⸥
title: ⸢rev•title⸥
five_wh_one_plus: ⸢rev•five_wh_one_plus⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•title⸥

## Answer

⸢rev•answer⸥
""".strip()

    id: str = Field(
        description="Stable, unique atom identifier, conventionally 'atom-<slug>'."
    )
    title: str = Field(
        description="Short, descriptive title for the atomic knowledge unit."
    )
    five_wh_one_plus: AtomQuestion = Field(
        description=(
            "The single 5WH1+ question this atom answers: one of "
            "what, why, how, how_not, when, where, for_whom."
        )
    )
    answer: str = Field(
        description=(
            "The curated raw answer to the selected 5WH1+ question, written as "
            "one stable knowledge unit."
        )
    )
    tags: list[AtomTag] = Field(
        default_factory=list,
        description=(
            "Namespaced semantic tags used for retrieval and grouping, each in the "
            "form namespace:value (e.g. system:deskops, topic:templates). Tags do "
            "not encode lifecycle, relations, evidence, or materialization."
        ),
    )
    provenance: str | None = Field(
        default=None,
        description=(
            "Optional URL or path to the authoritative source of this atom's "
            "knowledge. Used for traceability and provenance tracking."
        ),
    )

    @field_validator("id", mode="before")
    @classmethod
    def _id_follows_the_slug_convention(cls, value: object) -> object:
        return check_slug_id(value, "atom-", "atom")

    @field_validator("tags", mode="before")
    @classmethod
    def _tags_are_namespaced(cls, tags: object) -> object:
        return check_atom_tags(tags)

FILE:deskops/models/inbox.py
from typing import Literal, Optional

from pydantic import Field, field_validator

from sldb import StructuredNLDoc


class InboxNoteDoc(StructuredNLDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "inbox-note-{slug}",
        "status_default": "open",
        "tags": ["workspace:desk", "artifact:inbox-note"],
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

    @field_validator("ack_reason", mode="before")
    @classmethod
    def _absent_ack_reason_is_empty(cls, value: object) -> object:
        # A note written before ack_reason existed has no such key and reads as ''.
        return "" if value is None else value

    title: str = Field(description="Inbox note title shown as the H1 heading.")
    body: str = Field(description="Markdown body describing the question or suggestion in detail.")

FILE:deskops/cli/commands/atoms.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from deskops.atom_tags import add_namespace
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import ensure_default_namespaces
from deskops.atom_tags import sync_tag_declaration
from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.domain_tree import DomainTree
from deskops.operations import DeskopsOperations


class AtomsCLI:
    def run(self, args: Any) -> int:
        root = Path(getattr(args, "root", ".")).resolve()
        registry_path = default_registry_path(root)
        operations = DeskopsOperations(root)

        if args.atoms_command == "add-namespace":
            ensure_default_namespaces(registry_path)
            try:
                add_namespace(
                    registry_path,
                    args.namespace,
                    meaning=args.meaning,
                    use_when=args.use_when,
                    do_not_use_when=args.do_not_use_when,
                    examples=list(args.example or []),
                )
            except ValueError as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Added atom tag namespace {args.namespace}")
            print(f"Path: {registry_path}")
            # The store declares the registry's namespaces (sldb checks them): keep it in step.
            sync_tag_declaration(root)
            return 0

        if args.atoms_command == "validate":
            try:
                results = operations.validate_atoms(args.doc_id if not getattr(args, "all", False) else None)
                if getattr(args, "all", False):
                    results = _with_domain_checks(results, DomainTree(root).check())
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            invalid = False
            for record in results:
                print(f"Atom: {record['id']}")
                print(f"Path: {record['path']}")
                if record["errors"]:
                    invalid = True
                    for error in record["errors"]:
                        print(f"- {error}")
                else:
                    print("- valid")
            return 1 if invalid else 0

        if args.atoms_command == "create":
            try:
                result = operations.create_atom_from_source(
                    args.doc_id,
                    five_wh_one_plus=args.five_wh_one_plus,
                    title=getattr(args, "title", None),
                    tags=list(args.tag or []),
                    from_pill=getattr(args, "from_pill", None),
                    from_graph=getattr(args, "from_graph", None),
                    from_diagram=getattr(args, "from_diagram", None),
                    graph_path=getattr(args, "graph", None),
                )
            except (FileNotFoundError, ValueError, FileExistsError, RuntimeError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Created atom {result.doc_id}")
            print(f"Path: {result.path}")
            print(f"Source kind: {result.source_kind}")
            print(f"Source selector: {result.source_selector}")
            print(f"Source provenance: {result.provenance}")
            return 0

        if args.atoms_command == "delete":
            try:
                record = operations.delete_atom(args.doc_id, force=bool(getattr(args, "force", False)))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Deleted atom {record.doc_id}")
            print(f"Path: {record.path}")
            print(f"Store untracked: {'yes' if record.kind == 'atom-untracked' else 'no'}")
            return 0

        if args.atoms_command == "split":
            try:
                result = operations.split_atom(
                    args.doc_id,
                    into_ids=list(args.into or []),
                    section_flags=list(args.section or []),
                    force=bool(getattr(args, "force", False)),
                )
            except (FileNotFoundError, ValueError, FileExistsError, RuntimeError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Split atom {result.original_id}")
            print(f"Original path: {result.original_path}")
            for record in result.created:
                print(f"Created atom {record.doc_id} at {record.path}")
            print(f"Original kept as redirect stub: {'yes' if result.redirect_kept else 'no'}")
            if result.inbound_references:
                print("Inbound references acknowledged:")
                for item in result.inbound_references:
                    print(f"- {item}")
            return 0

        if args.atoms_command == "merge":
            try:
                result = operations.merge_atom(
                    args.doc_id,
                    into_selector=args.into,
                    force=bool(getattr(args, "force", False)),
                )
            except (FileNotFoundError, ValueError, FileExistsError, RuntimeError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Merged atom {result.source_id} into {result.target_id}")
            print(f"Source path: {result.source_path}")
            print(f"Target path: {result.target_path}")
            print(f"Source kept as redirect stub: {'yes' if result.redirect_kept else 'no'}")
            print(f"Inbound references rewritten: {len(result.rewritten_references)}")
            if result.rewritten_references:
                for item in result.rewritten_references:
                    print(f"- {item}")
            if result.ambiguities:
                print("Merge ambiguities acknowledged:")
                for item in result.ambiguities:
                    print(f"- {item}")
            return 0

        if args.atoms_command == "reorganize":
            try:
                report = operations.reorganize_atoms(dry_run=bool(getattr(args, "dry_run", False)))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            verb = "Would move" if report["dry_run"] else "Moved"
            print(f"Folder axis: {report['axis']}")
            if not report["moves"]:
                print("No atoms need to move.")
            for move in report["moves"]:
                print(f"{verb} {move['id']}: {move['from']} -> {move['to']}")
            for error in report["errors"]:
                print(f"Skipped: {error}")
            return 1 if report["errors"] else 0

        if args.atoms_command == "list":
            try:
                axis, payloads = operations.list_atoms(getattr(args, "axis_value", None))
            except (FileNotFoundError, ValueError) as exc:
                return render_error(
                    str(exc),
                    getattr(args, "format", "text"),
                    type_name=type(exc).__name__,
                    text=f"Error: {exc}",
                )
            return render(
                {"axis": axis, "atoms": payloads},
                getattr(args, "format", "text"),
                lambda _data: _format_atom_list(payloads, axis),
            )

        if args.atoms_command == "citations":
            return _run_citations(args, operations)

        if args.atoms_command in {"crossroad", "proto", "type", "tree"}:
            return self._run_domain_tree(args, root)

        if args.atoms_command == "show":
            args.command = "show"
            args.subject = "atom"
            from deskops.cli.commands.operations import OperationsCLI
            return OperationsCLI().run(args)

        return 1

    def _run_domain_tree(self, args: Any, root: Path) -> int:
        tree = DomainTree(root)
        try:
            if args.atoms_command == "crossroad":
                created = tree.create_crossroad(args.path, title=args.title, content=args.content)
                print(f"Created crossroad {created.doc_id}")
                print(f"Path: {created.path}")
                return 0
            if args.atoms_command == "proto":
                created = tree.create_protoatom(
                    args.doc_id, title=args.title, content=args.content, tags=list(args.tag or [])
                )
                print(f"Created protoatom {created.doc_id}")
                print(f"Path: {created.path}")
                return 0
            if args.atoms_command == "type":
                typed = tree.type_protoatom(
                    args.doc_id,
                    model_name=args.model,
                    doc_id=args.new_id,
                    content_field=args.content_field,
                    data=json.loads(args.data) if args.data else {},
                )
                print(f"Typed protoatom {typed.protoatom_id} as {typed.model} {typed.doc_id}")
                print(f"Path: {typed.path}")
                print(f"Protoatom kept as redirect stub: {typed.protoatom_path}")
                return 0
            report = tree.tree()
        except (FileNotFoundError, FileExistsError, ValueError, RuntimeError) as exc:
            return render_error(
                str(exc),
                getattr(args, "format", "text"),
                type_name=type(exc).__name__,
                text=f"Error: {exc}",
            )
        return render(
            report,
            getattr(args, "format", "text"),
            _format_tree,
        )


def _run_citations(args: Any, operations: DeskopsOperations) -> int:
    """``deskops atoms citations``: list, check (exit 1 on a broken citation) and record them."""
    try:
        report = operations.atoms.atom_citations(write=bool(getattr(args, "write", False)))
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}")
        return 1
    print(f"Citations: {len(report.citations)}")
    for item in report.citations:
        print(f"- {item.path}:{item.line} -> {item.atom_id}")
    if report.broken:
        print(f"Broken citations: {len(report.broken)}")
        for item in report.broken:
            print(f"- {item.path}:{item.line} -> {item.atom_id} (no such atom)")
    if report.orphans:
        print(f"Warning: atoms without a citation: {len(report.orphans)}")
        for atom_id in report.orphans:
            print(f"- {atom_id}")
    if report.written:
        print(f"Graph: {len(report.created)} cited_by relation(s) created, {len(report.removed)} removed.")
        for item in report.created:
            print(f"+ {item}")
        for item in report.removed:
            print(f"- {item}")
    return 1 if getattr(args, "check", False) and report.broken else 0


def _with_domain_checks(results: list[dict[str, Any]], domain: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add domain-tree errors to atom records and append crossroad and protoatom records."""
    merged = [dict(record, errors=list(record["errors"])) for record in results]
    by_path = {record["path"]: record for record in merged}
    for record in domain:
        if record["path"] in by_path:
            by_path[record["path"]]["errors"].extend(record["errors"])
        else:
            merged.append(record)
    return merged


def _format_atom_list(payloads: list[dict[str, Any]], axis: str | None) -> str:
    lines: list[str] = []
    for payload in payloads:
        label = payload.get("title") or payload["id"]
        if axis:
            values = ",".join(payload.get("axis_values") or []) or "-"
            lines.append(f"{payload['id']} | {label} | {axis}:{values}")
        else:
            lines.append(f"{payload['id']} | {label}")
    return "\n".join(lines)


def _format_tree(report: dict[str, Any]) -> str:
    lines: list[str] = []

    def walk(node: dict[str, Any], depth: int) -> None:
        pad = "  " * depth
        lines.append(f"{pad}{node['path']} — {node['title']}")
        for item in node["items"]:
            target = f" -> {item['typed_as']}" if item.get("typed_as") else ""
            lines.append(f"{pad}  · {item['id']}  {item['title']}{target}")
        for child in node["children"]:
            walk(child, depth + 1)

    for node in report["roots"]:
        walk(node, 0)
    if report["orphans"]:
        lines.append("Without a written crossroad:")
        for item in report["orphans"]:
            lines.append(f"  · {item['id']} (domain:{item['domain']})")
    if report["unplaced"]:
        lines.append(f"Without a domain tag: {len(report['unplaced'])} document(s)")
    return "\n".join(lines)

FILE:deskops/cli/commands/message.py
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import sys
from typing import Any

import yaml
from sldb.api import Transaction
from sldb.api import transaction
from sldb.cli.model_utils import registered_model
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError, SLDBValidationError
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.store.layout import project_root

from deskops import doc_access
from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.config import DeskConfig
from deskops.identity import EcosystemIdentity
from deskops.identity import UNKNOWN_PROJECT_IDENTITY
from deskops.identity import find_context_root
from deskops.identity import find_registered_desk
from deskops.identity import load_ecosystem_registry
from deskops.identity import resolve_registered_repo_by_root
from deskops.identity import find_local_store
from deskops.models import InboxNoteDoc
from deskops.errors import UsageError


class MessageCLI:
    """Send, list, read, or acknowledge cross-desk messages.

    The surface is `deskops message {send|list|read|ack}`; argparse requires
    the subcommand, so `deskops message` alone is a usage error (rc 2).
    """

    def run(self, args: Any) -> int:
        try:
            return self._run_message_command(args)
        except (SLDBStoreError, SLDBValidationError, ValueError) as exc:
            return render_error(
                str(exc),
                getattr(args, "format", "text"),
                type_name=type(exc).__name__,
                text=f"Error: {exc}",
            )

    def _run_message_command(self, args: Any) -> int:
        subcmd = args.message_command
        if subcmd == "send":
            args.message = args.body
            return self._deliver_note(args)
        if subcmd == "list":
            return self._list_notes(args)
        if subcmd == "read":
            args.show = args.selector
            return self._show_note(args)
        if subcmd == "ack":
            args.ack = args.selector
            return self._ack_note(args)
        return render_error(
            f"Unknown message command: {subcmd}",
            getattr(args, "format", "text"),
            type_name="DomainError",
        )

    def _deliver_note(self, args: Any) -> int:
        target_project, desk_root = self._resolve_target(args)
        inbox_dir = desk_root / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)

        created_at = datetime.now()
        title = args.title.strip() if args.title else self._derive_title(args.message)
        slug = self._slug(title)
        path = inbox_dir / f"{created_at.strftime('%Y%m%d-%H%M%S')}-{args.kind}-{slug}.md"
        sender_project = self._sender_project(args)
        payload = {
            "kind": args.kind,
            "sender_project": sender_project,
            "target_project": target_project,
            "created_at": created_at.isoformat(timespec="seconds"),
            "status": "open",
            "title": title,
            "body": args.message.strip(),
        }
        rendered = render_model_markdown(InboxNoteDoc, payload) + "\n"
        # Validate before writing: a note that cannot be read back should never
        # reach the target's inbox.
        valid, details = validate_model_input_roundtrip(InboxNoteDoc, rendered)
        if not valid:
            raise SLDBValidationError("Message failed validation", details)

        # The note and its tracking are written in the target store's transaction.
        # Tracking is a courtesy to the target's doctor: a foreign desk may keep its
        # models in a package this process cannot import, which must not turn a
        # delivered note into a reported failure, so a tracking error is caught inside
        # the block and the delivered note stays.
        context = self._note_store_context(args, desk_root)
        tracked_name = None
        if context is None:
            path.write_text(rendered, encoding="utf-8")
            self._warn_no_store(desk_root, path)
        else:
            store_path, _root = context
            with transaction(store_path, args.pythonpath) as tx:
                tx.write_file(path, rendered.encode("utf-8"))
                try:
                    tracked_name = self._track_note(tx, args, path, store_path)
                except Exception as exc:
                    print(
                        f"Warning: delivered to {path} but could not track it in that store: {exc}",
                        file=sys.stderr,
                    )
        result = {
            "sender_project": sender_project,
            "target_project": target_project,
            "path": str(path),
            "tracked_name": tracked_name,
            "verified": tracked_name is not None,
        }
        return self._print_delivery_result(result, args.format)

    def _list_notes(self, args: Any) -> int:
        notes = self._iter_notes(self._desk_root(args))[: args.limit]
        payload = [self._note_summary(path) for path in notes]
        return self._print(payload, args.format, key="notes")

    def _show_note(self, args: Any) -> int:
        note = self._resolve_note(self._desk_root(args), args.show)
        if note is None:
            return render_error(
                f"Unknown message: {args.show}",
                getattr(args, "format", "text"),
                type_name="DomainError",
            )
        payload = self._note_detail(note)
        return self._print(payload, args.format)

    def _ack_note(self, args: Any) -> int:
        target_project, desk_root = self._resolve_target(args)
        note = self._resolve_note(desk_root, args.ack)
        if note is None:
            return render_error(
                f"Unknown message: {args.ack}",
                getattr(args, "format", "text"),
                type_name="DomainError",
            )

        # The index entry as it is before the note is read: its source hash guards the update.
        context = self._note_store_context(args, desk_root)
        entry = doc_access.index_entry(context[1], note) if context is not None else None
        payload = extract_model_data(InboxNoteDoc, note.read_text(encoding="utf-8"))
        if payload.get("status") == "closed":
            raise ValueError(f"Message '{note.stem}' is already acknowledged.")

        acknowledged_at = datetime.now().isoformat(timespec="seconds")
        payload["status"] = "closed"
        payload["target_project"] = payload.get("target_project") or target_project
        payload["acknowledged_by"] = target_project
        payload["acknowledged_at"] = acknowledged_at
        ack_reason = (getattr(args, "reason", None) or "").strip()
        payload["ack_reason"] = ack_reason
        rendered = render_model_markdown(InboxNoteDoc, payload) + "\n"
        tracked_name = None
        if context is None:
            note.write_text(rendered, encoding="utf-8")
            self._warn_no_store(desk_root, note)
        else:
            # The ack is an update of the tracked note, guarded, in the store's transaction;
            # a note the store does not track yet is written and tracked in the same block,
            # so a tracking failure leaves the note as it was.
            store_path, root = context
            with transaction(store_path, args.pythonpath) as tx:
                if entry is not None:
                    doc_access.update_tracked_doc(tx, root, note, entry, payload)
                    tracked_name = entry.name
                else:
                    tx.write_file(note, rendered.encode("utf-8"))
                    tracked_name = self._track_note(tx, args, note, store_path)
        result = {
            "id": note.stem,
            "path": str(note),
            "status": "closed",
            "target_project": payload["target_project"],
            "acknowledged_by": target_project,
            "acknowledged_at": acknowledged_at,
            "ack_reason": ack_reason,
            "tracked_name": tracked_name,
            "verified": True,
        }
        return self._print_ack_result(result, args.format)

    def _desk_root(self, args: Any) -> Path:
        if getattr(args, "desk_root", None):
            return Path(args.desk_root).resolve()

        if getattr(args, "repo", None):
            return self._resolve_repo_desk(args.repo, args.store, args.pythonpath)

        if getattr(args, "root", None):
            return (Path(args.root).resolve() / "desk").resolve()

        if args.store:
            return (project_root(Path(args.store).resolve()) / "desk").resolve()

        local_store = find_local_store()
        if local_store is not None:
            return (project_root(local_store) / "desk").resolve()

        return (Path.cwd() / "desk").resolve()

    def _resolve_target(self, args: Any) -> tuple[str, Path]:
        desk_root = self._desk_root(args)
        repo_root = desk_root.parent.resolve()
        config = DeskConfig.load(desk_root) if desk_root.exists() else DeskConfig()

        target_project = None
        ecosystem = self._target_ecosystem(args, repo_root)
        if ecosystem is not None:
            target_project = ecosystem.what_repository_am_i_in(
                repo_root,
                require_registry_match=True,
                allow_unregistered=True,
                default_to_directory_name=True,
            )
        if target_project is None:
            config_identity = (config.project_identity or UNKNOWN_PROJECT_IDENTITY).strip() or UNKNOWN_PROJECT_IDENTITY
            target_project = (
                config_identity if config_identity != UNKNOWN_PROJECT_IDENTITY else repo_root.name
            )

        if config.project_identity.strip() in {"", UNKNOWN_PROJECT_IDENTITY}:
            print(
                f"Warning: target desk '{desk_root}' has no project_identity; "
                f"resolved it as '{target_project}' from its directory or registry.",
                file=sys.stderr,
            )
        return target_project, desk_root

    def _target_ecosystem(self, args: Any, repo_root: Path) -> EcosystemIdentity | None:
        """The ecosystem anchored at the target repo, never the sender's."""
        target_store = find_local_store(repo_root)
        if target_store is None and args.store:
            candidate = Path(args.store).resolve()
            if project_root(candidate).resolve() == repo_root:
                target_store = candidate
        if target_store is None:
            return None
        try:
            return EcosystemIdentity(str(target_store))
        except SLDBStoreError:
            return None

    def _sender_ecosystem(self) -> EcosystemIdentity | None:
        """The sender's own ecosystem; the target registry must never decide it."""
        try:
            return EcosystemIdentity(None)
        except SLDBStoreError:
            return None

    def _resolve_repo_desk(self, repo_name: str, store_arg: str | None, pythonpath: str | None) -> Path:
        _ = pythonpath
        return find_registered_desk(repo_name, store_arg)

    def _note_store_context(self, args: Any, desk_root: Path) -> tuple[Path, Path] | None:
        """The store that owns the target desk, or None when its repo has no store.

        ``--store`` may still describe the sender's store (for example with
        ``--to``/``--repo``), so it is honored only when it belongs to the
        target repo. The sender's store is never a fallback for the target.
        """
        repo_root = desk_root.parent.resolve()
        if args.store:
            store_path, root = get_store_context(args.store)
            if root.resolve() == repo_root:
                return store_path, root
        store_path = repo_root / ".sldb"
        if not store_path.is_dir():
            return None
        return store_path, repo_root

    def _iter_notes(self, desk_root: Path) -> list[Path]:
        inbox_dir = desk_root / "inbox"
        if not inbox_dir.exists():
            return []
        return sorted(inbox_dir.glob("*.md"), reverse=True)

    def _resolve_note(self, desk_root: Path, raw: str) -> Path | None:
        notes = self._iter_notes(desk_root)
        exact = next((path for path in notes if raw in {path.name, path.stem}), None)
        if exact is not None:
            return exact
        lowered = raw.lower()
        matches = [path for path in notes if lowered in path.stem.lower()]
        if len(matches) > 1:
            listing = ", ".join(path.stem for path in sorted(matches))
            raise UsageError(
                f"Ambiguous message selector '{raw}' matches {len(matches)} notes: {listing}. "
                "Pass the full filename or stem."
            )
        return matches[0] if matches else None

    def _note_summary(self, path: Path) -> dict[str, str | None]:
        frontmatter, title, _ = self._parse_note(path)
        return {
            "id": path.stem,
            "path": str(path),
            "kind": frontmatter.get("kind", ""),
            "sender_project": frontmatter.get("sender_project", ""),
            "target_project": frontmatter.get("target_project", ""),
            "status": frontmatter.get("status", ""),
            "created_at": frontmatter.get("created_at", ""),
            "acknowledged_by": frontmatter.get("acknowledged_by"),
            "acknowledged_at": frontmatter.get("acknowledged_at"),
            "title": title,
        }

    def _note_detail(self, path: Path) -> dict[str, str | None]:
        frontmatter, title, body = self._parse_note(path)
        return {
            "id": path.stem,
            "path": str(path),
            "title": title,
            "body": body,
            **frontmatter,
            # A note written before ack_reason existed reads as having no reason.
            "ack_reason": frontmatter.get("ack_reason") or "",
        }

    def _parse_note(self, path: Path) -> tuple[dict[str, str | None], str, str]:
        text = path.read_text(encoding="utf-8")
        frontmatter: dict[str, str | None] = {}
        body = text
        if text.startswith("---\n"):
            _, rest = text.split("---\n", 1)
            fm_block, body = rest.split("\n---\n", 1)
            frontmatter = yaml.safe_load(fm_block) or {}
        lines = body.strip().splitlines()
        title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else path.stem
        content = "\n".join(lines[1:]).strip() if lines and lines[0].startswith("# ") else body.strip()
        return frontmatter, title, content

    def _print(self, payload: Any, fmt: str, key: str | None = None) -> int:
        data = {key: payload} if key else payload
        if key == "notes":
            return render(data, fmt, lambda _data: self._format_note_list(payload))
        return render(data, fmt, lambda _data: self._format_note_detail(payload))

    @staticmethod
    def _format_note_list(payload: list[dict[str, Any]]) -> str:
        if not payload:
            return "No messages."
        return "\n".join(
            f"{item['id']} | {item['kind']} | {item['sender_project']} -> {item['target_project']} | {item['status']} | {item['title']}"
            for item in payload
        )

    @staticmethod
    def _format_note_detail(payload: dict[str, Any]) -> str:
        lines = [f"# {payload['title']}", ""]
        for meta in (
            "kind",
            "sender_project",
            "target_project",
            "created_at",
            "status",
            "acknowledged_by",
            "acknowledged_at",
            "path",
        ):
            if meta in payload and payload[meta] not in {None, ""}:
                lines.append(f"{meta}: {payload[meta]}")
            if meta == "acknowledged_at" and payload.get("ack_reason"):
                lines.append(f"Ack reason: {payload['ack_reason']}")
        lines.append("")
        lines.append(payload.get("body", ""))
        return "\n".join(lines)

    def _print_delivery_result(self, payload: dict[str, Any], fmt: str) -> int:
        def text(data: dict[str, Any]) -> str:
            lines = [
                "Delivered message "
                f"from {data['sender_project']} to {data['target_project']} at {data['path']}"
            ]
            if data.get("tracked_name"):
                lines.append(f"Tracked '{data['tracked_name']}'")
            else:
                lines.append("Not tracked in the target store (see the warning above).")
            return "\n".join(lines)

        return render(payload, fmt, text)

    def _print_ack_result(self, payload: dict[str, Any], fmt: str) -> int:
        def text(data: dict[str, Any]) -> str:
            lines = [
                f"Acknowledged {data['id']} as {data['status']} "
                f"by {data['acknowledged_by']} at {data['acknowledged_at']}",
                f"Path: {data['path']}",
            ]
            if data.get("ack_reason"):
                lines.append(f"Ack reason: {data['ack_reason']}")
            if data.get("tracked_name"):
                lines.append(f"Tracked '{data['tracked_name']}'")
            else:
                lines.append("Not tracked in the target store (see the warning above).")
            return "\n".join(lines)

        return render(payload, fmt, text)

    def _derive_title(self, message: str) -> str:
        first = message.strip().splitlines()[0] if message.strip() else "Message"
        return first[:72]

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "note"

    def _sender_project(self, args: Any) -> str:
        sender_root = find_context_root()
        ecosystem = self._sender_ecosystem()
        config_identity = self._config_identity(sender_root)
        explicit = getattr(args, "sender", None)

        if explicit:
            registered = ecosystem is not None and any(
                entry.id == explicit for entry in ecosystem.entries
            )
            if registered or config_identity == explicit:
                return explicit
            if config_identity is None and (ecosystem is None or not ecosystem.entries):
                # No sender registry or config to check against; honor the explicit id.
                return explicit
            raise SLDBStoreError(
                f"Sender identity '{explicit}' is not the sender repo's identity "
                f"'{config_identity or UNKNOWN_PROJECT_IDENTITY}' and is not in its registry."
            )

        if ecosystem is not None:
            sender_project = ecosystem.what_repository_am_i_in(
                sender_root,
                require_registry_match=False,
                allow_unregistered=True,
            )
            if sender_project is not None:
                return sender_project
        if config_identity is not None:
            return config_identity
        # Last: the ecosystem registry may name the sender's root.
        entry = resolve_registered_repo_by_root(load_ecosystem_registry(), sender_root)
        if entry is not None:
            return entry.id
        raise SLDBStoreError(
            f"Unable to resolve sender identity for '{sender_root}'. Use --sender or register the repository canonically."
        )

    @staticmethod
    def _config_identity(repo_root: Path) -> str | None:
        desk_root = repo_root / "desk"
        if not desk_root.exists():
            return None
        identity = (DeskConfig.load(desk_root).project_identity or UNKNOWN_PROJECT_IDENTITY).strip()
        return identity if identity not in {"", UNKNOWN_PROJECT_IDENTITY} else None

    @staticmethod
    def _warn_no_store(desk_root: Path, path: Path) -> None:
        print(
            f"Warning: no .sldb store at {desk_root.parent / '.sldb'}; "
            f"not tracking {path.name}.",
            file=sys.stderr,
        )

    def _track_note(self, tx: Transaction, args: Any, path: Path, store_path: Path) -> str:
        """Track the note at ``path`` in the open transaction of its store; its name."""
        model_type, _entry, _idx = registered_model(store_path, "InboxNoteDoc", args.pythonpath)

        rendered = path.read_text(encoding="utf-8")
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            raise SLDBValidationError("Message failed validation", details)

        note_name = path.stem
        try:
            tx.track(path, "InboxNoteDoc", note_name)
        except SLDBStoreError as exc:
            if "already tracked" not in str(exc):
                raise
            # Re-sign an existing tracking entry instead of tracking it twice.
            tx.untrack(note_name)
            tx.track(path, "InboxNoteDoc", note_name)
        return note_name

    def _store_context(self, args: Any) -> tuple[Path, Path] | None:
        if args.store:
            return get_store_context(args.store)
        local_store = find_local_store()
        if local_store is None:
            return None
        return local_store, project_root(local_store)

FILE:tests/test_atoms_cli.py
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.cli.main import main
from sldb.cli.main import main as sldb_main
from sldb.store.io import load_documents_index
from sldb.store.io import load_models_index
from sldb.store.io import load_store_index


ATOM_ARGS = [
    "--title",
    "Trackable atom",
    "--five-wh-one-plus",
    "what",
    "--answer",
    "Created atoms should be visible through deskops and sldb.",
]


def _install_sandbox(root: Path) -> None:
    assert main(["desk", "install", str(root)]) == 0


def test_atoms_validate_accepts_valid_atom(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_ARGS]) == 0
    capsys.readouterr()

    result = main(["atoms", "validate", "atom-trackable-atom", "--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 0
    assert "Atom: atom-trackable-atom" in captured.out
    assert "- valid" in captured.out


def test_atoms_validate_all_reports_slug_and_provenance_errors(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    atoms_dir = tmp_path / "desk" / "atoms"
    bad_atom = atoms_dir / "atom-bad.md"
    bad_atom.write_text(
        "---\n"
        "id: bad-atom\n"
        "title: Bad Atom\n"
        "five_wh_one_plus: what\n"
        "tags:\n"
        "- unknown:value\n"
        "provenance: docs/missing-source.md\n"
        "---\n\n"
        "# Bad Atom\n\n"
        "## Answer\n\n"
        "Broken atom.\n",
        encoding="utf-8",
    )

    result = main(["atoms", "validate", "--all", "--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 1
    assert "Atom: bad-atom" in captured.out
    assert "filename must match atom id 'bad-atom'" in captured.out
    assert "atom id must follow slug convention atom-<slug>" in captured.out
    # Without a store sldb checks no namespace (test_domain_tree covers the declared desk).
    assert "Unknown atom tag namespace" not in captured.out
    assert "provenance is not resolvable: docs/missing-source.md" in captured.out


def test_atoms_delete_blocks_when_inbound_references_exist(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_ARGS]) == 0
    capsys.readouterr()

    task_path = tmp_path / "desk" / "tasks" / "task-ref.md"
    task_path.write_text(
        "# Ref\n\nReferences atom:atom-trackable-atom from a task.\n",
        encoding="utf-8",
    )

    result = main(["atoms", "delete", "atom-trackable-atom", "--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 1
    assert "Refusing to delete atom-trackable-atom" in captured.out
    assert "desk/tasks/task-ref.md:3" in captured.out
    assert (tmp_path / "desk" / "atoms" / "atom-trackable-atom.md").exists()
    assert "atom:atom-trackable-atom" in task_path.read_text(encoding="utf-8")


def test_atoms_delete_force_removes_file_and_untracks_store(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    store = tmp_path / ".sldb"
    assert sldb_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert sldb_main(
        [
            "models",
            "add",
            "deskops.models:AtomDoc",
            "--store",
            str(store),
            "--pythonpath",
            str(ROOT),
        ]
    ) == 0
    capsys.readouterr()

    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_ARGS]) == 0
    capsys.readouterr()

    task_path = tmp_path / "desk" / "tasks" / "task-ref.md"
    task_path.write_text(
        "# Ref\n\nReferences atom:atom-trackable-atom from a task.\n",
        encoding="utf-8",
    )

    result = main(["atoms", "delete", "atom-trackable-atom", "--force", "--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 0
    assert "Deleted atom atom-trackable-atom" in captured.out
    assert "Store untracked: yes" in captured.out
    assert not (tmp_path / "desk" / "atoms" / "atom-trackable-atom.md").exists()
    assert "atom:atom-trackable-atom" in task_path.read_text(encoding="utf-8")

    store_index = load_store_index(store)
    model_entry = next(entry for entry in store_index.models if entry.name == "AtomDoc")
    models_index = load_models_index(tmp_path / model_entry.models_index)
    documents_index = load_documents_index(tmp_path / models_index.documents_index)
    assert all(entry.name != "atom-trackable-atom" for entry in documents_index.documents)

FILE:tests/test_message_cli.py
"""Canonical `deskops message` transport surface.

`deskops message {send|list|read|ack}` is the cross-desk coordination CLI.
It routes to `deskops.cli.commands.message.MessageCLI`; the retired `inbox`
alias is no longer a command.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TESTS = Path(__file__).resolve().parent
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))

from deskops.cli.main import main
from test_cli import _setup_inbox_identity_env


def _cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv], cwd=root, capture_output=True, text=True
    )


def _sldb_stores_check(store_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_path)],
        capture_output=True,
        text=True,
    )


def _init_repos(tmp_path: Path) -> tuple[Path, Path]:
    repos = []
    for name in ("repo-a", "repo-b"):
        repo = tmp_path / name
        repo.mkdir()
        result = _cli(repo, "init", str(repo))
        assert result.returncode == 0, result.stderr or result.stdout
        repos.append(repo)
    return repos[0], repos[1]


def _deliver(repo_a: Path, repo_b: Path, title: str) -> tuple[Path, dict]:
    result = _cli(
        repo_a,
        "message",
        "send",
        "A note for repo B.",
        "--title",
        title,
        "--kind",
        "suggestion",
        "--root",
        str(repo_b),
        "--format",
        "json",
    )
    assert result.returncode == 0, result.stderr or result.stdout
    notes = list((repo_b / "desk" / "inbox").glob("*.md"))
    assert len(notes) == 1
    return notes[0], json.loads(result.stdout)


def test_message_help_documents_transport_verbs(capsys) -> None:
    assert main(["message", "--help"]) == 0
    output = " ".join(capsys.readouterr().out.split())
    assert "{send,list,read,ack}" in output
    assert "deskops message send" in output


def test_message_without_subcommand_is_a_usage_error_naming_the_verbs(capsys) -> None:
    assert main(["message"]) == 2
    captured = capsys.readouterr()
    for verb in ("send", "list", "read", "ack"):
        assert verb in captured.err
    # A usage error, not the full help.
    assert "Examples:" not in captured.err + captured.out


def test_retired_inbox_alias_is_an_unknown_command(capsys) -> None:
    assert main(["inbox", "--list"]) == 2
    assert "invalid choice: 'inbox'" in capsys.readouterr().err


def test_message_send_list_read_ack_roundtrip(tmp_path: Path, monkeypatch, capsys) -> None:
    sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    monkeypatch.chdir(sender_repo)

    assert main(
        [
            "message",
            "send",
            "Please acknowledge this message.",
            "--title",
            "Transport verbs",
            "--kind",
            "suggestion",
            "--to",
            "target-repo",
            "--store",
            str(store_path),
            "--format",
            "json",
        ]
    ) == 0
    delivered = json.loads(capsys.readouterr().out)
    assert delivered["sender_project"] == "sender-repo"
    assert delivered["target_project"] == "target-repo"

    note = next((target_repo / "desk" / "inbox").glob("*.md"))
    monkeypatch.chdir(target_repo)

    assert main(
        ["message", "list", "--root", str(target_repo), "--store", str(target_repo / ".sldb"), "--format", "json"]
    ) == 0
    listed = json.loads(capsys.readouterr().out)
    assert [item["id"] for item in listed["notes"]] == [note.stem]

    assert main(
        ["message", "read", note.stem, "--root", str(target_repo), "--store", str(target_repo / ".sldb"), "--format", "json"]
    ) == 0
    read = json.loads(capsys.readouterr().out)
    assert read["status"] == "open"
    assert "Please acknowledge this message." in read["body"]

    assert main(
        ["message", "ack", note.stem, "--root", str(target_repo), "--store", str(target_repo / ".sldb"), "--format", "json"]
    ) == 0
    acked = json.loads(capsys.readouterr().out)
    assert acked["status"] == "closed"
    assert acked["acknowledged_by"] == "target-repo"


def test_message_list_reports_empty_inbox(tmp_path: Path, monkeypatch, capsys) -> None:
    _sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    monkeypatch.chdir(target_repo)

    assert main(["message", "list", "--root", str(target_repo), "--store", str(target_repo / ".sldb")]) == 0
    assert "No messages." in capsys.readouterr().out


def test_message_delivery_tracks_note_in_target_repo_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    repo_a, repo_b = _init_repos(tmp_path)
    note, payload = _deliver(repo_a, repo_b, "Tracked in the target store")

    assert payload["target_project"] == "repo-b"
    assert payload["verified"] is True
    assert doc_status(repo_a / ".sldb", note.stem).status == "missing"
    tracked = doc_status(repo_b / ".sldb", note.stem)
    assert tracked.status == "ok"
    assert tracked.path == f"desk/inbox/{note.name}"
    assert not Path(tracked.path).is_absolute()
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout
    assert "PASS" in check.stdout


def test_message_ack_refreshes_note_tracked_in_target_repo_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    repo_a, repo_b = _init_repos(tmp_path)
    note, _ = _deliver(repo_a, repo_b, "Acknowledged in the target store")

    result = _cli(
        repo_b,
        "message",
        "ack",
        note.stem,
        "--root",
        str(repo_b),
        "--format",
        "json",
    )
    assert result.returncode == 0, result.stderr or result.stdout
    acked = json.loads(result.stdout)
    assert acked["status"] == "closed"
    assert acked["acknowledged_by"] == "repo-b"
    assert doc_status(repo_b / ".sldb", note.stem).status == "ok"
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout
    assert "PASS" in check.stdout
    assert doc_status(repo_a / ".sldb", note.stem).status == "missing"


def test_message_ack_restores_note_when_tracking_fails(tmp_path: Path, monkeypatch) -> None:
    from sldb.api import doc_status
    from sldb.core.exceptions import SLDBStoreError

    repo_a, repo_b = _init_repos(tmp_path)
    note, _ = _deliver(repo_a, repo_b, "Restored when tracking fails")
    original = note.read_bytes()

    def failing_save(*_args, **_kwargs):
        raise SLDBStoreError("simulated refresh failure")

    # The ack is `Transaction.update` of the tracked note: the store's save step fails.
    monkeypatch.setattr("sldb.api.documents.transaction_ops.save_document_payload", failing_save)
    monkeypatch.chdir(repo_b)

    assert main(["message", "ack", note.stem, "--root", str(repo_b)]) == 1
    assert note.read_bytes() == original
    assert doc_status(repo_b / ".sldb", note.stem).status == "ok"
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout
    assert "PASS" in check.stdout


def test_message_ack_reason_is_stored_and_shown_by_read(tmp_path: Path) -> None:
    from sldb.api import doc_status

    repo_a, repo_b = _init_repos(tmp_path)
    note, _ = _deliver(repo_a, repo_b, "Acknowledged with a reason")
    reason = "Ya resuelto: la tarea X cubre esto"

    result = _cli(
        repo_b, "message", "ack", note.stem, "--root", str(repo_b), "--reason", reason, "--format", "json"
    )
    assert result.returncode == 0, result.stderr or result.stdout
    acked = json.loads(result.stdout)
    assert acked["status"] == "closed"
    assert acked["ack_reason"] == reason
    assert "ack_reason: 'Ya resuelto: la tarea X cubre esto'" in note.read_text(encoding="utf-8")
    assert doc_status(repo_b / ".sldb", note.stem).status == "ok"
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout

    read_json = _cli(repo_b, "message", "read", note.stem, "--root", str(repo_b), "--format", "json")
    assert read_json.returncode == 0, read_json.stderr or read_json.stdout
    assert json.loads(read_json.stdout)["ack_reason"] == reason

    read_text = _cli(repo_b, "message", "read", note.stem, "--root", str(repo_b))
    assert read_text.returncode == 0, read_text.stderr or read_text.stdout
    lines = read_text.stdout.splitlines()
    ack_at = next(i for i, line in enumerate(lines) if line.startswith("acknowledged_at: "))
    assert lines[ack_at + 1] == f"Ack reason: {reason}"


def test_message_ack_without_reason_leaves_ack_reason_empty(tmp_path: Path) -> None:
    repo_a, repo_b = _init_repos(tmp_path)
    note, _ = _deliver(repo_a, repo_b, "Acknowledged without a reason")

    result = _cli(repo_b, "message", "ack", note.stem, "--root", str(repo_b), "--format", "json")
    assert result.returncode == 0, result.stderr or result.stdout
    acked = json.loads(result.stdout)
    assert acked["status"] == "closed"
    assert acked["acknowledged_by"] == "repo-b"
    assert acked["ack_reason"] == ""

    read_json = _cli(repo_b, "message", "read", note.stem, "--root", str(repo_b), "--format", "json")
    assert json.loads(read_json.stdout)["ack_reason"] == ""
    read_text = _cli(repo_b, "message", "read", note.stem, "--root", str(repo_b))
    assert read_text.returncode == 0, read_text.stderr or read_text.stdout
    assert "Ack reason" not in read_text.stdout


OLD_NOTE = """---
kind: suggestion
sender_project: repo-a
target_project: repo-b
created_at: '2026-01-01T00:00:00'
status: open
---

# Old note

_Describe the incoming message with enough evidence to triage._

Written before ack_reason existed.
"""


def test_message_old_note_without_ack_reason_still_reads_and_acks(tmp_path: Path) -> None:
    repo = tmp_path / "repo-old"
    inbox = repo / "desk" / "inbox"
    inbox.mkdir(parents=True)
    note = inbox / "20260101-000000-suggestion-old-note.md"
    note.write_text(OLD_NOTE, encoding="utf-8")

    read_json = _cli(repo, "message", "read", note.stem, "--root", str(repo), "--format", "json")
    assert read_json.returncode == 0, read_json.stderr or read_json.stdout
    read = json.loads(read_json.stdout)
    assert read["status"] == "open"
    assert read["ack_reason"] == ""

    acked = _cli(repo, "message", "ack", note.stem, "--root", str(repo), "--reason", "Aviso leido", "--format", "json")
    assert acked.returncode == 0, acked.stderr or acked.stdout
    assert json.loads(acked.stdout)["ack_reason"] == "Aviso leido"
    reread = _cli(repo, "message", "read", note.stem, "--root", str(repo), "--format", "json")
    assert json.loads(reread.stdout)["ack_reason"] == "Aviso leido"

    # An old note acked without --reason, as before ack_reason existed.
    plain = inbox / "20260101-000001-suggestion-old-plain.md"
    plain.write_text(OLD_NOTE, encoding="utf-8")
    acked_plain = _cli(repo, "message", "ack", plain.stem, "--root", str(repo), "--format", "json")
    assert acked_plain.returncode == 0, acked_plain.stderr or acked_plain.stdout
    assert json.loads(acked_plain.stdout)["ack_reason"] == ""


def test_message_list_uses_store_when_no_root_is_given(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    """`--store` alone anchors the desk, so the old root default cannot mask it."""
    repo = tmp_path / "store-repo"
    inbox = repo / "desk" / "inbox"
    inbox.mkdir(parents=True)
    note = inbox / "20260101-000000-suggestion-stored.md"
    note.write_text(
        "---\nkind: suggestion\nsender_project: sender\ntarget_project: store-repo\n"
        "created_at: 2026-01-01T00:00:00\nstatus: open\ntitle: Stored note\n---\n\n"
        "# Stored note\n\nBody.\n",
        encoding="utf-8",
    )
    store = repo / ".sldb"
    (store / "core").mkdir(parents=True)
    (store / "core" / "store_index.yaml").write_text("{}\n", encoding="utf-8")

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)

    assert main(["message", "list", "--store", str(store), "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert [item["id"] for item in payload["notes"]] == [note.stem]


def test_message_ack_rejects_a_fragment_that_matches_two_notes(tmp_path: Path) -> None:
    """2026-10-19: `message ack 20261019-120241` acked 20261019-120253, whose title quoted it."""
    repo_a, repo_b = _init_repos(tmp_path)
    first, _ = _deliver(repo_a, repo_b, "sldb ci en verde")
    prefix = first.stem.split("-suggestion-")[0]
    result = _cli(
        repo_a, "message", "send", "Corrected hashes.", "--title", f"correccion de mi nota {prefix}",
        "--kind", "suggestion", "--root", str(repo_b),
    )
    assert result.returncode == 0, result.stderr or result.stdout
    (second,) = [path for path in (repo_b / "desk" / "inbox").glob("*.md") if path != first]
    assert prefix in second.stem

    ambiguous = _cli(repo_b, "message", "ack", prefix, "--root", str(repo_b))

    assert ambiguous.returncode == 2, ambiguous.stdout + ambiguous.stderr
    output = ambiguous.stdout + ambiguous.stderr
    assert first.stem in output and second.stem in output
    for note in (first, second):
        assert "status: open" in note.read_text(encoding="utf-8")

    exact = _cli(repo_b, "message", "ack", first.stem, "--root", str(repo_b))

    assert exact.returncode == 0, exact.stdout + exact.stderr
    assert "status: closed" in first.read_text(encoding="utf-8")
    assert "status: open" in second.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "body",
    [
        "docker inspect --format {{.State.Health.Status}} web",
        "texto {{a fin",
        "this is not valid json {{{",
        "valor {{ 7*7 }} y {# oculto #} fin",
    ],
)
def test_message_send_keeps_braces_in_the_body_literal(tmp_path: Path, monkeypatch, capsys, body: str) -> None:
    sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    monkeypatch.chdir(sender_repo)

    rc = main(
        ["message", "send", body, "--title", "Llaves", "--kind", "unclear",
         "--to", "target-repo", "--store", str(store_path), "--format", "json"]
    )

    assert rc == 0, capsys.readouterr()
    note = next((target_repo / "desk" / "inbox").glob("*.md"))
    assert body in note.read_text(encoding="utf-8")

FILE:instruccion
Cold-bundle de la tarea task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_atoms_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)


FILE:desk/tasks/task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt.md
---
sldb:
  by: agent
  at: '2026-11-23T05:07:56Z'
  authority: generated
  via: save_document_payload
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
- deskops/cli/registry.py
- deskops/cli/commands/operations.py
- deskops/operations.py
- deskops/services/atoms.py
- deskops/cli/commands/message.py
- tests/test_atoms_cli.py
- tests/test_message_cli.py
- tests/fixtures/model_contract_hashes.json
- tests/fixtures/golden/help/deskops_add_atom.txt
- tests/fixtures/golden/help/deskops_list_atoms.txt
- tests/fixtures/golden/help/deskops_message_send.txt
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

Entra: los dos modelos, la superficie real de add atom y list atoms (deskops/cli/registry.py, deskops/cli/commands/operations.py, deskops/operations.py, deskops/services/atoms.py), deskops/cli/commands/message.py, tests/fixtures/model_contract_hashes.json, los goldens de ayuda deskops_add_atom.txt, deskops_list_atoms.txt y deskops_message_send.txt, sldb models update de AtomDoc e InboxNoteDoc en el .sldb del repo, tests/test_atoms_cli.py y tests/test_message_cli.py. No entra: deskops/cli/commands/atoms.py (los alias viejos deskops atoms ... no ganan --conv), un verbo nuevo add agreement (el campo cubre el pedido), migrar los atoms viejos que tienen la referencia en provenance.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_atoms_cli.py (usan main(["add", "atom", "--root", ...]) en proceso, como los existentes): test_add_atom_with_conv_writes_conversation_ref, test_list_atoms_filters_by_conv, test_add_atom_refuses_duplicate_conv. p2: test en tests/test_message_cli.py: test_send_with_conv_writes_conversation_ref. p3: implementar. Superficie real (verificada): deskops add atom NO pasa por deskops/cli/commands/atoms.py (AtomsCLI es "deskops atoms ...", alias viejos); sus flags se generan de los campos del modelo en _add_subject_commands de deskops/cli/registry.py, el payload lo arma parse_artifact_input (deskops/cli/parse_input.py) y el add lo hace OperationsCLI (deskops/cli/commands/operations.py, rama args.command == "add") con doc_access.create_artifact. El campo nuevo genera solo --conversation-ref; --conv se agrega como alias del mismo argumento (flags ("--conversation-ref", "--conv")) en _add_subject_commands. deskops list atoms lo atiende OperationsCLI (rama list atoms) -> DeskopsOperations.list_atoms (deskops/operations.py) -> AtomsService.list_atoms (deskops/services/atoms.py); --conv se declara en _list_subject_commands (registry.py, junto a --axis-value) y se pasa como segundo filtro. message send --conv se declara en el Command ("message", "send") de registry.py (dest conversation_ref) y _deliver_note (deskops/cli/commands/message.py) lo agrega al payload. Semantica: comparacion literal sin normalizar "#"; vacio = None o solo espacios, no se escribe; el filtro de list acepta ref == hilo o ref que empieza por hilo + "/"; duplicado = otro atom con conversation_ref exactamente igual (tras strip), chequeado antes de crear en la rama add de OperationsCLI, mensaje a stderr "ya existe <atom id> con conversation_ref <ref>" y return 1 (add no tiene --format); message send no chequea duplicados; los atoms con la referencia solo en provenance no se listan. p4: contrato y goldens: actualizar AtomDoc e InboxNoteDoc en tests/fixtures/model_contract_hashes.json; regenerar goldens de ayuda con TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py --update-golden (cambian tests/fixtures/golden/help/deskops_add_atom.txt, deskops_list_atoms.txt, deskops_message_send.txt) y revisar el diff; en el store del desk: sldb models update AtomDoc --store .sldb --pythonpath . y sldb models update InboxNoteDoc --store .sldb --pythonpath . desde la raiz del worktree. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

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

FILE:deskops/cli/commands/operations.py
from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

from deskops.cli.parse_input import parse_artifact_input
from deskops.cli.parse_input import parse_task_input
from deskops.cli.render import normalize
from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.foreign_files import EXTERNAL_TASK_TYPE, foreign_repositories, task_warning
from deskops.lifecycle import finding_line
from deskops.models.task_types import closeout_evidence_kinds
from deskops.operations import DeskopsOperations
from deskops.operations import ARTIFACT_SUBJECTS
from deskops.services.closeout_gates import CloseoutEvidenceError
from deskops.services.closeout_gates import CLOSEOUT_EVIDENCE_VOCABULARY
from deskops.services.closeout_gates import normalize_declared_evidence
from deskops.services.closeout_gates import order_evidence_kinds


class OperationsCLI:
    def run(self, args: Any) -> int:
        root = Path(getattr(args, "root", ".")).resolve()
        operations = DeskopsOperations(root)

        if args.command == "add" and args.subject == "task":
            payload = parse_task_input(args)
            requested_type = str(payload.get("task_type") or "").strip()
            registry = operations.registered_task_types()
            if requested_type:
                if requested_type not in registry:
                    print(
                        f"Error: '{requested_type}' is not a registered task type. "
                        f"Registered types: {', '.join(sorted(registry))}."
                    )
                    return 1
                task_type = requested_type
            else:
                task_type = "task.code"
                print("Note: no --task-type given; defaulting to task.code.")
            payload["task_type"] = task_type

            type_model = registry[task_type]
            type_evidence = list(closeout_evidence_kinds(type_model) or ())
            try:
                declared = normalize_declared_evidence(payload.get("closeout_evidence"))
            except CloseoutEvidenceError as exc:
                print(f"Error: {exc}")
                return 1
            if declared:
                floor = [kind for kind in type_evidence if kind in CLOSEOUT_EVIDENCE_VOCABULARY]
                missing = [kind for kind in floor if kind not in declared]
                if missing:
                    print(
                        f"Error: --evidence removes closeout evidence the task type requires: "
                        f"{', '.join(missing)}. The type's evidence is a floor; add those kinds or drop --evidence."
                    )
                    return 1
                payload["closeout_evidence"] = order_evidence_kinds([*type_evidence, *declared])
            else:
                payload["closeout_evidence"] = []

            drawer_selector = getattr(args, "from_drawer", None)
            if not drawer_selector:
                raw_drawer = payload.get("from_drawer")
                drawer_selector = str(raw_drawer) if raw_drawer else None
            drawer_source = None
            if drawer_selector:
                try:
                    drawer_source = operations.resolve_drawer_source(drawer_selector)
                except (FileNotFoundError, ValueError) as exc:
                    print(f"Error: {exc}")
                    return 1
                payload = operations.attach_drawer_source(payload, drawer_source)
            bundle = operations.create_task_bundle(payload)
            print(f"Created task bundle {bundle.task_id}")
            print(f"Task: {bundle.task_path}")
            if task_type != EXTERNAL_TASK_TYPE:
                for repo_id in foreign_repositories(root, payload.get("files")):
                    print(task_warning(bundle.task_id, repo_id))
            if drawer_source is not None:
                print(f"From drawer: {drawer_source} (kept; remove it by hand once the task supersedes it)")
            return 0

        artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "add" and args.subject in artifact_subjects:
            artifact_id = artifact_subjects[args.subject]
            payload = parse_artifact_input(artifact_id, args)
            record = operations.create_artifact(artifact_id, payload)
            print(f"Created {record.kind} {record.doc_id}")
            print(f"Path: {record.path}")
            if args.subject == "repository":
                print("Note: this is a local repository artifact. Use 'deskops repo register' for canonical ecosystem registration.")
            return 0

        if args.command == "edit":
            try:
                record = operations.edit_artifact_field(args.subject, args.selector, args.field, args.value)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Updated {record.kind} {record.doc_id} field {args.field.replace('-', '_')}")
            print(f"Path: {record.path}")
            return 0

        if args.command == "bind" and args.subject == "pill":
            try:
                record, pill_id, changed = operations.bind_pill_to_task(args.task, args.pill)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            verb = "Bound" if changed else "Already bound"
            print(f"{verb} pill {pill_id} to task {record.doc_id}")
            print(f"Path: {record.path}")
            return 0

        if args.command == "next":
            try:
                if getattr(args, "diagram", False):
                    print(operations.render_next_action_diagram())
                    return 0
                report = operations.next_action_report(getattr(args, "task_id", None))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            self._print_next_action_report(report, why=getattr(args, "why", False))
            return 0

        if args.command == "list" and args.subject == "tasks":
            tasks = operations.list_tasks()
            repo_routes = operations.list_repo_task_routes() if getattr(args, "include_repos", False) else []
            payload: dict[str, Any] = {"tasks": tasks}
            if getattr(args, "include_repos", False):
                payload["repo_routes"] = repo_routes
            return render(payload, args.format, lambda _data: self._format_task_list(tasks, repo_routes))

        list_artifacts = {meta["list_subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "list" and args.subject == "atoms":
            try:
                axis, payloads = operations.list_atoms(getattr(args, "axis_value", None))
            except (FileNotFoundError, ValueError) as exc:
                return render_error(
                    str(exc),
                    args.format,
                    type_name=type(exc).__name__,
                    text=f"Error: {exc}",
                )
            return render(
                {"axis": axis, "atoms": payloads},
                args.format,
                lambda _data: self._format_artifact_list(payloads, axis=axis),
            )
        if args.command == "list" and args.subject in list_artifacts:
            artifact_id = list_artifacts[args.subject]
            payloads = operations.list_artifacts(artifact_id)
            return render(
                {args.subject: payloads},
                args.format,
                lambda _data: self._format_artifact_list(payloads),
            )

        if args.command == "show" and args.subject == "task":
            task, gates = operations.show_task(args.task_id)
            if task is None:
                return render_error(
                    f"No task found for {args.task_id}",
                    args.format,
                    type_name="DomainError",
                )
            payload = normalize(task)
            payload["lifecycle_gates"] = normalize(gates)
            return render(payload, args.format, lambda _data: self._format_task_detail(task, gates))

        show_artifacts = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "show" and args.subject in show_artifacts:
            artifact_id = show_artifacts[args.subject]
            try:
                payload = operations.show_artifact(artifact_id, args.doc_id)
                if args.subject == "atom":
                    # The files that cite the atom, as `deskops atoms citations --write` recorded them.
                    cited_by = operations.atoms.cited_by(str(payload["id"]))
                    if cited_by:
                        payload["cited_by"] = cited_by
            except (FileNotFoundError, ValueError) as exc:
                return render_error(
                    str(exc),
                    args.format,
                    type_name=type(exc).__name__,
                    text=f"Error: {exc}",
                )
            return render(
                payload,
                args.format,
                lambda _data: self._format_artifact_detail(args.subject, payload),
            )

        if args.command == "advance" and args.subject == "task":
            from deskops.lifecycle import HookDefinitionError
            from deskops.lifecycle import LifecycleGraphMissing

            back = bool(getattr(args, "back", False))
            reason = getattr(args, "reason", None)
            if reason is not None and not back:
                print("Error: --reason only goes with --back.", file=sys.stderr)
                return 2
            if back and not (reason or "").strip():
                print("Error: --back needs --reason \"<text>\" (why the task goes back).", file=sys.stderr)
                return 2
            try:
                task, result = operations.advance_task(args.task_id, back_reason=reason.strip() if back else None)
            except (LifecycleGraphMissing, HookDefinitionError) as exc:
                print(f"Error: {exc}", file=sys.stderr)
                return 1
            if task is None:
                print(f"No task found for {args.task_id}", file=sys.stderr)
                return 1
            print(f"Task: {task.id}")
            print(f"Status: {task.status}")
            print(f"Current node: {task.current_node}")
            print(f"Message: {result.message}")
            return 1 if result.blocked else 0

        return 1

    def _print_next_action_report(self, report: dict[str, Any], *, why: bool = False) -> None:
        kind = report.get("kind")
        if kind == "no_board_task":
            print("Next:")
            print(f"No active task is routed by {report['board']}.")
            print("Suggested commands:")
            for command in report["suggested_commands"]:
                print(command)
            return
        if kind == "multiple_board_tasks":
            print("Next:")
            print(f"Multiple active tasks are routed by {report['board']}; pass a task selector.")
            print("Routed tasks:")
            for task in report["tasks"]:
                print(f"- {task['id']} | {task['status']} | {task['title']}")
            print("Suggested commands:")
            for command in report["suggested_commands"]:
                print(command)
            return
        print(f"Task: {report['task']['id']}")
        print(f"Title: {report['task']['title']}")
        print(f"Status: {report['task']['status']}")
        print(f"Current node: {report['task']['current_node']}")
        if report['task'].get('task_type'):
            print(f"Task type: {report['task']['task_type']}")
        if report['task'].get('inherits_from'):
            print("Inherits from:")
            for item in report['task']['inherits_from']:
                print(f"- {item}")
        print(f"Phase: {report['phase']}")
        if report.get("ritual"):
            print("Required ritual:")
            print(f"- {report['ritual']}")
        if report.get("pills"):
            print("Required pills:")
            for pill in report["pills"]:
                print(f"- {pill}")
        if why:
            print("Why:")
            for item in report.get("why") or []:
                print(f"- {item}")
        print("Next actions:")
        for index, action in enumerate(report["next_actions"], start=1):
            print(f"{index}. {action}")
        if report.get("advance_when"):
            print("Advance when:")
            for item in report["advance_when"]:
                print(f"- {item}")
        if report.get("hooks"):
            print("Post-hooks:")
            for relation_type, hooks in report["hooks"].items():
                print(f"- {relation_type}:")
                for hook in hooks:
                    print(f"  - {hook['name']}: {' '.join(hook['run'])}")
        if report.get("findings"):
            print("Blocked by:")
            for finding in report["findings"]:
                print(f"- {finding_line(finding)}")
        print("Sources:")
        for label, path in report["sources"].items():
            print(f"- {label}: {path}")

    @staticmethod
    def _format_task_list(tasks: Any, repo_routes: Any) -> str:
        lines = [f"{task.id} | {task.status} | {task.current_node}" for task in tasks]
        lines.extend(
            f"{route.repo_id}:{route.task_id} | {route.status} | {route.title} | {route.task_path}"
            for route in repo_routes
        )
        return "\n".join(lines)

    @staticmethod
    def _format_artifact_list(payloads: list[dict[str, Any]], *, axis: str | None = None) -> str:
        lines: list[str] = []
        for payload in payloads:
            label = payload.get("title") or payload.get("name") or payload["id"]
            if axis:
                values = ",".join(payload.get("axis_values") or []) or "-"
                lines.append(f"{payload['id']} | {label} | {axis}:{values}")
            else:
                lines.append(f"{payload['id']} | {label}")
        return "\n".join(lines)

    @staticmethod
    def _format_task_detail(task: Any, gates: list[dict[str, Any]]) -> str:
        lines = [
            f"Task: {task.id}",
            f"Title: {task.title}",
            f"Status: {task.status}",
            f"Current node: {task.current_node}",
            f"Task type: {task.task_type}",
        ]
        if task.inherits_from:
            lines.append("Inherits from:")
            lines.extend(f"- {item}" for item in task.inherits_from)
        if task.from_drawer:
            lines.append(f"From drawer: {task.from_drawer}")
        if getattr(task, "closeout_evidence", None):
            lines.append(f"Closeout evidence: {', '.join(task.closeout_evidence)}")
        if task.effective_pills:
            lines.append("Effective pills:")
            lines.extend(f"- {item}" for item in task.effective_pills)
        if task.effective_atoms:
            lines.append("Effective atoms:")
            lines.extend(f"- {item}" for item in task.effective_atoms)
        if task.inherit_acceptance_context:
            lines.append("Effective validation:")
            lines.extend(f"- {item}" for item in task.effective_validation)
            lines.append(f"Effective done when: {task.effective_done_when}")
        if gates:
            lines.append("Lifecycle gates:")
            for gate in gates:
                state = "open" if gate["holds"] else "closed"
                condition = gate["condition"] or "(none)"
                lines.append(
                    f"- {gate['relation_type']} -> {gate['target']}: {state} [{condition}]"
                )
                for hook in gate.get("hooks") or []:
                    lines.append(f"  post-hook {hook['name']}: {' '.join(hook['run'])}")
                for finding in gate.get("findings") or []:
                    lines.append(f"  blocked by: {finding_line(finding)}")
        return "\n".join(lines)

    @staticmethod
    def _format_artifact_detail(subject: str, payload: dict[str, Any]) -> str:
        lines = [f"{subject.capitalize()}: {payload['id']}"]
        label = payload.get("title") or payload.get("name") or payload["id"]
        lines.append(f"Title: {label}")
        for key, value in payload.items():
            if key in {"id", "title", "current_node", "history", "tags", "cited_by"}:
                continue
            if isinstance(value, list):
                lines.append(f"{key}: {', '.join(str(item) for item in value)}")
            else:
                lines.append(f"{key}: {value}")
        if subject == "atom" and payload.get("cited_by"):
            lines.append("Cited by:")
            lines.extend(f"- {path}" for path in payload["cited_by"])
        return "\n".join(lines)

FILE:deskops/operations.py
"""The facade of one desk: every operation the CLI and the UIs call, as one call each.

``DeskopsOperations`` builds the arguments and delegates to the service that owns the
operation (tasks, atoms, closure, drawer, closeout gates), to ``deskops.doc_access`` for
plain document reads and writes, or to ``deskops.lifecycle``. No logic lives here.
"""

from __future__ import annotations

from contextlib import contextmanager
import logging
from pathlib import Path
from typing import Any
from typing import Iterator
from typing import TYPE_CHECKING

from deskops import doc_access
from deskops import lifecycle
from deskops.doc_access import ARTIFACT_MODELS
from deskops.doc_access import ARTIFACT_PATHS
from deskops.doc_access import ARTIFACT_SUBJECTS
from deskops.doc_access import DocumentRecord
from deskops.doc_access import RepoTaskRoute
from deskops.doc_access import slugify
from deskops.lifecycle import ReadSnapshot
from deskops.lifecycle import TransitionResult
from deskops.paths import data_path
from deskops.runtime import Task
from deskops.services.atoms import AtomCreateResult
from deskops.services.atoms import AtomMergeResult
from deskops.services.atoms import AtomSplitResult
from deskops.services.atoms import AtomValidationRecord
from deskops.services.closure import CloseoutGateReport
from deskops.services.tasks import TaskBundle

if TYPE_CHECKING:
    from deskops.services.atoms import AtomsService
    from deskops.services.closure import ClosureService
    from deskops.services.closeout_gates import CloseoutGatesService
    from deskops.services.drawer import DrawerService
    from deskops.services.tasks import TasksService

__all__ = [
    "ARTIFACT_MODELS",
    "ARTIFACT_PATHS",
    "ARTIFACT_SUBJECTS",
    "AtomCreateResult",
    "AtomMergeResult",
    "AtomSplitResult",
    "AtomValidationRecord",
    "CloseoutGateReport",
    "DeskopsOperations",
    "DocumentRecord",
    "RepoTaskRoute",
    "TaskBundle",
    "slugify",
]


class DeskopsOperations:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"
        self.spec_root = data_path("spec")
        self.snapshot: ReadSnapshot | None = None
        self._drawer: DrawerService | None = None
        self._tasks: TasksService | None = None
        self._closeout_gates: CloseoutGatesService | None = None
        self._closure: ClosureService | None = None
        self._atoms: AtomsService | None = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        log_file = self.root / ".deskops.log"
        self.logger = logging.getLogger("deskops")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    @contextmanager
    def read_snapshot(self) -> Iterator[None]:
        """Reuse task-independent graph reads for the duration of one read-only pass.

        Inside the block, the closeout graph context and the lifecycle transitions
        leaving each node are computed once and shared by every task read. The caller
        promises not to write the desk inside the block; nesting reuses the outer one.
        """
        if self.snapshot is not None:
            yield
            return
        self.snapshot = ReadSnapshot()
        try:
            yield
        finally:
            self.snapshot = None

    # ---------------------------------------------------------------- services
    @property
    def closeout_gates(self) -> "CloseoutGatesService":
        if self._closeout_gates is None:
            from deskops.services.closeout_gates import CloseoutGatesService

            self._closeout_gates = CloseoutGatesService(self.root)
        return self._closeout_gates

    @property
    def closure(self) -> "ClosureService":
        if self._closure is None:
            from deskops.services.closure import ClosureService

            self._closure = ClosureService(self.root, self)
        return self._closure

    @property
    def drawer(self) -> "DrawerService":
        if self._drawer is None:
            from deskops.services.drawer import DrawerService

            self._drawer = DrawerService(self.root)
        return self._drawer

    @property
    def tasks(self) -> "TasksService":
        if self._tasks is None:
            from deskops.services.tasks import TasksService

            self._tasks = TasksService(self.root, self)
        return self._tasks

    @property
    def atoms(self) -> "AtomsService":
        if self._atoms is None:
            from deskops.services.atoms import AtomsService

            self._atoms = AtomsService(self.root, self)
        return self._atoms

    # ---------------------------------------------------------------- documents
    def ensure_workspace(self) -> None:
        doc_access.ensure_workspace(self.root)

    def create_artifact(self, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
        return doc_access.create_artifact(self.root, artifact_id, raw_payload)

    def edit_artifact_field(self, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
        return doc_access.edit_artifact_field(self.root, subject, selector, field, raw_value)

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        return doc_access.list_artifacts(self.root, artifact_id)

    def show_artifact(self, artifact_id: str, doc_id: str) -> dict[str, Any]:
        return doc_access.show_artifact(self.root, artifact_id, doc_id)

    def list_repo_task_routes(self) -> list[RepoTaskRoute]:
        return doc_access.list_repo_task_routes(self.root)

    # ---------------------------------------------------------------- tasks
    def registered_task_types(self) -> dict[str, type[Any]]:
        return self.tasks.registered_task_types()

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        return self.tasks.create_task_bundle(raw_payload)

    def bind_pill_to_task(self, task_selector: str, pill_selector: str) -> tuple[DocumentRecord, str, bool]:
        return self.tasks.bind_pill_to_task(task_selector, pill_selector)

    def list_tasks(self) -> list[Task]:
        return self.tasks.list_tasks()

    def task_record(self, task_id: str, *, path: Path | None = None) -> tuple[Path, dict[str, Any], dict[str, Any]]:
        """``(path, model payload, payload with effective fields)`` of a task, read once per pass.

        Inside ``read_snapshot`` the record is kept under the resolved path, the file stem and
        the requested id; the payload cache also covers the tasks it inherits from. ``path``
        lets a caller that already has the file (a view row) skip resolving the selector again.
        """
        snapshot = self.snapshot
        resolved = Path(path).resolve() if path is not None else None
        keys = [str(resolved)] if resolved is not None else [str(task_id)]
        if resolved is not None:
            keys += [resolved.stem, str(task_id)]
        if snapshot is not None:
            for key in keys:
                if key in snapshot.task_records:
                    return snapshot.task_records[key]
        if resolved is None:
            resolved = doc_access.resolve_task_path(self.root, task_id)
        raw = doc_access.read_doc(resolved, doc_access.ARTIFACT_MODELS["artifact.task"])
        payload = doc_access.resolve_task_payload(
            self.root,
            resolved.stem,
            path=resolved,
            cache=snapshot.task_payloads if snapshot is not None else None,
        )
        record = (resolved, raw, payload)
        if snapshot is not None:
            for key in [str(resolved), resolved.stem, str(task_id), str(payload.get("id") or "")]:
                if key:
                    snapshot.task_records[key] = record
        return record

    def task_document(self, task_path: Path) -> str | None:
        """The ``Model:name`` a task's on_transition rules run under, once per pass."""
        snapshot = self.snapshot
        key = str(Path(task_path).resolve())
        if snapshot is not None and key in snapshot.task_documents:
            return snapshot.task_documents[key]
        document = lifecycle.task_document(self.root, Path(task_path))
        if snapshot is not None:
            snapshot.task_documents[key] = document
        return document

    def show_task(self, task_id: str) -> tuple[Task | None, list[dict[str, Any]]]:
        return self.tasks.show_task(task_id)

    def advance_task(self, task_id: str, back_reason: str | None = None) -> tuple[Task | None, TransitionResult | None]:
        return self.tasks.advance_task(task_id, back_reason=back_reason)

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        return self.tasks.next_action_report(task_selector)

    def render_next_action_diagram(self) -> str:
        return self.tasks.render_next_action_diagram()

    # ---------------------------------------------------------------- closeout
    def verify_task_closeout(self, task_selector: str, *, task_path: Path | None = None) -> dict[str, Any]:
        return self.closure.verify_task_closeout(task_selector, task_path=task_path)

    # ---------------------------------------------------------------- drawer
    def resolve_drawer_source(self, selector: str) -> Path:
        return self.drawer.resolve_drawer_source(selector)

    def attach_drawer_source(self, payload: dict[str, Any], drawer_file: Path) -> dict[str, Any]:
        return self.drawer.attach_drawer_source(payload, drawer_file)

    # ---------------------------------------------------------------- atoms
    def atom_folder_axis(self) -> str | None:
        return self.atoms.atom_folder_axis()

    def list_atoms(self, axis_value: str | None = None) -> tuple[str | None, list[dict[str, Any]]]:
        return self.atoms.list_atoms(axis_value)

    def reorganize_atoms(self, *, dry_run: bool = False) -> dict[str, Any]:
        return self.atoms.reorganize_atoms(dry_run=dry_run)

    def validate_atoms(self, selector: str | None = None) -> list[dict[str, Any]]:
        return self.atoms.validate_atoms(selector)

    def delete_atom(self, selector: str, *, force: bool = False) -> DocumentRecord:
        return self.atoms.delete_atom(selector, force=force)

    def create_atom_from_source(
        self,
        atom_id: str,
        *,
        five_wh_one_plus: str,
        title: str | None = None,
        tags: list[str] | None = None,
        from_pill: str | None = None,
        from_graph: str | None = None,
        from_diagram: str | None = None,
        graph_path: str | None = None,
    ) -> AtomCreateResult:
        return self.atoms.create_atom_from_source(
            atom_id,
            five_wh_one_plus=five_wh_one_plus,
            title=title,
            tags=tags,
            from_pill=from_pill,
            from_graph=from_graph,
            from_diagram=from_diagram,
            graph_path=graph_path,
        )

    def split_atom(
        self,
        selector: str,
        *,
        into_ids: list[str],
        section_flags: list[str] | None = None,
        force: bool = False,
    ) -> AtomSplitResult:
        return self.atoms.split_atom(
            selector,
            into_ids=into_ids,
            section_flags=section_flags,
            force=force,
        )

    def merge_atom(
        self,
        selector: str,
        *,
        into_selector: str,
        force: bool = False,
    ) -> AtomMergeResult:
        return self.atoms.merge_atom(selector, into_selector=into_selector, force=force)

    # ---------------------------------------------------------------- private helpers
    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        return doc_access.atom_doc_path(self.root, atom_id, tags)

FILE:deskops/services/atoms.py
"""Atom domain service: create, validate, reorganize, split, merge, retarget, delete.

Every atom write goes through ``deskops.doc_access`` and the desk's
``sldb.api.transaction``; split and merge each run inside one ``desk_transaction``
block so a failure restores the original files and store entries.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from dataclasses import field
import hashlib
from pathlib import Path
import re
import subprocess
from typing import Any
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from deskops import doc_access
from deskops.atom_tags import axis_folder
from deskops.atom_tags import axis_values
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import refuse_unplaced_tags
from deskops.atom_tags import tag_findings
from deskops.doc_access import DocumentRecord
from deskops.models import AtomDoc
from deskops.models import PillDoc
from deskops.models.validation import check_document
from deskops.models.validation import validated
from deskops.services.references import referrers_of
from deskops.services.references import rewrite_referrers

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


@dataclass(slots=True)
class AtomValidationRecord:
    doc_id: str
    path: Path
    errors: list[str]


@dataclass(slots=True)
class AtomSplitResult:
    original_id: str
    original_path: Path
    created: list[DocumentRecord]
    redirect_kept: bool
    inbound_references: list[str]


@dataclass(slots=True)
class AtomMergeResult:
    source_id: str
    source_path: Path
    target_id: str
    target_path: Path
    redirect_kept: bool
    rewritten_references: list[str]
    ambiguities: list[str]


@dataclass(slots=True)
class AtomCreateResult:
    doc_id: str
    path: Path
    source_kind: str
    source_selector: str
    provenance: str


# ---------------------------------------------------------------- code citations
#: The relation a ``--write`` of ``deskops atoms citations`` records: file path -> atom.
CITED_BY = "cited_by"
#: Where the ``cited_by`` RelationTypeDoc and the RelationDoc of each citation live.
CITATIONS_DIR = Path("desk") / "citations"
CITED_BY_TYPE_NAME = "type-cited_by"
_CITED_ATOM_ID = re.compile(r"^atom-[a-z0-9-]+$")
_COMMENT_CITATION = re.compile(r"# Atom: (\S+)")


@dataclass(frozen=True, slots=True)
class AtomCitation:
    """One code -> atom citation: the file (relative to the root), its line and the atom id."""

    path: str
    line: int
    atom_id: str


@dataclass(slots=True)
class AtomCitationReport:
    citations: list[AtomCitation]
    broken: list[AtomCitation]
    orphans: list[str]
    created: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    written: bool = False


def docstring_citations(source: str) -> list[tuple[int, str]]:
    """(line, atom id) of each ``Atoms:`` block entry in a module docstring.

    The block is a line that is exactly ``Atoms:`` followed by one ``atom-<slug>`` per line in
    column 0; it ends at the first empty line, the first line that is not an id, or the end of
    the docstring. A module without a docstring (or that does not parse) cites nothing.
    """
    try:
        module = ast.parse(source)
    except (SyntaxError, ValueError):
        return []
    first = module.body[0] if module.body else None
    if not (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        return []
    lines = first.value.value.split("\n")
    start = first.value.lineno
    found: list[tuple[int, str]] = []
    in_block = False
    for offset, line in enumerate(lines):
        if not in_block:
            in_block = line.rstrip("\r") == "Atoms:"
            continue
        text = line.rstrip("\r")
        if not _CITED_ATOM_ID.match(text):
            in_block = text == "Atoms:"
            continue
        found.append((start + offset, text))
    return found


def comment_citations(text: str) -> list[tuple[int, str]]:
    """(line, atom id) of each ``# Atom: <id>`` comment whose id is ``atom-<slug>``."""
    found: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for match in _COMMENT_CITATION.finditer(line):
            if _CITED_ATOM_ID.match(match.group(1)):
                found.append((number, match.group(1)))
    return found


def scan_citations(root: Path) -> list[AtomCitation]:
    """Every code -> atom citation in the files ``git ls-files`` lists under ``root``.

    ``*.py`` files cite in the ``Atoms:`` block of the module docstring; every other file with a
    ``# Atom: <id>`` comment. Files that do not decode as UTF-8 (or are gone) are skipped.
    """
    try:
        listed = subprocess.run(
            ["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True
        ).stdout.decode("utf-8", "surrogateescape")
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"Cannot list the versioned files of {root} with git ls-files: {exc}") from exc
    citations: list[AtomCitation] = []
    for relative in sorted(name for name in listed.split("\0") if name):
        path = root / relative
        if not path.is_file():
            continue
        try:
            text = path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        found = docstring_citations(text) if relative.endswith(".py") else comment_citations(text)
        citations.extend(AtomCitation(relative, line, atom_id) for line, atom_id in found)
    return citations


def citation_doc_name(path: str, atom_id: str) -> str:
    """The RelationDoc name of one (file, atom) citation: stable across runs."""
    digest = hashlib.sha1(f"{path}\0{atom_id}".encode("utf-8")).hexdigest()[:12]
    return f"cite-{digest}"


def reference_points_to_atom(root: Path, reference: str) -> bool:
    """Whether a task reference names an atom document of this desk (by path or by id)."""
    candidate = reference.strip()
    if not candidate:
        return False
    path_text = candidate.split("::", 1)[0]
    path = Path(path_text)
    if not path.is_absolute():
        path = root / path
    atoms_dir = doc_access.desk_root(root) / "atoms"
    if path.suffix == ".md" and path.exists():
        try:
            path.relative_to(atoms_dir)
            return True
        except ValueError:
            pass
    atom_id = candidate.removeprefix("atom:")
    if not atom_id.startswith("atom-"):
        return False
    return any(atom_path.stem == atom_id for atom_path in atoms_dir.rglob("*.md"))


class AtomsService:
    def __init__(self, root: Path, operations: "DeskopsOperations") -> None:
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger

    # Document access is ``deskops.doc_access``; these keep the service's own vocabulary.
    def ensure_workspace(self) -> None:
        doc_access.ensure_workspace(self.root)

    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        return doc_access.read_doc(path, model)

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        doc_access.write_doc(self.root, path, model, payload)

    def _write_new_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        doc_access.write_new_doc(self.root, path, model, payload)

    def _remove_created_file(self, path: Path) -> None:
        doc_access.remove_created_file(path)

    def _track_created_artifact(self, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
        doc_access.track_created_artifact(self.root, artifact_id, model, path, doc_id)

    def _resolve_artifact_selector(self, artifact_id: str, directory: Path, selector: str) -> Path:
        return doc_access.resolve_artifact_selector(self.root, artifact_id, directory, selector)

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        return doc_access.list_artifacts(self.root, artifact_id)

    def _resolve_artifact_selector_multi(self, artifact_id: str, directories: list[Path], selector: str) -> Path:
        return doc_access.resolve_artifact_selector_multi(self.root, artifact_id, directories, selector)

    def list_atoms(self, axis_value: str | None = None) -> tuple[str | None, list[dict[str, Any]]]:
        """List atoms annotated with their folder-axis value.

        Returns (axis, payloads). Each payload carries 'axis_values' with every
        value of the configured axis namespace found on the atom's tags.
        """
        axis = self.atom_folder_axis()
        if axis_value is not None and axis is None:
            raise ValueError(
                "--axis-value requires 'atom_folder_axis' to be configured in desk/config.json."
            )
        payloads = self.list_artifacts("artifact.atom")
        results: list[dict[str, Any]] = []
        for payload in payloads:
            values = axis_values(list(payload.get("tags") or []), axis) if axis else []
            payload["axis_values"] = values
            if axis_value is not None and axis_value not in values:
                continue
            results.append(payload)
        return axis, results

    def reorganize_atoms(self, *, dry_run: bool = False) -> dict[str, Any]:
        """Move atoms carrying a folder-axis tag into their axis subfolder.

        Idempotent: atoms already in the right place are skipped. Atoms without
        an axis tag are left untouched, preserving manual folder organization.
        Atoms with multiple axis values are reported as errors and skipped.
        """
        self.ensure_workspace()
        axis = self.atom_folder_axis()
        if axis is None:
            raise ValueError(
                "No 'atom_folder_axis' configured in desk/config.json; nothing to reorganize."
            )
        moves: list[dict[str, str]] = []
        errors: list[str] = []
        retargets: dict[str, str] = {}
        for path in self._all_atom_paths():
            try:
                payload = self._read_doc(path, AtomDoc)
            except Exception as exc:
                errors.append(f"{path.relative_to(self.root)}: unreadable atom ({exc})")
                continue
            atom_id = str(payload.get("id") or path.stem)
            tags = list(payload.get("tags") or [])
            try:
                value = folder_axis_value(tags, axis)
            except ValueError as exc:
                errors.append(f"{path.relative_to(self.root)}: {exc}")
                continue
            if value is None:
                continue
            target = self.desk_root / "atoms" / axis_folder(value) / f"{atom_id}.md"
            if target == path:
                continue
            if target.exists():
                errors.append(
                    f"{path.relative_to(self.root)}: target already exists at {target.relative_to(self.root)}"
                )
                continue
            moves.append({
                "id": atom_id,
                "from": str(path.relative_to(self.root)),
                "to": str(target.relative_to(self.root)),
            })
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                path.rename(target)
                retargets[atom_id] = str(target.relative_to(self.root))
        if retargets:
            self._retarget_atom_documents(retargets)
        return {"axis": axis, "moves": moves, "errors": errors, "dry_run": dry_run}

    def validate_atoms(self, selector: str | None = None) -> list[dict[str, Any]]:
        self.ensure_workspace()
        paths = [self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)] if selector else self._all_atom_paths()
        # Undeclared namespaces are sldb's tag family findings (only on tracked atoms).
        findings = tag_findings(self.root)
        results: list[dict[str, Any]] = []
        for path in paths:
            record = self._validate_atom_path(path, findings.get(str(path), {}).get("namespace", []))
            results.append({
                "id": record.doc_id,
                "path": str(path),
                "errors": list(record.errors),
            })
        return results

    def delete_atom(self, selector: str, *, force: bool = False) -> DocumentRecord:
        self.ensure_workspace()
        path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        payload = self._read_doc(path, AtomDoc)
        atom_id = str(payload.get("id") or path.stem)
        inbound_references = [item.location for item in referrers_of(self.root, path)]
        if inbound_references and not force:
            refs = "; ".join(inbound_references)
            raise ValueError(
                f"Refusing to delete {atom_id}; inbound references found: {refs}. Re-run with --force to delete without rewriting references."
            )
        untracked = doc_access.index_entry(self.root, path) is not None
        doc_access.delete_doc(self.root, path)
        return DocumentRecord(kind="atom-untracked" if untracked else "atom", doc_id=atom_id, path=path)

    def create_atom_from_source(
        self,
        atom_id: str,
        *,
        five_wh_one_plus: str,
        title: str | None = None,
        tags: list[str] | None = None,
        from_pill: str | None = None,
        from_graph: str | None = None,
        from_diagram: str | None = None,
        graph_path: str | None = None,
    ) -> AtomCreateResult:
        self.ensure_workspace()
        refuse_unplaced_tags(self.root, list(tags or []))
        source_flags = [flag for flag in (from_pill, from_graph, from_diagram) if flag]
        if len(source_flags) != 1:
            raise ValueError("Atom create requires exactly one source: --from-pill, --from-graph, or --from-diagram.")

        atom_id = str(atom_id).strip()
        normalized_question = str(five_wh_one_plus).strip()

        if from_pill:
            payload, source_selector, provenance = self._build_atom_from_pill(
                atom_id,
                from_pill,
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
            )
            source_kind = "pill"
        elif from_graph:
            payload, source_selector, provenance = self._build_atom_from_graph_finding(
                atom_id,
                from_graph,
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
                graph_path=graph_path,
            )
            source_kind = "graph"
        else:
            payload, source_selector, provenance = self._build_atom_from_diagram(
                atom_id,
                from_diagram or "",
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
            )
            source_kind = "diagram"

        validated(AtomDoc, payload)
        path = self._atom_doc_path(atom_id, list(payload.get("tags") or []))
        doc_access.create_doc(self.root, path, AtomDoc, payload, atom_id)
        return AtomCreateResult(
            doc_id=atom_id,
            path=path,
            source_kind=source_kind,
            source_selector=source_selector,
            provenance=provenance,
        )

    def split_atom(
        self,
        selector: str,
        *,
        into_ids: list[str],
        section_flags: list[str] | None = None,
        force: bool = False,
    ) -> AtomSplitResult:
        self.ensure_workspace()
        path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        payload = self._read_doc(path, AtomDoc)
        atom_id = str(payload.get("id") or path.stem)
        inbound_references = [item.location for item in referrers_of(self.root, path)]
        if inbound_references and not force:
            refs = "; ".join(inbound_references)
            raise ValueError(
                f"Refusing to split {atom_id}; inbound references found: {refs}. "
                "Re-run with --force to keep the original as a redirect stub without rewriting referrers."
            )

        normalized_ids = [str(item).strip() for item in into_ids if str(item).strip()]
        if len(normalized_ids) < 2:
            raise ValueError("Atom split requires at least two target ids via --into.")
        if len(set(normalized_ids)) != len(normalized_ids):
            raise ValueError("Atom split target ids must be unique.")
        if atom_id in normalized_ids:
            raise ValueError(f"Atom split target ids must not include the source atom id {atom_id}.")

        sections = self._split_atom_answer_sections(str(payload.get("answer") or ""))
        assignments = self._resolve_atom_split_assignments(normalized_ids, sections, section_flags or [])
        new_payloads: dict[str, dict[str, Any]] = {}
        for target_id in normalized_ids:
            heading, content = assignments[target_id]
            new_payloads[target_id] = {
                "id": target_id,
                "title": f"{payload['title']} — {heading}",
                "five_wh_one_plus": payload["five_wh_one_plus"],
                "answer": content,
                "tags": list(payload.get("tags") or []),
                "provenance": payload.get("provenance"),
            }
            validated(AtomDoc, new_payloads[target_id])

        created: list[DocumentRecord] = []

        with doc_access.desk_transaction(self.root):
            for target_id in normalized_ids:
                new_payload = new_payloads[target_id]
                new_path = self._atom_doc_path(target_id, list(new_payload.get("tags") or []))
                doc_access.create_doc(self.root, new_path, AtomDoc, new_payload, target_id)
                created.append(DocumentRecord(kind="atom", doc_id=target_id, path=new_path))

            payload["answer"] = self._render_atom_split_redirect_answer(atom_id, normalized_ids)
            self._write_doc(path, AtomDoc, payload)

        return AtomSplitResult(
            original_id=atom_id,
            original_path=path,
            created=created,
            redirect_kept=True,
            inbound_references=inbound_references,
        )

    def merge_atom(
        self,
        selector: str,
        *,
        into_selector: str,
        force: bool = False,
    ) -> AtomMergeResult:
        self.ensure_workspace()
        source_path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        target_path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", into_selector)
        if source_path == target_path:
            raise ValueError("Atom merge source and target must resolve to different atoms.")

        source_payload = self._read_doc(source_path, AtomDoc)
        target_payload = self._read_doc(target_path, AtomDoc)
        source_id = str(source_payload.get("id") or source_path.stem)
        target_id = str(target_payload.get("id") or target_path.stem)

        validated(AtomDoc, source_payload)
        validated(AtomDoc, target_payload)

        ambiguities = self._detect_atom_merge_ambiguities(source_payload, target_payload)
        if ambiguities and not force:
            details = "; ".join(ambiguities)
            raise ValueError(
                f"Refusing to merge {source_id} into {target_id}; merge is ambiguous: {details}. "
                "Re-run with --force to keep the target atom semantics and preserve the source atom as a redirect stub."
            )

        with doc_access.desk_transaction(self.root) as transaction:
            rewritten_references = rewrite_referrers(
                self.root, source_path, target_path, transaction=transaction, excluded=(target_path,)
            )
            merged_answer = self._merge_atom_answers(target_payload, source_payload)
            target_payload["answer"] = merged_answer
            target_payload["tags"] = self._merge_atom_tags(
                list(target_payload.get("tags") or []),
                list(source_payload.get("tags") or []),
            )
            self._write_doc(target_path, AtomDoc, target_payload)

            source_payload["answer"] = self._render_atom_merge_redirect_answer(source_id, target_id)
            self._write_doc(source_path, AtomDoc, source_payload)

        return AtomMergeResult(
            source_id=source_id,
            source_path=source_path,
            target_id=target_id,
            target_path=target_path,
            redirect_kept=True,
            rewritten_references=rewritten_references,
            ambiguities=ambiguities,
        )

    def _all_atom_paths(self) -> list[Path]:
        atoms_dir = self.desk_root / "atoms"
        if not atoms_dir.exists():
            return []
        return sorted(
            path for path in atoms_dir.rglob("*.md")
            if path.name != "tag-namespaces.yaml"
            # Crossroads and protoatoms have their own models: see deskops.domain_tree.
            and not path.name.startswith(("crossroad-", "proto-"))
        )

    def _build_atom_from_pill(
        self,
        atom_id: str,
        pill_selector: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
    ) -> tuple[dict[str, Any], str, str]:
        field_map = {
            "what": "what",
            "why": "why",
            "how": "how",
            "how_not": "how_not",
            "when": "when",
            "where": "where",
        }
        source_field = field_map.get(five_wh_one_plus)
        if source_field is None:
            raise ValueError(
                "Atom create from pill only supports questions that map directly to pill sections: what, why, how, how_not, when, where."
            )
        directories = [self.desk_root / "contexts", self.desk_root / "drawer" / "pills"]
        pill_path = self._resolve_artifact_selector_multi("artifact.pill", directories, pill_selector)
        pill_payload = self._read_doc(pill_path, PillDoc)
        answer = str(pill_payload.get(source_field) or "").strip()
        if not answer:
            raise ValueError(f"Pill section '{source_field}' is empty; cannot create atom from it.")
        relative_path = pill_path.relative_to(self.root).as_posix()
        source_selector = str(pill_payload.get("id") or pill_path.stem)
        provenance = f"{relative_path}::{source_field}"
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"{pill_payload['title']} — {source_field.replace('_', ' ').title()}",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": answer,
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, source_selector, provenance

    def _build_atom_from_graph_finding(
        self,
        atom_id: str,
        finding_selector: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
        graph_path: str | None,
    ) -> tuple[dict[str, Any], str, str]:
        from deskops.graph.checks import find_missing_graph_references

        source_id, target_id = self._parse_graph_finding_selector(finding_selector)
        resolved_graph_path = None
        if graph_path:
            resolved_graph_path = Path(graph_path)
            if not resolved_graph_path.is_absolute():
                resolved_graph_path = (self.root / resolved_graph_path).resolve()
        findings = [
            finding for finding in find_missing_graph_references(self.root, resolved_graph_path)
            if finding.source_id == source_id and finding.target_id == target_id
        ]
        if not findings:
            raise FileNotFoundError(
                f"Graph finding not found for selector {finding_selector}. Run 'deskops graph missing --root {self.root}' to inspect available findings."
            )
        if len(findings) > 1:
            kinds = ", ".join(sorted({finding.kind for finding in findings}))
            raise ValueError(
                f"Graph finding selector {finding_selector} matched multiple findings ({kinds}). Narrow the graph input so one finding remains."
            )
        finding = findings[0]
        provenance = self._compose_exact_provenance(finding.provenance_path, finding.provenance_locator)
        if provenance is None:
            raise ValueError(
                f"Graph finding {finding_selector} does not expose a resolvable provenance path; exact-source atom creation is blocked."
            )
        answer_lines = [
            f"Graph finding `{finding.kind}` records a missing reference from `{finding.source_id}` to `{finding.target_id}`.",
            "",
            f"- Reason: {finding.reason}",
        ]
        if finding.role:
            answer_lines.append(f"- Role: `{finding.role}`")
        if finding.extractor:
            answer_lines.append(f"- Extractor: `{finding.extractor}`")
        answer_lines.append(f"- Provenance: `{provenance}`")
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"Graph finding — {source_id} → {target_id}",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": "\n".join(answer_lines).strip(),
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, f"{source_id}->{target_id}", provenance

    def _build_atom_from_diagram(
        self,
        atom_id: str,
        diagram_path_value: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
    ) -> tuple[dict[str, Any], str, str]:
        diagram_path = Path(diagram_path_value)
        if not diagram_path.is_absolute():
            diagram_path = (self.root / diagram_path).resolve()
        if not diagram_path.exists() or not diagram_path.is_file():
            raise FileNotFoundError(f"Diagram source not found: {diagram_path_value}")
        relative_path = diagram_path.relative_to(self.root).as_posix()
        text = diagram_path.read_text(encoding="utf-8")
        provenance = relative_path
        answer = text.strip()
        if diagram_path.suffix == ".mmd":
            answer = f"```mermaid\n{answer}\n```".strip()
        elif diagram_path.suffix == ".md":
            mermaid_match = re.search(r"```mermaid\s*\n(?P<body>.*?)\n```", text, flags=re.DOTALL | re.IGNORECASE)
            if mermaid_match is not None:
                answer = f"```mermaid\n{mermaid_match.group('body').strip()}\n```".strip()
                provenance = f"{relative_path}::mermaid:1"
        if not answer:
            raise ValueError(f"Diagram source {diagram_path_value} is empty; cannot create atom from it.")
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"{diagram_path.stem.replace('-', ' ').replace('_', ' ').title()} — Diagram",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": answer,
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, relative_path, provenance

    def _parse_graph_finding_selector(self, selector: str) -> tuple[str, str]:
        source_id, separator, target_id = str(selector).partition("->")
        source_id = source_id.strip()
        target_id = target_id.strip()
        if not separator or not source_id or not target_id:
            raise ValueError(
                f"Invalid --from-graph value '{selector}'. Expected SOURCE_ID->TARGET_ID."
            )
        return source_id, target_id

    def _compose_exact_provenance(self, provenance_path: str | None, provenance_locator: str | None) -> str | None:
        path_text = str(provenance_path or "").strip()
        if not path_text:
            return None
        locator_text = str(provenance_locator or "").strip()
        return f"{path_text}::{locator_text}" if locator_text else path_text

    def _split_atom_answer_sections(self, answer: str) -> list[tuple[str, str]]:
        trimmed = answer.strip()
        if not trimmed:
            raise ValueError("Source atom answer is empty; nothing to split.")
        matches = list(re.finditer(r"^(#{2,6})\s+(.+?)\s*$", answer, flags=re.MULTILINE))
        if not matches:
            raise ValueError(
                "Source atom answer does not contain markdown subsections. Add heading-based sections under ## Answer or pass a differently structured atom."
            )
        leading = answer[:matches[0].start()].strip()
        if leading:
            raise ValueError(
                "Source atom answer contains content before the first subsection heading; split only supports heading-based sections that start immediately in the answer body."
            )
        sections: list[tuple[str, str]] = []
        for index, match in enumerate(matches):
            heading = match.group(2).strip()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(answer)
            content = answer[match.end():end].strip()
            if not content:
                raise ValueError(f"Source atom subsection '{heading}' is empty.")
            sections.append((heading, content))
        return sections

    def _resolve_atom_split_assignments(
        self,
        into_ids: list[str],
        sections: list[tuple[str, str]],
        section_flags: list[str],
    ) -> dict[str, tuple[str, str]]:
        by_heading = {heading: content for heading, content in sections}
        if len(by_heading) != len(sections):
            raise ValueError("Source atom answer subsection headings must be unique to support atom splitting.")

        if not section_flags:
            if len(sections) != len(into_ids):
                raise ValueError(
                    f"Source atom answer exposes {len(sections)} subsection(s) but --into lists {len(into_ids)} target ids. "
                    "Provide --section NEW_ATOM_ID:SECTION_HEADING for each target or align the counts."
                )
            return {
                target_id: (heading, content)
                for target_id, (heading, content) in zip(into_ids, sections, strict=True)
            }

        assignments: dict[str, tuple[str, str]] = {}
        for raw_flag in section_flags:
            target_id, separator, heading = str(raw_flag).partition(":")
            target_id = target_id.strip()
            heading = heading.strip()
            if not separator or not target_id or not heading:
                raise ValueError(
                    f"Invalid --section value '{raw_flag}'. Expected NEW_ATOM_ID:SECTION_HEADING."
                )
            if target_id not in into_ids:
                raise ValueError(
                    f"Section assignment references unknown target id '{target_id}'. Known ids: {', '.join(into_ids)}"
                )
            if target_id in assignments:
                raise ValueError(f"Section assignment for {target_id} was provided more than once.")
            if heading not in by_heading:
                available = ", ".join(heading_name for heading_name, _ in sections)
                raise ValueError(
                    f"Section heading '{heading}' was not found in the source atom answer. Available headings: {available}"
                )
            content = by_heading[heading]
            if any(existing_heading == heading for existing_heading, _ in assignments.values()):
                raise ValueError(f"Section heading '{heading}' was assigned more than once.")
            assignments[target_id] = (heading, content)

        missing = [target_id for target_id in into_ids if target_id not in assignments]
        if missing:
            raise ValueError(
                f"Missing --section assignment for target ids: {', '.join(missing)}"
            )
        return assignments

    def _render_atom_split_redirect_answer(self, atom_id: str, target_ids: list[str]) -> str:
        bullets = "\n".join(f"- atom:{target_id}" for target_id in target_ids)
        return (
            f"This atom has been split. Use the child atoms below instead of expanding atom:{atom_id} further.\n\n"
            "Redirect targets:\n"
            f"{bullets}\n\n"
            "The original atom is intentionally kept as a redirect stub so existing inbound references continue to resolve until callers are rerouted."
        )

    def _detect_atom_merge_ambiguities(
        self,
        source_payload: dict[str, Any],
        target_payload: dict[str, Any],
    ) -> list[str]:
        ambiguities: list[str] = []
        source_question = str(source_payload.get("five_wh_one_plus") or "").strip()
        target_question = str(target_payload.get("five_wh_one_plus") or "").strip()
        if source_question and target_question and source_question != target_question:
            ambiguities.append(
                f"five_wh_one_plus conflict ({source_question} vs {target_question})"
            )
        return ambiguities

    def _merge_atom_tags(self, target_tags: list[str], source_tags: list[str]) -> list[str]:
        merged: list[str] = []
        for tag in [*target_tags, *source_tags]:
            if tag not in merged:
                merged.append(tag)
        return merged

    def _merge_atom_answers(
        self,
        target_payload: dict[str, Any],
        source_payload: dict[str, Any],
    ) -> str:
        target_answer = str(target_payload.get("answer") or "").strip()
        source_answer = str(source_payload.get("answer") or "").strip()
        if not target_answer:
            return source_answer
        if not source_answer:
            return target_answer
        if source_answer == target_answer or source_answer in target_answer:
            return target_answer
        appendix = self._render_atom_merge_appendix(source_payload)
        if appendix in target_answer:
            return target_answer
        return f"{target_answer}\n\n{appendix}".strip()

    def _render_atom_merge_appendix(self, source_payload: dict[str, Any]) -> str:
        source_id = str(source_payload.get("id") or "").strip()
        source_title = str(source_payload.get("title") or source_id).strip()
        source_question = str(source_payload.get("five_wh_one_plus") or "").strip()
        source_provenance = str(source_payload.get("provenance") or "").strip()
        source_answer = str(source_payload.get("answer") or "").strip()
        metadata_lines = [
            f"Merged from atom:{source_id} ({source_title}).",
        ]
        if source_question:
            metadata_lines.append(f"Original question: `{source_question}`")
        if source_provenance:
            metadata_lines.append(f"Original provenance: `{source_provenance}`")
        metadata = "\n".join(f"- {line}" for line in metadata_lines)
        return f"### Merged from atom:{source_id}\n\n{metadata}\n\n{source_answer}".strip()

    def _render_atom_merge_redirect_answer(self, source_id: str, target_id: str) -> str:
        return (
            f"This atom has been merged into atom:{target_id}. Use atom:{target_id} instead of expanding atom:{source_id} further.\n\n"
            "The original atom is intentionally kept as a redirect stub so the old id remains traceable after inbound references are reconciled."
        )

    def _validate_atom_path(self, path: Path, namespace_errors: list[str] | None = None) -> AtomValidationRecord:
        try:
            payload, errors = check_document(AtomDoc, path.read_text(encoding="utf-8"), invalid="model validation failed")
        except Exception as exc:
            return AtomValidationRecord(doc_id=path.stem, path=path, errors=[f"model validation failed: {exc}"])
        doc_id = str(payload.get("id") or path.stem)

        if path.stem != doc_id:
            errors.append(f"filename must match atom id '{doc_id}'")

        errors.extend(namespace_errors or [])

        provenance = str(payload.get("provenance") or "").strip()
        if provenance and not self._provenance_is_resolvable(provenance):
            errors.append(f"provenance is not resolvable: {provenance}")

        return AtomValidationRecord(doc_id=doc_id, path=path, errors=errors)

    def _provenance_is_resolvable(self, provenance: str) -> bool:
        parsed = urlparse(provenance)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return True
        path_text = provenance.split("::", 1)[0].split("#", 1)[0].strip()
        if not path_text:
            return False
        path = Path(path_text)
        if not path.is_absolute():
            path = self.root / path
        return path.exists()

    def _retarget_atom_documents(self, retargets: dict[str, str]) -> bool:
        """Update tracked atom document paths in the .sldb store after moves.

        Retracking through SLDB's own track/untrack API keeps every derived index
        (semantic shards, sections, hashes, journal) consistent; editing the raw
        index files leaves the derived layers stale.
        """
        if not (self.root / ".sldb").is_dir():
            return False

        changed = False
        for atom_id, new_path in retargets.items():
            try:
                with doc_access.desk_transaction(self.root) as transaction:
                    doc_access.untrack_doc(self.root, atom_id)
                    transaction.track(self.root / new_path, "AtomDoc", atom_id)
            except Exception:
                continue
            doc_access.forget_index(self.root)
            changed = True
        return changed

    def _untrack_atom_document(self, atom_id: str) -> bool:
        if not (self.root / ".sldb").is_dir():
            return False
        try:
            doc_access.untrack_doc(self.root, atom_id)
        except Exception:
            return False
        return True

    def atom_folder_axis(self) -> str | None:
        """Return the configured folder axis namespace for atoms, or None (flat)."""
        return doc_access.atom_folder_axis(self.root)

    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        return doc_access.atom_doc_path(self.root, atom_id, tags)

    # ------------------------------------------------------------ code citations
    def atom_ids(self) -> set[str]:
        """The ids of the atoms under desk/atoms (the file stem when the id cannot be read)."""
        ids: set[str] = set()
        for path in self._all_atom_paths():
            try:
                ids.add(str(self._read_doc(path, AtomDoc).get("id") or path.stem))
            except Exception:
                ids.add(path.stem)
        return ids

    def atom_citations(self, *, write: bool = False) -> AtomCitationReport:
        """Scan the code -> atom citations: broken ones (the atom does not exist) and orphan
        atoms (no file cites them). With ``write``, keep one ``cited_by`` RelationDoc per valid
        (file, atom) citation in the desk's store and drop the ones no file makes any more."""
        self.ensure_workspace()
        known = self.atom_ids()
        citations = scan_citations(self.root)
        broken = [item for item in citations if item.atom_id not in known]
        cited = {item.atom_id for item in citations}
        report = AtomCitationReport(
            citations=citations,
            broken=broken,
            orphans=sorted(known - cited),
        )
        if write:
            self._write_citations(report, {(item.path, item.atom_id) for item in citations if item.atom_id in known})
        return report

    def _citation_docs(self) -> list[tuple[Path, dict[str, Any]]]:
        """(path, payload) of every tracked ``cited_by`` RelationDoc of the desk's store."""
        if not doc_access.has_store(self.root):
            return []
        from sldb.api import select_documents
        from sldb.models.relation_doc import RelationDoc

        found: list[tuple[Path, dict[str, Any]]] = []
        for row in select_documents(doc_access.store_path(self.root), {"model": "RelationDoc"}):
            path = self.root / row["path"]
            if not path.exists():
                continue
            payload = self._read_doc(path, RelationDoc)
            if payload.get("relation_type") == CITED_BY:
                found.append((path, payload))
        return found

    def cited_by(self, atom_id: str) -> list[str]:
        """The files whose ``cited_by`` RelationDoc names ``atom_id`` (what ``--write`` recorded)."""
        target = f"AtomDoc:{atom_id}"
        return sorted(
            {str(payload.get("source_id")) for _path, payload in self._citation_docs() if payload.get("target_id") == target}
        )

    def _write_citations(self, report: AtomCitationReport, wanted: set[tuple[str, str]]) -> None:
        if not doc_access.has_store(self.root):
            raise ValueError("--write needs the desk's sldb store; run 'deskops init' first.")
        from sldb.api import edge_node
        from sldb.api import relation_type_node_id
        from sldb.models.relation_doc import RelationDoc
        from sldb.models.relation_type_doc import RelationTypeDoc

        directory = self.root / CITATIONS_DIR
        existing = {
            (str(payload.get("source_id")), str(payload.get("target_id")).removeprefix("AtomDoc:")): path
            for path, payload in self._citation_docs()
        }
        has_type = edge_node(doc_access.store_path(self.root), relation_type_node_id(CITED_BY), include_linked=False) is not None
        with doc_access.desk_transaction(self.root):
            if not has_type:
                directory.mkdir(parents=True, exist_ok=True)
                doc_access.create_doc(
                    self.root,
                    directory / f"{CITED_BY_TYPE_NAME}.md",
                    RelationTypeDoc,
                    {
                        "title": "Cited by",
                        "name": CITED_BY,
                        "direction": "directed",
                        "cardinality": "many_to_many",
                        "axis": "PROVENANCE",
                        "source_types": [],
                        "target_types": ["AtomDoc"],
                        "condition": "",
                        "description": (
                            "A versioned file cites an atom: the Atoms: block of a Python module docstring "
                            "or a '# Atom: <id>' comment. Written by `deskops atoms citations --write`."
                        ),
                    },
                    CITED_BY_TYPE_NAME,
                )
            for source, atom_id in sorted(wanted - set(existing)):
                directory.mkdir(parents=True, exist_ok=True)
                name = citation_doc_name(source, atom_id)
                doc_access.create_doc(
                    self.root,
                    directory / f"{name}.md",
                    RelationDoc,
                    {
                        "title": f"{source} cites {atom_id}",
                        "source_id": source,
                        "target_id": f"AtomDoc:{atom_id}",
                        "relation_type": CITED_BY,
                        "condition": "",
                        "attributes": {},
                        "notes": "",
                    },
                    name,
                )
                report.created.append(f"{source} -> {atom_id}")
            for key in sorted(set(existing) - wanted):
                doc_access.delete_doc(self.root, existing[key])
                report.removed.append(f"{key[0]} -> {key[1]}")
        report.written = True

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

FILE:tests/fixtures/model_contract_hashes.json
{
  "AtomDoc": "ee1a85c1da9ee8ba88d3094404d7771d03e738aad81a0995067fd55369e8b939",
  "BoardDoc": "efc79456a8b75fb3ece9476ec5c84df977f7ab5a4491a40cfcb1398a12f085cc",
  "CrossroadDoc": "f1cb8901cf0b6375518de54bbd527963dd396e071243e9d8e2f15f9142ab971d",
  "DeskFAQDoc": "c05ce9c314e00f8a9338ce1cbaab37e5a6a16fb880dc41371ef78e6403037f80",
  "InboxNoteDoc": "963ba7690409be4164e1f8d440638796e7df0e71058aae78ad371d655f10e82d",
  "MaterializationContractDoc": "7a9c4f2a6d1393a581170cb62c4c3779b80310e3b31ebe865e8bfd92d6beaf1b",
  "PillDoc": "16cbc282a5f20f99f8e31d890d1006d8c243049a78e1d1fca1c0a62737fee5a6",
  "ProtoAtomDoc": "d9f08880b80caae90116c3c56c49aecad56db507843df80f706feef2318ca25d",
  "RelationDoc": "a71cc04505ddc23c00b8a9ff917e000e955fe11de68ddbaeb08da2bb1e68c9a6",
  "RelationTypeDoc": "57b63063959eb2f0b721697bc626d10bc4d960672ed03fa04f9d0a5e1f499699",
  "RepositoryDoc": "4e3d7ee7a6c1475b5bd6a9cce0510dfc1b7d7e3ede1f63f68f797108a5a817cc",
  "ReviewDoc": "f16882ab411b3ca17fed6de6494d082354c73679ec0db0603a8e21bd3a606759",
  "RitualDoc": "fd5777c6019cce9e2c3425026376c9de410e9f8c9c66fe52f88a26a8e8f398d6",
  "RoleDoc": "0133498aec7921a98513106e1893442b6dd39484b2ec2b5ea700ec6ed837705f",
  "RuleDoc": "411e41fc4ed0641c8436fc5c5c32aef148da868661d58951614298568a237fd2",
  "RunDoc": "39ae36d6191a211083ab84985efaa456d227f5a48ba4136dc86298e8a8c4d67e",
  "RuntimeProfileDoc": "b8ff370537a32427fddde6b889bb45fefe0ea3bb30ee7a7d88c8bb18834bde5e",
  "StepDoc": "faeb52e5f790fd84fed3b4718e5c3ece784a3cd61ed1212ed7cd11e59fdec64e",
  "TaskAggregateDoc": "6ecfd294671880bb41d5a72daa82bf310e4618809f3696bb64111d232c8ac9c3",
  "TaskCodeDoc": "fac7ef5325d87f49c624009f368c0ee7695b8e8c29c3b57df00e8d85c50fcb80",
  "TaskDebugDoc": "53dbba942bb0773e4fe6563cadaa9247a0005c0c727262091b284445ab5ae667",
  "TaskDecisionDoc": "8977e4980584dafddb756289693401a7776fe2643c18afab6bd751213fddea69",
  "TaskDoc": "9adfb625f52f6ab68e84d82e56d001755ed80377c4e678b591fecbfa5f4c172f",
  "TaskDocsDoc": "0b7ba3b70188f4ac397f6ed0e69dca858c95f58a63ae959e5480aec8202d5904",
  "TaskExternalDoc": "18c9b4f737e2efd59001a6b1d09075cac4eca474b2b89b816d2b4ee631fd1e1c",
  "TaskRefactorDoc": "c1246d2faf240237a620436f75d03f1341658637d2b8a207965b720b76e79976",
  "ViewDoc": "1616bd1b499ad0c18556a9a4cc0ccd4982aad885727c41aa8e7fd53262d69c2b"
}

FILE:tests/fixtures/golden/help/deskops_add_atom.txt
usage: deskops add atom [-h] [--root ROOT] [--from-yaml FROM_YAML]
                        [--title TITLE]
                        [--five-wh-one-plus {what,why,how,how_not,when,where,for_whom}]
                        [--answer ANSWER] [--tags TAGS [TAGS ...]]
                        [--provenance PROVENANCE]

Create an atom artifact.

options:
  -h, --help            show this help message and exit
  --root ROOT           Target repository root.
  --from-yaml FROM_YAML
                        Load the atom payload from a YAML file.
  --title TITLE         Short, descriptive title for the atomic knowledge
                        unit.
  --five-wh-one-plus {what,why,how,how_not,when,where,for_whom}
                        The single 5WH1+ question this atom answers: one of
                        what, why, how, how_not, when, where, for_whom.
  --answer ANSWER       The curated raw answer to the selected 5WH1+ question,
                        written as one stable knowledge unit.
  --tags TAGS [TAGS ...]
                        Namespaced semantic tags used for retrieval and
                        grouping, each in the form namespace:value (e.g.
                        system:deskops, topic:templates). Tags do not encode
                        lifecycle, relations, evidence, or materialization.
  --provenance PROVENANCE
                        Optional URL or path to the authoritative source of
                        this atom's knowledge. Used for traceability and
                        provenance tracking.

Example:
  deskops add atom --root . --title "Example" --five-wh-one-plus "what" --answer "..."

FILE:tests/fixtures/golden/help/deskops_list_atoms.txt
usage: deskops list atoms [-h] [--root ROOT] [--axis-value AXIS_VALUE]
                          [--format {text,json}]

List atoms.

options:
  -h, --help            show this help message and exit
  --root ROOT           Target repository root.
  --axis-value AXIS_VALUE
                        Filter atoms by the configured atom_folder_axis
                        namespace value (e.g. licitaciones).
  --format {text,json}  Output format.

FILE:tests/fixtures/golden/help/deskops_message_send.txt
usage: deskops message send [-h] [--title TITLE] [--kind {unclear,suggestion}]
                            [--to REPO] [--from SENDER] [--root ROOT]
                            [--desk-root DESK_ROOT] [--store STORE]
                            [--pythonpath PYTHONPATH]
                            [--format {text,json,yaml}]
                            body

Send a message to a project desk.

positional arguments:
  body                  Message body

options:
  -h, --help            show this help message and exit
  --title TITLE         Short title for the message
  --kind {unclear,suggestion}
                        Type of message to send
  --to REPO             Target a registered repository name in the ecosystem
  --from SENDER         Override the resolved sender identity with a
                        registered project id
  --root ROOT           Repository root whose desk/ holds the inbox
  --desk-root DESK_ROOT
                        Desk root directory override; defaults to the active
                        project desk
  --store STORE         Store path used to resolve the target project root for
                        the default desk
  --pythonpath PYTHONPATH
                        Project path used when auto-tracking messages through
                        the registered model
  --format {text,json,yaml}
                        Output format.

FILE:instruccion
Cold-bundle de la tarea task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_atoms_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)


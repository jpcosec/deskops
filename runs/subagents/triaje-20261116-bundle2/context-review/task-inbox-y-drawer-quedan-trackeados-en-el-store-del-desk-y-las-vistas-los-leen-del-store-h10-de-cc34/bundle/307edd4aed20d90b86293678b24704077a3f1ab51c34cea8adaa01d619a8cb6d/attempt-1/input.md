FILE:desk/tasks/task-inbox-y-drawer-quedan-trackeados-en-el-store-del-desk-y-las-vistas-los-leen-del-store-h10-de-cc34.md
---
sldb:
  by: agent
  at: '2026-11-16T05:52:05Z'
  authority: generated
  via: save_document_payload
id: task-inbox-y-drawer-quedan-trackeados-en-el-store-del-desk-y-las-vistas-los-leen-del-store-h10-de-cc34
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/data/desk_declaration.yaml
- deskops/data/views/board.md
- deskops/cli/commands/view.py
- deskops/cli/commands/message.py
- deskops/cli/commands/promote.py
- deskops/cli/commands/drawer.py
- tests/test_view.py
- tests/test_message_delivery.py
- tests/test_inbox_promote_cli_gaps.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-inbox-y-drawer-trackeados-en-el-store-del-desk-includes-en-desk-declaration-yaml-y-message-send-promote-trackean-al-escribir-h10-de-cc34.md
---

# Inbox y drawer quedan trackeados en el store del desk y las vistas los leen del store (H10 de CC34)

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (CC34, 2026-11-11). run_view de sldb solo ve documentos trackeados. desk_declaration.yaml no tiene globs de desk/inbox/*.md ni de desk/drawer/tasks/*.md, y deskops/cli/commands/view.py:16 y 359 leen drawer e inbox del disco. `deskops message send` ya trackea la nota al escribir (salida 'Tracked ...' observada el 2026-11-16); falta el drawer.

## Goal

_Describe the concrete result this task must produce._

deskops/data/desk_declaration.yaml incluye los globs de inbox y drawer; los comandos que escriben en el drawer (promote inbox-to-drawer-task y el alta de items del drawer) trackean al escribir; `deskops view` saca drawer e inbox de run_view como board y task. Al cerrar, se avisa a graph_ui para que verifique en navegador sus vistas de drawer e inbox.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/data/desk_declaration.yaml (seccion include: un glob desk/inbox/*.md para InboxNoteDoc y uno desk/drawer/tasks/*.md para TaskDoc, con el mismo formato que los globs existentes de esa seccion), dos ViewDocs nuevos en deskops/data/views/ (drawer.md e inbox.md, con el mismo formato que board.md y task.md), deskops/cli/commands/view.py (drawer e inbox salen de run_view con esos ViewDocs, como board y task hoy), los comandos que escriben en el drawer (deskops promote inbox-to-drawer-task en deskops/cli/commands/promote.py y los subcomandos de deskops/cli/commands/drawer.py que creen archivos) trackeando con la misma llamada que usa message send al escribir la nota, y sus tests. No entra: la verificacion en navegador, que hace graph_ui en la maquina local y no condiciona el cierre; migrar desks ajenos. La nota a graph_ui lleva el hash del commit que implementa esta tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Agregar los globs. 2) Trackear al escribir en el drawer. 3) view lee del store. 4) Tests en tests/test_view.py (una nota y un item nuevos aparecen en la vista sin desk update), tests/test_message_delivery.py y tests/test_inbox_promote_cli_gaps.py. 5) `deskops desk update --apply` en el desk de deskops. 6) `deskops message send --to graph_ui` con el hash.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_view.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_delivery.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_inbox_promote_cli_gaps.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los tests pasan; en el desk de deskops `deskops view` muestra un item del drawer recien creado sin desk update; nota a graph_ui enviada.

FILE:desk/atoms/workflow-model/atom-code-changes-close-with-tests-and-commit.md
---
id: atom-code-changes-close-with-tests-and-commit
title: Code changes close with tests and commit
five_wh_one_plus: when
tags:
- system:deskops
- topic:testing
- topic:git
- topic:closeout
---

# Code changes close with tests and commit

## Answer

A task that modifies code is not closed until relevant tests pass and the completed change is recorded in a descriptive git commit.

FILE:desk/atoms/workflow-model/atom-cli-mutation-testing-uses-sandbox-desk-roots.md
---
id: atom-cli-mutation-testing-uses-sandbox-desk-roots
title: CLI mutation testing uses sandbox desk roots
five_wh_one_plus: how
tags:
- system:deskops
- topic:testing
- topic:cli
- topic:materialization
---

# CLI mutation testing uses sandbox desk roots

## Answer

When testing or exploring mutating deskops CLI commands, agents should point writes at a disposable sandbox root such as `.tmp/deskops-cli-test` instead of the repository's real `desk/`. This keeps generated tasks, lifecycle documents, inbox notes, and other workflow artifacts out of tracked project surfaces unless the mutation is intentionally changing the real desk.

FILE:deskops/data/desk_declaration.yaml
# The desk a fresh repository gets: what `deskops init`, `deskops desk install`, `deskops desk
# update --apply` and the first desk operation create when it is missing (CC36, DP3).
#
# This is an sldb StoreDeclaration (`sldb.api.StoreDeclaration`) restricted to `folders`,
# `seeds` and `include`; deskops reads it, renders every seed for the desk at hand and passes
# the result in process to `sldb.api.scaffold_store` (`deskops.workspace.seed_desk`):
#
# - `{desk_name}` in a `file:` template or in a `document:` payload is replaced with the
#   project directory's name (`str.replace`, no other placeholder exists);
# - `file:` sources are read from `deskops/data/` (`templates/` for the desk's own files,
#   `lifecycle/` for the lifecycle graph);
# - `document:` seeds are rendered through their deskops model, as the Board and the review
#   runtime profile always were; the runtime profile's `system_prompt` is not data here: it
#   is `deskops.services.review.SYSTEM`, injected while the declaration is built.
#
# A desk's own files are `if_missing` seeds: a desk that already has the file keeps its own.
# The task lifecycle graph (CC31, GO09) is `managed`: the three RelationTypeDoc and the three
# RelationDoc under `desk/lifecycle/` are deskops' documents, written from `lifecycle/` and
# rewritten whenever a desk's copy differs (`deskops desk update --apply` reports it). Each
# RelationDoc carries the transition's effects in `attributes`: `sets` (the fields written on
# the task when the edge is taken) and `terminal` (the task closes). The activation gate of
# each factory task type (CC32, GO06/GO08) is a `managed` RuleDoc too, written from `rules/`
# to `desk/lifecycle/rule-activation-<type>.md`: `on_transition` over `ritual-execution`, with
# subject `model <= <TypeDoc>` so a desk subtype inherits it, it requires the review receipts
# the type asks for (accepted and intact) and the task's dependencies closed; sldb evaluates
# it when `deskops advance` asks for the holding edges. The closeout gate of each factory type
# (CC33b) is the same kind of managed RuleDoc, written from `rules/` to
# `desk/lifecycle/rule-closeout-<type>.md`: `on_transition` over `ritual-closeout`, it requires
# the evidence receipts `deskops closeout verify` writes (kinds in `rules/closeout-evidence.yaml`),
# accepted and intact, and `deskops closeout commit` evaluates it; the two
# `rule-closeout-alert-*.md` are `on_write` alerts over the task's own fields. The `include` rules say
# which desk documents `deskops desk update --apply` tracks under which model
# (`sldb.api.stores.apply_declaration.apply_includes`): the lifecycle documents, the rules,
# the three lifecycle rituals by their ids (`RitualDoc:ritual-<x>`, what the graph's edges
# name), the seeded Board (`BoardDoc:Board`) and phase ritual (`RitualDoc:ritual-phase`), which
# the selectors resolve through the store (CC35b d1), and one glob per desk folder. The tasks
# are tracked by their own paths.
folders:
- desk/tasks
- desk/contexts
- desk/rituals
- desk/atoms
- desk/roles
- desk/inbox
- desk/reviews
- desk/drawer
- desk/runtimes
- desk/materializations
- desk/steps
- desk/registry
- desk/faq
seeds:
- path: desk/config.json
  mode: if_missing
  file: templates/config.json
- path: desk/tasks/Board.md
  mode: if_missing
  track: false
  document:
    model: BoardDoc
    name: board-001
    payload:
      id: board-001
      title: '{desk_name} Board'
      scope: desk
      purpose: Route the active execution set for {desk_name}.
      tasks: []
      pills:
      - desk/contexts/pills.md
      rituals:
      - desk/rituals/phase.md
      - desk/rituals/execution.md
      - desk/rituals/testing.md
      - desk/rituals/closeout.md
      notes: Bootstrap complete. Add active task docs under `desk/tasks/` and route them here.
      tags:
      - workspace:desk
- path: desk/contexts/pills.md
  mode: if_missing
  file: templates/contexts/pills.md
- path: desk/rituals/phase.md
  mode: if_missing
  file: templates/rituals/phase.md
- path: desk/rituals/execution.md
  mode: if_missing
  file: templates/rituals/execution.md
- path: desk/rituals/testing.md
  mode: if_missing
  file: templates/rituals/testing.md
- path: desk/rituals/closeout.md
  mode: if_missing
  file: templates/rituals/closeout.md
- path: desk/drawer/README.md
  mode: if_missing
  file: templates/drawer/README.md
- path: desk/atoms/tag-namespaces.yaml
  mode: if_missing
  file: templates/atoms/tag-namespaces.yaml
- path: desk/runtimes/runtime-pi-deepseek-flash.md
  mode: if_missing
  track: false
  document:
    model: RuntimeProfileDoc
    name: runtime-pi-deepseek-flash
    payload:
      id: runtime-pi-deepseek-flash
      title: Pi deepseek-flash isolated reviewer
      status: active
      kind: pi
      binary: pi
      model_flag: --model
      fallback_models_flag: ''
      fallback_models_join: comma
      tools_flag: ''
      tools_join: comma
      system_prompt_flag: --system-prompt
      system_prompt_delivery: inline
      session_flag: ''
      extra_args:
      - --provider
      - deepseek
      - --model
      - deepseek-flash
      - --thinking
      - low
      - --offline
      - --no-session
      - --no-context-files
      - --no-skills
      - --no-extensions
      - --no-prompt-templates
      - --no-tools
      - --print
      unsupported_role_fields: []
      notes: 'Verified cheap profile for ritual-context-review step 3 (D4): offline, no session/context/skills/extensions/prompt-templates/tools.'
      summary: Isolated cheap reviewer profile (pi deepseek-flash) used by `deskops review`.
      tags:
      - system:deskops
- path: desk/lifecycle/type-task_activates.md
  mode: managed
  file: lifecycle/type-task_activates.md
- path: desk/lifecycle/type-task_hands_to_closeout.md
  mode: managed
  file: lifecycle/type-task_hands_to_closeout.md
- path: desk/lifecycle/type-task_completes.md
  mode: managed
  file: lifecycle/type-task_completes.md
- path: desk/lifecycle/execution-task_activates.md
  mode: managed
  file: lifecycle/execution-task_activates.md
- path: desk/lifecycle/testing-task_hands_to_closeout.md
  mode: managed
  file: lifecycle/testing-task_hands_to_closeout.md
- path: desk/lifecycle/closeout-task_completes.md
  mode: managed
  file: lifecycle/closeout-task_completes.md
- path: desk/lifecycle/rule-activation-task-code.md
  mode: managed
  file: rules/rule-activation-task-code.md
- path: desk/lifecycle/rule-activation-task-docs.md
  mode: managed
  file: rules/rule-activation-task-docs.md
- path: desk/lifecycle/rule-activation-task-debug.md
  mode: managed
  file: rules/rule-activation-task-debug.md
- path: desk/lifecycle/rule-activation-task-refactor.md
  mode: managed
  file: rules/rule-activation-task-refactor.md
- path: desk/lifecycle/rule-activation-task-decision.md
  mode: managed
  file: rules/rule-activation-task-decision.md
- path: desk/lifecycle/rule-activation-task-aggregate.md
  mode: managed
  file: rules/rule-activation-task-aggregate.md
- path: desk/lifecycle/rule-activation-task-external.md
  mode: managed
  file: rules/rule-activation-task-external.md
- path: desk/lifecycle/rule-closeout-task-code.md
  mode: managed
  file: rules/rule-closeout-task-code.md
- path: desk/lifecycle/rule-closeout-task-docs.md
  mode: managed
  file: rules/rule-closeout-task-docs.md
- path: desk/lifecycle/rule-closeout-task-debug.md
  mode: managed
  file: rules/rule-closeout-task-debug.md
- path: desk/lifecycle/rule-closeout-task-refactor.md
  mode: managed
  file: rules/rule-closeout-task-refactor.md
- path: desk/lifecycle/rule-closeout-task-decision.md
  mode: managed
  file: rules/rule-closeout-task-decision.md
- path: desk/lifecycle/rule-closeout-task-aggregate.md
  mode: managed
  file: rules/rule-closeout-task-aggregate.md
- path: desk/lifecycle/rule-closeout-task-external.md
  mode: managed
  file: rules/rule-closeout-task-external.md
- path: desk/lifecycle/rule-closeout-alert-implicit-code.md
  mode: managed
  file: rules/rule-closeout-alert-implicit-code.md
- path: desk/lifecycle/rule-closeout-alert-pill-graduation.md
  mode: managed
  file: rules/rule-closeout-alert-pill-graduation.md
include:
- model: RelationTypeDoc
  glob: desk/lifecycle/type-*.md
- model: RelationDoc
  paths:
  - desk/lifecycle/execution-task_activates.md
  - desk/lifecycle/testing-task_hands_to_closeout.md
  - desk/lifecycle/closeout-task_completes.md
- model: RuleDoc
  glob: desk/lifecycle/rule-activation-*.md
- model: RuleDoc
  glob: desk/lifecycle/rule-closeout-*.md
- model: BoardDoc
  paths:
  - desk/tasks/Board.md
- model: RitualDoc
  paths:
  - path: desk/rituals/phase.md
    name: ritual-phase
  - path: desk/rituals/execution.md
    name: ritual-execution
  - path: desk/rituals/testing.md
    name: ritual-testing
  - path: desk/rituals/closeout.md
    name: ritual-closeout
- model: BoardDoc
  glob: desk/tasks/board-*.md
- model: PillDoc
  glob: desk/contexts/pill-*.md
- model: RitualDoc
  glob: desk/rituals/ritual-*.md
- model: AtomDoc
  glob: desk/atoms/atom-*.md
- model: ProtoAtomDoc
  glob: desk/atoms/proto-*.md
- model: RoleDoc
  glob: desk/roles/*.md
- model: RepositoryDoc
  glob: desk/registry/*.md
- model: StepDoc
  glob: desk/steps/*.md
- model: DeskFAQDoc
  glob: desk/faq/*.md

FILE:deskops/data/views/board.md
---
id: board
name: board
nodes: []
relations: []
direction: both
notation: ''
layout: {}
params: []
sections:
- key: board
  select:
    path_glob: desk/tasks/Board.md
  fields:
  - tasks
  - pills
  edges:
  - relation: tasks
    direction: out
    as: tasks
  - relation: pills
    direction: out
    as: pills
  group_by: ''
  group_order: []
  rules: []
  transitions: null
- key: tasks
  select:
    model: TaskDoc
    path_glob: desk/tasks/**/*.md
  fields:
  - id
  - title
  - status
  - current_node
  - task_type
  edges:
  - relation: pills
    direction: out
    as: pills
  - relation: atoms
    direction: out
    as: atoms
  - relation: tasks
    direction: in
    as: boards
  group_by: current_node
  group_order:
  - ritual-execution
  - ritual-testing
  - ritual-closeout
  rules: []
  transitions: null
- key: pills
  select:
    model: PillDoc
  fields:
  - id
  - title
  - what
  - when
  - how_not
  edges: []
  group_by: ''
  group_order: []
  rules: []
  transitions: null
- key: atoms
  select:
    model: AtomDoc
  fields:
  - id
  - title
  - five_wh_one_plus
  - answer
  edges: []
  group_by: ''
  group_order: []
  rules: []
  transitions: null
---

# Board del desk

## Description

Tareas del Board por nodo del ciclo de vida (contrato de docs/deskops-ui.md, vista board). deskops view board la proyecta al contrato.

FILE:deskops/cli/commands/view.py
"""`deskops view`: the read-only views the deskops UI draws (contract: docs/deskops-ui.md).

`board` and `task` are sldb ViewDocs (`deskops/data/views/`) evaluated by
`sldb.api.run_view`; `project` turns that result into the contract. What the ViewDoc model
cannot express yet is added by the CLI from deskops' existing read operations, each named by
its pending sldb hypothesis (CC34 H1-H8):

- H1-H3 `gates`: `DeskopsOperations.show_task` (the transitions leaving the node, whether
  their condition holds, and the task's `on_transition` findings);
- H4 `closeout`: `verify_task_closeout` without writing receipts;
- H5 the lifecycle nodes' `phase`/`purpose` and `next`: the lifecycle spec and
  `next_action_report`;
- H6 the effective (inherited) pills, atoms, validation, done_when and references:
  `doc_access.resolve_task_payload`.

`drawer` and `inbox` read the desk's files (H7, H8, H10: those folders are not tracked in a
desk's store yet), and `agents` is what is not a document (`deskops.runtime.desk_agents`).
graph_ui reads `GET /views/<view>` from `sldb serve` and calls `project` in process.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import shlex
from typing import Any

from deskops.cli.render import render
from deskops.cli.render import render_error

CONTRACT_VERSION = 1
BOARD_REF = Path("desk") / "tasks" / "Board.md"
EXCERPT_LINES = 3
SLDB_VIEWS = ("board", "task")
_TEMPLATE_HINT = re.compile(r"^_.*_$")
_NOTE_STAMP = re.compile(r"^(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})-")


class ViewError(RuntimeError):
    """The view cannot be produced at all (no desk, unknown task)."""


# ---------------------------------------------------------------- sldb
def run_view(root: Path, name: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    """`sldb.api.run_view` of the ViewDoc `name` on the desk's store."""
    from sldb.api import run_view as sldb_run_view

    return sldb_run_view(Path(root) / ".sldb", name, params or {})


def _require_board(root: Path) -> Path:
    board = root / BOARD_REF
    if not board.is_file():
        raise ViewError(f"No desk board at {board}; run 'deskops init' first.")
    return board


def task_params(root: Path, selector: str) -> dict[str, str]:
    """The `task` ViewDoc's params for a task selector (id, unique prefix or file name)."""
    from deskops import doc_access

    root = Path(root).resolve()
    _require_board(root)
    try:
        path = doc_access.resolve_artifact_selector(root, "artifact.task", root / "desk" / "tasks", selector)
    except (FileNotFoundError, ValueError) as exc:
        raise ViewError(f"Task '{selector}' does not resolve: {exc}") from exc
    return {"id": str(doc_access.resolve_task_payload(root, path.stem).get("id") or path.stem)}


def board_view(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    _require_board(root)
    return project("board", run_view(root, "board"), root)


def task_view(root: Path, selector: str) -> dict[str, Any]:
    root = Path(root).resolve()
    return project("task", run_view(root, "task", task_params(root, selector)), root)


# ---------------------------------------------------------------- projection
def project(view: str, result: dict[str, Any], root: Path) -> dict[str, Any]:
    """The contract payload of `view` (`board` or `task`) from its `run_view` result, plus the
    CLI aggregates H1-H6 read from the desk at `root`."""
    if view not in SLDB_VIEWS:
        raise ViewError(f"Unknown view: {view}")
    from deskops.operations import DeskopsOperations

    root = Path(root).resolve()
    projection = _Projection(root, result, DeskopsOperations(root))
    with projection.ops.read_snapshot():
        return projection.board() if view == "board" else projection.task()


def _rows(result: dict[str, Any], key: str) -> list[dict[str, Any]]:
    section = (result.get("sections") or {}).get(key) or {}
    if "groups" in section:
        return [row for group in section["groups"] for row in group["rows"]]
    return list(section.get("rows") or [])


def _error(errors: list[dict[str, str]], reference: str, cause: str, task: str | None = None) -> None:
    item = {"reference": reference, "cause": cause}
    if task:
        item["task"] = task
    if item not in errors:
        errors.append(item)


class _Projection:
    def __init__(self, root: Path, result: dict[str, Any], ops: Any) -> None:
        self.root = root
        self.result = result
        self.ops = ops
        boards = _rows(result, "board")
        if not boards:
            raise ViewError(f"No desk board at {root / BOARD_REF}; run 'deskops init' first.")
        self.board_row = boards[0]
        self.pill_rows = _rows(result, "pills")
        self.atom_rows = _rows(result, "atoms")

    # ------------------------------------------------ lookups over the rows
    @staticmethod
    def _find(rows: list[dict[str, Any]], ref: str) -> dict[str, Any] | None:
        for row in rows:
            if ref in (row["name"], row["path"], str(row["fields"].get("id") or "")):
                return row
        return None

    def _board_pills(self) -> list[str]:
        return [str(p) for p in self.board_row["fields"].get("pills") or []]

    def _board_task_rows(self, errors: list[dict[str, str]]) -> list[dict[str, Any]]:
        """The rows of the tasks the Board lists, in the Board's order (the Board is the truth)."""
        tasks_dir = (self.root / "desk" / "tasks").resolve()
        by_path = {(self.root / row["path"]).resolve(): row for row in _rows(self.result, "tasks")}
        chosen: list[dict[str, Any]] = []
        for ref in self.board_row["fields"].get("tasks") or []:
            path = (self.root / str(ref)).resolve()
            if not path.is_relative_to(tasks_dir) or path.suffix != ".md" or path.name == "Board.md":
                _error(errors, str(ref), "Board reference is outside desk/tasks/ or is not a task file.")
                continue
            row = by_path.get(path)
            if row is None:
                _error(errors, str(ref), "Board reference points to a missing task file.")
                continue
            if any(row is seen for seen in chosen):
                _error(errors, str(ref), "Task listed twice in the Board.")
                continue
            chosen.append(row)
        return chosen

    def _pills(self, refs: list[tuple[str, str]], errors: list[dict[str, str]], *, detail: bool, task: str | None = None) -> list[dict[str, Any]]:
        pills = []
        for pill_id, source in refs:
            row = self._find(self.pill_rows, pill_id)
            if row is None:
                _error(errors, pill_id, f"Pill referenced by the {source} does not resolve to a PillDoc.", task if source == "task" else None)
                continue
            doc = row["fields"]
            item = {"id": pill_id, "title": str(doc.get("title") or ""), "source": source}
            if detail:
                item.update({key: str(doc.get(key) or "") for key in ("what", "when", "how_not")})
            pills.append(item)
        return pills

    def _atoms(self, ids: list[str], errors: list[dict[str, str]], *, detail: bool, task: str | None = None) -> list[dict[str, Any]]:
        atoms = []
        for atom_id in ids:
            row = self._find(self.atom_rows, atom_id)
            if row is None:
                _error(errors, atom_id, "Atom referenced by the task does not resolve to an AtomDoc.", task)
                continue
            doc = row["fields"]
            item = {"id": atom_id, "title": str(doc.get("title") or "")}
            if detail:
                item["question"] = str(doc.get("five_wh_one_plus") or "")
                item["answer"] = str(doc.get("answer") or "")
            atoms.append(item)
        return atoms

    # ------------------------------------------------ CLI aggregates (H1-H6)
    def _effective(self, stem: str, path: str | None = None) -> dict[str, Any]:
        """H6: the task's payload with its inherited fields (`resolve_task_payload`).

        The view row already names the file, so the record is read once per task and shared
        with its gates and closeout reads inside the same read snapshot.
        """
        return self.ops.task_record(stem, path=(self.root / path) if path else None)[2]

    @staticmethod
    def _atom_ids(payload: dict[str, Any]) -> list[str]:
        ids = [str(item) for item in payload.get("effective_atoms") or payload.get("atoms") or []]
        ids += [str(ref) for ref in payload.get("effective_references") or payload.get("references") or [] if str(ref).startswith("atom-")]
        return list(dict.fromkeys(ids))

    def _gates(self, stem: str, task_id: str, node: str, errors: list[dict[str, str]]) -> list[dict[str, Any]]:
        """H1-H3: `show_task`'s gates; no gate out of a non-final node is an error with its cause."""
        from deskops import lifecycle

        task, gates = self.ops.show_task(stem)
        if task is not None and not gates and node and node != lifecycle.COMPLETE:
            try:
                lifecycle.transitions_from(self.root, node, snapshot=self.ops.snapshot)
                cause = f"The desk lifecycle graph declares no transition leaving {node}."
            except Exception as exc:
                cause = f"Lifecycle gates unavailable: {exc}"
            _error(errors, task_id, cause)
        return [dict(gate) for gate in gates]

    def _closeout(self, stem: str, node: str, errors: list[dict[str, str]], path: str | None = None) -> dict[str, Any] | None:
        """H4: `verify_task_closeout` (read only), one evidence entry per gate."""
        try:
            report = self.ops.verify_task_closeout(stem, task_path=(self.root / path) if path else None)
        except Exception as exc:
            _error(errors, stem, f"verify_task_closeout failed: {exc}")
            return None
        at_closeout = node == "ritual-closeout"
        evidence = []
        for name, gate in report.get("gates", {}).items():
            state = "holds" if gate.get("ok") else ("failing" if at_closeout else "pending")
            evidence.append({"gate": name, "state": state, "evidence": list(gate.get("evidence") or []), "findings": list(gate.get("findings") or [])})
        for finding in report.get("findings", []):
            if finding.get("code") == "unknown_closeout_evidence":
                evidence.append({"gate": "unknown", "state": "failing", "evidence": [], "findings": [finding]})
        return {
            "ok": bool(report.get("ok")),
            "declared": list(report.get("declared") or []),
            "found": list(report.get("found") or []),
            "summary": report.get("summary"),
            "implicit_code": bool(report.get("implicit_code")),
            "alerts": list(report.get("alerts") or []),
            "evidence": evidence,
        }

    @staticmethod
    def _lifecycle_nodes() -> list[dict[str, Any]]:
        """H5: the lifecycle nodes with their phase and purpose, in the spec's order."""
        from deskops import lifecycle

        spec = lifecycle.load_lifecycle_spec()
        nodes = []
        for state in spec.states:
            node = str(state.get("current_node") or "")
            if not node or node == lifecycle.COMPLETE:
                continue
            nodes.append({"node": node, "phase": str(state.get("phase") or ""), "purpose": str(state.get("purpose") or "")})
        known = {item["node"] for item in nodes}
        nodes += [{"node": node, "phase": "", "purpose": ""} for node in spec.rituals if node not in known]
        return nodes

    # ------------------------------------------------ the card
    def _card(self, row: dict[str, Any], errors: list[dict[str, str]], *, detail: bool = False) -> tuple[dict[str, Any], dict[str, Any]]:
        fields = row["fields"]
        stem = Path(row["path"]).stem
        payload = self._effective(stem, row["path"])
        task_id = str(fields.get("id") or stem)
        node = str(fields.get("current_node") or "")
        gates = self._gates(stem, task_id, node, errors)
        pill_refs = [(str(p), "task") for p in payload.get("effective_pills") or payload.get("pills") or []]
        pill_refs += [(p, "board") for p in self._board_pills() if p not in {ref for ref, _ in pill_refs}]
        card = {
            "id": task_id,
            "title": str(fields.get("title") or ""),
            "status": str(fields.get("status") or ""),
            "current_node": node,
            "task_type": str(fields.get("task_type") or ""),
            "path": row["path"],
            "gates": gates,
            "gates_holding": sum(1 for gate in gates if gate.get("holds")),
            "gates_total": len(gates),
            "closeout": self._closeout(stem, node, errors, row["path"]),
            "pills": self._pills(pill_refs, errors, detail=detail, task=task_id),
            "atoms": self._atoms(self._atom_ids(payload), errors, detail=detail, task=task_id),
        }
        return card, payload

    # ------------------------------------------------ views
    def board(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        columns = {item["node"]: {**item, "in_lifecycle": True, "count": 0, "tasks": []} for item in self._lifecycle_nodes()}
        for row in self._board_task_rows(errors):
            try:
                card, _ = self._card(row, errors)
            except Exception as exc:
                _error(errors, row["path"], f"Task does not load: {exc}")
                continue
            node = card["current_node"]
            if node not in columns:
                _error(errors, card["id"], f"current_node '{node}' is not a node of the task lifecycle.")
                columns[node] = {"node": node, "phase": "", "purpose": "", "in_lifecycle": False, "count": 0, "tasks": []}
            columns[node]["tasks"].append(card)
            columns[node]["count"] += 1
        cards = [card for column in columns.values() for card in column["tasks"]]
        return {
            "view": "board",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "board": {"path": self.board_row["path"], "pills": self._pills([(p, "board") for p in self._board_pills()], errors, detail=False)},
            "columns": list(columns.values()),
            "counts": {
                "tasks": len(cards),
                "by_node": {node: column["count"] for node, column in columns.items()},
                "gates_holding": sum(card["gates_holding"] for card in cards),
                "gates_total": sum(card["gates_total"] for card in cards),
            },
            "errors": errors,
        }

    def task(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        rows = _rows(self.result, "task")
        if not rows:
            task_id = (self.result.get("params") or {}).get("id")
            raise ViewError(f"Task '{task_id}' does not resolve: it is not tracked in the desk's store.")
        row = rows[0]
        card, payload = self._card(row, errors, detail=True)
        fields = row["fields"]
        try:
            report = self.ops.next_action_report(Path(row["path"]).stem)
            next_info = {
                "phase": report.get("phase", ""),
                "ritual": report.get("ritual", ""),
                "next_actions": list(report.get("next_actions") or []),
                "advance_when": list(report.get("advance_when") or []),
            }
        except Exception as exc:
            next_info = None
            _error(errors, card["id"], f"next_action_report failed: {exc}")
        return {
            "view": "task",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "task": {
                **card,
                "on_board": row["export_id"] in (self.board_row.get("tasks") or []),
                "why": str(fields.get("why") or ""),
                "goal": str(fields.get("goal") or ""),
                "scope": str(fields.get("scope") or ""),
                "implementation_path": str(fields.get("implementation_path") or ""),
                "validation": [str(v) for v in payload.get("effective_validation") or payload.get("validation") or []],
                "done_when": str(payload.get("effective_done_when") or payload.get("done_when") or ""),
                "references": [str(r) for r in payload.get("effective_references") or payload.get("references") or []],
                "files": [str(f) for f in fields.get("files") or []],
                "depends_on": [str(d) for d in fields.get("depends_on") or []],
                "inherits_from": [str(i) for i in fields.get("inherits_from") or []],
                "from_drawer": str(fields.get("from_drawer") or ""),
                "history": [str(h) for h in fields.get("history") or []],
            },
            "next": next_info,
            # The ETag of the ViewDoc's result (GD25): the advance guard of graph_ui.
            "revision": self.result["revision"],
            "errors": errors,
        }


# ---------------------------------------------------------------- drawer and inbox (H10: read from disk)
def _rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return str(path)


def drawer_view(root: Path) -> dict[str, Any]:
    from deskops import doc_access
    from deskops.models import TaskDoc
    from deskops.operations import DeskopsOperations

    root = Path(root).resolve()
    _require_board(root)
    ops = DeskopsOperations(root)
    errors: list[dict[str, str]] = []
    drawer_dir = root / "desk" / "drawer" / "tasks"
    index_files = ops.drawer.DRAWER_INDEX_FILES
    entries = []
    files = sorted(p for p in drawer_dir.glob("*.md") if p.name not in index_files) if drawer_dir.is_dir() else []
    for path in files:
        rel = _rel(root, path)
        try:
            text = ops.drawer._read_markdown(path)
        except Exception as exc:
            _error(errors, rel, f"Drawer file does not parse: {exc}")
            continue
        try:
            doc = doc_access.read_doc(path, TaskDoc)
        except Exception as exc:
            doc = {}
            _error(errors, rel, f"Drawer file is not a valid TaskDoc: {exc}")
        lines = [
            line.strip()
            for line in text["body"].splitlines()
            if line.strip() and not line.lstrip().startswith("#") and not _TEMPLATE_HINT.match(line.strip())
        ]
        entries.append(
            {
                "id": str(doc.get("id") or path.stem),
                "markdown": path.read_text(encoding="utf-8"),
                "title": text["title"],
                "status": str(doc["status"]) if doc.get("status") else None,
                "excerpt": lines[:EXCERPT_LINES],
                "path": rel,
                "command": "deskops add task --root . --from-drawer " + shlex.quote(rel) + " --title " + shlex.quote(text["title"]),
            }
        )
    return {"view": "drawer", "contract": CONTRACT_VERSION, "root": str(root), "tasks": entries, "count": len(entries), "errors": errors}


def inbox_view(root: Path) -> dict[str, Any]:
    from deskops import doc_access
    from deskops.cli.commands.message import MessageCLI
    from deskops.models import InboxNoteDoc

    root = Path(root).resolve()
    _require_board(root)
    errors: list[dict[str, str]] = []
    reader = MessageCLI()
    notes = []
    for path in reader._iter_notes(root / "desk"):
        rel = _rel(root, path)
        try:
            detail = reader._note_detail(path)
        except Exception as exc:
            _error(errors, rel, f"Inbox note does not parse: {exc}")
            continue
        try:
            body = str(doc_access.read_doc(path, InboxNoteDoc).get("body") or "")
        except Exception as exc:
            body = str(detail.get("body") or "")
            _error(errors, rel, f"Inbox note is not a valid InboxNoteDoc; body shown raw: {exc}")
        match = _NOTE_STAMP.match(path.name)
        date = "{}-{}-{}T{}:{}:{}".format(*match.groups()) if match else None
        if date is None:
            _error(errors, rel, "Inbox note filename carries no YYYYMMDD-HHMMSS stamp.")
        status = str(detail.get("status") or "")
        notes.append(
            {
                "id": path.stem,
                "path": rel,
                "kind": str(detail.get("kind") or ""),
                "title": str(detail.get("title") or ""),
                "sender": str(detail.get("sender_project") or ""),
                "target": str(detail.get("target_project") or ""),
                "date": date,
                "status": status,
                "acknowledged": status == "closed",
                "acknowledged_by": detail.get("acknowledged_by"),
                "acknowledged_at": detail.get("acknowledged_at"),
                "body": body,
                # The guard of the inbox actions: sha256 of the note's bytes (H8).
                "revision": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    return {
        "view": "inbox",
        "contract": CONTRACT_VERSION,
        "root": str(root),
        "notes": notes,
        "count": len(notes),
        "open": sum(1 for note in notes if not note["acknowledged"]),
        "errors": errors,
    }


# ---------------------------------------------------------------- text rendering
def _errors_text(view: dict[str, Any]) -> list[str]:
    return [f"! {item['reference']}: {item['cause']}" for item in view.get("errors") or []]


def render_text(view: dict[str, Any]) -> str:
    kind = view.get("view")
    lines: list[str] = []
    if kind == "board":
        for column in view["columns"]:
            lines.append(f"{column['node']} ({column['count']})")
            for card in column["tasks"]:
                lines.append(f"  {card['id']} [{card['status']}] gates {card['gates_holding']}/{card['gates_total']} - {card['title']}")
    elif kind == "task":
        task = view["task"]
        lines += [f"{task['id']} [{task['status']}] {task['current_node']}", task["title"], f"revision {view['revision']}"]
        for gate in task["gates"]:
            lines.append(f"  gate {gate['relation_type']} -> {gate['target']}: {'holds' if gate['holds'] else 'pending'} ({gate['condition'] or 'no condition'})")
        for item in (task.get("closeout") or {}).get("evidence", []):
            lines.append(f"  evidence {item['gate']}: {item['state']}")
    elif kind == "drawer":
        for entry in view["tasks"]:
            lines.append(f"{entry['id']} [{entry['status'] or '-'}] {entry['title']}")
    elif kind == "inbox":
        for note in view["notes"]:
            lines.append(f"{note['id']} [{'ack' if note['acknowledged'] else 'open'}] {note['sender']} -> {note['target']}: {note['title']}")
    elif kind == "agents":
        if view["workers"] is None:
            lines.append(f"workers unavailable: {view['workers_error']}")
        else:
            lines.append(f"live workers: {view['live_workers']}")
            for worker in view["workers"]:
                lines.append(f"  {worker.get('pane')} | {worker.get('kind')} | {worker.get('status')} | {worker.get('cwd') or ''}")
        lines.append(f"runs (latest {len(view['runs'])} of {view['runs_total']}):")
        for run in view["runs"]:
            lines.append(f"  {run['task_id']} | {run['mode'] or '-'} | {run['run_dir'] or '-'}")
    return "\n".join([*lines, *_errors_text(view)])


class ViewCLI:
    """Read-only views of a desk for the deskops UI (contract: docs/deskops-ui.md)."""

    def run(self, args: Any) -> int:
        from sldb.core.exceptions import SLDBError

        fmt = getattr(args, "format", "text")
        root = Path(args.root).resolve()
        try:
            command = args.view_command
            if command == "board":
                payload = board_view(root)
            elif command == "task":
                payload = task_view(root, args.task_id)
            elif command == "drawer":
                payload = drawer_view(root)
            elif command == "inbox":
                payload = inbox_view(root)
            elif command == "agents":
                from deskops.runtime.desk_agents import agents_view

                payload = agents_view(root, runs_limit=getattr(args, "runs", 20), herdr=getattr(args, "herdr", "herdr"))
            else:
                return render_error(f"Unknown view: {command}", fmt, type_name="DomainError")
        except (ViewError, SLDBError, FileNotFoundError, ValueError) as exc:
            return render_error(str(exc), fmt, type_name=type(exc).__name__, text=f"Error: {exc}")
        return render(payload, fmt, render_text)

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

    Canonical surface is `deskops message {send|list|read|ack}`. The legacy
    `deskops inbox` flag grammar routes through `_run_legacy` for backward
    compatibility.
    """

    def run(self, args: Any) -> int:
        try:
            if getattr(args, "message_command", None) is not None:
                return self._run_message_command(args)
            return self._run_legacy(args)
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

    def _run_legacy(self, args: Any) -> int:
        if getattr(args, "list", False):
            return self._list_notes(args)
        if getattr(args, "show", None):
            return self._show_note(args)
        if getattr(args, "ack", None):
            return self._ack_note(args)
        if not getattr(args, "message", None):
            return render_error(
                "Provide a message or use send/list/read/ack.",
                getattr(args, "format", "text"),
                type_name="DomainError",
            )
        return self._deliver_note(args)

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

FILE:deskops/cli/commands/promote.py
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from deskops.doc_access import template_placeholders
from deskops.models import TaskDoc
from deskops.services.drawer import DrawerService


_TASK_SECTION_FIELDS: tuple[tuple[str, str], ...] = (
    ("why", "Rationale"),
    ("goal", "Goal"),
    ("scope", "Scope"),
    ("implementation_path", "Implementation Path"),
    ("validation", "Validation"),
    ("done_when", "Done When"),
)

_TASK_HEADING_TO_FIELD = {heading.lower(): field for field, heading in _TASK_SECTION_FIELDS}

def _task_section_placeholder(heading: str) -> str | None:
    """The TaskDoc template's placeholder paragraph under ``heading``: the same source that
    ``deskops edit`` normalizes with, never a list kept by hand."""
    field = _TASK_HEADING_TO_FIELD.get(heading.lower())
    return template_placeholders(TaskDoc).get(field) if field else None


def _strip_markdown_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    try:
        _, rest = text.split("---\n", 1)
        _frontmatter, body = rest.split("\n---\n", 1)
    except ValueError:
        return text
    return body


def _parse_task_sections(text: str) -> dict[str, Any]:
    """Read task-shaped headings from a free-form inbox note.

    Inbox notes are not TaskDocs: they have no frontmatter contract and no
    model that can extract them. This private helper only recovers sections
    that happen to look like a task so the drawer candidate preserves them.
    TaskDoc reads never use it; they go through sldb's extractor.
    """
    body = _strip_markdown_frontmatter(text)
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]

    preamble: list[str] = []
    sections: dict[str, str] = {}
    active_heading: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer, active_heading
        if active_heading is None:
            return
        heading = active_heading
        active_heading = None
        field = _TASK_HEADING_TO_FIELD[heading.lower()]
        if field in sections:
            buffer = []
            return
        content = "\n".join(buffer).strip()
        placeholder = _task_section_placeholder(heading)
        if placeholder:
            content_lines = content.splitlines()
            while content_lines and not content_lines[0].strip():
                content_lines.pop(0)
            if content_lines and content_lines[0].strip() == placeholder:
                content_lines.pop(0)
                while content_lines and not content_lines[0].strip():
                    content_lines.pop(0)
            content = "\n".join(content_lines).strip()
        sections[field] = content
        buffer = []

    for line in lines:
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            heading = match.group(1).strip()
            if heading.lower() in _TASK_HEADING_TO_FIELD:
                flush()
                active_heading = heading
                continue
        if active_heading is None:
            preamble.append(line)
        else:
            buffer.append(line)
    flush()

    cleaned_preamble = "\n".join(preamble).strip()
    return {
        "fields": sections,
        "preamble": cleaned_preamble,
        "has_task_sections": bool(sections),
    }


class PromoteCLI:
    """Promote inbox notes into loose drawer candidates.

    There is deliberately no drawer -> active task promotion. The drawer holds
    disorganized, loosely shaped material; an active task is a fully authored
    TaskDoc routed on the board and walked through the desk's lifecycle graph.
    Converting one into the other mechanically meant filling every required
    field with generic placeholders, producing a task that looked structured
    but was not. A drawer item becomes active work only when someone authors
    the task explicitly with `deskops add task`.
    """

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if args.promote_command == "inbox-to-drawer-task":
            result = DrawerService(root).promote_inbox_to_drawer_task(
                args.selector,
                args.title,
                parse_sections=_parse_task_sections,
            )
            for message in result.messages:
                print(message)
            return result.exit_code
        return 1

FILE:deskops/cli/commands/drawer.py
from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.services.drawer import DrawerService


class DrawerCLI:
    """Drawer entry maintenance."""

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if args.drawer_command == "remove":
            result = DrawerService(root).remove_entry(args.selector, force=args.force)
            for message in result.messages:
                print(message)
            return result.exit_code
        return 1

FILE:tests/test_view.py
"""deskops view: board and task are sldb ViewDocs evaluated by run_view (CC34), drawer, inbox
and agents read what is not in the store; all over real temporary desks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from sldb import api

from deskops.cli.commands.view import ViewError
from deskops.cli.commands.view import board_view
from deskops.cli.commands.view import drawer_view
from deskops.cli.commands.view import inbox_view
from deskops.cli.commands.view import project
from deskops.cli.commands.view import run_view
from deskops.cli.commands.view import task_view
from deskops.cli.main import main
from deskops.operations import DeskopsOperations
from deskops.runtime.desk_agents import agents_view
from tests.view_desk import VIEWS_DIR
from tests.view_desk import build_view_desk

REPO = Path(__file__).resolve().parents[1]


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.relative_to(root).parts):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def _cli_json(capsys: pytest.CaptureFixture[str], *argv: str) -> dict:
    capsys.readouterr()
    assert main(list(argv)) == 0
    return json.loads(capsys.readouterr().out)


@pytest.fixture
def desk(lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    ids = build_view_desk(lifecycle_desk, monkeypatch)
    return {"root": lifecycle_desk, "ops": DeskopsOperations(lifecycle_desk), **ids}


def test_the_seed_viewdocs_are_board_and_task_and_list_in_the_store(desk: dict) -> None:
    assert sorted(p.stem for p in VIEWS_DIR.glob("*.md")) == ["board", "task"]
    listed = {view["name"]: view for view in api.list_views(desk["root"] / ".sldb")}
    assert listed["board"]["sections"] == ["board", "tasks", "pills", "atoms"]
    assert listed["task"]["sections"] == ["board", "task", "pills", "atoms"]
    assert [param["name"] for param in listed["task"]["params"]] == ["id"]


def test_board_groups_by_current_node_in_spec_order_and_gates_are_show_task(desk: dict) -> None:
    view = board_view(desk["root"])
    assert [column["node"] for column in view["columns"]] == ["ritual-execution", "ritual-testing", "ritual-closeout"]
    by_node = {column["node"]: [card["id"] for card in column["tasks"]] for column in view["columns"]}
    assert by_node == {"ritual-execution": [desk["execution"]], "ritual-testing": [desk["testing"]], "ritual-closeout": [desk["closeout"]]}
    groups = run_view(desk["root"], "board")["sections"]["tasks"]["groups"]
    assert [(group["value"], [row["name"] for row in group["rows"]]) for group in groups] == list(by_node.items())
    for column in view["columns"]:
        for card in column["tasks"]:
            _, gates = desk["ops"].show_task(card["id"])
            assert card["gates"] == gates and card["gates_total"] == len(gates)
            report = desk["ops"].verify_task_closeout(card["id"])
            assert card["closeout"]["declared"] == report["declared"] and card["closeout"]["found"] == report["found"]


def test_unresolvable_pill_and_atom_go_to_errors_not_to_the_card(desk: dict) -> None:
    view = board_view(desk["root"])
    cards = {card["id"]: card for column in view["columns"] for card in column["tasks"]}
    first, second = cards[desk["execution"]], cards[desk["testing"]]
    assert [(p["id"], p["title"]) for p in first["pills"]] == [(desk["pill"], "Guardrail: view pill")]
    assert [a["id"] for a in first["atoms"]] == [desk["atom"]]
    assert second["pills"] == [] and second["atoms"] == []
    references = {item["reference"]: item.get("task") for item in view["errors"]}
    assert references["pill-does-not-exist"] == desk["testing"]
    assert references["atom-does-not-exist"] == desk["testing"]


def test_project_of_the_run_view_result_is_the_cli_payload(desk: dict, capsys: pytest.CaptureFixture[str]) -> None:
    """c6: what graph_ui gets from GET /views/<view> (run_view) projects to `deskops view`."""
    root = desk["root"]
    assert project("board", run_view(root, "board"), root) == _cli_json(capsys, "view", "board", "--root", str(root), "--format", "json")
    task = _cli_json(capsys, "view", "task", desk["execution"], "--root", str(root), "--format", "json")
    assert project("task", run_view(root, "task", {"id": desk["execution"]}), root) == task


def test_task_revision_is_the_etag_of_the_task_view(desk: dict) -> None:
    root = desk["root"]
    view = task_view(root, desk["execution"])
    task = view["task"]
    assert task["goal"] == "goal of View golden execution" and task["on_board"] is True
    assert task["pills"][0]["how_not"] == "how not text" and task["atoms"][0]["answer"] == "the answer"
    assert view["next"]["next_actions"] and view["next"]["advance_when"]
    assert view["revision"] == run_view(root, "task", {"id": desk["execution"]})["revision"]
    assert main(["edit", "task", desk["execution"], "goal", "a new goal", "--root", str(root)]) == 0
    moved = task_view(root, desk["execution"])
    assert moved["task"]["goal"] == "a new goal" and moved["revision"] != view["revision"]


def test_unknown_task_raises(desk: dict) -> None:
    with pytest.raises(ViewError):
        task_view(desk["root"], "task-nope")


def test_a_desk_without_board_is_a_view_error(tmp_path: Path) -> None:
    with pytest.raises(ViewError, match="No desk board"):
        board_view(tmp_path)


def test_drawer_inbox_and_agents_read_what_is_on_disk(desk: dict, capsys: pytest.CaptureFixture[str]) -> None:
    root = desk["root"]
    runs = root / "runs/subagents/index.jsonl"
    runs.parent.mkdir(parents=True)
    runs.write_text(
        json.dumps({"task_id": desk["execution"], "run_id": None, "run_dir": None, "mode": "manual", "commit": None}) + "\n"
        + json.dumps({"task_id": "task-gone", "run_id": "r1", "run_dir": "runs/subagents/x", "commit": None}) + "\n",
        encoding="utf-8",
    )
    drawer = drawer_view(root)
    [entry] = drawer["tasks"]
    assert entry["title"] == "Deferred idea" and entry["status"] == "deferred"
    assert entry["markdown"] == (root / entry["path"]).read_text(encoding="utf-8")
    assert entry["command"].startswith(f"deskops add task --root . --from-drawer {entry['path']} --title ")

    inbox = inbox_view(root)
    listed = _cli_json(capsys, "message", "list", "--root", str(root), "--format", "json")["notes"]
    assert [note["id"] for note in inbox["notes"]] == [note["id"] for note in listed]
    [note] = inbox["notes"]
    assert note["title"] == "Open question" and note["body"] == "Question body" and note["date"] == "2026-11-04T10:16:00"
    assert note["revision"] == hashlib.sha256((root / note["path"]).read_bytes()).hexdigest()

    agents = agents_view(root, workers_provider=lambda: [{"pane_id": "w1:p1", "agent": "pi", "agent_status": "idle", "cwd": str(root)}])
    assert agents["live_workers"] == 1 and agents["workers"][0]["pane"] == "w1:p1"
    assert [run["task_id"] for run in agents["runs"]] == ["task-gone", desk["execution"]]
    assert [run["on_board"] for run in agents["runs"]] == [False, True]


def test_agents_without_herdr_reports_the_cause(desk: dict) -> None:
    def broken() -> list:
        raise RuntimeError("herdr not running")

    agents = agents_view(desk["root"], workers_provider=broken)
    assert agents["workers"] is None and "herdr not running" in agents["workers_error"]
    assert agents["errors"][0]["reference"] == "runtime workers"


def test_no_view_writes(desk: dict) -> None:
    root = desk["root"]
    board_view(root)  # the first read may build the store's caches
    before = _tree_hash(root)
    board_view(root)
    task_view(root, desk["execution"])
    drawer_view(root)
    inbox_view(root)
    agents_view(root, workers_provider=lambda: [])
    assert _tree_hash(root) == before


def test_view_text_lists_the_board(desk: dict, capsys: pytest.CaptureFixture[str]) -> None:
    capsys.readouterr()
    assert main(["view", "board", "--root", str(desk["root"])]) == 0
    assert desk["execution"] in capsys.readouterr().out


def test_a_store_without_the_viewdocs_is_an_error_envelope(lifecycle_desk: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """A store where sldb finds no ViewDoc `board` (neither its own nor a linked one) is sldb's
    error in the envelope, not an invented view. Since sldb resolves a ViewDoc of a linked store
    (H9, sldb 04a0e94e), whether a test desk finds the package's views depends on whether the
    deskops repo's own store was built (CI builds it first), so the missing view is simulated at
    sldb's API instead of relied on."""
    from sldb.core.exceptions import SLDBDocumentTargetError

    def no_view(store, name, params=None):
        raise SLDBDocumentTargetError(f"Unknown view: {name}")

    monkeypatch.setattr(api, "run_view", no_view)
    capsys.readouterr()
    assert main(["view", "board", "--root", str(lifecycle_desk), "--format", "json"]) == 1
    error = json.loads(capsys.readouterr().out)["error"]
    assert error["message"] == "Unknown view: board"


def test_view_is_registered_read_only() -> None:
    from deskops.cli.registry import command_registry

    view_commands = [command for command in command_registry() if command.path[0] == "view"]
    assert {command.path for command in view_commands} == {
        ("view",), ("view", "board"), ("view", "task"), ("view", "drawer"), ("view", "inbox"), ("view", "agents")
    }
    assert not any(command.mutates for command in view_commands)


def test_the_old_view_service_is_gone() -> None:
    hits = [
        f"{path.relative_to(REPO)}"
        for path in (REPO / "deskops").rglob("*.py")
        if "desk_view" in path.read_text(encoding="utf-8") or "DeskView" in path.read_text(encoding="utf-8")
    ]
    assert hits == []


def test_a_gate_read_failure_is_the_card_error(desk: dict, monkeypatch: pytest.MonkeyPatch) -> None:
    """`_gates` turns a failure to read the transitions into the card's error, not a crash."""
    from deskops import lifecycle

    def no_graph(*args: object, **kwargs: object) -> list:
        raise RuntimeError("lifecycle graph unavailable")

    monkeypatch.setattr(lifecycle, "transitions_from", no_graph)
    view = board_view(desk["root"])
    errors = [item for item in view["errors"] if item["cause"].startswith("Lifecycle gates unavailable: ")]
    assert errors and errors[0]["cause"] == "Lifecycle gates unavailable: lifecycle graph unavailable"


def test_a_closeout_read_failure_is_the_card_error(desk: dict, monkeypatch: pytest.MonkeyPatch) -> None:
    """`_closeout` records a failed read-only verify instead of dropping the card."""
    def broken(self: DeskopsOperations, task_selector: str, **kwargs: object) -> dict:
        raise RuntimeError("closeout unavailable")

    monkeypatch.setattr(DeskopsOperations, "verify_task_closeout", broken)
    view = board_view(desk["root"])
    errors = [item for item in view["errors"] if item["cause"] == "verify_task_closeout failed: closeout unavailable"]
    assert errors
    assert all(card["closeout"] is None for column in view["columns"] for card in column["tasks"])

FILE:tests/test_message_delivery.py
"""Message delivery must not depend on the target desk registering the sender.

These are the three failures reported on 2026-10-18:

* a target without ``project_identity`` refused the note,
* a sender was resolved against the target's registry (so a repo that only
  registered itself made every foreign sender unresolvable),
* ``ack`` stopped finding the repo itself once its registry registered some
  other repo.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.models import InboxNoteDoc
from deskops.models import RepositoryDoc
from sldb.runtime.validation import render_model_markdown


def _cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv], cwd=root, capture_output=True, text=True
    )


def _init_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    result = _cli(path, "init", str(path))
    assert result.returncode == 0, result.stderr or result.stdout
    return path


def _register(repo: Path, repo_id: str, repo_path: str) -> None:
    registry_dir = repo / "desk" / "registry"
    registry_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": repo_id,
        "name": repo_id,
        "path": repo_path,
        "status": "active",
        "description": f"Repository for {repo_id}.",
        "tags": [],
    }
    (registry_dir / f"repo-{repo_id}.md").write_text(
        render_model_markdown(RepositoryDoc, payload) + "\n", encoding="utf-8"
    )


def _store_snapshot(repo: Path) -> dict[str, bytes]:
    store = repo / ".sldb"
    return {
        path.relative_to(store).as_posix(): path.read_bytes()
        for path in sorted(store.rglob("*"))
        if path.is_file()
    }


def _write_note(repo: Path, stem: str, *, target_project: str) -> Path:
    inbox = repo / "desk" / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": "suggestion",
        "sender_project": "sender-repo",
        "target_project": target_project,
        "created_at": "2026-01-01T00:00:00",
        "status": "open",
        "title": "Ack me",
        "body": "Please acknowledge this note.",
    }
    note = inbox / f"{stem}.md"
    note.write_text(render_model_markdown(InboxNoteDoc, payload) + "\n", encoding="utf-8")
    return note


def test_send_to_target_without_project_identity_uses_directory_name(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender-repo")
    target = _init_repo(tmp_path / "TraderBot")
    (target / "desk" / "config.json").write_text("{}\n", encoding="utf-8")

    result = _cli(
        sender,
        "message",
        "send",
        "A note for an unconfigured desk.",
        "--title",
        "No identity",
        "--root",
        str(target),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["sender_project"] == "sender-repo"
    assert payload["target_project"] == "TraderBot"
    assert "no project_identity" in result.stderr
    assert len(list((target / "desk" / "inbox").glob("*.md"))) == 1


def test_send_resolves_sender_from_sender_repo_not_target_registry(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender-repo")
    target = _init_repo(tmp_path / "target-repo")
    # The target's local registry knows only itself, exactly like the reported case.
    _register(target, "target-repo", str(target))

    without_from = _cli(
        sender,
        "message",
        "send",
        "Sender comes from the sending repo.",
        "--title",
        "No sender override",
        "--root",
        str(target),
        "--format",
        "json",
    )
    with_from = _cli(
        sender,
        "message",
        "send",
        "Sender comes from the sending repo.",
        "--title",
        "Explicit sender",
        "--from",
        "sender-repo",
        "--root",
        str(target),
        "--format",
        "json",
    )

    assert without_from.returncode == 0, without_from.stderr or without_from.stdout
    assert with_from.returncode == 0, with_from.stderr or with_from.stdout
    assert json.loads(without_from.stdout)["sender_project"] == "sender-repo"
    assert json.loads(with_from.stdout)["sender_project"] == "sender-repo"
    assert json.loads(without_from.stdout)["target_project"] == "target-repo"


def test_send_with_root_tracks_only_in_target_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    sender = _init_repo(tmp_path / "repo-a")
    target = _init_repo(tmp_path / "repo-b")
    before = _store_snapshot(sender)

    result = _cli(
        sender,
        "message",
        "send",
        "A note addressed through --root.",
        "--title",
        "To a root",
        "--root",
        str(target),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["verified"] is True
    assert _store_snapshot(sender) == before
    note = next((target / "desk" / "inbox").glob("*.md"))
    tracked = doc_status(target / ".sldb", note.stem)
    assert tracked.status == "ok"
    assert tracked.path == f"desk/inbox/{note.name}"
    assert not Path(tracked.path).is_absolute()
    assert doc_status(sender / ".sldb", note.stem).status == "missing"


def test_send_to_registered_repo_tracks_only_in_target_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    sender = _init_repo(tmp_path / "repo-a")
    target = _init_repo(tmp_path / "repo-b")
    _register(sender, "repo-b", str(target))
    before = _store_snapshot(sender)

    result = _cli(
        sender,
        "message",
        "send",
        "A note addressed through --to.",
        "--title",
        "To a registered repo",
        "--to",
        "repo-b",
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["verified"] is True
    assert _store_snapshot(sender) == before
    note = next((target / "desk" / "inbox").glob("*.md"))
    tracked = doc_status(target / ".sldb", note.stem)
    assert tracked.status == "ok"
    assert tracked.path == f"desk/inbox/{note.name}"
    assert not Path(tracked.path).is_absolute()
    assert doc_status(sender / ".sldb", note.stem).status == "missing"


def test_legacy_inbox_repo_tracks_only_in_target_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    sender = _init_repo(tmp_path / "repo-a")
    target = _init_repo(tmp_path / "repo-b")
    _register(sender, "repo-b", str(target))
    before = _store_snapshot(sender)

    result = _cli(
        sender,
        "inbox",
        "A note addressed through the deprecated alias.",
        "--title",
        "Legacy repo alias",
        "--repo",
        "repo-b",
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["verified"] is True
    assert _store_snapshot(sender) == before
    note = next((target / "desk" / "inbox").glob("*.md"))
    tracked = doc_status(target / ".sldb", note.stem)
    assert tracked.status == "ok"
    assert tracked.path == f"desk/inbox/{note.name}"
    assert not Path(tracked.path).is_absolute()
    assert doc_status(sender / ".sldb", note.stem).status == "missing"


def test_ack_falls_back_to_config_when_registry_lacks_itself(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "graph-repo")
    # Registering somebody else used to hide the repo's own identity from ack.
    _register(repo, "graph_ui", str(tmp_path / "elsewhere"))
    note = _write_note(repo, "20260101-000000-suggestion-ackme", target_project="graph-repo")

    result = _cli(
        repo,
        "message",
        "ack",
        note.stem,
        "--root",
        str(repo),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["status"] == "closed"
    assert payload["acknowledged_by"] == "graph-repo"
    assert payload["target_project"] == "graph-repo"

FILE:tests/test_inbox_promote_cli_gaps.py
"""Regression tests for the CLI gaps reported in desk/inbox/.

Covers the inbox note:
  - 20260827-160657 "CLI gaps: inbox --root, promote deja notas tracked
    huerfanas, sin listado de drawer"

Drawer -> active task promotion was removed rather than repaired: the drawer
is loose by design and an active task is a compiled, fully authored bundle,
so a drawer item becomes a task only through `deskops add task`.
"""

from __future__ import annotations

from pathlib import Path

from deskops.cli.main import main


def _install_desk(tmp_path: Path) -> None:
    assert main(["desk", "install", str(tmp_path)]) == 0


def _write_note(tmp_path: Path, stem: str, body: str) -> Path:
    note = tmp_path / "desk" / "inbox" / f"{stem}.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text(
        "---\nkind: suggestion\nstatus: open\n---\n\n" + body,
        encoding="utf-8",
    )
    return note


# ── inbox --root ──────────────────────────────────────────────────────────────


def test_inbox_accepts_root_like_every_other_subcommand(tmp_path: Path, capsys) -> None:
    """The epilog documented `deskops inbox --list --root .` while the parser
    only accepted --desk-root, so the documented invocation failed outright."""
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-hello", "# Hello\n\nBody.\n")
    capsys.readouterr()

    assert main(["inbox", "--list", "--root", str(tmp_path)]) == 0

    assert "Hello" in capsys.readouterr().out


def test_inbox_desk_root_wins_over_root(tmp_path: Path, capsys) -> None:
    """--desk-root is the more specific flag and must keep precedence."""
    _install_desk(tmp_path)
    other = tmp_path / "other"
    other.mkdir()
    _install_desk(other)
    _write_note(tmp_path, "20260101-000000-suggestion-in-root", "# InRoot\n\nBody.\n")
    _write_note(other, "20260101-000001-suggestion-in-desk-root", "# InDeskRoot\n\nBody.\n")
    capsys.readouterr()

    assert main(["inbox", "--list", "--root", str(tmp_path), "--desk-root", str(other / "desk")]) == 0

    out = capsys.readouterr().out
    assert "InDeskRoot" in out
    assert "InRoot" not in out


# ── inbox -> drawer stays loose ──────────────────────────────────────────────


def test_inbox_to_drawer_keeps_the_note_body_loose(tmp_path: Path) -> None:
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-plain", "# Plain\n\nRaw dump of context.\n")

    assert main(["promote", "inbox-to-drawer-task", "plain", "--root", str(tmp_path)]) == 0

    text = (tmp_path / "desk" / "drawer" / "tasks" / "task-plain.md").read_text(encoding="utf-8")
    assert "Raw dump of context." in text
    assert not (tmp_path / "desk" / "tasks" / "task-plain.md").exists()


def test_inbox_to_drawer_rejects_task_structure_flags(tmp_path: Path) -> None:
    """Goal/scope/validation are authored when a task is created, not injected
    while a note is still a loose drawer candidate."""
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-shaped", "# Shaped\n\nBody.\n")

    assert main(["promote", "inbox-to-drawer-task", "shaped", "--root", str(tmp_path), "--goal", "X"]) != 0


def test_drawer_to_active_task_promotion_no_longer_exists(tmp_path: Path) -> None:
    """Drawer content is loose; a task is a compiled bundle. The old direct
    promotion filled every required field with generic placeholders, so it was
    removed: a drawer item becomes a task only via `deskops add task`."""
    _install_desk(tmp_path)
    drawer = tmp_path / "desk" / "drawer" / "tasks"
    drawer.mkdir(parents=True, exist_ok=True)
    (drawer / "task-loose.md").write_text("# Loose\n\nID: task-loose\nStatus: deferred\n", encoding="utf-8")

    assert main(["promote", "drawer-task-to-active-task", "loose", "--root", str(tmp_path)]) != 0
    assert not (tmp_path / "desk" / "tasks" / "task-loose.md").exists()


def test_list_tasks_does_not_surface_drawer_items(tmp_path: Path, capsys) -> None:
    """An available task is board-routed work, not a drawer item."""
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-candidate", "# Candidate\n\nBody.\n")
    assert main(["promote", "inbox-to-drawer-task", "candidate", "--root", str(tmp_path)]) == 0
    capsys.readouterr()

    assert main(["list", "tasks", "--root", str(tmp_path)]) == 0

    assert "task-candidate" not in capsys.readouterr().out


# ── promote untracks the note ────────────────────────────────────────────────


def test_promote_untracks_the_note_from_the_store(tmp_path: Path) -> None:
    """Regression: promote unlinked the inbox file but left the tracked
    InboxNoteDoc entry behind, so `deskops status` reported it as an invalid
    missing document forever after."""
    from sldb.cli import main as sldb_main

    _install_desk(tmp_path)
    note = _write_note(tmp_path, "20260101-000000-suggestion-tracked", "# Tracked\n\nBody.\n")

    assert sldb_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert sldb_main(["models", "add", "deskops.models:InboxNoteDoc", "--store", str(tmp_path / ".sldb")]) == 0
    assert sldb_main([
        "docs", "track", str(note), "--model", "InboxNoteDoc",
        "--name", note.stem, "--store", str(tmp_path / ".sldb"), "--force",
    ]) == 0
    assert _tracked_names(tmp_path) == [note.stem]

    assert main(["promote", "inbox-to-drawer-task", "tracked", "--root", str(tmp_path)]) == 0

    assert not note.exists()
    assert _tracked_names(tmp_path) == []


def _tracked_names(tmp_path: Path) -> list[str]:
    from sldb.store.io import load_documents_index, load_models_index, load_store_index

    names: list[str] = []
    for entry in load_store_index(tmp_path / ".sldb").models:
        models_idx = load_models_index(tmp_path / entry.models_index)
        names.extend(d.name for d in load_documents_index(tmp_path / models_idx.documents_index).documents)
    return sorted(names)


def test_promote_still_succeeds_without_a_store(tmp_path: Path) -> None:
    """A desk with no .sldb must still promote; untracking is best effort."""
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-nostore", "# NoStore\n\nBody.\n")

    assert main(["promote", "inbox-to-drawer-task", "nostore", "--root", str(tmp_path)]) == 0

    assert (tmp_path / "desk" / "drawer" / "tasks" / "task-nostore.md").exists()


# ── add task --from-drawer ───────────────────────────────────────────────────


def _drawer_file(tmp_path: Path, relative: str, body: str = "# Loose idea\n\nUnstructured notes.\n") -> Path:
    path = tmp_path / "desk" / "drawer" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def _authored_task_argv(tmp_path: Path, *extra: str) -> list[str]:
    # --validation takes nargs="+", so it has to stay last.
    return [
        "add", "task", "--root", str(tmp_path),
        "--title", "Authored From Drawer", "--task-type", "task.docs",
        "--goal", "G.", "--scope", "S.", "--implementation-path", "I.", "--done-when", "D.",
        *extra,
        "--validation", "pytest",
    ]


def _task_doc(tmp_path: Path, task_id: str) -> dict:
    from sldb.runtime.validation import extract_model_data

    from deskops.models import TaskDoc

    return extract_model_data(TaskDoc, (tmp_path / "desk" / "tasks" / f"{task_id}.md").read_text(encoding="utf-8"))


def test_add_task_from_drawer_records_source_and_keeps_the_file(tmp_path: Path) -> None:
    _install_desk(tmp_path)
    source = _drawer_file(tmp_path, "tasks/task-loose-idea.md")

    assert main(_authored_task_argv(tmp_path, "--from-drawer", "loose-idea")) == 0

    doc = _task_doc(tmp_path, "task-authored-from-drawer")
    assert doc["from_drawer"] == "desk/drawer/tasks/task-loose-idea.md"
    assert source.exists(), "the drawer file is kept for manual cleanup"


def test_add_task_from_drawer_resolves_any_drawer_subfolder(tmp_path: Path) -> None:
    """The drawer holds features, issues and questions, not only tasks."""
    _install_desk(tmp_path)
    _drawer_file(tmp_path, "features/feature-shiny.md")

    assert main(_authored_task_argv(tmp_path, "--from-drawer", "feature-shiny")) == 0

    assert _task_doc(tmp_path, "task-authored-from-drawer")["from_drawer"] == "desk/drawer/features/feature-shiny.md"


def test_add_task_from_drawer_rejects_an_unknown_selector(tmp_path: Path) -> None:
    _install_desk(tmp_path)

    assert main(_authored_task_argv(tmp_path, "--from-drawer", "nothing-like-this")) != 0
    assert not (tmp_path / "desk" / "tasks" / "task-authored-from-drawer.md").exists()


def test_add_task_from_drawer_rejects_an_ambiguous_selector(tmp_path: Path) -> None:
    _install_desk(tmp_path)
    _drawer_file(tmp_path, "tasks/task-idea-one.md")
    _drawer_file(tmp_path, "features/feature-idea-two.md")

    assert main(_authored_task_argv(tmp_path, "--from-drawer", "idea")) != 0
    assert not (tmp_path / "desk" / "tasks" / "task-authored-from-drawer.md").exists()


def test_add_task_from_drawer_rejects_paths_outside_the_drawer(tmp_path: Path) -> None:
    _install_desk(tmp_path)

    assert main(_authored_task_argv(tmp_path, "--from-drawer", "desk/tasks/Board.md")) != 0
    assert not (tmp_path / "desk" / "tasks" / "task-authored-from-drawer.md").exists()


def test_from_drawer_survives_replacing_references(tmp_path: Path) -> None:
    """Why the origin is its own field: closeout replaces the whole
    references list via `deskops edit task <id> references ...`."""
    _install_desk(tmp_path)
    _drawer_file(tmp_path, "tasks/task-loose-idea.md")
    assert main(_authored_task_argv(tmp_path, "--from-drawer", "loose-idea")) == 0

    assert main([
        "edit", "task", "task-authored-from-drawer", "references", '["pytest tests/x.py"]',
        "--root", str(tmp_path),
    ]) == 0

    doc = _task_doc(tmp_path, "task-authored-from-drawer")
    assert doc["references"] == ["pytest tests/x.py"]
    assert doc["from_drawer"] == "desk/drawer/tasks/task-loose-idea.md"


def test_tasks_not_from_the_drawer_do_not_carry_the_field(tmp_path: Path) -> None:
    """from_drawer is written only when set, so every task already tracked in
    every desk keeps byte-identical content and an unchanged hash."""
    _install_desk(tmp_path)

    assert main(_authored_task_argv(tmp_path)) == 0

    text = (tmp_path / "desk" / "tasks" / "task-authored-from-drawer.md").read_text(encoding="utf-8")
    assert "from_drawer" not in text


def test_show_task_reports_the_drawer_origin(tmp_path: Path, capsys) -> None:
    _install_desk(tmp_path)
    _drawer_file(tmp_path, "tasks/task-loose-idea.md")
    assert main(_authored_task_argv(tmp_path, "--from-drawer", "loose-idea")) == 0
    capsys.readouterr()

    assert main(["show", "task", "task-authored-from-drawer", "--root", str(tmp_path)]) == 0

    assert "From drawer: desk/drawer/tasks/task-loose-idea.md" in capsys.readouterr().out


# ── drawer remove ────────────────────────────────────────────────────────────


def _drawer_board(tmp_path: Path) -> Path:
    board = tmp_path / "desk" / "drawer" / "tasks" / "Board.md"
    board.parent.mkdir(parents=True, exist_ok=True)
    board.write_text(
        "# Drawer Board\n\n"
        "Deferred task backlog:\n\n"
        "- `task-keep-me` — kept entry\n"
        "- `task-loose-idea` — removed entry (**blocked**)\n"
        "- `task-keep-me-too` — another kept entry\n",
        encoding="utf-8",
    )
    return board


def test_drawer_remove_deletes_the_entry_and_its_board_bullets(tmp_path: Path) -> None:
    _install_desk(tmp_path)
    entry = _drawer_file(tmp_path, "tasks/task-loose-idea.md")
    board = _drawer_board(tmp_path)

    assert main(["drawer", "remove", "loose-idea", "--root", str(tmp_path)]) == 0

    assert not entry.exists()
    text = board.read_text(encoding="utf-8")
    assert "task-loose-idea" not in text
    assert "- `task-keep-me` — kept entry" in text
    assert "- `task-keep-me-too` — another kept entry" in text


def test_drawer_remove_alerts_each_reference_it_leaves_behind(tmp_path: Path, capsys) -> None:
    """The stem bullet goes with the entry; the path bullet and a task naming the entry stay, each
    reported on stderr (no rewrite, exit unchanged)."""
    _install_desk(tmp_path)
    # The id makes the entry the graph node `task:task-loose-idea` the bullets and the task name.
    entry = _drawer_file(tmp_path, "tasks/task-loose-idea.md", "---\nid: task-loose-idea\n---\n\n# Loose idea\n\nNotes.\n")
    board = _drawer_board(tmp_path)
    board.write_text(board.read_text(encoding="utf-8") + "- `tasks/task-loose-idea.md` — path bullet\n", encoding="utf-8")
    task = tmp_path / "desk" / "tasks" / "task-ref.md"
    task.write_text("# Ref\n\n## Related Tasks\n\n- task-loose-idea\n", encoding="utf-8")
    capsys.readouterr()

    assert main(["drawer", "remove", "loose-idea", "--root", str(tmp_path)]) == 0
    captured = capsys.readouterr()

    assert not entry.exists()
    assert "Removed drawer entry desk/drawer/tasks/task-loose-idea.md" in captured.out
    assert "alert" not in captured.out
    assert captured.err.splitlines() == [
        "alert: desk/drawer/tasks/task-loose-idea.md still referenced by desk/drawer/tasks/Board.md",
        "alert: desk/drawer/tasks/task-loose-idea.md still referenced by desk/tasks/task-ref.md",
    ]
    assert "- `tasks/task-loose-idea.md` — path bullet" in board.read_text(encoding="utf-8")
    assert "- task-loose-idea" in task.read_text(encoding="utf-8")


def test_drawer_remove_refuses_when_an_active_task_records_the_entry(tmp_path: Path, capsys) -> None:
    _install_desk(tmp_path)
    entry = _drawer_file(tmp_path, "tasks/task-loose-idea.md")
    board = _drawer_board(tmp_path)
    assert main(_authored_task_argv(tmp_path, "--from-drawer", "loose-idea")) == 0
    capsys.readouterr()

    assert main(["drawer", "remove", "loose-idea", "--root", str(tmp_path)]) != 0

    assert entry.exists()
    assert "- `task-loose-idea` — removed entry (**blocked**)" in board.read_text(encoding="utf-8")
    assert "task-authored-from-drawer" in capsys.readouterr().out


def test_drawer_remove_force_skips_the_active_task_check(tmp_path: Path) -> None:
    _install_desk(tmp_path)
    entry = _drawer_file(tmp_path, "tasks/task-loose-idea.md")
    board = _drawer_board(tmp_path)
    assert main(_authored_task_argv(tmp_path, "--from-drawer", "loose-idea")) == 0

    assert main(["drawer", "remove", "loose-idea", "--force", "--root", str(tmp_path)]) == 0

    assert not entry.exists()
    assert "task-loose-idea" not in board.read_text(encoding="utf-8")
    assert (tmp_path / "desk" / "tasks" / "task-authored-from-drawer.md").exists()


def test_drawer_remove_untracks_the_entry_from_the_store(tmp_path: Path) -> None:
    from sldb.cli import main as sldb_main

    _install_desk(tmp_path)
    entry = _drawer_file(
        tmp_path,
        "tasks/task-tracked.md",
        "---\nkind: suggestion\ncreated_at: 2026-10-18T00:00:00\nstatus: open\n---\n\n# Tracked\n\nBody.\n",
    )
    assert sldb_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert sldb_main(["models", "add", "deskops.models:InboxNoteDoc", "--store", str(tmp_path / ".sldb")]) == 0
    assert sldb_main([
        "docs", "track", str(entry), "--model", "InboxNoteDoc",
        "--name", entry.stem, "--store", str(tmp_path / ".sldb"), "--force",
    ]) == 0
    assert _tracked_names(tmp_path) == [entry.stem]

    assert main(["drawer", "remove", "tracked", "--root", str(tmp_path)]) == 0

    assert not entry.exists()
    assert _tracked_names(tmp_path) == []

FILE:instruccion
Cold-bundle de la tarea task-inbox-y-drawer-quedan-trackeados-en-el-store-del-desk-y-las-vistas-los-leen-del-store-h10-de-cc34: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_view.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_delivery.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_inbox_promote_cli_gaps.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea


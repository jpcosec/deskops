FILE:desk/tasks/task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista.md
---
sldb:
  by: agent
  at: '2026-11-17T01:25:26Z'
  authority: generated
  via: create_document
id: task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-095054-suggestion-respuesta-a-20261116-011047-la-ui-del-desk-no-muestra-findings-de-gates-ni-recibos-tarea-abierta-en-graph-ui.md
depends_on: []
pills: []
files:
- deskops/cli/commands/view.py
- docs/deskops-ui.md
- tests/test_view.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops view task entrega los recibos de la tarea en un campo receipts del contrato de la vista

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui (nota 20261116-095054) ya dibuja los findings de los gates, pero no puede mostrar los recibos (ReviewDoc con kind, verdict, anchor_state) porque deskops view task no los entrega: solo aparecen dentro del texto de un finding (seen). Pide un campo en el contrato de deskops view (docs/deskops-ui.md) y lo dibuja cuando exista.

## Goal

_Describe the concrete result this task must produce._

deskops view task <id> --format json trae task.receipts: una lista con un objeto por ReviewDoc cuyo subject es la tarea, con id, kind, verdict, anchor_state y created_at, ordenada por created_at; docs/deskops-ui.md documenta el campo.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/view.py (armado de la tarjeta de view task), docs/deskops-ui.md (contrato) y tests en tests/test_view.py. Sale: view board (no lleva recibos), la UI de graph_ui y cualquier cambio en ReviewDoc. anchor_state se lee como lo calcula hoy deskops review status para la tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ver como deskops review status obtiene los ReviewDoc de una tarea y su anchor_state, y reusarlo. 2) Agregar receipts a la salida de view task (json, yaml y text; en text una linea por recibo). 3) Documentar el campo en docs/deskops-ui.md junto a gates. 4) Test en desk sandbox con un recibo registrado por deskops review record.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_view.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_view_goldens.py

## Done When

_Name the observable condition that makes the task complete._

view task --format json trae receipts con los cinco campos para una tarea con recibos, la lista vacia para una sin recibos, docs/deskops-ui.md lo documenta y los dos archivos de la Validation pasan. Al cerrar se avisa a graph_ui con deskops message send --to graph_ui.

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

FILE:docs/deskops-ui.md
# deskops view: el contrato de datos de la UI de deskops

`deskops view {board,task <id>,drawer,inbox,agents} --root <repo> --format json|text`
produce las vistas que dibuja la UI de deskops (graph_ui, `frontends/desk/`).

`board` y `task` son `ViewDoc` de sldb: las semillas `deskops/data/views/board.md` y
`task.md` (viven solo en el paquete, sin `desk/views/`), trackeadas como `ViewDoc` en el
store del propio repo deskops. `deskops view` las evalúa con `sldb.api.run_view` sobre el
store del desk y `deskops.cli.commands.view.project(view, resultado, root)` proyecta el
resultado a este contrato. graph_ui lee `GET /views/<vista>` de `sldb serve` (con ETag) y
llama a la misma `project` en proceso, así que sirve exactamente el mismo JSON. `drawer`,
`inbox` y `agents` los arma el CLI (ver «Fuentes de cada campo»).

Mientras sldb no resuelva una `ViewDoc` de un store enlazado (hipótesis H9), `board` y
`task` responden solo en un desk cuyo propio store trackea las `ViewDoc` (el repo deskops);
en los demás salen con el sobre de error `Unknown view: <vista>`.

Reglas comunes:

- **Solo lectura.** Ninguna vista escribe en `desk/`, `.sldb/` ni `runs/`.
- **Una lectura por corrida.** `board` y `task` abren un `read_snapshot`: la ruta y el
  payload de cada tarea, sus transiciones, el grafo de reglas y el contexto del grafo de
  closeout se leen una vez y se comparten entre las tarjetas. El grafo no recorre `runs/`
  salvo que una materialización declare un `target_identity` allí. Es una optimización de
  lectura: el JSON y el texto no cambian (los fijan los goldens de `tests/test_view_goldens.py`).
- **Sin datos inventados.** Una referencia que no resuelve (pill, atom, tarea del Board,
  nota, línea del índice de corridas, runtime de Herdr) no aparece como dato: va a
  `errors` como `{"reference": "<id o ruta>", "cause": "<por qué>"}`; si la referencia la hace
  una tarea (una pill o un atom de la tarea), el error lleva además `"task": "<id de la tarea>"`
  para que la UI marque la tarjeta.
- `--format json` es el contrato estable; `--format text` es un resumen legible.
- Toda vista lleva `view` (nombre), `contract` (versión, hoy `1`), `root` (ruta absoluta
  del repo) y `errors`.
- Un error que impide la vista entera (no hay `desk/tasks/Board.md`, la tarea no resuelve)
  sale como el sobre de error de deskops (`{"ok": false, "error": {...}}`) con código 1.

## board

Una columna por nodo del ciclo de vida, en el orden de
`deskops/spec/workflows/task_lifecycle.yaml` (`ritual-execution`, `ritual-testing`,
`ritual-closeout`). Las tareas salen de `desk/tasks/Board.md` (el Board es la verdad).

```json
{
  "view": "board", "contract": 1, "root": "/abs/repo",
  "board": {"path": "desk/tasks/Board.md", "pills": [{"id": "pill-…", "title": "…", "source": "board"}]},
  "columns": [
    {"node": "ritual-execution", "phase": "execution", "purpose": "…", "in_lifecycle": true,
     "count": 1, "tasks": [CARD]}
  ],
  "counts": {"tasks": 1, "by_node": {"ritual-execution": 1, "ritual-testing": 0, "ritual-closeout": 0},
             "gates_holding": 1, "gates_total": 1},
  "errors": []
}
```

Una tarea cuyo `current_node` no es un nodo del ciclo de vida aparece en una columna
extra con `in_lifecycle: false` y además en `errors`.

`CARD`:

```json
{
  "id": "task-…", "title": "…", "status": "draft", "current_node": "ritual-execution",
  "task_type": "code", "path": "desk/tasks/task-….md",
  "gates": [{"relation_type": "task_activates", "target": "ritual-testing", "condition": "", "holds": true}],
  "gates_holding": 1, "gates_total": 1,
  "closeout": {
    "ok": false, "declared": ["tests", "commit"], "found": [], "summary": "…",
    "implicit_code": false, "alerts": [],
    "evidence": [{"gate": "tests", "state": "pending", "evidence": [], "findings": [{"code": "…", "message": "…"}]}]
  },
  "pills": [{"id": "pill-…", "title": "…", "source": "task|board"}],
  "atoms": [{"id": "atom-…", "title": "…"}]
}
```

- `gates` es exactamente lo que devuelve `DeskopsOperations.show_task` (transiciones que
  salen del nodo actual, con su condición sldb y si se cumple hoy).
- `closeout` resume `verify_task_closeout`: `declared`/`found` tal cual; `evidence` trae
  una entrada por compuerta (`tests`, `atom_or_materialization_link`, `commit`,
  `document`, `external`) con `state`:
  `holds` (la compuerta se cumple), `pending` (falta, y la tarea aún no está en
  `ritual-closeout`) o `failing` (falta y la tarea está en `ritual-closeout`, o el tipo
  declarado no existe en el vocabulario).
- `pills`: `effective_pills` de la tarea (`source: task`) más las pills del Board
  (`source: board`), resueltas a `PillDoc`, igual que las fusiona `deskops next`.
- `atoms`: `effective_atoms` más las referencias `atom-*`, resueltos a `AtomDoc`.

## task

```json
{
  "view": "task", "contract": 1, "root": "/abs/repo",
  "task": {
    CARD…,
    "on_board": true,
    "why": "…", "goal": "…", "scope": "…", "implementation_path": "…",
    "validation": ["…"], "done_when": "…", "references": ["…"], "files": ["…"],
    "depends_on": ["…"], "inherits_from": ["…"], "from_drawer": "", "history": ["task_activates"],
    "pills": [{"id": "…", "title": "…", "source": "task", "what": "…", "when": "…", "how_not": "…"}],
    "atoms": [{"id": "…", "title": "…", "question": "what", "answer": "…"}]
  },
  "next": {"phase": "execution", "ritual": "desk/rituals/execution.md", "next_actions": ["…"], "advance_when": ["…"]},
  "revision": "<sha256 hex>",
  "errors": []
}
```

- `validation`, `done_when` y `references` son los efectivos (con herencia).
- `next` viene de `next_action_report`; si falla, `next` es `null` y la causa va a `errors`.
- `revision` = el ETag de la vista `task` (`run_view(...)["revision"]`, GD25): cambia cuando
  cambia la tarea, el Board o una pill o un atom que la vista leyó. Es la guarda que usa
  `POST /api/desk/advance` de graph_ui: con un `revision` viejo responde 409.

## drawer

```json
{
  "view": "drawer", "contract": 1, "root": "/abs/repo", "count": 1,
  "tasks": [{
    "id": "task-…", "markdown": "<texto completo del archivo>", "title": "…", "status": "deferred",
    "excerpt": ["primeras líneas del cuerpo"], "path": "desk/drawer/tasks/task-….md",
    "command": "deskops add task --root . --from-drawer desk/drawer/tasks/task-….md --title '…'"
  }],
  "errors": []
}
```

- Archivos `desk/drawer/tasks/*.md` salvo `Board.md` y `README.md`.
- `markdown`: el archivo completo, para la vista en crudo (solo lectura).
- `excerpt`: hasta 3 líneas no vacías del cuerpo, sin encabezados ni las pistas en cursiva
  de la plantilla (`_Explain …_`).
- `status` es `null` si el archivo no es un `TaskDoc` válido (la causa va a `errors`).
- `command` es el inicio del comando para autorizar la tarea; el resto de campos
  (`--goal`, `--scope`, `--validation`, `--task-type`…) los decide quien la promueve.

## inbox

```json
{
  "view": "inbox", "contract": 1, "root": "/abs/repo", "count": 2, "open": 1,
  "notes": [{
    "id": "20261104-101500-suggestion-…", "path": "desk/inbox/….md", "kind": "suggestion",
    "title": "…", "sender": "sldb", "target": "deskops", "date": "2026-11-04T10:15:00",
    "status": "open", "acknowledged": false, "acknowledged_by": null, "acknowledged_at": null,
    "body": "…", "revision": "<sha256 de los bytes de la nota>"
  }],
  "errors": []
}
```

- Mismo orden y misma lectura del frontmatter que `deskops message list` (más nuevas
  primero); `acknowledged` es `status == "closed"`, que es lo que escribe `message ack`.
- `date` sale del sello `YYYYMMDD-HHMMSS` del nombre de archivo; sin sello, `null` y aviso.
- `body` es el campo `body` del `InboxNoteDoc`.
- `revision` = `sha256(bytes del archivo de la nota)`: la guarda de las acciones del inbox
  (Reconocer, Pasar al drawer) en la UI.

## agents

```json
{
  "view": "agents", "contract": 1, "root": "/abs/repo",
  "workers": [{"pane": "w1:p1", "kind": "claude", "name": null, "status": "idle", "cwd": "…",
               "title": "…", "workspace": "w1", "seq": 3, "focused": false}],
  "workers_error": null, "live_workers": 1,
  "runs": [{"task_id": "task-…", "run_id": null, "run_dir": null, "commit": null, "mode": "manual", "on_board": false}],
  "runs_total": 122, "runs_limit": 20,
  "errors": []
}
```

- `workers` es la forma pública de `deskops runtime workers` (Herdr, toda la máquina, no
  solo este desk). Si Herdr no responde: `workers: null`, `live_workers: null`,
  `workers_error` con la causa y una entrada en `errors`; nunca una lista vacía muda.
- `runs`: las últimas `--runs` (20 por omisión) líneas de `runs/subagents/index.jsonl`, la
  más nueva primero; `on_board` dice si la tarea sigue en el Board.

## Fuentes de cada campo (CC34)

`run_view` es la vista `ViewDoc` evaluada por sldb. «Agregado CLI, pendiente de sldb Hn»
es un campo que el CLI todavía arma con una operación de lectura que ya existía, porque el
modelo de `ViewDoc` no lo expresa aún; cada uno se retira cuando sldb cierre su hipótesis.

| Campo | Fuente |
|---|---|
| `view`, `contract`, `root` | constantes del CLI |
| `board.path`, `board.pills` (ids) | `run_view`, sección `board` (campos `tasks`, `pills`) |
| tareas del Board, su orden, `errors` de referencias | `run_view`, secciones `board` y `tasks` (el Board manda) |
| columnas (`node`, agrupación) | `run_view`, sección `tasks` (`group_by: current_node`) |
| `phase`, `purpose`, `in_lifecycle` de cada columna | agregado CLI, pendiente de sldb H5 (spec del ciclo de vida) |
| `CARD.id/title/status/current_node/task_type/path` | `run_view`, filas de `tasks` / `task` |
| `CARD.gates`, `gates_holding`, `gates_total` | agregado CLI, pendiente de sldb H1-H3 (`show_task`) |
| `CARD.closeout` | agregado CLI, pendiente de sldb H4 (`verify_task_closeout` sin recibos) |
| `CARD.pills`, `CARD.atoms` (títulos y detalle) | `run_view`, secciones `pills` y `atoms` |
| lista efectiva de pills y atoms; `validation`, `done_when`, `references` | agregado CLI, pendiente de sldb H6 (`resolve_task_payload`) |
| `counts` | suma del CLI sobre las tarjetas |
| `task.on_board` | `run_view`, arista `tasks` del Board |
| `task.why/goal/scope/implementation_path/files/depends_on/inherits_from/from_drawer/history` | `run_view`, fila de `task` |
| `next` | agregado CLI, pendiente de sldb H5 (`next_action_report`) |
| `revision` (task) | `run_view` (ETag de GD25) |
| `drawer.*` (`markdown`, `excerpt`, `command`...) | agregado CLI, lectura del archivo, pendiente de H7 y H10 |
| `inbox.*`, `notes[].revision` | agregado CLI, lectura del archivo, pendiente de H8 y H10 |
| `agents.*` | CLI (`deskops/runtime/desk_agents.py`): no son documentos |

## Mapeo de la pantalla de Stitch a fuentes reales

Copiado del alcance del plan deskops-ui (2026-11-04; plan retirado del drawer el 2026-11-17, queda en el historial de git).

| Elemento de Stitch | Fuente real | Campo de la vista | Si no hay fuente |
|---|---|---|---|
| Columnas por etapa | `current_node` de cada tarea del Board; orden del spec | `board.columns` | — |
| Checklist de gates de la tarjeta | `show_task` → gates, más evidencia de `verify_task_closeout` | `CARD.gates`, `CARD.closeout.evidence` | — |
| "n de m rituales" | conteo de los mismos gates | `CARD.gates_holding`/`gates_total` | — |
| Pills de la tarjeta | `effective_pills` + pills del Board → `PillDoc` | `CARD.pills` (+ `what/when/how_not` en task) | id en `errors` |
| Atoms | `atoms` y referencias `atom-*` → `AtomDoc` | `CARD.atoms` (+ `answer` en task) | id en `errors` |
| "Promover a Atom" | no hay operación | — | botón deshabilitado: "requiere operación de graduación (no existe)" |
| "Iniciar ejecución" | no hay dispatch | — | deshabilitado: "llega con runtime dispatch (fábrica E3)" |
| Avanzar | `POST /api/desk/advance` de graph_ui | `task.revision` (ETag) | — |
| Diferir a drawer | no hay operación | — | deshabilitado con motivo |
| Drawer: lista y vista raw | `desk/drawer/tasks/*.md` | `drawer.tasks` | — |
| Drawer: "Promover a Desk" | `add task --from-drawer` | `drawer.tasks[].command` | se muestra el comando, no un botón |
| Inbox: lista, lectura, emisor → destino | `InboxNoteDoc` | `inbox.notes` | — |
| Inbox: Reconocer | `deskops message ack` | — (acción de UI05) | — |
| Inbox: Pasar a drawer | `promote inbox-to-drawer-task` | — (acción de UI05) | — |
| Agentes y corridas | `runtime workers`, `runs/subagents/index.jsonl` | `agents.workers`, `agents.runs` | causa en `workers_error` |
| Métricas de cabecera | conteos derivables | `board.counts`, `drawer.count`, `inbox.open`, `agents.live_workers` | ningún porcentaje inventado |
| Hilo del inbox, firmas, prioridad, TTL, autor, versión | no existe | — | no se dibuja |
| Gates por tipo, recibos, `anchor_state` | plan `gates-por-tipo`, sldb GO07 | — | no se dibuja hasta que existan |

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

FILE:instruccion
Cold-bundle de la tarea task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_view.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_view_goldens.py


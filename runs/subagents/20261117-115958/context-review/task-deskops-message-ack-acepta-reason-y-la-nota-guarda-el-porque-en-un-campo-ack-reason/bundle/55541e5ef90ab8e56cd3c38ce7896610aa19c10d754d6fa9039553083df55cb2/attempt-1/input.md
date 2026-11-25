FILE:desk/tasks/task-deskops-message-ack-acepta-reason-y-la-nota-guarda-el-porque-en-un-campo-ack-reason.md
---
sldb:
  by: agent
  at: '2026-11-17T01:29:59Z'
  authority: generated
  via: create_document
id: task-deskops-message-ack-acepta-reason-y-la-nota-guarda-el-porque-en-un-campo-ack-reason
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-222401-suggestion-deskops-message-ack-no-admite-una-raz-n-y-inboxnote-no-tiene-un-campo-para-guardarla.md
depends_on: []
pills: []
files:
- deskops/models/inbox.py
- deskops/cli/registry.py
- deskops/cli/commands/message.py
- tests/test_message_cli.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
---

# deskops message ack acepta --reason y la nota guarda el porque en un campo ack_reason

## Rationale

_Explain why this task exists or the business driver behind it._

IR (nota 20261116-222401): al cerrar notas con deskops message ack no hay forma de dejar el porque. ack no acepta --reason y el modelo de la nota (deskops/models/inbox.py) solo tiene kind, sender_project, target_project, created_at, status, acknowledged_by y acknowledged_at, asi que deskops edit inbox-note tampoco puede escribirlo. Con la regla de JP de procesar cada nota al llegar (ack si es aviso o ya resuelta, tarea o drawer y ack si es trabajo), el porque de cada ack tiene que quedar en el desk.

## Goal

_Describe the concrete result this task must produce._

deskops message ack <selector> --reason <texto> marca la nota como acknowledged y guarda el texto en un campo opcional ack_reason del modelo de la nota; sin --reason el ack funciona como hoy y ack_reason queda vacio; deskops message read muestra ack_reason cuando existe.

## Scope

_State what is in scope and what is out of scope._

Entra: el campo opcional ack_reason en deskops/models/inbox.py (y lo que el store necesite para declararlo), la opcion --reason de message ack en deskops/cli/registry.py y deskops/cli/commands/message.py, la salida de message read, y tests. Sale: notas ya existentes (no se migran; ack_reason vacio es valido) y otros desks.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Agregar ack_reason (texto, opcional, por defecto vacio) al modelo de la nota. 2) --reason en message ack; escribirlo junto con acknowledged_by y acknowledged_at. 3) message read lo muestra. 4) Tests en desk sandbox (tmp_path): ack con --reason lo guarda y read lo muestra; ack sin --reason sigue igual; una nota vieja sin el campo sigue leyendose. 5) Correr test_command_registry.py y los goldens de ayuda (cambia la ayuda de message ack).

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_command_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py

## Done When

_Name the observable condition that makes the task complete._

ack --reason guarda y read muestra ack_reason, el ack sin --reason no cambia, las notas viejas siguen leyendose y los tres archivos de la Validation pasan.

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

FILE:desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---
sldb:
  by: agent
  at: '2026-11-17T01:11:30Z'
  authority: generated
  via: create_document
id: atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
title: deskops message es el unico comando de mensajeria del desk
five_wh_one_plus: what
tags:
- system:deskops
- topic:inbox
provenance: tests/test_message_cli.py
---

# deskops message es el unico comando de mensajeria del desk

## Answer

Las notas del inbox de un desk se envian, listan, leen y confirman con deskops message send|list|read|ack (send con --to <repo> para otro desk del ecosistema). El alias deskops inbox se retiro el 2026-11-16: deskops inbox ya no es un comando (invalid choice). Docs, la skill deskops-workflow y los tests usan solo deskops message.

FILE:deskops/models/inbox.py
from typing import Literal, Optional

from pydantic import Field

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
    title: str = Field(description="Inbox note title shown as the H1 heading.")
    body: str = Field(description="Markdown body describing the question or suggestion in detail.")

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


# sldb renders a field value as Jinja source (sldb/core/renderer_engine/base.py replace_markers):
# two or three opening braces raise TemplateSyntaxError and a valid expression is evaluated and
# stored altered with rc 0. Reported to sldb; this pins the literal contract until sldb fixes it.
SLDB_JINJA_VALUE_NOTE = (
    "20261117-015212-suggestion-render-model-markdown-interpreta-como-jinja-el-valor-de-los-campos"
    "-llaves-dobles-rompen-expresiones-se-evaluan.md"
)


@pytest.mark.xfail(strict=True, reason=SLDB_JINJA_VALUE_NOTE)
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
Cold-bundle de la tarea task-deskops-message-ack-acepta-reason-y-la-nota-guarda-el-porque-en-un-campo-ack-reason: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_command_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py


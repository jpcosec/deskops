FILE:desk/tasks/task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li.md
---
sldb:
  by: agent
  at: '2026-11-17T01:26:04Z'
  authority: generated
  via: create_document
id: task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-221318-suggestion-restos-del-retiro-del-alias-deskops-inbox.md
depends_on: []
pills: []
files:
- deskops/cli/commands/message.py
- tests/e2e_agent/scenarios/inbox-to-task.yaml
- tests/test_repo_identity.py
- tests/test_inbox_promote_cli_gaps.py
- tests/test_message_cli.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
---

# se borra el camino legacy de deskops message y el escenario e2e inbox-to-task usa deskops message list

## Rationale

_Explain why this task exists or the business driver behind it._

Seguimiento del retiro del alias deskops inbox (8667e8f1, closeout 49465a27; nota 20261116-221318). Quedaron: _run_legacy y su docstring en deskops/cli/commands/message.py, que solo alcanza deskops message sin subcomando; el escenario tests/e2e_agent/scenarios/inbox-to-task.yaml, cuya rama 'deskops inbox list --root .' ahora falla y cae a su alternativa con ||; y docstrings que nombran deskops inbox como comando en tests/test_repo_identity.py y tests/test_inbox_promote_cli_gaps.py.

## Goal

_Describe the concrete result this task must produce._

deskops message sin subcomando da un error de uso claro (la ayuda de message con sus subcomandos) sin pasar por _run_legacy, que se borra; el escenario e2e usa deskops message list --root .; los dos docstrings dejan de presentar deskops inbox como comando vigente.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/message.py, tests/e2e_agent/scenarios/inbox-to-task.yaml, tests/test_repo_identity.py y tests/test_inbox_promote_cli_gaps.py (solo docstrings), y tests de message. Sale: el registro de comandos (deskops inbox ya no existe) y docs.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer _run_legacy y quien lo llama en message.py. 2) Borrarlo y hacer que message sin subcomando imprima el error de uso de argparse o la ayuda, con rc 2. 3) Cambiar la rama del escenario e2e. 4) Ajustar los dos docstrings. 5) Test: deskops message sin subcomando da rc 2 y nombra send, list, read y ack.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_command_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py

## Done When

_Name the observable condition that makes the task complete._

grep de _run_legacy en deskops/ no da nada, el escenario e2e no usa deskops inbox, el test nuevo pasa y los tres archivos de la Validation pasan.

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

FILE:tests/e2e_agent/scenarios/inbox-to-task.yaml
id: inbox-to-task
notes: Triage across the inbox and the drawer, then authoring a task, from the agent skill only.
intent: |
  This repo already uses deskops. Another project left a note in this desk's inbox asking for a
  documented release process. It is not urgent: defer it to the drawer first, the way deskops
  expects deferred work to be kept. Then decide to do it now and turn it into a real deskops task
  (validation: `pytest`). Leave the task open.
docs: [.opencode/skills/use-deskops/SKILL.md]
setup:
  - git init -q
  - mkdir -p tests && printf 'def test_ok():\n    assert True\n' > tests/test_ok.py
  - deskops init . >/dev/null
  - deskops add inbox-note --root . --title "Document the release process" --kind suggestion --sender-project other-project --target-project repo --created-at 2026-10-16T12:00:00 --status open --body "Please document how this repo cuts a release." >/dev/null
  - git add -A && git commit -qm "initial"
reference:
  - deskops inbox list --root . || deskops list inbox-notes --root .
  - deskops promote inbox-to-drawer-task document-the-release-process --root .
  - deskops add task --root . --title "Document the release process" --goal "Write down how releases are made" --scope "docs only" --task-type task.docs --validation pytest
checks:
  - name: the note was deferred into the drawer
    run: |-
      grep -rqi 'release process' desk/drawer
  - name: an open task about the release process exists
    run: |-
      grep -lqi 'release process' desk/tasks/task-*.md
  - name: the local store passes sldb stores check
    run: |-
      sldb stores check --store .sldb

FILE:tests/test_repo_identity.py
from __future__ import annotations

import json
from pathlib import Path

import pytest
from sldb.core.exceptions import SLDBStoreError
from sldb.runtime.validation import render_model_markdown

from deskops.cli.main import main
from deskops.identity import EcosystemIdentity
from deskops.identity import load_repository_registry
from deskops.identity import resolve_store_context
from deskops.models import RepositoryDoc


def _write_repo_doc(registry_dir: Path, *, repo_id: str, repo_path: str, name: str | None = None, filename: str | None = None) -> Path:
    payload = {
        "id": repo_id,
        "name": name or repo_id,
        "path": repo_path,
        "status": "active",
        "description": f"Repository for {repo_id}.",
        "tags": [],
    }
    path = registry_dir / (filename or f"repo-{repo_id}.md")
    path.write_text(render_model_markdown(RepositoryDoc, payload) + "\n", encoding="utf-8")
    return path


def _write_config(repo_root: Path, project_identity: str) -> None:
    desk_root = repo_root / "desk"
    desk_root.mkdir(parents=True, exist_ok=True)
    (desk_root / "config.json").write_text(
        json.dumps({"project_identity": project_identity}, indent=2) + "\n",
        encoding="utf-8",
    )


def test_repo_identity_resolver_returns_single_registered_match(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    repo_root = tmp_path / "sender-repo"
    (repo_root / "desk").mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="sender-repo", repo_path="sender-repo", name="Sender Repo")

    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    assert EcosystemIdentity(str(store_path)).how_do_i_find_another("sender-repo") == (repo_root / "desk").resolve()
    assert EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root / "subdir", require_registry_match=False) == "sender-repo"


def test_repo_identity_resolver_fails_on_duplicate_id(tmp_path: Path) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="shared-id", repo_path="repo-one", filename="repo-one.md")
    _write_repo_doc(registry_dir, repo_id="shared-id", repo_path="repo-two", filename="repo-two.md")

    with pytest.raises(SLDBStoreError, match="Duplicate repository id 'shared-id'"):
        load_repository_registry(tmp_path / "desk", tmp_path)


def test_repo_identity_resolver_fails_on_duplicate_root(tmp_path: Path) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="repo-one", repo_path="shared-root", filename="repo-one.md")
    _write_repo_doc(registry_dir, repo_id="repo-two", repo_path="shared-root", filename="repo-two.md")

    with pytest.raises(SLDBStoreError, match="Duplicate repository root"):
        load_repository_registry(tmp_path / "desk", tmp_path)


def test_repo_whoami_prints_canonical_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo_root = tmp_path / "deskops-child"
    _write_config(repo_root, "deskops-child")
    registry_dir = repo_root / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="deskops-child", repo_path=".")

    store_path = repo_root / ".sldb"
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, repo_root))

    result = main(["repo", "whoami", "--root", str(repo_root), "--store", str(store_path)])

    captured = capsys.readouterr()
    assert result == 0
    assert captured.out.strip() == "deskops-child"


def test_repo_local_desk_without_a_registry_is_its_own_authority(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A desk that keeps no registry must still resolve its own identity.

    Without this, `deskops inbox --ack` and `deskops next` inside such a repo
    fail with "Repository id '<name>' not found in registry", which makes inbox
    triage impossible from the repository the note is addressed to.
    """
    repo_root = tmp_path / "repo-local"
    _write_config(repo_root, "repo-local")

    store_path = repo_root / ".sldb"
    store_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, repo_root))

    assert EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root, require_registry_match=True) == "repo-local"
    assert EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root, require_registry_match=False) == "repo-local"


def test_a_registry_that_lacks_the_repo_still_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The fallback is only for a missing registry, not for a disagreement."""
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="someone-else", repo_path="someone-else")

    repo_root = tmp_path / "repo-local"
    _write_config(repo_root, "repo-local")
    store_path = repo_root / ".sldb"
    store_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    with pytest.raises(SLDBStoreError, match="not found in registry"):
        EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root, require_registry_match=True)


def _make_store(root: Path) -> Path:
    store = root / ".sldb"
    (store / "core").mkdir(parents=True)
    (store / "core" / "store_index.yaml").write_text("{}\n", encoding="utf-8")
    return store


def test_nested_sandbox_never_reads_the_outer_repository_store(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A sandbox with its own desk/ is the boundary; the repo store above it is invisible."""
    outer = tmp_path / "outer"
    (outer / ".git").mkdir(parents=True)
    (outer / "desk").mkdir()
    outer_store = _make_store(outer)

    sandbox = outer / ".tmp" / "deskops-cli-test"
    (sandbox / "desk").mkdir(parents=True)
    monkeypatch.chdir(sandbox)

    assert outer_store.exists()
    with pytest.raises(SLDBStoreError, match="No local store found"):
        resolve_store_context(None)


def test_nested_sandbox_uses_its_own_store_when_it_has_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    outer = tmp_path / "outer"
    (outer / ".git").mkdir(parents=True)
    (outer / "desk").mkdir()
    _make_store(outer)

    sandbox = outer / ".tmp" / "deskops-cli-test"
    (sandbox / "desk").mkdir(parents=True)
    sandbox_store = _make_store(sandbox)
    monkeypatch.chdir(sandbox)

    store, root = resolve_store_context(None)

    assert store == sandbox_store.resolve()
    assert root == sandbox.resolve()

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


# ── message list --root ──────────────────────────────────────────────────────────────


def test_message_list_accepts_root_like_every_other_subcommand(tmp_path: Path, capsys) -> None:
    """The documented `--root .` invocation must list the desk's inbox notes;
    the parser once only accepted --desk-root, so it failed outright."""
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-hello", "# Hello\n\nBody.\n")
    capsys.readouterr()

    assert main(["message", "list", "--root", str(tmp_path)]) == 0

    assert "Hello" in capsys.readouterr().out


def test_message_list_desk_root_wins_over_root(tmp_path: Path, capsys) -> None:
    """--desk-root is the more specific flag and must keep precedence."""
    _install_desk(tmp_path)
    other = tmp_path / "other"
    other.mkdir()
    _install_desk(other)
    _write_note(tmp_path, "20260101-000000-suggestion-in-root", "# InRoot\n\nBody.\n")
    _write_note(other, "20260101-000001-suggestion-in-desk-root", "# InDeskRoot\n\nBody.\n")
    capsys.readouterr()

    assert main(["message", "list", "--root", str(tmp_path), "--desk-root", str(other / "desk")]) == 0

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
Cold-bundle de la tarea task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_command_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py


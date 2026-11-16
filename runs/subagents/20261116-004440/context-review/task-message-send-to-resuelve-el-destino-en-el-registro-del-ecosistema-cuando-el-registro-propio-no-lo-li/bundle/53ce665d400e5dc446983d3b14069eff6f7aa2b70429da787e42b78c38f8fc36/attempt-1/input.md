FILE:desk/tasks/task-message-send-to-resuelve-el-destino-en-el-registro-del-ecosistema-cuando-el-registro-propio-no-lo-li.md
---
sldb:
  by: agent
  at: '2026-11-16T00:44:24Z'
  authority: generated
  via: save_document_payload
id: task-message-send-to-resuelve-el-destino-en-el-registro-del-ecosistema-cuando-el-registro-propio-no-lo-li
status: draft
summary: message send --to cae al registro del ecosistema (~/setup/desk/registry)
  cuando el registro del remitente no lista el destino
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/identity.py
- deskops/cli/commands/message.py
- deskops/cli/commands/repo.py
- tests/test_message_ecosystem_registry.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# message send --to resuelve el destino en el registro del ecosistema cuando el registro propio no lo lista

## Rationale

_Explain why this task exists or the business driver behind it._

MEPU (15-11, prioridad alta): deskops message send --to deskops no resuelve desde otro repo porque solo se lee el desk/registry del remitente y el de MEPU no lista a nadie; bloquea a los agentes que avisan entre repos.

## Goal

_Describe the concrete result this task must produce._

--to <repo> busca primero en el registro del remitente y despues en el registro del ecosistema (~/setup/desk/registry, o la variable DESKOPS_ECOSYSTEM_REGISTRY), tambien desde un repo sin store; las rutas del registro aceptan ~ para valer en todas las maquinas; una raiz registrada que no existe en esta maquina es un error y no se escribe nada.

## Scope

_State what is in scope and what is out of scope._

deskops/identity.py (ecosystem_registry_dir, load_ecosystem_registry, find_registered_desk, expanduser en resolve_registered_root), deskops/cli/commands/message.py (destino por find_registered_desk; identidad del remitente por raiz en el registro del ecosistema como ultimo recurso), deskops/cli/commands/repo.py (repo register resuelve la ruta con la misma resolve_registered_root de identity.py, con ~), tests/test_message_ecosystem_registry.py. Fuera: registrar repos en ~/setup (se hace despues con deskops repo register), cambiar el modelo RepositoryDoc. Precisiones (preflight-1): p1 DESKOPS_ECOSYSTEM_REGISTRY, si esta definida y no vacia, gana sobre el valor por defecto ~/setup/desk/registry; es el directorio registry (el que tiene repo-*.md), y las rutas relativas de sus entradas resuelven contra la raiz del repo que lo contiene (padre de desk/). p2 el ~ se expande solo en el campo path de RepositoryDoc, en todos los registros (local y del ecosistema); las rutas relativas siguen como hoy. p3 solo cuenta la entrada del repo pedido: si su raiz no existe en esta maquina, SLDBStoreError con 'does not exist on this machine' y rc 1; entradas ajenas no afectan. p4 no se escribe nada en ningun lado: ni inbox ni directorios del destino, ni la nota. p5 la raiz del remitente (find_context_root) se compara con resolve_registered_repo_by_root sobre las entradas del ecosistema; se toma el id de esa entrada; si no aparece, el error actual 'Unable to resolve sender identity'. Orden del remitente: registro propio, desk/config.json, ecosistema. p6 sin store en el remitente solo cambia la busqueda (no hay registro propio); la nota se escribe en el inbox del destino igual que hoy, con su store si lo tiene. p7 la entrega no cambia: un archivo nuevo desk/inbox/<fecha>-<kind>-<slug>.md en el destino, como hoy. p8 en repo.py solo cambia _resolve_registered_root de repo register.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm python -m pytest -q -p no:cacheprovider tests/test_message_ecosystem_registry.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_message_ecosystem_registry.py en verde con el CLI real; deskops message send --to deskops desde un repo sin registro propio entrega en desk/inbox de deskops.

FILE:deskops/identity.py
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError
from sldb.runtime.validation import extract_model_data
from sldb.store.layout import project_root
from sldb.store.layout import store_exists

from deskops.config import DeskConfig
from deskops.models import RepositoryDoc

UNKNOWN_PROJECT_IDENTITY = "unknown-project"

#: Environment variable naming the ecosystem registry directory (``.../desk/registry``).
ECOSYSTEM_REGISTRY_ENV = "DESKOPS_ECOSYSTEM_REGISTRY"
#: The ecosystem registry every repo of the user can read when its own registry does not
#: list a target: the ``desk/registry`` of the user's ``~/setup`` control repo.
DEFAULT_ECOSYSTEM_REGISTRY = "~/setup/desk/registry"


@dataclass(frozen=True)
class RegisteredRepository:
    id: str
    name: str | None
    source_path: Path
    relative_path: str | None
    repo_root: Path | None

    @property
    def desk_root(self) -> Path | None:
        if self.repo_root is None:
            return None
        return self.repo_root / "desk"


def find_context_root(start: Path | None = None) -> Path:
    """Return the nearest ancestor that looks like a project boundary.

    The upward walk stops at the first directory containing ``desk/`` or
    ``.git``. Nothing above that boundary is considered, so a sandbox nested
    inside a repository never falls through to the repository's store or
    registry. With no matching ancestor the current directory is the boundary.
    """
    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for directory in [current, *current.parents]:
        if (directory / "desk").is_dir() or (directory / ".git").exists():
            return directory
    return current


def find_local_store(start: Path | None = None) -> Path | None:
    """Return the store at the project boundary, never an ancestor's store."""
    candidate = find_context_root(start) / ".sldb"
    return candidate if store_exists(candidate) else None


def resolve_store_context(store_arg: str | None) -> tuple[Path, Path]:
    if store_arg:
        return get_store_context(store_arg)
    local_store = find_local_store()
    if local_store is None:
        raise SLDBStoreError("No local store found. Use --store to anchor the repo lookup.")
    return local_store, project_root(local_store)


def load_repository_registry(registry_desk_root: Path, ecosystem_root: Path) -> list[RegisteredRepository]:
    registry_dir = registry_desk_root / "registry"
    if not registry_dir.exists():
        return []

    entries: list[RegisteredRepository] = []
    for path in sorted(registry_dir.glob("repo-*.md")):
        payload = extract_model_data(RepositoryDoc, path.read_text(encoding="utf-8"))
        repo_id = str(payload.get("id") or path.stem.removeprefix("repo-"))
        repo_path = payload.get("path")
        resolved_root = resolve_registered_root(ecosystem_root, repo_path)
        entries.append(
            RegisteredRepository(
                id=repo_id,
                name=payload.get("name"),
                source_path=path.resolve(),
                relative_path=repo_path,
                repo_root=resolved_root,
            )
        )

    _raise_on_duplicate_ids(entries)
    _raise_on_duplicate_roots(entries)
    return entries


def resolve_registered_repo(
    entries: list[RegisteredRepository],
    repo_id: str,
    *,
    registry_dir: Path | None = None,
) -> RegisteredRepository:
    matches = [entry for entry in entries if entry.id == repo_id]
    if not matches:
        raise SLDBStoreError(_missing_repository_message(repo_id, entries, registry_dir=registry_dir))
    if len(matches) > 1:
        raise SLDBStoreError(_duplicate_id_message(repo_id, matches))
    return matches[0]


def resolve_registered_repo_by_root(
    entries: list[RegisteredRepository],
    repo_root: Path,
) -> RegisteredRepository | None:
    candidate = repo_root.resolve()
    matches = [
        entry
        for entry in entries
        if entry.repo_root is not None
        and (candidate == entry.repo_root or _is_relative_to(candidate, entry.repo_root))
    ]
    if not matches:
        return None
    if len(matches) > 1:
        joined = ", ".join(f"{entry.id} ({entry.repo_root})" for entry in matches)
        raise SLDBStoreError(
            f"Repository root '{candidate}' is ambiguous in registry; matches: {joined}."
        )
    return matches[0]


class EcosystemIdentity:
    """Canonical resolution path answering 'what repository am I in right now' and 'how do I find another'."""
    def __init__(self, store_arg: str | None) -> None:
        self.store_path, self.ecosystem_root = resolve_store_context(store_arg)
        self.registry_desk_root = self.ecosystem_root / "desk"
        self.registry_dir = self.registry_desk_root / "registry"
        self.entries = load_repository_registry(self.registry_desk_root, self.ecosystem_root)

    def what_repository_am_i_in(
        self,
        repo_root: Path,
        *,
        require_registry_match: bool,
        allow_unregistered: bool = False,
        default_to_directory_name: bool = False,
    ) -> str | None:
        """Resolve the identity of the repo at ``repo_root``.

        ``allow_unregistered`` lets a repo whose desk config names it fall back
        to that config when the local registry does not list it at all. That is
        the `message ack` case: creating a register for somebody else must not
        hide the repo's own identity.

        ``default_to_directory_name`` resolves a desk without
        ``project_identity`` from its directory name instead of failing, which
        lets a message be delivered to a desk that never configured itself.
        """
        repo_root = repo_root.resolve()
        desk_root = repo_root / "desk"
        config_identity = UNKNOWN_PROJECT_IDENTITY
        if desk_root.exists():
            config = DeskConfig.load(desk_root)
            config_identity = (config.project_identity or UNKNOWN_PROJECT_IDENTITY).strip() or UNKNOWN_PROJECT_IDENTITY

        entry_by_root = resolve_registered_repo_by_root(self.entries, repo_root)

        if not self.entries:
            if require_registry_match and config_identity == UNKNOWN_PROJECT_IDENTITY:
                if default_to_directory_name:
                    return repo_root.name
                raise SLDBStoreError("Desk config project_identity is not established (found 'unknown-project').")
            return config_identity if config_identity != UNKNOWN_PROJECT_IDENTITY else None

        if require_registry_match:
            if config_identity == UNKNOWN_PROJECT_IDENTITY:
                if not default_to_directory_name:
                    raise SLDBStoreError("Desk config project_identity is not established (found 'unknown-project').")
                return entry_by_root.id if entry_by_root is not None else repo_root.name
            matches = [entry for entry in self.entries if entry.id == config_identity]
            if not matches and allow_unregistered:
                if entry_by_root is not None:
                    raise SLDBStoreError(
                        f"Desk config project_identity '{config_identity}' disagrees with registry root match '{entry_by_root.id}' for '{repo_root}'."
                    )
                return config_identity
            repo_by_id = resolve_registered_repo(
                self.entries, config_identity, registry_dir=self.registry_dir
            )
            if entry_by_root is None:
                raise SLDBStoreError(
                    _unregistered_current_repo_message(repo_root, registry_dir=self.registry_dir)
                )
            if repo_by_id.id != entry_by_root.id:
                raise SLDBStoreError(
                    f"Desk config project_identity '{config_identity}' disagrees with registry root match '{entry_by_root.id}' for '{repo_root}'."
                )
            return config_identity
        else:
            if entry_by_root is None:
                if allow_unregistered and config_identity != UNKNOWN_PROJECT_IDENTITY:
                    return config_identity
                return None
            if config_identity != UNKNOWN_PROJECT_IDENTITY and config_identity != entry_by_root.id:
                raise SLDBStoreError(
                    f"Desk config project_identity '{config_identity}' disagrees with registry id '{entry_by_root.id}' for '{entry_by_root.repo_root}'."
                )
            return entry_by_root.id

    def how_do_i_find_another(self, repo_id: str) -> Path:
        """The desk of ``repo_id``: the local registry first, then the ecosystem registry."""
        if any(entry.id == repo_id for entry in self.entries):
            entry = resolve_registered_repo(self.entries, repo_id, registry_dir=self.registry_dir)
        else:
            entry = _ecosystem_entry(repo_id, self.entries, self.registry_dir)
        if entry.desk_root is None:
            raise SLDBStoreError(f"Repository id '{repo_id}' has no registered root path.")
        return entry.desk_root.resolve()


def ecosystem_registry_dir() -> Path:
    """The ecosystem registry: ``$DESKOPS_ECOSYSTEM_REGISTRY``, else ``~/setup/desk/registry``."""
    raw = os.environ.get(ECOSYSTEM_REGISTRY_ENV, "").strip() or DEFAULT_ECOSYSTEM_REGISTRY
    return Path(raw).expanduser()


def load_ecosystem_registry() -> list[RegisteredRepository]:
    """Entries of the ecosystem registry; relative paths resolve against its repo root."""
    registry_dir = ecosystem_registry_dir()
    desk_root = registry_dir.parent
    return load_repository_registry(desk_root, desk_root.parent)


def find_registered_desk(repo_id: str, store_arg: str | None = None) -> Path:
    """The desk of a registered repo, resolvable from any repo of the ecosystem.

    The sender's own registry answers first (when the sender has a store); a repo it does
    not list is looked up in the ecosystem registry (``ecosystem_registry_dir``), so a repo
    that never registered its neighbours can still write to them. The registered root must
    exist on this machine: a path that only exists on another machine is an error, never a
    directory to create.
    """
    try:
        desk_root = EcosystemIdentity(store_arg).how_do_i_find_another(repo_id)
    except SLDBStoreError:
        if store_arg:
            raise
        # No local store to anchor a local registry: the ecosystem registry alone answers.
        entry = _ecosystem_entry(repo_id, [], None)
        if entry.desk_root is None:
            raise SLDBStoreError(f"Repository id '{repo_id}' has no registered root path.")
        desk_root = entry.desk_root.resolve()
    if not desk_root.parent.is_dir():
        raise SLDBStoreError(
            f"Repository id '{repo_id}' is registered at '{desk_root.parent}', which does not exist "
            "on this machine. Fix its path in the registry (a '~/...' path resolves on every machine)."
        )
    return desk_root


def _ecosystem_entry(
    repo_id: str,
    local_entries: list[RegisteredRepository],
    local_registry_dir: Path | None,
) -> RegisteredRepository:
    registry_dir = ecosystem_registry_dir()
    is_local = local_registry_dir is not None and registry_dir.resolve() == local_registry_dir.resolve()
    entries = [] if is_local else load_ecosystem_registry()
    matches = [entry for entry in entries if entry.id == repo_id]
    if not matches:
        raise SLDBStoreError(
            _missing_repository_message(repo_id, [*local_entries, *entries], registry_dir=local_registry_dir)
            + f" The ecosystem registry at '{registry_dir}' does not list it either."
        )
    return resolve_registered_repo(entries, repo_id, registry_dir=registry_dir)


def _raise_on_duplicate_ids(entries: list[RegisteredRepository]) -> None:
    by_id: dict[str, list[RegisteredRepository]] = {}
    for entry in entries:
        by_id.setdefault(entry.id, []).append(entry)
    for repo_id, matches in by_id.items():
        if len(matches) > 1:
            raise SLDBStoreError(_duplicate_id_message(repo_id, matches))


def _raise_on_duplicate_roots(entries: list[RegisteredRepository]) -> None:
    by_root: dict[Path, list[RegisteredRepository]] = {}
    for entry in entries:
        if entry.repo_root is None:
            continue
        by_root.setdefault(entry.repo_root, []).append(entry)
    for root, matches in by_root.items():
        if len(matches) > 1:
            ids = ", ".join(f"{entry.id} [{entry.source_path}]" for entry in matches)
            raise SLDBStoreError(f"Duplicate repository root '{root}' in registry: {ids}.")


def _duplicate_id_message(repo_id: str, matches: list[RegisteredRepository]) -> str:
    locations = ", ".join(str(entry.source_path) for entry in matches)
    return f"Duplicate repository id '{repo_id}' in registry: {locations}."


def _missing_repository_message(repo_id: str, entries: list[RegisteredRepository], *, registry_dir: Path | None) -> str:
    registry_hint = f" at '{registry_dir}'" if registry_dir is not None else ""
    found = ", ".join(sorted(e.id for e in entries)) if entries else "none"
    return (
        f"Repository id '{repo_id}' not found in registry{registry_hint} (found: {found}). "
        "Supported path: run 'deskops repo register <name> --path <abs>' "
        "or add an entry to the ecosystem registry."
    )


def _unregistered_current_repo_message(repo_root: Path, *, registry_dir: Path | None) -> str:
    registry_hint = f" at '{registry_dir}'" if registry_dir is not None else ""
    return (
        f"Current repository root '{repo_root}' is not registered in the ecosystem registry{registry_hint}. "
        f"Supported path: run 'deskops repo register <name> --path {repo_root}' "
        "or add an entry to the ecosystem registry."
    )


def resolve_registered_root(ecosystem_root: Path, repo_path: str | None) -> Path | None:
    if not repo_path:
        return None
    candidate = Path(repo_path).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (ecosystem_root / candidate).resolve()


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
    except ValueError:
        return False
    return True

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

FILE:deskops/cli/commands/repo.py
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from sldb.cli.model_utils import registered_model
from sldb.cli.store_context import get_store_context
from sldb.api import transaction
from sldb.core.exceptions import SLDBStoreError, SLDBValidationError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.layout import project_root

from deskops import doc_access
from deskops.identity import load_repository_registry, EcosystemIdentity
from deskops.identity import find_local_store
from deskops.identity import resolve_registered_root


class RepoCLI:
    """Handle repository registration and discovery."""

    def run(self, args: Any) -> int:
        if args.repo_command == "register":
            return self.register(args)
        if args.repo_command == "whoami":
            return self.whoami(args)
        if args.repo_command == "remove":
            return self.remove(args)
        return 1

    def register(self, args: Any) -> int:
        name = args.name
        path = args.path_option or args.path
        if not path:
            print("Error: repository path is required. Use 'deskops repo register <name> --path <abs>' or provide the positional path.")
            return 1
        repo_id = args.id or self._slug(name)
        description = args.description or f"Repository for {name}."
        tags = [t.strip() for p in (args.tags or "").split(",") if (t := p.strip())]

        payload = {
            "name": name,
            "id": repo_id,
            "path": path,
            "status": "active",
            "description": description,
            "tags": tags,
        }

        # Preflight: resolve store context and model before any mutation
        try:
            store_path, root = self._store_context(args)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        try:
            model_type, entry, idx = registered_model(
                store_path, "RepositoryDoc", args.pythonpath
            )
        except SLDBStoreError:
            print("Error: RepositoryDoc model is not registered in the store.")
            print("Register it first with: python -m sldb models add deskops.models:RepositoryDoc --store <path>")
            return 1
        except (FileNotFoundError, OSError) as e:
            print(f"Error: cannot read store at {store_path}: {e}")
            return 1

        desk_root = self._desk_root(args)
        registry_dir = desk_root / "registry"
        filename = f"repo-{repo_id}.md"
        output_path = registry_dir / filename

        if output_path.exists():
            print(f"Error: Repository file already exists at {output_path}")
            return 1

        try:
            existing_entries = load_repository_registry(desk_root, root)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        resolved_repo_root = self._resolve_registered_root(root, path)
        for existing_entry in existing_entries:
            if existing_entry.id == repo_id:
                print(
                    f"Error: Repository id '{repo_id}' is already registered by {existing_entry.source_path}."
                )
                return 1
            if existing_entry.repo_root is not None and resolved_repo_root == existing_entry.repo_root:
                print(
                    "Error: Repository root "
                    f"'{resolved_repo_root}' is already registered as '{existing_entry.id}' by {existing_entry.source_path}."
                )
                return 1

        from sldb.store.io import load_models_index, load_documents_index
        models_idx = load_models_index(root / entry.models_index)
        docs_idx = load_documents_index(root / models_idx.documents_index)
        if any(d.name == f"repo-{repo_id}" for d in docs_idx.documents):
            print(f"Error: Repository repo-{repo_id} is already registered in the store.")
            return 1

        rendered = render_model_markdown(model_type, payload)
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            print("Error: Repository registration failed validation.")
            for issue in details:
                print(f"  - {issue}")
            return 1

        # All prerequisites verified: the file and its tracking in one transaction.
        with transaction(store_path, args.pythonpath) as tx:
            tx.write_file(output_path, (rendered + "\n").encode("utf-8"))
            print(f"Wrote {output_path}")
            tx.track(output_path, "RepositoryDoc", f"repo-{repo_id}")
        print(f"Tracked 'repo-{repo_id}'")

        return 0

    def remove(self, args: Any) -> int:
        root = Path(args.root).resolve()
        desk_root = root / "desk"
        try:
            entries = load_repository_registry(desk_root, root)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        selector = args.selector
        matches = [
            entry
            for entry in entries
            if selector in {entry.id, entry.source_path.stem, f"repo-{entry.id}"}
        ]
        if not matches:
            known = ", ".join(sorted(entry.id for entry in entries)) or "(none)"
            print(f"Error: Repository '{selector}' is not registered. Registered ids: {known}")
            return 1
        if len(matches) > 1:
            paths = ", ".join(str(entry.source_path) for entry in matches)
            print(f"Error: Repository selector '{selector}' is ambiguous: {paths}")
            return 1

        entry = matches[0]
        doc_access.delete_doc(root, entry.source_path)
        print(entry.source_path)
        return 0

    def whoami(self, args: Any) -> int:
        try:
            project_id = EcosystemIdentity(args.store).what_repository_am_i_in(Path(args.root), require_registry_match=True)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1
        print(project_id)
        return 0

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "repo"

    def _desk_root(self, args: Any) -> Path:
        if args.store:
            return (project_root(Path(args.store).resolve()) / "desk").resolve()
        local_store = find_local_store()
        if local_store is not None:
            return (project_root(local_store) / "desk").resolve()
        return (Path.cwd() / "desk").resolve()

    def _store_context(self, args: Any) -> tuple[Path, Path]:
        if args.store:
            try:
                return get_store_context(args.store)
            except (SLDBStoreError, FileNotFoundError, OSError) as e:
                raise SLDBStoreError(str(e))
        local_store = find_local_store()
        if local_store is None:
            raise SLDBStoreError("No store found to anchor the registry.")
        return local_store, project_root(local_store)

    def _resolve_registered_root(self, ecosystem_root: Path, repo_path: str) -> Path:
        return resolve_registered_root(ecosystem_root, repo_path)

FILE:tests/test_message_ecosystem_registry.py
"""`message send --to <repo>` resolves the target from the ecosystem registry.

MEPU (2026-11-15): `deskops message send --to deskops` did not resolve from another repo,
because only the sender's own ``desk/registry`` was read and MEPU's lists nobody. The
target is looked up first in the sender's registry and then in the ecosystem registry
(``~/setup/desk/registry``, or ``$DESKOPS_ECOSYSTEM_REGISTRY``). A registered root that does
not exist on this machine is an error and nothing is written.

The tests run the real CLI in subprocesses; ``HOME`` is the throwaway home of conftest, so
``~/setup`` is built inside it.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

from deskops.models import RepositoryDoc
from sldb.runtime.validation import render_model_markdown

ROOT = Path(__file__).resolve().parents[1]
# The CLI subprocess imports this checkout (and the sldb conftest put on sys.path), not
# whatever deskops the interpreter has installed.
_PYTHONPATH = os.pathsep.join([str(ROOT), *(p for p in sys.path if p)])


def _cli(cwd: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv],
        cwd=cwd,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": _PYTHONPATH, **(env or {})},
    )


def _init_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    result = _cli(path, "init", str(path))
    assert result.returncode == 0, result.stderr or result.stdout
    return path


def _register(registry_dir: Path, repo_id: str, repo_path: str) -> None:
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


def _home() -> Path:
    return Path(os.environ["HOME"])


def _inbox(repo: Path) -> list[Path]:
    return sorted((repo / "desk" / "inbox").glob("*.md"))


def _send(sender: Path, to: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return _cli(
        sender, "message", "send", "Hola desde otro repo.", "--title", "Hola", "--to", to,
        "--format", "json", env=env,
    )


def test_send_to_repo_missing_from_sender_registry_uses_ecosystem_registry(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "mepu")
    target = _init_repo(_home() / "proyectos" / "SLDB_1" / "deskops")
    # The ecosystem registry names the target with a '~' path, valid on every machine.
    _register(_home() / "setup" / "desk" / "registry", "deskops", "~/proyectos/SLDB_1/deskops")
    assert not (sender / "desk" / "registry").exists() or not list((sender / "desk" / "registry").glob("repo-*.md"))

    result = _send(sender, "deskops")

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert Path(payload["path"]).parent == (target / "desk" / "inbox").resolve()
    assert len(_inbox(target)) == 1
    assert _inbox(sender) == []


def test_send_from_repo_without_store_uses_ecosystem_registry(tmp_path: Path) -> None:
    sender = tmp_path / "plain-repo"
    (sender / ".git").mkdir(parents=True)
    target = _init_repo(tmp_path / "sldb")
    registry = _home() / "setup" / "desk" / "registry"
    _register(registry, "sldb", str(target))
    # Neither store nor desk config: the ecosystem registry names the sender too.
    _register(registry, "plain-repo", str(sender))

    result = _send(sender, "sldb")

    assert result.returncode == 0, result.stderr or result.stdout
    assert json.loads(result.stdout)["sender_project"] == "plain-repo"
    assert len(_inbox(target)) == 1


def test_sender_registry_wins_over_ecosystem_registry(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender")
    local_target = _init_repo(tmp_path / "local-spec2viz")
    other_target = _init_repo(tmp_path / "other-spec2viz")
    _register(sender / "desk" / "registry", "spec2viz", str(local_target))
    _register(_home() / "setup" / "desk" / "registry", "spec2viz", str(other_target))

    result = _send(sender, "spec2viz")

    assert result.returncode == 0, result.stderr or result.stdout
    assert len(_inbox(local_target)) == 1
    assert _inbox(other_target) == []


def test_registry_dir_comes_from_environment(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender")
    target = _init_repo(tmp_path / "target")
    registry = tmp_path / "eco" / "desk" / "registry"
    # Relative paths resolve against the root of the repo that holds the registry.
    _register(registry, "target", "../target")

    result = _send(sender, "target", env={"DESKOPS_ECOSYSTEM_REGISTRY": str(registry)})

    assert result.returncode == 0, result.stderr or result.stdout
    assert len(_inbox(target)) == 1


def test_root_missing_on_this_machine_is_an_error_and_writes_nothing(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender")
    elsewhere = tmp_path / "other-machine" / "mepu"
    _register(_home() / "setup" / "desk" / "registry", "mepu", str(elsewhere))

    result = _send(sender, "mepu")

    assert result.returncode != 0
    assert "does not exist on this machine" in (result.stdout + result.stderr)
    assert not elsewhere.exists()
    assert _inbox(sender) == []


def test_unknown_repo_names_both_registries(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender")
    _register(_home() / "setup" / "desk" / "registry", "sldb", str(tmp_path / "sldb"))

    result = _send(sender, "ghost")

    assert result.returncode != 0
    output = result.stdout + result.stderr
    assert "Repository id 'ghost' not found" in output
    assert "ecosystem registry" in output
    assert "sldb" in output

FILE:instruccion
Cold-bundle de la tarea task-message-send-to-resuelve-el-destino-en-el-registro-del-ecosistema-cuando-el-registro-propio-no-lo-li: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm python -m pytest -q -p no:cacheprovider tests/test_message_ecosystem_registry.py


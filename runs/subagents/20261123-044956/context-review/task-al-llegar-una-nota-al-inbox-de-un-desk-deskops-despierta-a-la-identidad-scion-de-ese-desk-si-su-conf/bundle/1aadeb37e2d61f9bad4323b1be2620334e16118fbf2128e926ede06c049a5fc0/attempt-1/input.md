FILE:desk/tasks/task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf.md
---
sldb:
  by: agent
  at: '2026-11-23T04:37:52Z'
  authority: generated
  via: create_document
id: task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-234436-suggestion-hook-que-despierta-a-la-identidad-scion-del-desk-cuando-llega-una-nota-al-inbox.md
depends_on: []
pills: []
files:
- deskops/config.py
- deskops/cli/commands/message.py
- deskops/queue.py
- tests/test_message_delivery.py
- tests/test_config.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Al llegar una nota al inbox de un desk, deskops despierta a la identidad scion de ese desk si su config lo pide (identity.wake), respetando el gate de memoria

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-234436 (scion-coordination, encargo de JP para el workflow scion + deskops): JP pidió "uno por desk, pero en scion y se activa por hook en deskops"; la identidad queda parada por defecto y se despierta cuando le llega trabajo. Hoy nada avisa: deskops message send (MessageCLI._deliver_note en deskops/cli/commands/message.py) solo escribe la nota, y los hooks de deskops/lifecycle_hooks.py corren solo al avanzar una transición. Es la pieza de activación de task-governance-agente-interno-por-desk-en-scion-activado-por-hooks-de-deskops (el paraguas, todavía borrador); esta tarea no la duplica: hace solo el disparo por nota.

## Goal

_Describe the concrete result this task must produce._

(1) DeskConfig (deskops/config.py) gana un campo opcional identity con: scion_project (str), agent (str), wake (bool, por defecto false) y command (lista de argv opcional con los marcadores {agent}, {project} y {note}; por defecto ["scion", "message", "--wake", "@{agent}", "--project", "{project}", "nota nueva: {note}"]). Se espera que viva en el config.local.json del desk (es de la máquina), que DeskConfig.load ya mezcla sobre config.json. (2) Una función wake_identity(root, note_name) en un módulo nuevo de deskops: si identity falta o wake es false no hace nada; si deskops.queue.wait_reason(config) da un motivo, no despierta y devuelve "bloqueado: <motivo>"; si no, corre el argv sin shell (stdin DEVNULL, timeout 60 s) y devuelve "despertado" o "fallo: <rc>". (3) Después de escribir la nota en el desk destino, deskops message send llama a wake_identity con la raíz del desk destino. Un fallo o un bloqueo nunca hace fallar el send: se imprime un aviso en stderr. Si quedó bloqueado y el desk destino declara en queue_jobs el tipo wake-identity, se encola con deskops.queue.enqueue para el siguiente ciclo de la cola. (4) Un subcomando deskops message wake --root <desk> [--note <id>] corre wake_identity a mano y sale con código 3 cuando el gate bloquea (para que la cola lo reintente con retry_exit_codes [3]).

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/config.py, deskops/cli/commands/message.py, el módulo nuevo, sus goldens de ayuda, tests/test_message_delivery.py y tests/test_config.py. No entra: arreglar --wake en el fork de scion (nota 20261122-233912 del desk de scion; hoy --wake falla, así que el uso real espera ese arreglo, pero la implementación y los tests no), el límite de 5 agentes vivos (lo controla el despacho), crear el RoleDoc de identidad (tarea aparte), lanzar scion de verdad en los tests.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_message_delivery.py con un command falso ["sh", "-c", "echo \"$0 $1\" >> <archivo>", "{agent}", "{note}"] en el config.local.json de un desk temporal: test_send_wakes_the_target_identity (el archivo recibe el agente y el nombre de la nota), test_send_does_not_wake_when_wake_is_false, test_send_with_memory_gate_blocked_enqueues_wake_identity (wait_reason parcheado; el send termina con rc 0 y queda un trabajo wake-identity pendiente), test_wake_command_exits_3_when_blocked. p2: test en tests/test_config.py: DeskConfig.load toma identity del config.local.json. p3: implementar. p4: goldens de ayuda. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_delivery.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_config.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los cinco tests nuevos pasan; deskops message send en un desk sin identity se comporta igual que hoy (los tests existentes de tests/test_message_delivery.py y tests/test_message_cli.py siguen verdes sin cambios).

FILE:deskops/config.py
from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

from typing import Literal

from pydantic import BaseModel, Field

from deskops.constants import CURRENT_DESK_FORMAT


class SandboxPolicy(BaseModel):
    enabled: bool = False
    sandbox_root: str | None = None


class VersionExpectations(BaseModel):
    desk_format: str = CURRENT_DESK_FORMAT
    model_version: str = "1.0.0"


class QueueJob(BaseModel):
    run: list[str] = Field(min_length=1, description="argv executed without a shell")
    timeout: int = Field(default=3600, gt=0, description="Seconds before the job is killed")
    retry_exit_codes: list[int] = Field(
        default_factory=list,
        description="Exit codes that leave the job pending for the next run instead of failing it",
    )


class IntegrateConfig(BaseModel):
    remote_url: str = Field(min_length=1, description="URL or path of the remote that receives the push")
    branch: str = Field(min_length=1, description="Remote branch that receives the code commit and the tip")
    suite: list[str] = Field(min_length=1, description="argv of the full suite, run in the clean copy")
    suite_timeout: int = Field(default=5400, gt=0, description="Seconds before the suite is killed")
    tests_lock: str | None = Field(default=None, description="Lock file taken exclusively around the suite")
    tools_checkout: str | None = Field(default=None, description="Tools checkout updated after the push")
    push_env: dict[str, str] = Field(default_factory=dict, description="Environment added to the git push and gh commands")
    mode: Literal["push", "pr"] = Field(
        default="push",
        description="'push' pushes the tip to the branch; 'pr' pushes task/<id> and opens a PR to the branch",
    )


class DispatchRole(BaseModel):
    role: str = Field(min_length=1, description="RoleDoc id or name")
    harness: str = Field(min_length=1, description="Runtime profile kind / scion harness")
    model_alias: str = Field(min_length=1, description="Scion model size alias")
    harness_auth: str | None = Field(default=None, description="Scion harness auth type")
    env_config: str | None = Field(default=None, description="Path passed to scion start --config")


class DispatchRoles(BaseModel):
    executor: DispatchRole
    tester: DispatchRole


class DispatchConfig(BaseModel):
    project: str = Field(min_length=1, description="Scion project")
    workspace: str = Field(min_length=1, description="Absolute workspace path")
    templates_dir: str = Field(min_length=1, description="Scion project templates folder")
    context_file: str = Field(min_length=1, description="Scion context JSON path")
    roles: DispatchRoles
    roles_root: str | None = Field(
        default=None,
        description="Repo whose desk/roles holds the RoleDocs; default is the task root. Relative paths resolve against the task root.",
    )
    quick_gates: list[str] | None = Field(
        default=None,
        description="Optional argv of the fast gates the executor and the tester must run (rc 0) before the commit and the verdict.",
    )


class DeskConfig(BaseModel):
    project_identity: str = Field(default="unknown-project", description="Canonical project desk identity")
    versions: VersionExpectations = Field(default_factory=VersionExpectations)
    sandbox: SandboxPolicy = Field(default_factory=SandboxPolicy)
    atom_folder_axis: str | None = Field(
        default=None,
        description="Tag namespace used as the physical folder axis for atoms under desk/atoms/. Null keeps flat layout.",
    )
    queue_jobs: dict[str, QueueJob] = Field(
        default_factory=dict,
        description="Host queue job kinds: kind -> {run: argv, timeout: seconds}.",
    )
    dispatch: DispatchConfig | None = Field(
        default=None,
        description="deskops dispatch: scion project, workspace, templates and per-role launch settings.",
    )
    integrate: IntegrateConfig | None = Field(
        default=None,
        description="deskops integrate: remote, branch, suite and tools checkout of the integration.",
    )
    queue_min_available_gb: int = Field(default=8, description="Minimum MemAvailable (GB) to start a queued job.")
    queue_max_psi_avg60: float = Field(default=10, description="Memory PSI some avg60 at or above which jobs wait.")
    load_warnings: list[str] = Field(default_factory=list, exclude=True)

    @property
    def has_load_warnings(self) -> bool:
        return bool(self.load_warnings)

    @classmethod
    def load(cls, desk_root: Path) -> "DeskConfig":
        merged_data: dict[str, Any] = {}
        load_warnings: list[str] = []

        for config_path in (desk_root / "config.json", desk_root / "config.local.json"):
            file_data = _load_json_object(config_path, load_warnings)
            if file_data is None:
                continue
            merged_data = _deep_merge_dicts(merged_data, file_data)

        return cls(**merged_data, load_warnings=load_warnings)


def _load_json_object(path: Path, load_warnings: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        message = f"Failed to parse desk config {path}: {exc.msg}"
        load_warnings.append(message)
        warnings.warn(message, stacklevel=2)
        return None

    if not isinstance(data, dict):
        message = f"Desk config {path} must contain a JSON object at the top level."
        load_warnings.append(message)
        warnings.warn(message, stacklevel=2)
        return None

    return data


def _deep_merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = dict(base)
    for key, override_value in override.items():
        base_value = merged.get(key)
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            merged[key] = _deep_merge_dicts(base_value, override_value)
        else:
            merged[key] = override_value
    return merged

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

FILE:deskops/queue.py
"""Host job queue: `deskops queue {add|run|list}`.

Post-hooks that run inside a container enqueue heavy jobs (full suite,
integration, push) as JSON files under ``<root>/runs/queue``; a runner on the
host takes them one at a time. A state change is an ``os.replace`` between the
state folders, so a job is always in exactly one of them.
"""

from __future__ import annotations

import contextlib
import fcntl
import io
import json
import os
import signal
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterator

from deskops.cli.render import render
from deskops.config import DeskConfig
from deskops.errors import UsageError

STATES = ("pending", "running", "done", "failed")
LOCK_NAME = "run.lock"
_MEMINFO = Path("/proc/meminfo")
_PRESSURE = Path("/proc/pressure/memory")


def queue_dir(root: Path) -> Path:
    return root / "runs" / "queue"


def _ensure_dirs(queue: Path) -> None:
    for name in (*STATES, "logs"):
        (queue / name).mkdir(parents=True, exist_ok=True)


def _load_config(root: Path) -> DeskConfig:
    return DeskConfig.load(root / "desk")


def _write_job(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def _read_job(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def enqueue(root: Path, kind: str, task_id: str | None, transition: str | None) -> str:
    config = _load_config(root)
    if kind not in config.queue_jobs:
        declared = ", ".join(sorted(config.queue_jobs)) or "(none)"
        raise UsageError(f"Unknown queue job kind '{kind}'. Declared kinds: {declared}")
    task_id = (task_id or os.environ.get("DESKOPS_TASK_ID", "")).strip()
    if not task_id:
        raise UsageError("queue add needs --task or DESKOPS_TASK_ID.")
    transition = (transition if transition is not None else os.environ.get("DESKOPS_TRANSITION", "")).strip()

    queue = queue_dir(root)
    _ensure_dirs(queue)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    while True:
        job_id = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{kind}-{task_id}"
        path = queue / "pending" / f"{job_id}.json"
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        except FileExistsError:
            now = now + timedelta(seconds=1)
            continue
        os.close(fd)
        break
    _write_job(
        path,
        {
            "id": job_id,
            "kind": kind,
            "task_id": task_id,
            "transition": transition,
            "enqueued_at": now.isoformat().replace("+00:00", "Z"),
        },
    )
    return job_id



def _jobs(queue: Path, state: str) -> list[Path]:
    folder = queue / state
    return sorted(folder.glob("*.json")) if folder.is_dir() else []


def _memory_state() -> tuple[float | None, float | None]:
    """(MemAvailable in GB, memory PSI some avg60); None when unreadable."""
    available = None
    try:
        for line in _MEMINFO.read_text(encoding="utf-8").splitlines():
            if line.startswith("MemAvailable:"):
                available = int(line.split()[1]) / (1024 * 1024)
                break
    except (OSError, ValueError, IndexError):
        pass
    avg60 = None
    try:
        for line in _PRESSURE.read_text(encoding="utf-8").splitlines():
            if line.startswith("some "):
                for part in line.split()[1:]:
                    if part.startswith("avg60="):
                        avg60 = float(part.split("=", 1)[1])
    except (OSError, ValueError):
        pass
    return available, avg60


def wait_reason(config: DeskConfig) -> str | None:
    available, avg60 = _memory_state()
    if available is not None and available < config.queue_min_available_gb:
        return f"memoria disponible {available:.1f} GB < minimo {config.queue_min_available_gb} GB"
    if avg60 is not None and avg60 >= config.queue_max_psi_avg60:
        return f"presion de memoria avg60 {avg60:.2f} >= maximo {config.queue_max_psi_avg60:g}"
    return None


def _notify_failure(root: Path, job: dict[str, Any], *, interrupted: bool) -> None:
    """Leave an inbox note with the function behind `deskops message send`."""
    from deskops.cli.commands.message import MessageCLI

    if interrupted:
        body = f"Trabajo {job['id']} interrumpido. Tipo: {job['kind']}. Tarea: {job['task_id']}."
    else:
        code = "timeout" if job.get("timeout") else job.get("exit_code")
        body = (
            f"Tipo: {job['kind']}. Tarea: {job['task_id']}. "
            f"Codigo de salida: {code}. Log: {job.get('log')}"
        )
    args = SimpleNamespace(
        title=f"queue: {job['id']}",
        message=body,
        kind="unclear",
        root=str(root),
        desk_root=None,
        repo=None,
        store=None,
        pythonpath=None,
        sender=None,
        format="json",
    )
    cwd = os.getcwd()
    try:
        os.chdir(root)
        with contextlib.redirect_stdout(io.StringIO()):
            MessageCLI()._deliver_note(args)
    except Exception as exc:  # the job already failed; a lost note must not hide that
        print(f"Warning: could not leave the inbox note for {job['id']}: {exc}", file=sys.stderr)
    finally:
        os.chdir(cwd)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _recover_interrupted(root: Path, queue: Path) -> None:
    for path in _jobs(queue, "running"):
        job = _read_job(path)
        job.update({"ended_at": _now(), "exit_code": None, "interrupted": True})
        _write_job(path, job)
        os.replace(path, queue / "failed" / path.name)
        _notify_failure(root, job, interrupted=True)


def _execute(root: Path, queue: Path, config: DeskConfig, path: Path) -> str:
    """Run one pending job; "ok", "failed" or "retry" (back to pending, exit code in retry_exit_codes)."""
    running = queue / "running" / path.name
    os.replace(path, running)
    job = _read_job(running)
    spec = config.queue_jobs.get(job["kind"])
    log_path = queue / "logs" / f"{job['id']}.log"
    job["started_at"] = _now()
    job["log"] = str(log_path)
    code: int | None = None
    if spec is None:
        log_path.write_text(f"queue kind '{job['kind']}' is no longer declared in queue_jobs\n", encoding="utf-8")
        code = 127
    else:
        env = dict(os.environ)
        env.update(
            DESKOPS_ROOT=str(root),
            DESKOPS_TASK_ID=job["task_id"],
            DESKOPS_TRANSITION=job.get("transition", ""),
            DESKOPS_JOB_ID=job["id"],
            DESKOPS_JOB_KIND=job["kind"],
        )
        with log_path.open("wb") as log:
            try:
                proc = subprocess.Popen(
                    spec.run, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL, start_new_session=True,
                )
            except OSError as exc:
                log.write(f"cannot start {spec.run}: {exc}\n".encode())
                code = 127
            else:
                try:
                    code = proc.wait(timeout=spec.timeout)
                except subprocess.TimeoutExpired:
                    with contextlib.suppress(ProcessLookupError):
                        os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
                    job["timeout"] = True
                    code = None
    job["ended_at"] = _now()
    if not job.get("timeout"):
        job["exit_code"] = code
    ok = code == 0
    if spec is not None and not ok and not job.get("timeout") and code in spec.retry_exit_codes:
        for key in ("started_at", "ended_at", "exit_code", "log"):
            job.pop(key, None)
        job["attempts"] = int(job.get("attempts", 0)) + 1
        _write_job(running, job)
        os.replace(running, path)
        return f"retry:{code}"
    _write_job(running, job)
    os.replace(running, queue / ("done" if ok else "failed") / path.name)
    if not ok:
        _notify_failure(root, job, interrupted=False)
    return "ok" if ok else "failed"


@contextlib.contextmanager
def _try_lock(queue: Path) -> Iterator[bool]:
    with (queue / LOCK_NAME).open("a+") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def run_queue(root: Path, run_all: bool) -> int:
    queue = queue_dir(root)
    _ensure_dirs(queue)
    config = _load_config(root)
    with _try_lock(queue) as locked:
        if not locked:
            print("ocupado: otro queue run en curso")
            return 0
        _recover_interrupted(root, queue)
        waiting: set[str] = set()  # jobs left pending in this run; not retried until the next one
        while True:
            pending = [p for p in _jobs(queue, "pending") if p.stem not in waiting]
            if not pending:
                print("sin trabajos" if not waiting else "sin trabajos ejecutables: todos en espera")
                return 0
            reason = wait_reason(config)
            if reason:
                print(f"en espera: {reason}")
                return 0
            path = pending[0]
            print(f"ejecutando {path.stem}")
            outcome = _execute(root, queue, config, path)
            if outcome.startswith("retry:"):
                print(f"en espera: {path.stem} ocupado (exit {outcome.split(':', 1)[1]})")
                if not run_all:
                    return 0
                waiting.add(path.stem)
                continue
            if outcome == "failed":
                print(f"fallo {path.stem}")
                return 1
            print(f"listo {path.stem}")
            if not run_all:
                return 0


def set_job_field(root: Path, job: str, field: str, raw_value: str) -> str:
    """Set one field of a queue_jobs entry in ``desk/config.json``; nothing else in the file changes.

    ``raw_value`` is parsed as JSON (``[3]``, ``600``, ``["sh", "-c", "x"]``) and falls back to a plain string.
    The edited config must still validate as a DeskConfig, otherwise the file is left untouched.
    """
    from pydantic import ValidationError

    from deskops.config import QueueJob

    config_path = root / "desk" / "config.json"
    if not config_path.is_file():
        raise UsageError(f"No desk/config.json under {root}")
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise UsageError(f"desk/config.json is not valid JSON: {exc.msg}") from exc
    jobs = data.get("queue_jobs") if isinstance(data, dict) else None
    if not isinstance(jobs, dict) or job not in jobs or not isinstance(jobs[job], dict):
        declared = ", ".join(sorted(jobs)) if isinstance(jobs, dict) else "(none)"
        raise UsageError(f"Unknown queue job '{job}' in desk/config.json. Declared: {declared or '(none)'}")
    fields = sorted(QueueJob.model_fields)
    if field not in fields:
        raise UsageError(f"Unknown queue job field '{field}'. Valid fields: {', '.join(fields)}")
    try:
        value = json.loads(raw_value)
    except json.JSONDecodeError:
        value = raw_value
    updated = dict(jobs[job])
    updated[field] = value
    try:
        QueueJob.model_validate(updated)
    except ValidationError as exc:
        first = exc.errors()[0]
        raise UsageError(f"Invalid value for {job}.{field}: {first['msg']}") from exc
    jobs[job] = updated
    config_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return f"{job}.{field} = {json.dumps(value, ensure_ascii=False)}"


def list_jobs(root: Path) -> dict[str, list[dict[str, Any]]]:
    queue = queue_dir(root)
    result: dict[str, list[dict[str, Any]]] = {}
    for state in STATES:
        items = []
        for path in _jobs(queue, state):
            job = _read_job(path)
            job["state"] = state
            items.append(job)
        result[state] = items
    return result


class QueueCLI:
    """`deskops queue {add|run|list|job set}`; the subcommand is required."""

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        cmd = args.queue_command
        if cmd == "add":
            print(enqueue(root, args.kind, args.task, args.transition))
            return 0
        if cmd == "run":
            return run_queue(root, bool(args.all))
        if cmd == "job" and args.queue_job_command == "set":
            print(set_job_field(root, args.job, args.field, args.value))
            return 0
        if cmd == "list":
            return render(list_jobs(root), args.format, _format_list)
        raise UsageError(f"Unknown queue command: {cmd}")


def _format_list(data: dict[str, list[dict[str, Any]]]) -> str:
    lines: list[str] = []
    for state in STATES:
        lines.append(f"{state} ({len(data[state])})")
        for job in data[state]:
            extra = ""
            if state in ("done", "failed"):
                extra = " | timeout" if job.get("timeout") else f" | exit {job.get('exit_code')}"
            lines.append(f"  {job['id']} | {job['kind']} | {job['task_id']}{extra}")
    return "\n".join(lines)

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

FILE:tests/test_config.py
from pathlib import Path

import pytest

from deskops.config import DeskConfig
from deskops.constants import CURRENT_DESK_FORMAT

def test_load_desk_config_defaults(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    config = DeskConfig.load(desk)
    assert config.project_identity == "unknown-project"
    assert config.versions.desk_format == CURRENT_DESK_FORMAT
    assert not config.sandbox.enabled

def test_load_desk_config_from_json(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('''
    {
        "project_identity": "test-repo",
        "sandbox": {
            "enabled": true,
            "sandbox_root": "/tmp/test"
        }
    }
    ''')
    config = DeskConfig.load(desk)
    assert config.project_identity == "test-repo"
    assert config.sandbox.enabled is True
    assert config.sandbox.sandbox_root == "/tmp/test"

def test_load_desk_config_local_override(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('''
    {
        "project_identity": "test-repo",
        "sandbox": {
            "enabled": false,
            "sandbox_root": "/tmp/test"
        }
    }
    ''')
    (desk / "config.local.json").write_text('''
    {
        "sandbox": {
            "enabled": true
        }
    }
    ''')
    config = DeskConfig.load(desk)
    assert config.project_identity == "test-repo"
    assert config.sandbox.enabled is True
    assert config.sandbox.sandbox_root == "/tmp/test"


def test_load_desk_config_deep_merges_nested_versions(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('''
    {
        "versions": {
            "desk_format": "1.0.0",
            "model_version": "1.0.0"
        }
    }
    ''')
    (desk / "config.local.json").write_text('''
    {
        "versions": {
            "model_version": "2.0.0"
        }
    }
    ''')

    config = DeskConfig.load(desk)

    assert config.versions.desk_format == CURRENT_DESK_FORMAT
    assert config.versions.model_version == "2.0.0"


def test_load_desk_config_surfaces_malformed_json_warning(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('{"sandbox": {"enabled": true}')

    with pytest.warns(UserWarning, match="Failed to parse desk config"):
        config = DeskConfig.load(desk)

    assert config.has_load_warnings is True
    assert config.load_warnings
    assert config.sandbox.enabled is False

FILE:instruccion
Cold-bundle de la tarea task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_delivery.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_config.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)


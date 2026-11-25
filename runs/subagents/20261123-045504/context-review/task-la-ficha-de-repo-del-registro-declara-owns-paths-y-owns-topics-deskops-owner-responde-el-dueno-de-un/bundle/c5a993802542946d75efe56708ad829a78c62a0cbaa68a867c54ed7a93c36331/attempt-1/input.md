FILE:desk/tasks/task-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-deskops-owner-responde-el-dueno-de-un.md
---
sldb:
  by: agent
  at: '2026-11-23T04:38:22Z'
  authority: generated
  via: create_document
id: task-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-deskops-owner-responde-el-dueno-de-un
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-234458-suggestion-mapa-de-propiedad-por-desk-y-destino-unico-de-lo-sin-dueno-governance-en-el-registro.md
- desk/atoms/atom-sin-dueno-lo-que-no-tiene-dueno-en-sldb-1-va-al-inbox-de-deskops.md
depends_on: []
pills: []
files:
- deskops/models/repository.py
- deskops/config.py
- deskops/cli/commands/repo.py
- deskops/cli/commands/message.py
- tests/test_message_ecosystem_registry.py
- tests/test_config.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La ficha de repo del registro declara owns_paths y owns_topics, deskops owner responde el dueño de una ruta o tema, y message send --to unowned va al destino de config unowned_target

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-234458 (scion-coordination, workflow scion + deskops de JP): no hay dónde declarar qué rutas y temas son de cada desk ni a dónde va lo que no es de nadie. Caso real: heyantonia/mepu#459, dos notas que eran de etlkit (shared_etl-plataforma) quedaron en tareas de mepu. El piloto registró un acuerdo provisional en atom-sin-dueno-lo-que-no-tiene-dueno-en-sldb-1-va-al-inbox-de-deskops (JP no lo confirmó; por eso el destino va en config y no en código).

## Goal

_Describe the concrete result this task must produce._

(1) RepositoryDoc (deskops/models/repository.py) gana owns_paths (lista de globs relativos a la raíz del ecosistema, por defecto vacía) y owns_topics (lista de strings, por defecto vacía); deskops repo register acepta --owns-paths y --owns-topics separados por coma. (2) deskops owner <ruta|tema> --root . responde el id del repo dueño: para una ruta, el repo con el glob más largo que la cubre (y, si ninguno, el repo cuya raíz contiene la ruta); para un tema, el repo que lo lista en owns_topics; si nadie, imprime "sin dueno" y sale con código 1; si dos repos empatan, los lista y sale con código 2. (3) DeskConfig gana unowned_target (id de repo registrado, opcional); deskops message send --to unowned entrega al repo de unowned_target, y si no está configurado falla con "unowned_target no configurado en desk/config.json ni en config.local.json".

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/models/repository.py, deskops/config.py, deskops/cli/commands/repo.py, deskops/cli/commands/message.py, el comando owner, goldens de ayuda y de contrato del modelo, tests/test_message_ecosystem_registry.py y tests/test_config.py. No entra: registrar Governance (project_identity repo-governance, heyantonia/Governance) en el registro (lo hace quien coordina el registro con deskops repo register, después de esta tarea), fijar el valor de unowned_target (lo confirma JP), llenar owns_paths de cada repo.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_message_ecosystem_registry.py sobre un ecosistema temporal con dos repos registrados: test_owner_resolves_path_by_longest_glob, test_owner_resolves_topic, test_owner_without_owner_exits_1, test_owner_tie_exits_2, test_send_to_unowned_uses_unowned_target, test_send_to_unowned_without_config_fails. p2: test en tests/test_config.py de unowned_target en config.local.json. p3: implementar. p4: goldens (ayuda y contrato de RepositoryDoc) y sldb models update del modelo en el store del desk. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_ecosystem_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_config.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los siete tests nuevos pasan y las fichas de desk/registry existentes siguen cargando sin cambios (owns_* vacíos por defecto).

FILE:deskops/models/repository.py
from typing import Optional

from pydantic import Field

from sldb import StructuredNLDoc


class RepositoryDoc(StructuredNLDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "repo-{slug}",
        "status_default": "active",
        "tags": ["workspace:desk", "artifact:repository"],
    }
    """Model for registering a repository/tool within the opsys ecosystem."""

    __semantics__ = {
        "type": ["desk", "repository"],
        "workspace": ["desk", "registry"],
    }
    __template__ = """---
# repo-xxx
id: ⸢rev•id⸥
# Relative path to repository
path: ⸢rev•path⸥
# active | maintenance | archived
status: ⸢rev•status⸥
# e.g., type:tool, layer:infra
tags: ⸢rev•tags⸥
---

# Repository: ⸢rev•name⸥

## Description

_Describe the repository purpose, scope, and role in the ecosystem._

⸢rev,markdown•description⸥
"""

    name: str = Field(description="Short human-readable name of the repository.")
    id: Optional[str] = Field(
        default=None,
        description="Stable unique identifier for the repository."
    )
    path: Optional[str] = Field(
        default=None,
        description="Relative path to the repository root from the ecosystem root."
    )
    status: str = Field(
        default="active",
        description="Current status of the repository (e.g., active, maintenance, archived).",
    )
    description: str = Field(description="Markdown description of the repository's purpose and scope.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags for categorization (e.g., type:tool, layer:infra).",
    )

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

FILE:deskops/cli/commands/repo.py
from __future__ import annotations

import os
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

        # Preflight: resolve store context and model before any mutation
        try:
            store_path, root = self._store_context(args)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        desk_root = self._desk_root(args)
        registry_dir = desk_root / "registry"
        resolved_repo_root = self._resolve_registered_root(root, path)
        payload = {
            "name": name,
            "id": repo_id,
            # Stored relative to the root of the repo that holds the registry directory
            # (desk/registry -> the desk's repo, ~/setup/desk/registry -> ~/setup), so the
            # entry resolves on any machine that checks the ecosystem out side by side.
            "path": self._registry_relative_path(registry_dir, resolved_repo_root),
            "status": "active",
            "description": description,
            "tags": tags,
        }

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

    def _registry_relative_path(self, registry_dir: Path, repo_root: Path) -> str:
        """``repo_root`` relative to the repo containing ``registry_dir`` (its grandparent)."""
        registry_repo_root = registry_dir.resolve().parent.parent
        return Path(os.path.relpath(repo_root, registry_repo_root)).as_posix()

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
Cold-bundle de la tarea task-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-deskops-owner-responde-el-dueno-de-un: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_ecosystem_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_config.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)


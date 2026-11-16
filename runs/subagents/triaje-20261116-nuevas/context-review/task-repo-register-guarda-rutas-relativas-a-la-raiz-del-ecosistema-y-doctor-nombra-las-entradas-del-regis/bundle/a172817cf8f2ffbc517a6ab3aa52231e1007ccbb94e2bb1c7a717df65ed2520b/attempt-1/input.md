FILE:desk/tasks/task-repo-register-guarda-rutas-relativas-a-la-raiz-del-ecosistema-y-doctor-nombra-las-entradas-del-regis.md
---
sldb:
  by: agent
  at: '2026-11-16T06:10:57Z'
  authority: generated
  via: create_document
id: task-repo-register-guarda-rutas-relativas-a-la-raiz-del-ecosistema-y-doctor-nombra-las-entradas-del-regis
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-012947-suggestion-registro-del-ecosistema-con-rutas-de-otra-m-quina-lo-de-sldb-est-resuelto-a2bfdf91-queda-doctor-en-deskops.md
depends_on: []
pills: []
files:
- deskops/cli/commands/repo.py
- deskops/doc_access.py
- deskops/cli/commands/doctor.py
- tests/test_repo_identity.py
- tests/test_registry_robustness.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# repo register guarda rutas relativas a la raiz del ecosistema y doctor nombra las entradas del registro que no resuelven

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de sldb del 2026-11-16 (de una nota de mepu): el registro del ecosistema guarda rutas absolutas de la maquina que registra (desde robocop2 queda /mnt/ssd/..., que se rompe en la laptop; en ~/setup/desk/registry varias entradas apuntan a /home/jp/... que no existe en robocop2). sldb ya lo corrigio en su propio registro (a2bfdf91: path ., ../deskops, ../UIs/graph_ui). En deskops quedan dos cosas: deskops repo register (deskops/cli/commands/repo.py, metodo register alrededor de la linea 32) guarda la ruta absoluta, y deskops doctor solo dice 'the linked store is missing' cuando una entrada del registro no resuelve.

## Goal

_Describe the concrete result this task must produce._

(1) `deskops repo register` guarda en path la ruta relativa a la raiz del repo que contiene el registro donde escribe (desk/registry del desk, o ~/setup/desk/registry para el del ecosistema, con ~ expandido solo al resolver), y acepta leer entradas viejas con ruta absoluta o con ~. (2) `deskops doctor` reporta, por cada entrada del registro del desk cuyo path no resuelve en esta maquina, un hallazgo con el id del repo, el path guardado y la ruta resuelta, ademas del mensaje actual del store enlazado.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/repo.py, deskops/doc_access.py (registered_repositories, alrededor de la linea 934) o el modulo que resuelva rutas del registro, deskops/cli/commands/doctor.py y tests (tests/test_repo_identity.py, tests/test_registry_robustness.py). No entra: reescribir entradas existentes de ~/setup (lo hace su dueño con el CLI nuevo), cambiar el formato de RepositoryDoc.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer repo.py, registered_repositories y deskops/identity.py (resolve_registered_root). 2) register calcula os.path.relpath(destino, raiz_del_registro). 3) doctor recorre registered_repositories y agrega el hallazgo. 4) Tests: register desde un sandbox guarda ruta relativa; una entrada con ruta absoluta inexistente da el hallazgo en doctor; una entrada vieja absoluta valida sigue resolviendo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_repo_identity.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_registry_robustness.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_ecosystem_registry.py
- {'cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas': 'cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea'}

## Done When

_Name the observable condition that makes the task complete._

Los tres casos del paso 4 pasan y los tests de registro existentes siguen verdes.

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

FILE:deskops/doc_access.py
"""Reading, writing and resolving the documents of one desk.

Every function takes the repository ``root`` (the directory that holds ``desk/``) and
works on the desk documents under it: parse a document into its model payload, write
one through ``sldb.api.transaction``, resolve a selector to a file, read a task with
its inherited context, or list the artifacts of one kind. ``DeskopsOperations`` is a
facade over these functions and the services; the services call them directly.

Writes: every document write of deskops goes through the desk's ``sldb.api.transaction``
(``desk_transaction``), so a service that writes several documents wraps them in one block
and a failure anywhere restores them all. An update of a tracked document carries
``expected_source_hash``: the hash the store had indexed for the document when
``read_doc`` read it (``index_entry``, from the store's indexes alone), so a document the
store rewrote in between is refused with the deskops conflict message and nothing is
written. A document edited by hand and not reindexed keeps its indexed hash, so the next
deskops edit of it goes through.
"""

from __future__ import annotations

from contextlib import contextmanager
import copy
from functools import lru_cache
from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys
from typing import Any, Iterator

import yaml
from sldb.api import AmbiguousSelectionError
from sldb.api import ConflictError
from sldb.api import Transaction
from sldb.api import store_fingerprint
from sldb.api import tracked_documents
from sldb.api import select_documents
from sldb.api import transaction
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.store.layout import store_exists
from sldb.api.documents.frontmatter_keys import undeclared_frontmatter_keys
from sldb.api.documents.structural_noise import find_structural_noise
from sldb.cli.utils import parse_data_value
from sldb.core.ast import AST_Handler
from sldb.core.template_extractor import TemplateExtractor
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops.atom_tags import axis_folder
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import load_namespaces
from deskops.atom_tags import refuse_unplaced_tags
from deskops.config import DeskConfig
# CC35b-a3: untracked surface, resolved on disk
from deskops.desk_paths import resolve_selector
from deskops.desk_paths import relative_candidates
from deskops.doc_readability import is_unreadable_by_model, unread_section_fields
from deskops.errors import DomainError
from deskops.models import AtomDoc
from deskops.models import BoardDoc
from deskops.models import DeskFAQDoc
from deskops.models import InboxNoteDoc
from deskops.models import MaterializationContractDoc
from deskops.models import PillDoc
from deskops.models import RepositoryDoc
from deskops.models import ReviewDoc
from deskops.models import RoleDoc
from deskops.models import RuntimeProfileDoc
from deskops.models import RitualDoc
from deskops.models import StepDoc
from deskops.models import TaskDoc
from deskops.models.validation import validated
from deskops.paths import package_pythonpath
from deskops.runtime import Task
from deskops.specs import compile_artifact_spec
from deskops.specs import compile_task_spec
from deskops.workspace import seed_desk


ARTIFACT_MODELS = {
    "artifact.task": TaskDoc,
    "artifact.pill": PillDoc,
    "artifact.ritual": RitualDoc,
    "artifact.board": BoardDoc,
    "artifact.atom": AtomDoc,
    "artifact.materialization": MaterializationContractDoc,
    "artifact.repository": RepositoryDoc,
    "artifact.review": ReviewDoc,
    "artifact.inbox_note": InboxNoteDoc,
    "artifact.faq": DeskFAQDoc,
    "artifact.step": StepDoc,
    "artifact.role": RoleDoc,
    "artifact.runtime_profile": RuntimeProfileDoc,
}

ARTIFACT_PATHS = {
    "artifact.task": "tasks",
    "artifact.pill": "contexts",
    "artifact.ritual": "rituals",
    "artifact.board": "tasks",
    "artifact.atom": "atoms",
    "artifact.materialization": "materializations",
    "artifact.repository": "registry",
    "artifact.review": "reviews",
    "artifact.inbox_note": "inbox",
    "artifact.faq": "faq",
    "artifact.step": "steps",
    "artifact.role": "roles",
    "artifact.runtime_profile": "runtimes",
}

ARTIFACT_SUBJECTS = {
    "artifact.pill": {"subject": "pill", "list_subject": "pills"},
    "artifact.ritual": {"subject": "ritual", "list_subject": "rituals"},
    "artifact.board": {"subject": "board", "list_subject": "boards"},
    "artifact.atom": {"subject": "atom", "list_subject": "atoms"},
    "artifact.materialization": {"subject": "materialization", "list_subject": "materializations"},
    "artifact.repository": {"subject": "repository", "list_subject": "repositories"},
    "artifact.review": {"subject": "review", "list_subject": "reviews", "create": False},
    "artifact.inbox_note": {"subject": "inbox-note", "list_subject": "inbox-notes"},
    "artifact.faq": {"subject": "faq-doc", "list_subject": "faq-docs"},
    "artifact.step": {"subject": "step", "list_subject": "steps"},
    "artifact.role": {"subject": "role", "list_subject": "roles"},
    "artifact.runtime_profile": {"subject": "runtime-profile", "list_subject": "runtime-profiles"},
}

# Fields whose value is an effect of a workflow command, not a free edit. The
# value names who writes the field, so the refusal teaches the correct entry
# point instead of only saying no.
_TASK_OWNED_FIELDS = {
    "status": "deskops advance (transition effects) and deskops closeout commit",
    "current_node": "deskops advance",
    "history": "deskops advance and deskops closeout (append-only)",
    "task_type": "deskops add task --task-type (create a new task to change the type)",
    "closeout_evidence": "the task type, and deskops add task --evidence at creation",
}

# Artifacts whose documents are named by hand: their files are not `<id_pattern>.md`.
_FREE_NAMED_ARTIFACTS = {"artifact.inbox_note", "artifact.board", "artifact.ritual", "artifact.review", "artifact.role"}

# Artifacts tracked in the desk's store on creation whatever their surface; ``create_artifact``
# also tracks every other artifact it writes on a tracked surface (``_tracked_surface``).
_TRACKED_ON_CREATE = {"artifact.atom", "artifact.pill", "artifact.materialization"}

# (absolute path, model) -> (text, payload): ``read_doc`` parses a document once per text.
_DOC_PAYLOADS: dict[tuple[str, Any], tuple[str, dict[str, Any]]] = {}

# absolute path -> the source hash the store had indexed for the document when ``read_doc``
# last read it (None: not tracked then): the ``expected_source_hash`` of its next update.
_READ_HASHES: dict[str, str | None] = {}

# resolved store path -> (store index signature, {relative path: IndexEntry}).
_INDEX_ENTRIES: dict[str, tuple[tuple[int, int], dict[str, "IndexEntry"]]] = {}


def slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    slug = "-".join(parts) or "item"
    return slug[:100].rstrip("-")


@dataclass(slots=True)
class DocumentRecord:
    kind: str
    doc_id: str
    path: Path


@dataclass(slots=True)
class RepoTaskRoute:
    repo_id: str
    repo_root: Path
    task_id: str
    task_path: Path
    board_path: Path
    title: str
    status: str


def desk_root(root: Path) -> Path:
    return root / "desk"


# ---------------------------------------------------------------- workspace
def ensure_workspace(root: Path) -> None:
    """The desk scaffold: its declared folders (the artifact directories among them), seed files
    and default tag namespaces, whichever are missing (``seed_desk``)."""
    seed_desk(root)


# ---------------------------------------------------------------- store
@dataclass(frozen=True)
class IndexEntry:
    """What the desk's store records about one tracked document: its model, its name and
    the ``source_hash`` of the text it last indexed."""

    model: str
    name: str
    source_hash: str


def store_path(root: Path) -> Path:
    return root / ".sldb"


def has_store(root: Path) -> bool:
    """Whether the root has an sldb store: a ``.sldb/`` that only holds runtime files
    (graph snapshots, caches) is not one."""
    return store_exists(store_path(root))


def _absolute(root: Path, path: Path | str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


def relative_path(root: Path, path: Path | str) -> str:
    """``path`` relative to the project root with ``/`` separators, as the store records it."""
    absolute = _absolute(root, path).resolve()
    try:
        return absolute.relative_to(root.resolve()).as_posix()
    except ValueError:
        return absolute.as_posix()


def _model_name(model: Any) -> str:
    return model if isinstance(model, str) else str(getattr(model, "__name__", model))


@contextmanager
def desk_transaction(root: Path) -> Iterator[Transaction | None]:
    """``sldb.api.transaction`` over the desk's store, importing its models from the deskops package.

    Nested blocks over the same root join the open one, so a service that writes several
    documents wraps them in one block and a failure anywhere restores them all. A root
    without a store (a desk before ``deskops init``, the desks some tests build) has no
    transaction: the block runs with ``None`` and each write is a plain file write.
    """
    if not has_store(root):
        yield None
        return
    with transaction(store_path(root), pythonpath=package_pythonpath()) as tx:
        yield tx


def _index_signature(root: Path) -> tuple[int, int]:
    try:
        stat = (store_path(root) / "core" / "store_index.yaml").stat()
    except OSError:
        return (0, 0)
    return (stat.st_mtime_ns, stat.st_size)


def index_entries(root: Path) -> dict[str, IndexEntry]:
    """Relative path -> index entry of every document the desk's store tracks.

    Read from the store's indexes alone (``store_fingerprint`` for the hashes,
    ``tracked_documents`` for the paths): no model is imported and no document is extracted.
    Kept per process while the store index keeps its signature: every sldb write moves it, a
    hand edit of a document does not, which is what the update guard needs (the hash of the
    text the store indexed, not of the file on disk).
    """
    if not has_store(root):
        return {}
    store = store_path(root)
    key = str(store.resolve())
    signature = _index_signature(root)
    hit = _INDEX_ENTRIES.get(key)
    if hit is not None and hit[0] == signature:
        return hit[1]
    fingerprint = store_fingerprint(store)
    refs = {key.replace(":", "/", 1): key for key in fingerprint.documents}
    statuses = tracked_documents(store, list(refs))
    entries = {
        str(status.path): IndexEntry(
            model=str(status.model),
            name=str(status.name),
            source_hash=fingerprint.documents[refs[ref]].source_hash,
        )
        for ref, status in statuses.items()
    }
    _INDEX_ENTRIES[key] = (signature, entries)
    return entries


def forget_index(root: Path) -> None:
    _INDEX_ENTRIES.pop(str(store_path(root).resolve()), None)


def index_entry(root: Path, path: Path | str) -> IndexEntry | None:
    """The store's entry for ``path``, or None when it is not tracked (or there is no store)."""
    return index_entries(root).get(relative_path(root, path))


def _store_root_of(path: Path) -> Path | None:
    """The root whose store may track ``path``: the nearest parent with a store, unless a
    desk without one (``desk/`` and no ``.sldb``) comes first."""
    for parent in path.resolve().parents:
        if has_store(parent):
            return parent
        if (parent / "desk").is_dir():
            return None
    return None


def _note_read(path: Path) -> None:
    """Keep the source hash the store has for ``path`` as of this read."""
    root = _store_root_of(path)
    entry = index_entry(root, path) if root is not None else None
    _READ_HASHES[os.path.abspath(path)] = entry.source_hash if entry is not None else None


def _note_written(root: Path, path: Path) -> None:
    forget_index(root)
    entry = index_entry(root, path)
    _READ_HASHES[os.path.abspath(path)] = entry.source_hash if entry is not None else None


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def conflict_error(root: Path, path: Path | str) -> DomainError:
    """The deskops conflict: the store rewrote the document after deskops read it."""
    return DomainError(
        f"Error: {relative_path(root, path)} changed since deskops read it; nothing was written. Re-run the command."
    )


def update_tracked_doc(tx: Transaction, root: Path, path: Path, entry: IndexEntry, payload: dict[str, Any]) -> None:
    """``Transaction.update`` of the tracked document at ``path``, guarded by the source hash
    deskops read for it (``read_doc``; ``entry.source_hash`` when the caller read it another
    way). A failed guard raises the deskops conflict, and the transaction writes nothing."""
    key = os.path.abspath(path)
    expected = _READ_HASHES.get(key, entry.source_hash)
    try:
        tx.update(relative_path(root, path), payload, expected_source_hash=expected)
    except ConflictError as exc:
        raise conflict_error(root, path) from exc
    _note_written(root, path)


def delete_doc(root: Path, path: Path) -> None:
    """Delete a document: ``Transaction.delete`` when the store tracks it (entry and file),
    else the file alone, recorded so the transaction restores it on failure."""
    with desk_transaction(root) as tx:
        if tx is not None and index_entry(root, path) is not None:
            tx.delete(relative_path(root, path))
        else:
            if tx is not None:
                tx.record(relative_path(root, path))
            if path.exists():
                path.unlink()
    _READ_HASHES.pop(os.path.abspath(path), None)
    forget_index(root)


def untrack_doc(root: Path, ref: Path | str) -> bool:
    """``Transaction.untrack`` by path or document name. A document the store does not
    track, or a root without a store, is left alone (False)."""
    with desk_transaction(root) as tx:
        if tx is None:
            return False
        if isinstance(ref, Path):
            entry = index_entry(root, ref)
            name = entry.name if entry is not None else None
        else:
            name = next((entry.name for entry in index_entries(root).values() if entry.name == ref), None)
        if name is None:
            return False
        tx.untrack(name)
    forget_index(root)
    return True


# ---------------------------------------------------------------- read / write
def read_doc(path: Path, model: type[Any]) -> dict[str, Any]:
    """The model payload of a document, parsed once per text of the file.

    The parse is kept for the whole process under (path, model) with the text it came
    from, and handed out as a copy: a reader that builds a new ``DeskopsOperations`` per
    request (the UI's server) does not re-parse unchanged documents, and a caller that
    edits the payload it got does not edit the kept one.
    """
    raw_text = path.read_text(encoding="utf-8")
    _note_read(path)
    key = (os.path.abspath(path), model)
    hit = _DOC_PAYLOADS.get(key)
    if hit is not None and hit[0] == raw_text:
        return copy.deepcopy(hit[1])
    payload = extract_model_data(model, raw_text)
    if "id" not in payload:
        payload["id"] = path.stem
    _DOC_PAYLOADS[key] = (raw_text, copy.deepcopy(payload))
    return payload


def write_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
    rendered = render_model_markdown(model, payload) + "\n"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        # A short new value is not proof the model cannot read the file: only
        # refuse when the current text really extracts empty for that field.
        unreadable = set(is_unreadable_by_model(model, existing))
        lost = [field for field in unread_section_fields(model, existing, rendered) if field in unreadable]
        if lost:
            raise ValueError(
                f"Refusing to rewrite {path.name}: its model cannot read "
                f"{', '.join(lost)} from the current file, so writing this payload "
                "would erase that content. The document was not produced by the "
                "model's own renderer; rewrite it through sldb (or fix the model's "
                "template) before editing it here."
            )
        # Headings and frontmatter keys the template never declares are dropped by
        # extraction; refuse when the rewrite would erase one. A heading counts only
        # if re-rendering the file's own payload loses it, so replacing a field that
        # carries a heading (atoms split/merge) is not refused.
        kept = set((render_model_markdown(model, extract_model_data(model, existing)) + "\n").splitlines())
        erased = [line for line in find_structural_noise(model, existing, path.name).undeclared if line not in kept]
        erased += [f"frontmatter key '{key}'" for key in undeclared_frontmatter_keys(model, existing)]
        if erased:
            raise ValueError(
                f"Refusing to rewrite {path.name}: it has content its model "
                f"({model.__name__}) does not declare, and rewriting would erase it: "
                f"{'; '.join(erased)}. Move that content into a declared field "
                "(or remove it) before editing the document here."
            )
    with desk_transaction(root) as tx:
        if tx is None:
            _write_text(path, rendered)
            return
        entry = index_entry(root, path)
        if entry is None:
            tx.write_file(relative_path(root, path), rendered.encode("utf-8"))
            return
        update_tracked_doc(tx, root, path, entry, payload)


def write_new_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
    """A new document the store does not track yet, as a file the desk's transaction restores
    on failure (``write_file``); ``track_created_document`` tracks it when its kind is tracked."""
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing document: {path}")
    rendered = render_model_markdown(model, payload) + "\n"
    with desk_transaction(root) as tx:
        if tx is None:
            _write_text(path, rendered)
        else:
            tx.write_file(relative_path(root, path), rendered.encode("utf-8"))


def create_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any], name: str) -> None:
    """A new tracked document: ``Transaction.create`` renders it under its registered model
    and tracks it in one step. Without a store, the file alone."""
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing document: {path}")
    with desk_transaction(root) as tx:
        if tx is None:
            _write_text(path, render_model_markdown(model, payload) + "\n")
            return
        tx.create(_model_name(model), name, payload, relative_path(root, path))
    _note_written(root, path)


def remove_created_file(path: Path) -> None:
    if path.exists():
        path.unlink()


def track_created_document(root: Path, model: type[Any], path: Path, doc_id: str) -> None:
    """``Transaction.track`` of a document deskops just wrote, if the root has a store."""
    with desk_transaction(root) as tx:
        if tx is not None:
            tx.track(relative_path(root, path), _model_name(model), doc_id)
    _note_written(root, path)


def track_created_artifact(root: Path, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
    if artifact_id not in _TRACKED_ON_CREATE:
        return
    track_created_document(root, model, path, doc_id)


# ---------------------------------------------------------------- values
def coerce_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def merge_unique(*values: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for value_list in values:
        for value in value_list:
            item = str(value)
            if item in seen:
                continue
            seen.add(item)
            merged.append(item)
    return merged


def _parse_field_value(model: type[Any], field_name: str, raw_value: str) -> Any:
    """Parse `edit` input as JSON/YAML, but keep text fields as the literal text.

    YAML folds the line breaks of multi-line text and reads `**bold` as an alias,
    so a text field (`str` or `str | None`) takes the raw value as written. A JSON
    string literal (`"..."`) is still decoded, for callers that quote their text.
    """
    annotation = model.model_fields[field_name].annotation
    if annotation in (str, str | None):
        if raw_value.startswith('"'):
            try:
                decoded = json.loads(raw_value)
            except ValueError:
                return raw_value
            if isinstance(decoded, str):
                return decoded
        return raw_value
    return parse_data_value(raw_value)


@lru_cache(maxsize=None)
def template_placeholders(model: type[Any]) -> dict[str, str]:
    """The placeholder paragraph of each field in ``model``'s template, by field name.

    A placeholder is the literal italic paragraph the template writes right before a field's
    marker (``_Outline the expected implementation route or affected surface._`` before
    ``⸢rev•implementation_path⸥``). sldb reads it as a paragraph anchor: render always writes it
    and extract consumes it, so it is never part of the field. The template is the only source.
    """
    nodes = AST_Handler().split_nodes(model.__template__)
    recipes = TemplateExtractor().extract_nodes(nodes)
    placeholders: dict[str, str] = {}
    for anchor, recipe in zip(recipes, recipes[1:]):
        if anchor.get("outer_type") != "paragraph" or not anchor.get("anchor") or anchor.get("props"):
            continue
        fields = recipe.get("props") or ([recipe["name"]] if recipe.get("name") else [])
        if len(fields) != 1:
            continue
        text = _paragraph_text(nodes[anchor["outer_index"]])
        if len(text) > 2 and text[0] in "_*" and text[-1] == text[0]:
            placeholders[fields[0]] = text
    return placeholders


def _paragraph_text(node: Any) -> str:
    return "".join(child.content for child in node.children).strip()


def strip_template_placeholders(model: type[Any], field_name: str, value: Any) -> Any:
    """``value`` without the paragraphs that are exactly the template's placeholder of the field.

    Only a text field (``str`` or ``str | None``) is normalized. A top-level paragraph whose
    whole text is the placeholder is dropped, with the blank lines after it; a value that is
    only the placeholder becomes ``""``. The phrase inside a longer paragraph, a quote, a list
    or a code block is content and stays. Written as is, the placeholder would be rendered
    after the template's own anchor and read back as content, one more copy per edit.
    """
    if model.model_fields[field_name].annotation not in (str, str | None) or not isinstance(value, str):
        return value
    placeholder = template_placeholders(model).get(field_name)
    if not placeholder or placeholder not in value:
        return value
    dropped = [
        node.map
        for node in AST_Handler().split_nodes(value)
        if node.type == "paragraph" and node.map and _paragraph_text(node) == placeholder
    ]
    if not dropped:
        return value
    lines = value.split("\n")
    drop: set[int] = set()
    for start, end in dropped:
        drop.update(range(start, end))
        while end < len(lines) and not lines[end].strip():
            drop.add(end)
            end += 1
    return "\n".join(line for index, line in enumerate(lines) if index not in drop).strip("\n")


# ---------------------------------------------------------------- paths and selectors
def artifact_path(root: Path, artifact_id: str, doc_id: str) -> Path:
    return desk_root(root) / ARTIFACT_PATHS[artifact_id] / f"{doc_id}.md"


def artifact_glob_pattern(artifact_id: str) -> str:
    if artifact_id in _FREE_NAMED_ARTIFACTS:
        return "*.md"
    id_pattern = str(getattr(ARTIFACT_MODELS[artifact_id], "__artifact__", {})["id_pattern"])
    return id_pattern.replace("{slug}", "*") + ".md"


def atom_folder_axis(root: Path) -> str | None:
    """Return the configured folder axis namespace for atoms, or None (flat)."""
    axis = DeskConfig.load(desk_root(root)).atom_folder_axis
    if axis is None:
        return None
    axis = str(axis).strip()
    if not axis:
        return None
    namespaces = load_namespaces(default_registry_path(root))
    if axis not in namespaces:
        raise ValueError(
            f"Configured atom_folder_axis '{axis}' is not a registered atom tag namespace. "
            "Register it with 'deskops atoms add-namespace' or fix desk/config.json."
        )
    return axis


def atom_doc_path(root: Path, atom_id: str, tags: list[str]) -> Path:
    base = desk_root(root) / "atoms"
    axis = atom_folder_axis(root)
    if axis is not None:
        value = folder_axis_value(tags, axis)
        if value is not None:
            return base / axis_folder(value) / f"{atom_id}.md"
    return base / f"{atom_id}.md"


# Desk folders the store does not track (CC35b-a3): the include of
# ``deskops/data/desk_declaration.yaml`` declares neither, so their documents resolve on disk.
_UNTRACKED_DESK_FOLDERS = ("drawer", "issues")


def _tracked_surface(root: Path, directory: Path) -> bool:
    """Whether documents under ``directory`` resolve through the store: the root has one and
    the directory is not one of the desk folders it leaves untracked."""
    if not has_store(root):
        return False
    try:
        relative = directory.resolve().relative_to(desk_root(root).resolve())
    except ValueError:
        return True
    return not (relative.parts and relative.parts[0] in _UNTRACKED_DESK_FOLDERS)


def _select_one(root: Path, query: dict[str, str], selector: str, what: str) -> Path | None:
    """The one document ``query`` names (``select_documents``, ``expect="one"``), or None.

    Several matches raise the deskops ambiguity message, its candidates the rows of the same
    query (``expect="many"``) that ``AmbiguousSelectionError`` names, relative to ``desk/``.
    """
    store = store_path(root)
    try:
        rows = select_documents(store, query, expect="one")
    except AmbiguousSelectionError as error:
        named = set(error.candidates)
        paths = [root / row["path"] for row in select_documents(store, query) if row["export_id"] in named]
        raise ValueError(f"Ambiguous {what} selector '{selector}': {relative_candidates(desk_root(root), paths)}") from None
    except SLDBDocumentTargetError:
        return None
    return root / rows[0]["path"]


def resolve_document(
    root: Path,
    directory: Path,
    selector: str,
    what: str,
    *,
    pattern: str = "*.md",
    recursive: bool = True,
    model: str | None = None,
) -> Path:
    """The document ``selector`` names under ``directory`` (``pattern``; ``recursive`` reaches subfolders).

    A tracked surface asks ``sldb.api.select_documents`` twice, in order (TaskDoc c3): by
    name (``prefix``, where an exact name wins over the unique prefix match), then, only if
    that found nothing, by file name (``path_glob`` of ``<selector>*.md``), which keeps the
    files whose name differs from their document's (``desk/rituals/execution.md`` is
    ``ritual-execution``). An ambiguous query stops there. Zero matches raise
    ``FileNotFoundError``, several ``ValueError``, with the messages the disk rule uses.
    """
    if not selector or not str(selector).strip():
        raise ValueError(f"Empty or whitespace-only selector provided for {what}")
    if not _tracked_surface(root, directory):
        # CC35b-a3: untracked surface, resolved on disk
        return resolve_selector(desk_root(root), [directory], selector, pattern, what, recursive=recursive)
    base = relative_path(root, directory) + ("/**/" if recursive else "/")
    by_name = {"prefix": selector, "path_glob": base + pattern}
    if model is not None:
        by_name["model"] = model
    for query in (by_name, {"path_glob": f"{base}{selector}*.md"}):
        found = _select_one(root, query, selector, what)
        if found is not None:
            return found
    raise FileNotFoundError(f"No {what} file found for selector '{selector}'")


def resolve_glob(root: Path, directory: Path, doc_id: str) -> Path:
    return resolve_document(root, directory, doc_id, "task", recursive=False)


def resolve_artifact_selector_multi(root: Path, artifact_id: str, directories: list[Path], selector: str) -> Path:
    """``resolve_artifact_selector`` over several directories, in order: the first that
    names the selector wins (a review resolves by its id, the name the store tracks it by)."""
    for directory in directories:
        try:
            return resolve_artifact_selector(root, artifact_id, directory, selector)
        except FileNotFoundError:
            continue
    raise FileNotFoundError(f"No {artifact_id} file found for selector '{selector}'")


def resolve_artifact_selector(root: Path, artifact_id: str, directory: Path, selector: str) -> Path:
    try:
        return resolve_document(root, directory, selector, artifact_id, pattern=artifact_glob_pattern(artifact_id))
    except FileNotFoundError:
        if artifact_id != "artifact.task" or not _tracked_surface(root, directory):
            raise
    # Tasks written before the `task-*` naming are still tracked: every task type extends
    # TaskDoc, so its model family names them whatever their file is called.
    return resolve_document(root, directory, selector, artifact_id, model="TaskDoc")


def resolve_ritual_selector(root: Path, selector: str) -> Path:
    directory = desk_root(root) / ARTIFACT_PATHS["artifact.ritual"]
    return resolve_artifact_selector(root, "artifact.ritual", directory, selector)


def editable_artifact(root: Path, subject: str, selector: str) -> tuple[type[Any], Path, str]:
    """The model, file and kind of the document `deskops edit <subject> <selector>` names."""
    if subject == "task":
        try:
            path = resolve_artifact_selector(root, "artifact.task", desk_root(root) / "tasks", selector)
        except FileNotFoundError:
            # Drawer candidates are tasks too; an active task with the same
            # selector wins because it resolved before this fallback.
            path = resolve_artifact_selector(root, "artifact.task", desk_root(root) / "drawer" / "tasks", selector)
        return TaskDoc, path, "task"
    artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
    if subject not in artifact_subjects:
        raise ValueError(f"Unsupported edit subject: {subject}")
    artifact_id = artifact_subjects[subject]
    model = ARTIFACT_MODELS[artifact_id]
    if artifact_id == "artifact.ritual":
        return model, resolve_ritual_selector(root, selector), subject
    directories = [desk_root(root) / ARTIFACT_PATHS[artifact_id]]
    if artifact_id == "artifact.pill":
        directories.append(desk_root(root) / "drawer" / "pills")
    path = resolve_artifact_selector_multi(root, artifact_id, directories, selector)
    return model, path, subject


# ---------------------------------------------------------------- tasks
def resolve_task_path(root: Path, task_id: str) -> Path:
    """The file a task id, unique prefix or file name names under ``desk/tasks``."""
    return resolve_glob(root, desk_root(root) / "tasks", task_id)


def resolve_task_payload(
    root: Path,
    task_id: str,
    stack: tuple[str, ...] = (),
    *,
    path: Path | None = None,
    cache: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """The normalized payload of a task with its inherited context (``effective_*``).

    ``path`` skips resolving ``task_id`` again (a caller that already has the file, such as a
    view row); ``cache`` keeps one payload per task id for a read-only pass, so a task read by
    several operations and the parents it inherits from are parsed and resolved once.
    """
    if task_id in stack:
        chain = " -> ".join([*stack, task_id])
        raise ValueError(f"Task inheritance cycle detected: {chain}")
    if cache is not None and task_id in cache:
        return copy.deepcopy(cache[task_id])
    path = Path(path) if path is not None else resolve_task_path(root, task_id)
    payload = compile_task_spec(read_doc(path, TaskDoc), entry_node="").task_payload
    inherited_ids = coerce_list(payload.get("inherits_from") or [])
    inherited_payloads = [resolve_task_payload(root, parent_id, (*stack, task_id), cache=cache) for parent_id in inherited_ids]

    payload["effective_references"] = merge_unique(
        *[parent.get("effective_references", parent.get("references", [])) for parent in inherited_payloads],
        payload.get("references", []),
    )
    payload["effective_pills"] = merge_unique(
        *[parent.get("effective_pills", parent.get("pills", [])) for parent in inherited_payloads],
        payload.get("pills", []),
    )
    payload["effective_tags"] = merge_unique(
        *[parent.get("effective_tags", parent.get("tags", [])) for parent in inherited_payloads],
        payload.get("tags", []),
    )
    payload["effective_atoms"] = merge_unique(
        *[parent.get("effective_atoms", parent.get("atoms", [])) for parent in inherited_payloads],
        payload.get("atoms", []),
    )

    if payload.get("inherit_acceptance_context"):
        payload["effective_validation"] = merge_unique(
            *[parent.get("effective_validation", parent.get("validation", [])) for parent in inherited_payloads],
            payload.get("validation", []),
        )
        parent_done_when = next(
            (
                str(parent.get("effective_done_when") or parent.get("done_when") or "")
                for parent in inherited_payloads
                if str(parent.get("effective_done_when") or parent.get("done_when") or "")
            ),
            "",
        )
        payload["effective_done_when"] = str(payload.get("done_when") or parent_done_when)
    else:
        payload["effective_validation"] = coerce_list(payload.get("validation") or [])
        payload["effective_done_when"] = str(payload.get("done_when") or "")
    if cache is not None:
        cache[task_id] = copy.deepcopy(payload)
    return payload


def hydrate_task(payload: dict[str, Any]) -> Task:
    return Task(
        id=payload["id"],
        title=payload["title"],
        status=payload["status"],
        summary=payload["goal"],
        tags=list(payload.get("tags") or []),
        current_node=payload.get("current_node", ""),
        history=list(payload.get("history") or []),
        goal=payload.get("goal", ""),
        scope=payload.get("scope", ""),
        references=list(payload.get("references") or []),
        depends_on=list(payload.get("depends_on") or []),
        pills=list(payload.get("pills") or []),
        files=list(payload.get("files") or []),
        implementation_path=payload.get("implementation_path", ""),
        validation=list(payload.get("validation") or []),
        done_when=payload.get("done_when", ""),
        task_type=payload.get("task_type", ""),
        inherits_from=list(payload.get("inherits_from") or []),
        inherit_acceptance_context=bool(payload.get("inherit_acceptance_context") or False),
        atoms=list(payload.get("atoms") or []),
        from_drawer=payload.get("from_drawer") or "",
        closeout_evidence=list(payload.get("closeout_evidence") or []),
        effective_references=list(payload.get("effective_references") or payload.get("references") or []),
        effective_pills=list(payload.get("effective_pills") or payload.get("pills") or []),
        effective_tags=list(payload.get("effective_tags") or payload.get("tags") or []),
        effective_atoms=list(payload.get("effective_atoms") or payload.get("atoms") or []),
        effective_validation=list(payload.get("effective_validation") or payload.get("validation") or []),
        effective_done_when=payload.get("effective_done_when", payload.get("done_when", "")),
    )


def load_task(root: Path, task_id: str) -> Task:
    return hydrate_task(resolve_task_payload(root, task_id))


# ---------------------------------------------------------------- artifacts
def list_artifacts(root: Path, artifact_id: str) -> list[dict[str, Any]]:
    model = ARTIFACT_MODELS[artifact_id]
    directory = desk_root(root) / ARTIFACT_PATHS[artifact_id]
    if not directory.exists():
        if not desk_root(root).exists():
            raise FileNotFoundError(f"Desk root not found at {desk_root(root)}. Run 'deskops init' to initialize.")
        return []
    pattern = artifact_glob_pattern(artifact_id)
    results = []
    for path in sorted(directory.rglob(pattern)):
        try:
            results.append(read_doc(path, model))
        except Exception as e:
            print(f"Warning: Failed to load artifact {path}: {e}", file=sys.stderr)
    return results


def show_artifact(root: Path, artifact_id: str, doc_id: str) -> dict[str, Any]:
    if not doc_id:
        raise ValueError(f"No {artifact_id} ID provided")
    model = ARTIFACT_MODELS[artifact_id]
    directories = [desk_root(root) / ARTIFACT_PATHS[artifact_id]]
    if artifact_id == "artifact.pill":
        directories.append(desk_root(root) / "drawer" / "pills")
    return read_doc(resolve_artifact_selector_multi(root, artifact_id, directories, doc_id), model)


def create_artifact(root: Path, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
    ensure_workspace(root)
    model = ARTIFACT_MODELS[artifact_id]
    compiled = compile_artifact_spec(artifact_id, raw_payload, model_fields=model.model_fields.keys())
    validated(model, compiled.artifact_payload)
    doc_id = compiled.artifact_payload["id"]
    if artifact_id == "artifact.atom":
        tags = list(compiled.artifact_payload.get("tags") or [])
        refuse_unplaced_tags(root, tags)
        path = atom_doc_path(root, doc_id, tags)
    else:
        path = artifact_path(root, artifact_id, doc_id)
    # Every artifact `add` writes on a tracked surface is tracked as it is created: since CC35b
    # the selectors of `show`/`edit` resolve those surfaces through the store only, so a
    # document `add` left untracked could not be shown or edited until `desk update --apply`.
    if artifact_id in _TRACKED_ON_CREATE or _tracked_surface(root, path.parent):
        create_doc(root, path, model, compiled.artifact_payload, doc_id)
    else:
        write_new_doc(root, path, model, compiled.artifact_payload)
    return DocumentRecord(kind=artifact_id.split(".")[-1], doc_id=doc_id, path=path)


def edit_artifact_field(root: Path, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
    ensure_workspace(root)
    model, path, kind = editable_artifact(root, subject, selector)
    field_name = field.replace("-", "_")
    if field_name not in model.model_fields:
        raise ValueError(f"Unknown field '{field_name}' for {subject}")
    if field_name == "id":
        raise ValueError("Cannot edit immutable field 'id'")
    if subject == "task" and field_name in _TASK_OWNED_FIELDS:
        raise ValueError(
            f"{field_name} is not editable with edit task; "
            f"it is written by {_TASK_OWNED_FIELDS[field_name]}."
        )
    if subject == "review" and field_name in {"verdict", "reason", "disposed_at", "disposed_by"}:
        raise ValueError(
            "verdict is written by deskops review dispose (GC03); a new review is a new document"
        )
    payload = read_doc(path, model)
    payload[field_name] = strip_template_placeholders(
        model, field_name, _parse_field_value(model, field_name, raw_value)
    )
    write_doc(root, path, model, payload)
    return DocumentRecord(kind=kind, doc_id=str(payload.get("id", path.stem)), path=path)


# ---------------------------------------------------------------- registry
def registered_repositories(root: Path) -> list[dict[str, Any]]:
    """The repositories of ``desk/registry/repo-*.md``: the documents the store tracks there
    (``select_documents``), or the files on disk in a desk without a store."""
    registry_dir = desk_root(root) / "registry"
    if not registry_dir.exists():
        return []
    if has_store(root):
        pattern = relative_path(root, registry_dir) + "/repo-*.md"
        paths = [root / row["path"] for row in select_documents(store_path(root), {"path_glob": pattern})]
    else:
        # CC35b-a3: untracked surface, resolved on disk
        paths = sorted(registry_dir.glob("repo-*.md"))
    repositories = []
    for path in paths:
        try:
            repositories.append(read_doc(path, RepositoryDoc))
        except Exception as e:
            print(f"Warning: Failed to load repository {path}: {e}", file=sys.stderr)
            continue
    return repositories


def repository_root(root: Path, repository: dict[str, Any]) -> Path:
    repo_path = Path(str(repository["path"]))
    if repo_path.is_absolute():
        return repo_path.resolve()
    return (root / repo_path).resolve()


def _resolve_repo_board_task_path(repo_root: Path, task_ref: str) -> Path | None:
    tasks_root = (repo_root / "desk" / "tasks").resolve()
    task_path = Path(task_ref)
    if not task_path.is_absolute():
        task_path = repo_root / task_path
    task_path = task_path.resolve()
    try:
        task_path.relative_to(tasks_root)
    except ValueError:
        return None
    if not task_path.name.startswith("task-") or task_path.suffix != ".md":
        return None
    if not task_path.is_file():
        return None
    return task_path


def _task_route_summary(task_path: Path) -> dict[str, str]:
    text = task_path.read_text(encoding="utf-8")
    payload: dict[str, Any] = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
            except yaml.YAMLError:
                frontmatter = None
            if isinstance(frontmatter, dict):
                payload = frontmatter
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), task_path.stem)
    legacy_status = next((line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith("Status:")), "unknown")
    task_id = str(payload.get("id") or task_path.stem)
    if not task_id.startswith("task-"):
        raise ValueError(f"Routed task id must start with 'task-': {task_id}")
    return {
        "id": task_id,
        "status": str(payload.get("status") or legacy_status),
        "title": title,
    }


def list_repo_task_routes(root: Path) -> list[RepoTaskRoute]:
    routes: list[RepoTaskRoute] = []
    for repository in registered_repositories(root):
        repo_root = repository_root(root, repository)
        board_path = repo_root / "desk" / "tasks" / "Board.md"
        if not board_path.exists():
            continue
        try:
            board_payload = read_doc(board_path, BoardDoc)
        except Exception:
            continue
        for task_ref in board_payload.get("tasks") or []:
            task_path = _resolve_repo_board_task_path(repo_root, str(task_ref))
            if task_path is None:
                continue
            try:
                summary = _task_route_summary(task_path)
            except (OSError, UnicodeDecodeError, ValueError):
                continue
            routes.append(
                RepoTaskRoute(
                    repo_id=str(repository["id"]),
                    repo_root=repo_root,
                    task_id=summary["id"],
                    task_path=task_path,
                    board_path=board_path,
                    title=summary["title"],
                    status=summary["status"],
                )
            )
    return routes

FILE:deskops/cli/commands/doctor.py
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from deskops import absolute_paths
from deskops.bootstrap import MODEL_REFS, SLDBBootstrap
from deskops.doc_readability import is_unreadable_by_model
from deskops.doctor_findings import (
    REGISTER,
    Findings,
    invalid_document_findings,
    invalid_task_findings,
    invalid_task_paths,
    moved_documents,
    print_findings,
    read_store_check,
    seed_drift,
)
from deskops.foreign_files import open_foreign_tasks, task_warning
from deskops.workspace import inspect_desk
from deskops.workspace import modeled_desk_markdown_docs
from deskops.workspace import desk_seed_text
from deskops.workspace import seed_desk


_IGNORED_MODELED_NAMES = {
    "Board.md",
    "pills.md",
    "execution.md",
    "testing.md",
    "closeout.md",
    "phase.md",
    "README.md",
    "tag-namespaces.yaml",
}


class DoctorCLI:
    """Report what breaks the desk (errors) apart from what only moved (alerts).

    Exit 1 only when an error is left; alerts alone exit 0 and are always printed. `--repair`
    acts on errors only: an alert is not damage, it is registered with `deskops desk update
    --apply`. See `deskops.doctor_findings`.
    """

    def run(self, args: argparse.Namespace) -> int:
        root = Path(args.root).resolve()
        repair = getattr(args, "repair", False)
        inspection = inspect_desk(root)
        desk_dir = root / "desk"
        if inspection.classification == "absent" and not (desk_dir / "config.json").exists():
            print(f"No desk at {root}: this repository has no desk/ (run deskops init to create one).")
            return 0
        findings = Findings()
        self._check_structure(root, desk_dir, inspection, repair, findings)
        if desk_dir.exists():
            self._check_documents(root, desk_dir, repair, findings)
            self._check_managed_seeds(root, findings)
            self._check_foreign_files(root, findings)
            self._check_absolute_paths(root, repair, findings)
            self._check_models(root, repair, findings)
        return self._report(findings, repair)

    def _check_structure(self, root: Path, desk_dir: Path, inspection, repair: bool, findings: Findings) -> None:
        missing = [rel for rel, exists in (
            ("desk/tasks/Board.md", (desk_dir / "tasks" / "Board.md").exists()),
            ("desk/drawer/", (desk_dir / "drawer").exists()),
            ("desk/rituals/phase.md", (desk_dir / "rituals" / "phase.md").exists()),
        ) if desk_dir.exists() and not exists]
        if missing and repair:
            seed_desk(root)
            findings.fixed.append(f"Scaffolded missing desk/ structure: {', '.join(missing)}")
        elif missing:
            findings.errors.append(f"Missing desk structure: {', '.join(missing)}")
        if inspection.classification == "legacy":
            surfaces = [*inspection.missing_surfaces, *inspection.malformed_surfaces]
            findings.errors.append(
                "Legacy desk detected: "
                + (", ".join(surfaces) if surfaces else "board/task/pill surfaces need explicit migration")
                + ". Migrate with: deskops desk migrate --root <repo>."
            )

    def _check_documents(self, root: Path, desk_dir: Path, repair: bool, findings: Findings) -> None:
        findings.errors += invalid_task_findings(root)
        task_paths = invalid_task_paths(root)
        payload = self._store_check(root, findings)
        if payload is None:
            return
        findings.errors += [
            f"Invalid desk document: {rel}: {what}"
            for rel, what in invalid_document_findings(payload)
            if rel not in task_paths
        ]
        docs = read_store_check(root, payload)
        modeled = {p.resolve() for p in modeled_desk_markdown_docs(root, desk_dir) if p.name not in _IGNORED_MODELED_NAMES}
        untracked = sorted(p for p in modeled if p not in docs.tracked)
        moves, gone, untracked = moved_documents(root, docs.missing, untracked)
        findings.alerts += [f"Edited: {d}" for d in docs.changed]
        findings.alerts += [f"Moved: {m}" for m in moves]
        findings.alerts += [f"Not tracked yet: {p.relative_to(root)}" for p in untracked]
        findings.alerts += docs.store_alerts
        findings.errors += [f"Tracked document is gone: {p.relative_to(root)} (restore it, or untrack it with {REGISTER})" for p in gone]
        findings.errors += [f"Invalid desk document: {d}" for d in docs.unknown]
        findings.errors += docs.store_errors
        findings.errors += self._unreadable(root, docs.by_model)

    def _check_managed_seeds(self, root: Path, findings: Findings) -> None:
        """The managed seeds (the lifecycle graph and its rules) whose desk copy differs from the
        package: what ``deskops desk update --apply`` would rewrite, by the same comparison
        (``seed_desk(apply=False, restore_managed=True)``). One finding per file; an error when a
        lifecycle edge's transition fields differ (``advance`` refuses it), else an alert (b1)."""
        try:
            rewritten = seed_desk(root, apply=False, restore_managed=True).rewritten_paths
        except Exception as exc:
            findings.errors.append(f"Could not compare the desk's managed seeds with the deskops package: {exc}")
            return
        for path in rewritten:
            rel = path.resolve().relative_to(root).as_posix()
            drift = seed_drift(rel, desk_seed_text(root.name, rel), path.read_text(encoding="utf-8"))
            (findings.errors if drift.governs_transition else findings.alerts).append(drift.line)

    def _check_foreign_files(self, root: Path, findings: Findings) -> None:
        """An alert per open task, not task.external, whose files belong to another registered repo."""
        try:
            found = open_foreign_tasks(root)
        except Exception:
            return
        findings.alerts += [task_warning(task_id, repo_id) for task_id, repo_id in found]

    def _check_absolute_paths(self, root: Path, repair: bool, findings: Findings) -> None:
        """An alert per absolute path in a desk document; ``--repair`` rewrites those the store's
        links and the registry resolve (``deskops.absolute_paths``). The exit code never changes."""
        try:
            report = absolute_paths.check(root, repair=repair)
        except Exception as exc:
            findings.alerts.append(f"Could not check the desk for absolute paths: {exc}")
            return
        findings.alerts += report.alerts
        findings.fixed += report.fixed

    def _store_check(self, root: Path, findings: Findings) -> dict | None:
        result = subprocess.run(
            [sys.executable, "-m", "sldb", "stores", "check", "--store", str(root / ".sldb"), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        if not result.stdout:
            if result.returncode != 0:
                first = result.stderr.strip().split("\n")[0]
                findings.errors.append(f"SLDB store check crashed (likely malformed documents): {first}")
            return None
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            findings.errors.append("Failed to parse SLDB store check output.")
            return None

    def _unreadable(self, root: Path, by_model: list[tuple[str | None, Path]]) -> list[str]:
        """Documents whose model cannot read their own content: an edit through the model erases it."""
        out = []
        for model_name, doc_path in by_model:
            model = _resolve_deskops_model(model_name)
            if model is None or not doc_path.exists():
                continue
            if fields := is_unreadable_by_model(model, doc_path.read_text(encoding="utf-8")):
                out.append(
                    f"Model cannot read its own document: {doc_path.relative_to(root)} ({model_name}: {', '.join(fields)}). "
                    "Any edit through the model renders these fields back empty; rebuild the text through sldb and retrack it."
                )
        return out

    def _check_models(self, root: Path, repair: bool, findings: Findings) -> None:
        store_dir = root / ".sldb"
        if not store_dir.exists():
            return
        try:
            registered = SLDBBootstrap()._registered_model_names(store_dir)
        except Exception:
            findings.errors.append("Could not read the local .sldb store index; unregistered-model check skipped.")
            return
        if not (unregistered := sorted(name for name in MODEL_REFS if name not in registered)):
            return
        if repair and self._register_models(root):
            findings.fixed.append(f"Registered missing models: {', '.join(unregistered)}")
        else:
            findings.errors.append(f"Unregistered models: {', '.join(unregistered)}. Register them with {REGISTER}.")

    def _register_models(self, root: Path) -> bool:
        try:
            return SLDBBootstrap().init_local_store(root) == 0
        except Exception:
            return False

    def _report(self, findings: Findings, repair: bool) -> int:
        if not findings.errors and not findings.alerts and not findings.fixed:
            print("Desk is healthy. No issues found.")
            return 0
        print_findings(findings, repair=repair)
        if not findings.errors:
            print(f"\nDesk is healthy{f', with {len(findings.alerts)} alert(s)' if findings.alerts else ''}.")
            return 0
        return 1


def _resolve_deskops_model(name: str | None) -> type | None:
    """The deskops model registered under `name`, or None when it is not ours."""
    if not name:
        return None
    import deskops.models as models

    candidate = getattr(models, name, None)
    return candidate if isinstance(candidate, type) else None

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

FILE:tests/test_registry_robustness.py
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import re

import pytest
from sldb.core.exceptions import SLDBStoreError
from sldb.runtime.validation import render_model_markdown

from deskops.bootstrap import SLDBBootstrap
from sldb.api import doc_exists

from deskops.cli.main import main
from deskops.identity import load_repository_registry
from deskops.identity import EcosystemIdentity
from deskops.models import RepositoryDoc


def _write_repo_doc(
    registry_dir: Path,
    *,
    repo_id: str,
    repo_path: str,
    name: str | None = None,
    filename: str | None = None,
) -> Path:
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


def _init_ecosystem(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        assert SLDBBootstrap().init_local_store(root) == 0
    desk_root = root / "desk"
    desk_root.mkdir(parents=True, exist_ok=True)
    (desk_root / "config.json").write_text(
        json.dumps({"project_identity": "graph_ui"}, indent=2) + "\n",
        encoding="utf-8",
    )
    return root / ".sldb"


def test_repo_remove_then_register_same_path_under_correct_id(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A mis-registered id is removable so the same root can be registered again."""
    root = tmp_path / "ecosystem"
    store_path = _init_ecosystem(root)
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)

    register_wrong = main([
        "repo", "register", "graph-ui", str(root), "--store", str(store_path),
    ])
    capsys.readouterr()
    assert register_wrong == 0

    registry_file = root / "desk" / "registry" / "repo-graph-ui.md"
    assert registry_file.exists()
    assert doc_exists(root / ".sldb", registry_file.relative_to(root).as_posix())

    removed = main(["repo", "remove", "graph-ui", "--store", str(store_path)])
    remove_out = capsys.readouterr().out
    assert removed == 0
    assert str(registry_file) in remove_out
    assert not registry_file.exists()
    assert not doc_exists(root / ".sldb", registry_file.relative_to(root).as_posix())

    missing = main(["repo", "remove", "not-registered", "--store", str(store_path)])
    missing_out = capsys.readouterr().out
    assert missing == 1
    assert "not-registered" in missing_out
    assert "(none)" in missing_out

    register_right = main([
        "repo",
        "register",
        "graph_ui",
        str(root),
        "--id",
        "graph_ui",
        "--store",
        str(store_path),
    ])
    capsys.readouterr()
    assert register_right == 0
    assert (root / "desk" / "registry" / "repo-graph_ui.md").exists()

    whoami = main(["repo", "whoami", "--root", str(root), "--store", str(store_path)])
    whoami_out = capsys.readouterr().out
    assert whoami == 0
    assert whoami_out.strip() == "graph_ui"


def test_repo_remove_missing_id_lists_existing_ids(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="graph-ui", repo_path="graph-ui")
    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    result = main(["repo", "remove", "ghost", "--store", str(store_path)])
    captured = capsys.readouterr()

    assert result == 1
    assert "Repository 'ghost' is not registered" in captured.out
    assert "graph-ui" in captured.out
    assert (registry_dir / "repo-graph-ui.md").exists()


def test_resolve_registered_desk_reports_actionable_missing_registry_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "desk" / "registry").mkdir(parents=True)
    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    with pytest.raises(SLDBStoreError, match="Supported path: run 'deskops repo register <name> --path <abs>'"):
        EcosystemIdentity(str(store_path)).how_do_i_find_another("deskops")



def test_resolve_canonical_project_identity_reports_actionable_unregistered_root_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    repo_root = tmp_path / "sender-repo"
    _write_config(repo_root, "sender-repo")
    _write_repo_doc(registry_dir, repo_id="sender-repo", repo_path="other-root")

    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    expected = f"Supported path: run 'deskops repo register <name> --path {repo_root.resolve()}'"
    with pytest.raises(SLDBStoreError, match=re.escape(expected)):
        EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root, require_registry_match=True)



def test_repo_register_accepts_optional_path_flag_and_does_not_crash_on_registry_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "ecosystem"
    desk_root = root / "desk"
    registry_dir = desk_root / "registry"
    registry_dir.mkdir(parents=True)
    # A real store that registers RepositoryDoc: the registration is written and tracked in
    # its transaction (the old fake tracking seam is gone with doc_io).
    from sldb.api import add_model, init_store

    init_store(path=root)
    store_path = root / ".sldb"
    add_model(store_path, "deskops.models:RepositoryDoc", pythonpath=str(Path(__file__).resolve().parents[1]))

    _write_repo_doc(registry_dir, repo_id="existing-repo", repo_path="tools/existing-repo")

    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    monkeypatch.setattr("deskops.cli.commands.repo.get_store_context", lambda _arg: (store_path, root))
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, root))
    monkeypatch.setattr("deskops.cli.commands.repo.find_local_store", lambda: store_path)

    repo_root = (tmp_path / "external" / "deskops").resolve()
    result = main([
        "repo",
        "register",
        "deskops",
        "--path",
        str(repo_root),
        "--store",
        str(store_path),
    ])

    captured = capsys.readouterr()
    output_path = registry_dir / "repo-deskops.md"

    assert result == 0
    assert output_path.exists()
    assert doc_exists(store_path, "repo-deskops")
    assert "Unexpected:" not in captured.out
    assert f"Wrote {output_path}" in captured.out

    entries = load_repository_registry(desk_root, root)
    deskops_entry = next(entry for entry in entries if entry.id == "deskops")
    assert deskops_entry.repo_root == repo_root

FILE:instruccion
Cold-bundle de la tarea task-repo-register-guarda-rutas-relativas-a-la-raiz-del-ecosistema-y-doctor-nombra-las-entradas-del-regis: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_repo_identity.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_registry_robustness.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_ecosystem_registry.py
- {'cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas': 'cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea'}


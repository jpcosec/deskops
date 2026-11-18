FILE:desk/tasks/task-los-git-que-deskops-parsea-usan-core-quotepath-false-y-los-ids-nuevos-se-pliegan-a-ascii.md
---
sldb:
  by: agent
  at: '2026-11-18T19:43:12Z'
  authority: generated
  via: save_document_payload
id: task-los-git-que-deskops-parsea-usan-core-quotepath-false-y-los-ids-nuevos-se-pliegan-a-ascii
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-nombres-de-tarea-con-acentos-git-cita-las-rutas-y-el-hook-de-wt-las-rechaza.md
- desk/inbox/20261118-154919-unclear-queue-20261118t184427z-integrate-task-deskops-desk-update-apply-sobre-el-repo-de-deskops-no-vac-a-el-path-de-los-modelos-en-sldb-core-mode.md
depends_on: []
pills: []
files:
- deskops/specs/compiler.py
- deskops/doc_access.py
- deskops/services/drawer.py
- deskops/services/closure.py
- tests/test_ascii_ids.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# Los git que deskops parsea usan core.quotepath=false y los ids nuevos se pliegan a ASCII

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de AntonIA (2026-11-09): con ids que llevan acentos (p. ej. task-cc35a-transacción-...) git imprime las rutas citadas con escapes octales (core.quotepath=true por defecto) y un hook externo de worktrees las rechaza; hoy se esquiva poniendo core.quotepath=false por entorno. En deskops, `git ls-files .sldb` ya imprime rutas citadas (inbox-note-decisi\303\263n-...). deskops/services/drawer.py ya pliega los slugs a [a-z0-9], pero deskops/specs/compiler.py y deskops/doc_access.py conservan acentos (usan str.isalnum).

## Goal

_Describe the concrete result this task must produce._

(1) Toda llamada a git dentro de deskops cuya salida se parsea pasa -c core.quotepath=false (no se usa -z en esta tarea). (2) Los ids que deskops deriva de un titulo se pliegan a ASCII (á->a, ñ->n, ü->u) con un solo helper compartido por compiler.py, doc_access.py y drawer.py; un id dado explicitamente por el usuario no se toca. (3) Los ids existentes con acentos siguen resolviendo por selector exacto; no se renombran ni se migran; si el id plegado de una tarea nueva coincide con uno existente, se aplica la regla de colision que ya tenga add task.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/specs/compiler.py (alrededor de las lineas 155-159), deskops/doc_access.py (157-161), deskops/services/drawer.py (288-290), las llamadas git de deskops/services/closure.py (alrededor de 645, 695 y 1555) y cualquier otra llamada git con salida parseada que muestre `grep -rn '"git"' deskops/`; un test nuevo tests/test_ascii_ids.py. No entra: renombrar o migrar ids ya commiteados (CC35a y otros), el hook externo de worktrees (no vive en este repo), cambiar la longitud maxima de los ids. Incluye además deskops/integrate.py (posterior a esta tarea): load_closed_task y _receipt_commit (alrededor de la línea 100) parsean 'git ls-tree --name-only' y 'git log'. Con un id con tilde, ls-tree cita la ruta y el recibo evidence-commit no se encuentra. Así falló el 2026-11-18 el integrate automático de la tarea de desk update (nota de la cola en references). Test: integrate encuentra el código de una tarea cerrada cuyo id tiene tilde.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Helper `ascii_slug(text)` en un modulo comun (unicodedata.normalize('NFKD') y descarte de marcas combinantes, luego la regla de caracteres actual). 2) Reemplazar las tres implementaciones por el helper. 3) Agregar `-c core.quotepath=false` (o -z con parseo por NUL) a cada git cuya salida se parsea. 4) tests/test_ascii_ids.py: `deskops add task --title 'Transacción ñandú'` en un desk sandbox produce un id solo ASCII; un TaskDoc con id acentuado creado por la API sigue resolviendo con `deskops show task <id>`; un archivo sin trackear con nombre acentuado en .sldb no rompe el parseo de git del cierre. Precisiones del preflight 1: el helper vive en un modulo nuevo deskops/slugs.py (funcion ascii_slug); la regla de caracteres es la de deskops/services/drawer.py _slug: minusculas, re.sub(r'[^a-z0-9]+', '-', ...) y strip('-'), con el plegado NFKD aplicado antes; la longitud maxima de cada llamador se conserva. La auditoria cubre las llamadas a subprocess cuyo argv empieza con 'git' (literal o lista) en deskops/; llamadas armadas dinamicamente que no aparezcan con grep -rn "'git'\|\"git\"" quedan fuera.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_ascii_ids.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

tests/test_ascii_ids.py pasa; `grep -rn quotepath deskops/` muestra la opcion en las llamadas git parseadas; los ids acentuados existentes siguen resolviendo; suite sin fallas nuevas.

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

FILE:deskops/specs/compiler.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from collections.abc import Collection

from pydantic.fields import PydanticUndefined

from deskops.cli.model_introspection import artifact_id_pattern
from deskops.cli.model_introspection import artifact_status_default
from deskops.cli.model_introspection import artifact_tags_default
from deskops.models.task import TaskDoc
from deskops.models.task_types import declared_evidence_list


@dataclass(slots=True)
class CompiledTaskSpec:
    task_payload: dict[str, Any]


@dataclass(slots=True)
class CompiledArtifactSpec:
    artifact_payload: dict[str, Any]


def compile_task_spec(
    raw_payload: dict[str, Any],
    *,
    entry_node: str,
) -> CompiledTaskSpec:
    """Compile a task payload. The task starts at ``entry_node`` of the lifecycle graph
    (deskops/lifecycle.py); no per-task primitives or routine are generated.

    This is the one normalization of a task payload: a missing ``title`` is a ``KeyError``
    (the raw payload has no such key; a blank title is the model's own refusal, ``TaskDoc``),
    every list field is coerced to a list of strings, and
    ``closeout_evidence`` is stripped of blanks. ``current_node`` keeps the payload's value
    and falls back to ``entry_node`` (pass ``""`` to normalize a stored task as it is).
    """
    artifact = getattr(TaskDoc, "__artifact__", {})
    if raw_payload.get("title") is None:
        raise KeyError("Task payload must include 'title'")
    title = str(raw_payload["title"]).strip()
    slug = _slugify(title)
    task_id = str(raw_payload.get("id") or str(artifact.get("id_pattern", "task-{slug}")).format(slug=slug))
    task_payload = {
        "title": title,
        "id": task_id,
        "status": str(raw_payload.get("status") or artifact.get("status_default") or "draft"),
        "why": str(raw_payload.get("why") or "Not provided."),
        "goal": str(raw_payload.get("goal") or ""),
        "scope": str(raw_payload.get("scope") or ""),
        "references": _coerce_list(raw_payload.get("references") or []),
        "depends_on": _coerce_list(raw_payload.get("depends_on") or []),
        "pills": _coerce_list(raw_payload.get("pills") or []),
        "files": _coerce_list(raw_payload.get("files") or []),
        "implementation_path": str(raw_payload.get("implementation_path") or ""),
        "validation": _coerce_list(raw_payload.get("validation") or []),
        "done_when": str(raw_payload.get("done_when") or ""),
        "history": _coerce_list(raw_payload.get("history") or []),
        "tags": _coerce_list(raw_payload.get("tags") or list(artifact.get("tags") or [])),
        "task_type": str(raw_payload.get("task_type") or ""),
        "inherits_from": _coerce_list(raw_payload.get("inherits_from") or []),
        "inherit_acceptance_context": bool(raw_payload.get("inherit_acceptance_context") or False),
        "atoms": _coerce_list(raw_payload.get("atoms") or []),
        "from_drawer": str(raw_payload.get("from_drawer") or ""),
        "closeout_evidence": declared_evidence_list(raw_payload.get("closeout_evidence")),
    }
    task_payload["current_node"] = str(raw_payload.get("current_node") or entry_node)
    return CompiledTaskSpec(task_payload=task_payload)


def compile_artifact_spec(
    artifact_id: str,
    raw_payload: dict[str, Any],
    *,
    model_fields: Collection[str] | None = None,
) -> CompiledArtifactSpec:
    """Compile a raw payload into an artifact payload using the Pydantic model.

    The Pydantic model is the single source of truth for which fields exist and
    their defaults. Its ``__artifact__`` attribute carries the artifact-level
    config: id_pattern, status_default and the default tags.
    """
    from deskops.doc_access import ARTIFACT_MODELS

    display_value = raw_payload.get("title") or raw_payload.get("name") or raw_payload.get("id")
    if display_value is None:
        raise KeyError(f"Payload for {artifact_id} must include 'title', 'name', or 'id'")
    title = str(display_value).strip()
    if not title:
        raise ValueError(f"Payload for {artifact_id} has empty title/name/id after stripping whitespace")
    slug = _slugify(title)

    id_pattern = artifact_id_pattern(artifact_id)
    doc_id = str(raw_payload.get("id") or id_pattern.format(slug=slug))

    supported = set(model_fields or [])
    payload: dict[str, Any] = {"id": doc_id}
    if "title" in supported:
        payload["title"] = title

    model = ARTIFACT_MODELS.get(artifact_id)
    if model is not None:
        for field_name, field_info in model.model_fields.items():
            if field_name == "id":
                continue  # already handled

            # Value from raw_payload overrides everything
            if field_name in raw_payload and raw_payload[field_name] is not None:
                payload[field_name] = raw_payload[field_name]
                continue

            # Apply defaults from the Pydantic model
            default = field_info.default
            if default is PydanticUndefined:
                factory = getattr(field_info, "default_factory", None)
                if factory is not None:
                    payload[field_name] = []  # default_factory=list
                # else: required field, leave as None (model validation handles it)
            elif isinstance(default, str):
                payload[field_name] = default
            elif isinstance(default, (list, tuple)):
                payload[field_name] = list(default)
            # else: other default types — leave for model validation

    # Handle status_default from the artifact config (not in the model); an artifact
    # that declares none (atom, materialization) keeps the historical "active".
    if "status" in supported and "status" not in payload:
        status_default = artifact_status_default(artifact_id)
        payload["status"] = "active" if status_default is None else str(status_default)

    # Handle tags default — prefer model factory, fall back to artifact config
    if "tags" in supported and "tags" not in payload:
        # Check if model has default_factory for tags
        if model is not None and "tags" in model.model_fields:
            field_info = model.model_fields["tags"]
            factory = getattr(field_info, "default_factory", None)
            if factory is not None:
                payload["tags"] = []
            else:
                payload["tags"] = _coerce_list(artifact_tags_default(artifact_id))
        else:
            payload["tags"] = _coerce_list(artifact_tags_default(artifact_id))

    return CompiledArtifactSpec(artifact_payload=payload)


def _coerce_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def _slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    slug = "-".join(parts) or "item"
    return slug[:100].rstrip("-")

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
from deskops.desk_paths import not_found_message
from deskops.desk_paths import resolve_selector
from deskops.desk_paths import selector_stem
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
    A path selector (``desk/...``) asks by its stem (``selector_stem``).
    """
    if not selector or not str(selector).strip():
        raise ValueError(f"Empty or whitespace-only selector provided for {what}")
    if not _tracked_surface(root, directory):
        # CC35b-a3: untracked surface, resolved on disk
        return resolve_selector(desk_root(root), [directory], selector, pattern, what, recursive=recursive)
    stem = selector_stem(desk_root(root), selector)
    base = relative_path(root, directory) + ("/**/" if recursive else "/")
    by_name = {"prefix": stem, "path_glob": base + pattern}
    if model is not None:
        by_name["model"] = model
    for query in (by_name, {"path_glob": f"{base}{stem}*.md"}):
        found = _select_one(root, query, selector, what)
        if found is not None:
            return found
    raise FileNotFoundError(not_found_message(what, selector))


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
    raise FileNotFoundError(not_found_message(artifact_id, selector))


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
    """The registered repository's root: ``~`` expanded, a relative path against ``root``
    (the repo that holds ``desk/registry``), the same resolution as every registry reader."""
    from deskops.identity import resolve_registered_root

    return resolve_registered_root(root, str(repository["path"])) or root.resolve()


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

FILE:deskops/services/drawer.py
"""Drawer lookup and inbox-to-drawer promotion.

The drawer holds disorganized material (features, issues, questions, loose task
candidates). This service resolves a drawer file by selector, records a task's
drawer origin, and promotes an inbox note into a loose drawer task candidate.
It never promotes drawer material into an active task.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
import re
from typing import Any
from typing import Callable

import yaml
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops import doc_access
from deskops.models import TaskDoc
from deskops.services.references import alert_dangling
from deskops.services.references import dangling_referrers


@dataclass
class DrawerPromotion:
    """Outcome of one inbox-to-drawer promotion, ready for the CLI to print."""

    exit_code: int
    messages: list[str] = field(default_factory=list)


@dataclass
class DrawerRemoval:
    """Outcome of removing one drawer entry, ready for the CLI to print."""

    exit_code: int
    messages: list[str] = field(default_factory=list)


class DrawerService:
    DRAWER_INDEX_FILES = {"README.md", "Board.md"}

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"

    def resolve_drawer_source(self, selector: str) -> Path:
        """The desk/drawer/ file a task is being authored from.

        Accepts a path (relative to the repo root, or absolute) or a stem /
        unique slug fragment searched across every drawer subfolder, since the
        drawer holds features, issues and questions, not only task candidates.
        The file must live under desk/drawer/.
        """
        drawer_root = (self.desk_root / "drawer").resolve()
        candidate = Path(selector)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        if candidate.is_file():
            resolved = candidate.resolve()
            if drawer_root not in resolved.parents:
                raise ValueError(f"--from-drawer must point inside desk/drawer/: {selector}")
            return resolved
        if not drawer_root.exists():
            raise FileNotFoundError(f"No drawer found at {drawer_root}")
        files = sorted(
            path for path in drawer_root.rglob("*.md")
            if path.is_file() and path.name not in self.DRAWER_INDEX_FILES
        )
        exact = [path for path in files if selector in {path.name, path.stem}]
        matches = exact or [path for path in files if selector.lower() in path.stem.lower()]
        if not matches:
            raise FileNotFoundError(f"No drawer file matches '{selector}'")
        if len(matches) > 1:
            listing = ", ".join(str(path.relative_to(drawer_root)) for path in matches)
            raise ValueError(f"Ambiguous drawer selector '{selector}': {listing}")
        return matches[0].resolve()

    def attach_drawer_source(self, payload: dict[str, Any], drawer_file: Path) -> dict[str, Any]:
        """Record where an authored task came from, without copying or deleting it.

        Stored in the task's own from_drawer field, not in references:
        `deskops edit task <id> references ...` replaces that whole list (the
        closeout step does exactly that), which would silently drop the origin.
        One field, one fact -- no parallel tag that could drift from it.
        Cleanup of the drawer file is left to a human."""
        relative = drawer_file.resolve().relative_to(self.root.resolve()).as_posix()
        return {**payload, "from_drawer": relative}

    def promote_inbox_to_drawer_task(
        self,
        selector: str,
        title_override: str | None = None,
        *,
        parse_sections: Callable[[str], dict[str, Any]],
    ) -> DrawerPromotion:
        """Promote one inbox note into a loose drawer task candidate."""
        source = self._resolve_unique(self.desk_root / "inbox", selector)
        if source is None:
            return DrawerPromotion(1, [f"No inbox note found for {selector}"])
        if isinstance(source, list):
            listing = ", ".join(path.stem for path in source)
            return DrawerPromotion(1, [f"Ambiguous inbox note selector {selector}: {listing}"])

        note = self._read_markdown(source)
        title = (title_override or note["title"] or source.stem).strip()
        task_id = f"task-{self._slug(title)}"
        target = self.desk_root / "drawer" / "tasks" / f"{task_id}.md"
        if target.exists():
            return DrawerPromotion(1, [f"Drawer task already exists: {target}"])

        parsed = parse_sections(note["body"])
        messages = [f"Created drawer task candidate {task_id}"]
        with doc_access.desk_transaction(self.root) as transaction:
            if transaction is not None:
                transaction.record(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                self._render_drawer_task(
                    title=title,
                    task_id=task_id,
                    source_path=source.relative_to(self.root),
                    body=note["body"],
                    parsed_sections=parsed,
                ),
                encoding="utf-8",
            )
            # Untrack before deleting: the note is a tracked InboxNoteDoc, so
            # unlinking the file alone leaves an orphan entry in the store and
            # `deskops status` reports it as an invalid missing document.
            # Untrack first so a store failure cannot destroy the source file.
            untrack_message = self._untrack_note(source)
            if transaction is not None:
                transaction.record(source)
            source.unlink(missing_ok=True)
        if untrack_message:
            messages.append(untrack_message)
        messages.append(f"Deleted source file {source}")
        messages.append(f"Path: {target}")
        return DrawerPromotion(0, messages)

    def remove_entry(self, selector: str, *, force: bool = False) -> DrawerRemoval:
        """Remove one drawer file, its tracking, and its bullets on the drawer board.

        Every other reference to it (``sldb.api.referrers`` over the desk graph) is left as it
        is and reported on stderr as ``alert: <entry> still referenced by <referrer>``.

        A task in desk/tasks/ that records the entry in from_drawer blocks the
        removal unless force is set, so deleting the source cannot silently
        leave active work pointing at a file someone still expects to exist.
        """
        try:
            source = self.resolve_drawer_source(selector)
        except (FileNotFoundError, ValueError) as exc:
            return DrawerRemoval(1, [f"Error: {exc}"])

        relative = source.relative_to(self.root).as_posix()
        if not force:
            owners = self._tasks_recording(relative)
            if owners:
                listing = ", ".join(owners)
                return DrawerRemoval(
                    1,
                    [
                        f"Error: refusing to remove {relative}: "
                        f"task records it in from_drawer ({listing}). Use --force to remove it anyway."
                    ],
                )

        board = self.desk_root / "drawer" / "tasks" / "Board.md"
        board_changed = False
        with doc_access.desk_transaction(self.root) as transaction:
            if board.exists():
                original = board.read_text(encoding="utf-8")
                updated = self._without_entry_bullets(original, source.stem)
                if updated != original:
                    if transaction is not None:
                        transaction.record(board)
                    board.write_text(updated, encoding="utf-8")
                    board_changed = True
            # Read after the Board lost its bullets: what is left still names the entry once it is gone.
            dangling = dangling_referrers(self.root, source)
            doc_access.delete_doc(self.root, source)
        alert_dangling(relative, dangling)

        messages = [f"Removed drawer entry {relative}"]
        if board_changed:
            messages.append(f"Removed its bullets from {board.relative_to(self.root).as_posix()}")
        return DrawerRemoval(0, messages)

    def _tasks_recording(self, relative: str) -> list[str]:
        """Active task ids in desk/tasks/ whose from_drawer points at relative."""
        tasks_dir = self.desk_root / "tasks"
        if not tasks_dir.exists():
            return []
        owners: list[str] = []
        for path in sorted(tasks_dir.glob("task-*.md")):
            try:
                payload = extract_model_data(TaskDoc, path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001 - one unreadable task must not block the check
                continue
            if payload.get("from_drawer") == relative:
                owners.append(str(payload.get("id") or path.stem))
        return owners

    def _without_entry_bullets(self, text: str, stem: str) -> str:
        """Drop every line that starts with ``- `<stem>` ``."""
        prefix = f"- `{stem}` "
        return "".join(
            line for line in text.splitlines(keepends=True) if not line.startswith(prefix)
        )

    def _untrack_note(self, source: Path) -> str | None:
        """Drop the promoted note from the sldb store, best effort.

        Returns a human-readable line describing what happened, or None when
        there is nothing to say. Never raises: a promotion must not be left
        half-done because the store was unavailable."""
        store_path = self.root / ".sldb"
        if not store_path.exists():
            return None
        try:
            doc_access.untrack_doc(self.root, source)
            return None
        except Exception as exc:  # noqa: BLE001 - store problems must not abort the promotion
            return f"Warning: could not untrack '{source.stem}' from the store: {exc}"

    def _resolve_unique(self, directory: Path, selector: str) -> Path | list[Path] | None:
        if not directory.exists():
            return None
        candidates = sorted(directory.glob("*.md"))
        exact = [path for path in candidates if selector in {path.name, path.stem}]
        if exact:
            return exact[0] if len(exact) == 1 else exact
        lowered = selector.lower()
        matches = [path for path in candidates if lowered in path.stem.lower()]
        if not matches:
            return None
        return matches[0] if len(matches) == 1 else matches

    def _read_markdown(self, path: Path) -> dict[str, str]:
        text = path.read_text(encoding="utf-8")
        frontmatter: dict[str, Any] = {}
        body = text
        if text.startswith("---\n"):
            _, rest = text.split("---\n", 1)
            fm_block, body = rest.split("\n---\n", 1)
            frontmatter = yaml.safe_load(fm_block) or {}
        lines = body.strip().splitlines()
        title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else str(frontmatter.get("title") or path.stem)
        content = "\n".join(lines[1:]).strip() if lines and lines[0].startswith("# ") else body.strip()
        return {"title": title, "body": content}

    def _render_drawer_task(
        self,
        *,
        title: str,
        task_id: str,
        source_path: Path,
        body: str,
        parsed_sections: dict[str, Any],
    ) -> str:
        # A drawer task is a TaskDoc like any other task, so `add task --from-drawer`,
        # the store and the readers that extract TaskDoc can all read it.
        fields = parsed_sections["fields"]
        validation = fields.get("validation") or []
        if isinstance(validation, str):
            validation = [line.lstrip("- ").strip() for line in validation.splitlines() if line.strip()]
        payload = {
            "id": task_id,
            "title": title,
            "status": "deferred",
            "why": fields.get("why") or f"Promoted from the inbox note `{source_path}`.",
            "goal": fields.get("goal") or f"Triage and resolve the inbox message promoted from `{source_path}`.",
            "scope": fields.get("scope") or body.strip() or "No additional detail provided.",
            "implementation_path": fields.get("implementation_path") or "To be defined when the task is promoted.",
            "validation": validation,
            "done_when": fields.get("done_when") or "The message is resolved, answered, or promoted into active work.",
            # The source note is deleted below, so it is named in `why`, not referenced.
            "tags": ["workspace:desk", "artifact:task", "source:inbox"],
        }
        return render_model_markdown(TaskDoc, payload) + "\n"

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "task"

FILE:instruccion
Cold-bundle de la tarea task-los-git-que-deskops-parsea-usan-core-quotepath-false-y-los-ids-nuevos-se-pliegan-a-ascii: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_ascii_ids.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea


FILE:desk/tasks/task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe.md
---
sldb:
  by: agent
  at: '2026-11-16T15:28:46Z'
  authority: generated
  via: save_document_payload
id: task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-103216-unclear-closeout-supersede-rechaza-3-taskdocs-de-marcado-con-claves-checklists-routine.md
depends_on: []
pills: []
files:
- deskops/workspace.py
- deskops/cli/commands/desk.py
- tests/test_legacy_task_states.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# desk update migra las claves legacy checklists y routine del frontmatter de las tareas para que supersede y edit puedan reescribirlas

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de marcado del 2026-11-16 (desk/inbox/20261116-103216-unclear-closeout-supersede-rechaza-3-taskdocs-de-marcado-con-claves-checklists-routine.md). En UIs/marcado, deskops closeout supersede rechaza tres TaskDocs heredados de antes de la migracion (task-close-the-runtime-pipeline-baseline, task-close-the-source-and-marker-model-baseline, task-design-the-runtime-architecture-and-extension-model) con "Refusing to rewrite <id>.md: it has content its model (TaskDoc) does not declare, and rewriting would erase it: frontmatter key 'checklists'; frontmatter key 'routine'". El rechazo sale de write_doc en deskops/doc_access.py (undeclared_frontmatter_keys). desk update dice up to date y no las ve, deskops edit no puede quitarlas y retire exige estado cerrado. Bloquea la tarea de marcado task-cerrar-con-supersede-las-53-tareas-de-spec-y-diseno-de-marcado-b3 (50/53 cerradas). Prioridad 1 del supervisor.

## Goal

_Describe the concrete result this task must produce._

deskops desk update (dry-run) lista cada TaskDoc de desk/tasks cuyo frontmatter tiene la clave checklists o routine, que TaskDoc no declara, con el archivo y la clave, y da rc 1 como cualquier migracion pendiente; deskops desk update --apply quita esas dos claves del frontmatter (sin tocar el resto del documento) e imprime por cada archivo la clave quitada y su valor anterior en una linea, para que quede en la salida y en el commit. Despues de --apply, deskops closeout supersede sobre esa tarea ya no da el error de claves no declaradas. La lista de claves es cerrada (checklists, routine): otras claves no declaradas siguen dando el rechazo actual de write_doc.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/workspace.py (junto a legacy_task_states y migrate_legacy_task_states, que ya migran estados legacy de tareas), deskops/cli/commands/desk.py (el reporte y la condicion de "up to date") y tests en tests/test_legacy_task_states.py. No entra: cambiar write_doc ni su rechazo, agregar un flag a supersede, declarar checklists o routine en TaskDoc, cerrar las tareas de marcado (lo hace su coordinador con el CLI nuevo), ni el fallo de deskops message send sin --root que menciona la misma nota. Precisiones del preflight 1: (a) salida de --apply, una linea por clave quitada con la forma '<ruta relativa a la raiz>: removed <clave> = <valor anterior en JSON compacto de una linea>'. (b) desk update --apply da rc 0 si la migracion termina sin errores, igual que las otras migraciones de --apply; solo el dry-run con claves pendientes da rc 1. (c) Caso mixto: si una tarea tiene checklists o routine y ademas otra clave no declarada, --apply quita igual checklists y routine y deja la otra clave; supersede sigue rechazando la tarea por esa otra clave. (d) La edicion es textual sobre el frontmatter: se borran solo las lineas del bloque de esas claves y las demas claves conservan orden y texto, sin re-serializar el YAML. (e) desk/tasks es el de la raiz del desk (--root), igual que el resto de desk update.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer legacy_task_states y migrate_legacy_task_states en deskops/workspace.py, write_doc y undeclared_frontmatter_keys en deskops/doc_access.py, y el bloque de desk update en deskops/cli/commands/desk.py. 2) Detectar en desk/tasks los TaskDocs con checklists o routine en el frontmatter. 3) Reporte en el dry-run y rc 1. 4) En --apply, reescribir el frontmatter sin esas claves e imprimir clave y valor anterior. 5) Tests en un desk sandbox (tmp_path): una tarea con checklists y routine da el reporte y rc 1 en dry-run; tras --apply el archivo ya no tiene esas claves, conserva el cuerpo y el resto del frontmatter, y closeout supersede sobre ella no da el error de claves no declaradas; una tarea con otra clave no declarada no se toca y supersede sigue rechazandola.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_legacy_task_states.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas, cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los casos del paso 5 pasan y desk update --apply deja una tarea con checklists y routine reescribible por closeout supersede.

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

FILE:deskops/workspace.py
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
import importlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
from typing import Literal

import yaml

from deskops.constants import CURRENT_DESK_FORMAT
from deskops.paths import data_path

DeskClassification = Literal["absent", "empty", "legacy", "current"]

_MODELED_DESK_TOP_LEVEL_DIRS = {
    "tasks",
    "contexts",
    "rituals",
    "atoms",
    "roles",
    "registry",
    "steps",
    "faq",
}


@dataclass
class DeskScaffoldResult:
    created_paths: list[Path]
    #: Managed seeds whose bytes differed from the package's and were restored (the lifecycle graph).
    rewritten_paths: list[Path] = field(default_factory=list)

    @property
    def wrote_anything(self) -> bool:
        return bool(self.created_paths or self.rewritten_paths)


@dataclass
class DeskInspection:
    classification: DeskClassification
    surface_docs: list[Path]
    missing_surfaces: list[str]
    malformed_surfaces: list[str]
    tracked_surface_docs: set[Path]
    invalid_surface_docs: list[str]
    store_check_message: str | None = None


@dataclass
class DeskMigrationResult:
    adopted: list[str]
    preserved: list[str]
    still_manual: list[str]

    @property
    def changed(self) -> bool:
        return bool(self.adopted)


def ensure_target_directory(path: Path) -> tuple[bool, str | None]:
    if not path.exists():
        return False, f"Error: Path {path} does not exist."
    if not path.is_dir():
        return False, f"Error: Path {path} is not a directory."
    return True, None


def classify_desk(root: Path) -> DeskClassification:
    return inspect_desk(root).classification


def inspect_desk(root: Path) -> DeskInspection:
    desk_dir = root / "desk"
    if not desk_dir.exists():
        return DeskInspection(
            classification="absent",
            surface_docs=[],
            missing_surfaces=["desk/"],
            malformed_surfaces=[],
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    surface_docs = _surface_docs(desk_dir)
    if not surface_docs:
        return DeskInspection(
            classification="empty",
            surface_docs=[],
            missing_surfaces=[],
            malformed_surfaces=[],
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    missing_surfaces: list[str] = []
    malformed_surfaces: list[str] = []

    config_path = desk_dir / "config.json"
    if not config_path.exists():
        missing_surfaces.append("desk/config.json")
        return DeskInspection(
            classification="legacy",
            surface_docs=surface_docs,
            missing_surfaces=missing_surfaces,
            malformed_surfaces=malformed_surfaces,
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    desk_format = _read_declared_desk_format(config_path)
    if desk_format != CURRENT_DESK_FORMAT:
        malformed_surfaces.append(
            f"desk/config.json (versions.desk_format={desk_format!r}; expected {CURRENT_DESK_FORMAT!r})"
        )

    tracked_surface_docs, invalid_surface_docs, store_check_message = _inspect_surface_store_health(root, surface_docs)
    malformed_surfaces.extend(invalid_surface_docs)
    if store_check_message:
        malformed_surfaces.append(store_check_message)

    classification: DeskClassification = "legacy" if malformed_surfaces else "current"
    return DeskInspection(
        classification=classification,
        surface_docs=surface_docs,
        missing_surfaces=missing_surfaces,
        malformed_surfaces=malformed_surfaces,
        tracked_surface_docs=tracked_surface_docs,
        invalid_surface_docs=invalid_surface_docs,
        store_check_message=store_check_message,
    )


def migrate_desk(root: Path) -> DeskMigrationResult:
    before = inspect_desk(root)
    adopted: list[str] = []
    preserved = [str(path.relative_to(root)) for path in before.surface_docs]
    still_manual: list[str] = []

    result = seed_desk(root)
    adopted.extend(str(path.relative_to(root)) for path in result.created_paths)

    if _write_or_patch_config(root) == "updated":
        adopted.append("desk/config.json (patched desk_format)")

    after = inspect_desk(root)
    tracked_after = after.tracked_surface_docs if after.classification in {"legacy", "current"} else set()
    for path in after.surface_docs:
        rel = str(path.relative_to(root))
        if path not in tracked_after:
            still_manual.append(f"{rel} (preserved; manual model conversion or sldb docs track required)")

    for invalid in after.invalid_surface_docs:
        still_manual.append(f"{invalid} (manual SLDB/model repair required)")

    if after.store_check_message:
        still_manual.append(f"{after.store_check_message} (manual SLDB health follow-up)")

    return DeskMigrationResult(
        adopted=_dedupe(adopted),
        preserved=_dedupe(preserved),
        still_manual=_dedupe(still_manual),
    )


#: The one placeholder the desk templates use (CC36, e3): replaced with the project directory's
#: name by ``str.replace``; the JSON and YAML templates have braces of their own.
DESK_NAME_PLACEHOLDER = "{desk_name}"

#: The declaration of the desk a repository gets; its ``file:`` seeds are relative to ``deskops/data/``
#: (``templates/`` for the desk's own files, ``lifecycle/`` for the lifecycle graph's documents).
DESK_DECLARATION_PATH = data_path("data", "desk_declaration.yaml")
DESK_DATA_PATH = data_path("data")
DESK_TEMPLATES_PATH = DESK_DATA_PATH / "templates"

#: The document seed whose ``system_prompt`` is code (``deskops.services.review.SYSTEM``), not
#: declaration data (CC36, f3).
_REVIEW_RUNTIME_SEED = "runtime-pi-deepseek-flash"


def desk_declaration(name: str) -> Any:
    """The desk declaration (``deskops/data/desk_declaration.yaml``) for a desk called ``name``.

    The ``folders`` and ``include`` rules are the file's; every seed comes back rendered as
    ``text`` with its ``mode``: ``file:`` templates read from ``deskops/data/`` and ``document:``
    payloads rendered through their deskops model, both with ``{desk_name}`` replaced. The bytes
    are the ones ``deskops init`` always wrote, and sldb only has to write them: its own
    ``document`` seed resolves the model from the store, which ``desk install`` and the first desk
    operation do not have yet. The lifecycle graph's seeds are ``managed``: a desk's copy that
    differs is rewritten.
    """
    from sldb.api import Seed
    from sldb.api import StoreDeclaration

    declared = StoreDeclaration.model_validate(yaml.safe_load(DESK_DECLARATION_PATH.read_text(encoding="utf-8")))
    seeds = [Seed(path=seed.path, mode=seed.mode, text=_seed_text(seed, name)) for seed in declared.seeds]
    return StoreDeclaration(folders=declared.folders, seeds=seeds, include=declared.include)


def _seed_text(seed: Any, name: str) -> str:
    if seed.text is not None:
        return seed.text.replace(DESK_NAME_PLACEHOLDER, name)
    if seed.file is not None:
        template = (DESK_DATA_PATH / seed.file).read_text(encoding="utf-8")
        return template.replace(DESK_NAME_PLACEHOLDER, name)
    document = seed.document
    payload = _replace_desk_name(document["payload"], name)
    if document["name"] == _REVIEW_RUNTIME_SEED:
        from deskops.services.review import SYSTEM

        payload["system_prompt"] = SYSTEM
    return _render_document(document["model"], payload)


def _render_document(model_name: str, payload: dict[str, Any]) -> str:
    """A document seed rendered by its model, as ``deskops init`` rendered the Board."""
    from sldb.runtime.validation import render_model_markdown

    import deskops.models as models

    return render_model_markdown(getattr(models, model_name), payload) + "\n"


def _replace_desk_name(value: Any, name: str) -> Any:
    if isinstance(value, str):
        return value.replace(DESK_NAME_PLACEHOLDER, name)
    if isinstance(value, list):
        return [_replace_desk_name(item, name) for item in value]
    if isinstance(value, dict):
        return {key: _replace_desk_name(item, name) for key, item in value.items()}
    return value


def seed_desk(target_path: Path, *, apply: bool = True, restore_managed: bool = False) -> DeskScaffoldResult:
    """Create the declared desk folders and seed files that are missing and, with
    ``restore_managed``, restore the managed ones that differ (``sldb.api.scaffold_store``).

    A desk's own files are ``if_missing`` seeds, so a desk that exists keeps them. The lifecycle
    graph's documents are ``managed``: ``deskops init`` and ``deskops desk update --apply`` restore
    a desk's copy that differs (``rewritten_paths``) and report it; every other scaffold (the first
    desk operation, ``doctor --repair``) only creates what is missing, so an edit to the desk's
    lifecycle is never undone silently. ``created_paths`` are the absolute paths of what was
    created, folders first and then seeds in declaration order; with ``apply=False`` nothing is
    written and both lists are what a run would do. A rewritten document the store tracks is
    reindexed (sldb's scaffold writes the file but does not rehash it).
    """
    from sldb.api import Seed
    from sldb.api import StoreDeclaration
    from sldb.api import scaffold_store

    declaration = desk_declaration(target_path.name)
    if not restore_managed:
        declaration = StoreDeclaration(
            folders=declaration.folders,
            seeds=[Seed(path=seed.path, mode="if_missing", text=seed.text) for seed in declaration.seeds],
            include=declaration.include,
        )
    report = scaffold_store(target_path, declaration=declaration, apply=apply)
    if apply and report.rewritten and (target_path / ".sldb" / "core").exists():
        from sldb.api import update_store_indexes

        from deskops.paths import package_pythonpath

        update_store_indexes(target_path / ".sldb", package_pythonpath(), wait=False)
    return DeskScaffoldResult(
        created_paths=[target_path / relative for relative in report.created],
        rewritten_paths=[target_path / relative for relative in report.rewritten],
    )


def desk_seed_text(name: str, path: str) -> str:
    """The text the desk seed at ``path`` (project-relative) carries for a desk called ``name``."""
    for seed in desk_declaration(name).seeds:
        if seed.path == path:
            return seed.text
    raise KeyError(path)


def default_ritual_text(ritual_id: str, name: str) -> str:
    """The ritual `deskops init` writes for one lifecycle state."""
    return desk_seed_text(name, f"desk/rituals/{ritual_id.removeprefix('ritual-')}.md")


def pending_desk_includes(root: Path) -> list[tuple[str, str]]:
    """``(model, path)`` of each desk document the declared includes name and the store does not
    track yet: what ``apply_desk_includes`` would track (every declared file when there is no store)."""
    from sldb.api.stores.declared_files import declared_files
    from sldb.api.stores.declared_includes import tracked_rows

    root = root.resolve()
    store_dir = root / ".sldb"
    tracked = set(tracked_rows(store_dir, root)) if store_dir.exists() else set()
    return [
        (model, path)
        for model, path, name in declared_files(root, desk_declaration(root.name))
        if (model, path, name) not in tracked and (root / path).is_file()
    ]


def apply_desk_includes(root: Path) -> list[str]:
    """Track every pending declared desk document under its declared model; the paths tracked."""
    from sldb.api.stores.apply_declaration import apply_includes

    root = root.resolve()
    return apply_includes(root / ".sldb", root, desk_declaration(root.name))


def _write_or_patch_config(root: Path) -> str | None:
    """Patch an existing ``desk/config.json`` to the current desk format and identity.

    The file itself is a seed, written by ``seed_desk`` before this runs; a missing one is left
    alone (this is migration, not scaffold).
    """
    config_path = root / "desk" / "config.json"
    if not config_path.exists():
        return None

    data: dict[str, object]
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        payload = {}

    if not isinstance(payload, dict):
        payload = {}

    data = dict(payload)
    versions = data.get("versions")
    if not isinstance(versions, dict):
        versions = {}
    versions = dict(versions)
    changed = versions.get("desk_format") != CURRENT_DESK_FORMAT
    versions["desk_format"] = CURRENT_DESK_FORMAT
    data["versions"] = versions
    data.setdefault("project_identity", root.name)

    rendered = json.dumps(data, indent=2) + "\n"
    if config_path.read_text(encoding="utf-8") != rendered:
        config_path.write_text(rendered, encoding="utf-8")
        return "updated"
    return None


def desk_markdown_docs(desk_dir: Path) -> list[Path]:
    return sorted(path for path in desk_dir.rglob("*.md") if path.is_file())


def desk_doc_is_modeled_by_sldb(root: Path, doc_path: Path) -> bool:
    try:
        relative = doc_path.resolve().relative_to((root / "desk").resolve())
    except ValueError:
        return False

    parts = relative.parts
    if not parts:
        return False

    top_level = parts[0]
    if len(parts) == 1 and relative.suffix == ".md":
        return False

    return top_level in _MODELED_DESK_TOP_LEVEL_DIRS


def desk_doc_unmodeled_reason(root: Path, doc_path: Path) -> str | None:
    try:
        relative = doc_path.resolve().relative_to((root / "desk").resolve())
    except ValueError:
        return None

    parts = relative.parts
    if not parts:
        return None

    top_level = parts[0]
    if len(parts) == 1 and relative.suffix == ".md":
        return f"desk/{relative.name} is a top-level desk note intentionally not SLDB-modeled"
    if top_level not in _MODELED_DESK_TOP_LEVEL_DIRS:
        return f"desk/{top_level}/** is intentionally not SLDB-modeled"
    return None


def modeled_desk_markdown_docs(root: Path, desk_dir: Path) -> list[Path]:
    return [path for path in desk_markdown_docs(desk_dir) if desk_doc_is_modeled_by_sldb(root, path)]


def unmodeled_desk_markdown_docs(root: Path, desk_dir: Path) -> list[Path]:
    return [path for path in desk_markdown_docs(desk_dir) if not desk_doc_is_modeled_by_sldb(root, path)]


def _surface_docs(desk_dir: Path) -> list[Path]:
    docs: list[Path] = []
    board = desk_dir / "tasks" / "Board.md"
    if board.exists():
        docs.append(board)

    tasks_dir = desk_dir / "tasks"
    if tasks_dir.exists():
        docs.extend(sorted(path for path in tasks_dir.glob("*.md") if path.name != "Board.md"))

    contexts_dir = desk_dir / "contexts"
    if contexts_dir.exists():
        docs.extend(sorted(path for path in contexts_dir.glob("*.md")))
    return docs


def _read_declared_desk_format(config_path: Path) -> str | None:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    versions = payload.get("versions")
    if not isinstance(versions, dict):
        return None
    desk_format = versions.get("desk_format")
    return desk_format if isinstance(desk_format, str) else None


def _inspect_surface_store_health(root: Path, surface_docs: list[Path]) -> tuple[set[Path], list[str], str | None]:
    store_path = root / ".sldb"
    if not store_path.exists():
        return set(), [], None

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sldb",
            "stores",
            "check",
            "--store",
            str(store_path),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    tracked: set[Path] = set()
    invalid: list[str] = []
    tracked_surface_set = {path.resolve() for path in surface_docs}

    payload: dict[str, object] | None = None
    if result.stdout.strip():
        try:
            loaded = json.loads(result.stdout)
        except json.JSONDecodeError:
            return tracked, invalid, "sldb stores check returned unreadable JSON"
        if isinstance(loaded, dict):
            payload = loaded

    if payload is not None:
        for model in payload.get("models", []):
            if not isinstance(model, dict):
                continue
            for doc in model.get("documents", []):
                if not isinstance(doc, dict):
                    continue
                doc_path = doc.get("path")
                if not isinstance(doc_path, str):
                    continue
                absolute = (root / doc_path).resolve()
                if absolute not in tracked_surface_set:
                    continue
                tracked.add(absolute)
                # An edited, re-contracted or moved document is an alert, not a malformed
                # surface: it does not make the desk legacy (see deskops.doctor_findings).
                note = doc.get("note")
                if note not in _NOT_MALFORMED_NOTES:
                    invalid.append(f"{doc_path} ({note})")

    # `stores check` exits 1 on a store that only moved; its JSON is the verdict, the exit
    # code only matters when there is no JSON to read.
    if result.returncode != 0 and payload is None:
        stderr = result.stderr.strip().splitlines()
        if stderr:
            return tracked, invalid, f"sldb stores check failed: {stderr[0]}"
        return tracked, invalid, "sldb stores check failed"

    return tracked, invalid, None


#: A document the model rejects is broken (`store/doc-invalid`), but it is reported by its own
#: listing (doctor's invalid task findings and sldb's finding), not as a legacy surface.
_NOT_MALFORMED_NOTES = frozenset({"ok", "benign_mutation", "data_mutation", "contract_mutation", "missing", "doc_invalid"})


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


# ---------------------------------------------------------------------------
# Desk-local task type registration and legacy task_type migration (GC01).
#
# A desk adds its own task types as `desk/models/*.py` subclasses (DC7); `desk update
# --apply` registers them with `sldb add_model` and `pythonpath` = the desk root. Legacy
# `task_type` strings are then re-tracked under the model their canonical type names
# (TaskDoc precisión 4).

_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)

#: The legacy ``task_type`` values that map onto a known type (the same map the migration
#: uses). Anything else is an unknown legacy value and migrates to ``task.code``.
LEGACY_TASK_TYPE_KEYS = frozenset({"code", "implementation", "test", "docs", "spec", "design", "external", ""})


def _task_frontmatter(path: Path) -> tuple[dict, str] | None:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None
    data = yaml.safe_load(match.group(1)) or {}
    return (data if isinstance(data, dict) else {}), text


def _frontmatter_task_type(path: Path) -> str:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return ""
    return str(parsed[0].get("task_type") or "").strip()


def discover_local_task_type_models(desk_dir: Path) -> list[tuple[str, str]]:
    """``(model_ref, class_name)`` for every ``TaskDoc`` subclass defined in ``desk/models/*.py``."""
    from deskops.models import TaskDoc

    models_dir = desk_dir / "models"
    if not models_dir.is_dir():
        return []
    desk_root = str(desk_dir.resolve())
    added = desk_root not in sys.path
    if added:
        sys.path.insert(0, desk_root)
    found: list[tuple[str, str]] = []
    try:
        for path in sorted(models_dir.glob("*.py")):
            if path.name.startswith("_"):
                continue
            module_name = f"models.{path.stem}"
            try:
                module = importlib.import_module(module_name)
            except Exception:
                continue
            for name in dir(module):
                obj = getattr(module, name, None)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, TaskDoc)
                    and obj is not TaskDoc
                    and getattr(obj, "__module__", "") == module.__name__
                ):
                    found.append((f"{module_name}:{name}", name))
    finally:
        if added:
            sys.path.remove(desk_root)
    return found


def pending_local_task_type_models(root: Path) -> list[str]:
    """Desk-local task type models that are not registered yet, as readable labels."""
    store_dir = root / ".sldb"
    if not store_dir.exists():
        return []
    try:
        from deskops.bootstrap import SLDBBootstrap

        registered = {name for name in SLDBBootstrap()._registered_model_entries(store_dir)}
    except Exception:
        registered = set()
    return [
        f"{module_ref} ({class_name})"
        for module_ref, class_name in discover_local_task_type_models(root / "desk")
        if class_name not in registered
    ]


def register_local_task_type_models(root: Path) -> list[str]:
    """Register unregistered desk-local task types; one change line per registration."""
    from sldb.api import add_model

    from deskops.bootstrap import SLDBBootstrap

    store_dir = root / ".sldb"
    if not store_dir.exists():
        return []
    registered = {name for name in SLDBBootstrap()._registered_model_entries(store_dir)}
    pythonpath = str((root / "desk").resolve())
    changes: list[str] = []
    for module_ref, class_name in discover_local_task_type_models(root / "desk"):
        if class_name in registered:
            continue
        try:
            add_model(store_dir, module_ref, pythonpath=pythonpath)
        except Exception as exc:
            raise RuntimeError(f"could not register desk-local task type {class_name}: {exc}") from exc
        changes.append(f"registered {class_name} from {module_ref}")
    return changes


def _task_type_migration_plan(root: Path) -> list[dict]:
    """Per-task migration plan for ``desk/tasks``, including the canonical type and target model."""
    from deskops.models.task_types import LEGACY_TASK_TYPE_MAP
    from deskops.models.task_types import canonical_task_type_name
    from deskops.operations import DeskopsOperations

    tasks_dir = root / "desk" / "tasks"
    if not tasks_dir.is_dir():
        return []
    operations = DeskopsOperations(root)
    registry = operations.registered_task_types()
    fallback = registry.get("task.code")
    plan: list[dict] = []
    for path in sorted(tasks_dir.glob("*.md")):
        if path.name == "Board.md" or path.name.startswith("board-"):
            continue
        raw = _frontmatter_task_type(path)
        canonical = raw if raw in registry else canonical_task_type_name(raw)
        target = registry.get(canonical) or fallback
        plan.append(
            {
                "path": path,
                "raw": raw,
                "canonical": canonical,
                "target_cls": target,
                "target_name": target.__name__ if target is not None else "TaskDoc",
                "unknown": bool(raw) and raw not in registry and raw not in LEGACY_TASK_TYPE_MAP,
                "lifecycle_errors": _task_lifecycle_errors(path),
            }
        )
    return plan


def _task_lifecycle_errors(path: Path) -> list[str]:
    """Why the task's lifecycle is inconsistent (``TaskDoc``'s validator); such a task is not written (CC37)."""
    from deskops.models.task_lifecycle import lifecycle_errors

    data = (_task_frontmatter(path) or ({}, ""))[0]
    history = data.get("history") or []
    return lifecycle_errors(str(data.get("status") or ""), str(data.get("current_node") or ""), [str(h) for h in history] if isinstance(history, list) else [str(history)])


def _inconsistent_task_line(item: dict, rel: str) -> str:
    return f"inconsistent task lifecycle in {rel}, not written: {'; '.join(item['lifecycle_errors'])}"


def pending_task_type_migration(root: Path) -> list[str]:
    """The change lines ``migrate_task_types`` would apply, so the dry run can list them."""
    from sldb.api.stores.doc_status import doc_status

    store_dir = root / ".sldb"
    lines: list[str] = []
    for item in _task_type_migration_plan(root):
        path = item["path"]
        rel = path.relative_to(root).as_posix()
        if item["lifecycle_errors"]:
            lines.append(_inconsistent_task_line(item, rel))
            continue
        tracked_model = None
        if store_dir.exists():
            status = doc_status(store_dir, rel)
            if status.exists:
                tracked_model = status.model
        needs_rewrite = item["raw"] != item["canonical"]
        needs_retrack = store_dir.exists() and tracked_model != item["target_name"]
        if not needs_rewrite and not needs_retrack:
            continue
        lines.append(_task_type_migration_line(item, rel))
    return lines


def _task_type_migration_line(item: dict, rel: str) -> str:
    if item["unknown"]:
        return (
            f"unknown legacy task_type {item['raw']!r} in {rel}: migrated to {item['canonical']} "
            f"(tracked as {item['target_name']})"
        )
    return (
        f"migrated {rel}: task_type {item['raw']!r} -> {item['canonical']!r} "
        f"(tracked as {item['target_name']})"
    )


def _rewrite_task_type(path: Path, canonical: str) -> None:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return
    data, text = parsed
    data["task_type"] = canonical
    body = text[_FRONTMATTER_RE.match(text).end():]
    path.write_text(
        "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body,
        encoding="utf-8",
    )


def migrate_task_types(root: Path) -> list[str]:
    """Rewrite legacy ``task_type`` values and re-track each task under its type's model.

    Idempotent: a second run changes nothing. ``closeout_evidence`` is preserved because the
    frontmatter rewrite only touches ``task_type``.
    """
    from sldb.api import track_document_file
    from sldb.api import untrack_document
    from sldb.api.stores.doc_status import doc_status

    store_dir = root / ".sldb"
    pythonpath = str((root / "desk").resolve())
    changes: list[str] = []
    for item in _task_type_migration_plan(root):
        path = item["path"]
        rel = path.relative_to(root).as_posix()
        if item["lifecycle_errors"]:
            changes.append(_inconsistent_task_line(item, rel))
            continue
        tracked_model = None
        if store_dir.exists():
            status = doc_status(store_dir, rel)
            if status.exists:
                tracked_model = status.model
        needs_rewrite = item["raw"] != item["canonical"]
        needs_retrack = store_dir.exists() and tracked_model != item["target_name"]
        if not needs_rewrite and not needs_retrack:
            continue
        if needs_rewrite:
            _rewrite_task_type(path, item["canonical"])
        if store_dir.exists() and item["target_cls"] is not None:
            if tracked_model is not None:
                try:
                    untrack_document(store_dir, status.name, pythonpath=pythonpath)
                except Exception:
                    pass
            track_document_file(store_dir, item["target_cls"].__name__, path, name=path.stem, pythonpath=pythonpath, force=True)
        changes.append(_task_type_migration_line(item, rel))
    return changes


# Alias de compatibilidad hacia atrás
scaffold_desk = seed_desk



# ---------------------------------------------------------------------------
# Tasks with a legacy lifecycle state (desks migrated before CC31): a terminal or drawer status
# with an empty history at a node, or a non-terminal one (active, ready_for_testing) with an
# empty history. TaskDoc's validator (CC37) rejects them on every model read,
# so they are listed from the frontmatter, one finding per document, and the migration table of
# ``deskops.models.task_lifecycle.legacy_state_migration`` writes the frontmatter directly.


@dataclass(frozen=True)
class LegacyTaskState:
    """One task under ``desk/tasks`` whose lifecycle TaskDoc's validator rejects."""

    path: Path
    rel: str
    task_id: str
    errors: list[str]
    #: ``{field: (before, after)}`` the table writes; empty when the table does not decide it.
    changes: dict[str, tuple[Any, Any]] = field(default_factory=dict)
    #: The task's summary before the migration (the migration to draft prepends its note to it).
    summary: str = ""

    def written_fields(self, today: Any = None) -> dict[str, Any]:
        """The frontmatter fields the migration writes: the table's, plus the summary with the
        migration note when the status moves to draft (n2). The note is not a report line."""
        from deskops.models.task_lifecycle import summary_with_migration_note

        written = {name: after for name, (_before, after) in self.changes.items()}
        if "status" in self.changes:
            written["summary"] = summary_with_migration_note(self.summary, str(self.changes["status"][0]), today)
        return written

    def migration_lines(self) -> list[str]:
        """``<file>: <field> <before> -> <after>``, one per changed field (b4)."""
        return [f"{self.rel}: {name} {_state_value(a)} -> {_state_value(b)}" for name, (a, b) in self.changes.items()]

    def finding(self) -> str:
        from deskops.models.task_lifecycle import UNMIGRATABLE_SUGGESTION

        return f"{self.rel}: {'; '.join(self.errors)}. To fix it, {UNMIGRATABLE_SUGGESTION}."


def _state_value(value: Any) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(str(item) for item in value) + "]"
    return str(value) if value not in ("", None) else "''"


def _task_files(root: Path) -> list[Path]:
    tasks_dir = root / "desk" / "tasks"
    if not tasks_dir.is_dir():
        return []
    return [p for p in sorted(tasks_dir.glob("*.md")) if p.name != "Board.md" and not p.name.startswith("board-")]


def _model_errors(text: str) -> list[str]:
    """Why ``TaskDoc`` rejects the document; ``[]`` when it reads it."""
    from deskops.models import TaskDoc
    from deskops.models.validation import validation_messages
    from pydantic import ValidationError
    from sldb.runtime.validation import extract_model_data

    try:
        extract_model_data(TaskDoc, text)
    except ValidationError as exc:
        return validation_messages(exc)
    except Exception as exc:  # noqa: BLE001 - any reason the model cannot read it is the finding
        return [str(exc)]
    return []


def legacy_task_states(root: Path) -> tuple[list[LegacyTaskState], list[LegacyTaskState]]:
    """``(migratable, unmigratable)``: the tasks the model rejects, read from their frontmatter.

    Each task is validated on its own, so one invalid document does not stop the walk (b8). A
    task whose lifecycle the table decides is migratable; any other rejected task is a finding
    with the validator's text and the fixed suggestion (b1).
    """
    from deskops.models.task_lifecycle import legacy_state_migration
    from deskops.models.task_lifecycle import lifecycle_errors

    migratable: list[LegacyTaskState] = []
    unmigratable: list[LegacyTaskState] = []
    for path in _task_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            parsed = _task_frontmatter(path)
        except (yaml.YAMLError, UnicodeDecodeError) as exc:
            unmigratable.append(LegacyTaskState(path, rel, path.stem, [f"unreadable frontmatter: {exc}"]))
            continue
        if parsed is None:
            continue
        data, text = parsed
        raw_history = data.get("history") or []
        history = [str(h) for h in raw_history] if isinstance(raw_history, list) else [str(raw_history)]
        status, node = str(data.get("status") or ""), str(data.get("current_node") or "")
        task_id = str(data.get("id") or path.stem)
        errors = lifecycle_errors(status, node, history)
        if not errors:
            errors = _model_errors(text)
            if errors:
                unmigratable.append(LegacyTaskState(path, rel, task_id, errors))
            continue
        changes = legacy_state_migration(status, node, history)
        target = migratable if changes else unmigratable
        summary = data.get("summary")
        target.append(LegacyTaskState(path, rel, task_id, errors, changes or {}, "" if summary is None else str(summary)))
    return migratable, unmigratable


def _migrated_frontmatter(frontmatter: str, changes: dict[str, Any]) -> str:
    """The frontmatter with only the named top-level fields rewritten, so nothing else moves.

    A field is its ``name:`` line plus the block-list items under it (``- x`` or indented);
    a scalar is written plain (``''`` when empty, single-quoted when YAML would not read it back
    as the same string), a list as a block list. A missing field is appended.
    """
    lines = frontmatter.split("\n")
    for name, after in changes.items():
        if isinstance(after, list):
            value_lines = [f"{name}:"] + [f"- {item}" for item in after]
        else:
            value_lines = [f"{name}: {_yaml_scalar(after)}" if after else f"{name}: ''"]
        index = next((i for i, line in enumerate(lines) if line.startswith(f"{name}:")), None)
        if index is None:
            lines.extend(value_lines)
            continue
        end = index + 1
        while end < len(lines) and lines[end][:1] in (" ", "-"):
            end += 1
        lines[index:end] = value_lines
    return "\n".join(lines)


def _yaml_scalar(value: Any) -> str:
    """``value`` plain when YAML reads it back as the same string, else single-quoted."""
    text = str(value)
    try:
        if "\n" not in text and yaml.safe_load(f"k: {text}") == {"k": text}:
            return text
    except yaml.YAMLError:
        pass
    return "'" + text.replace("\n", " ").replace("'", "''") + "'"


def rewrite_task_fields(path: Path, changes: dict[str, Any]) -> list[str]:
    """Write ``changes`` into a task's frontmatter without the model; ``[]`` once ``TaskDoc``
    reads the result, else why not (and the file is restored byte for byte).

    For a task the model rejects, which no model write can load: the migration of legacy
    states and ``closeout supersede`` of an incoherent task.
    """
    original = path.read_bytes()
    text = original.decode("utf-8")
    match = _FRONTMATTER_RE.match(text)
    if match is None:
        return ["no frontmatter"]
    new_text = "---\n" + _migrated_frontmatter(match.group(1), changes) + "\n---\n" + text[match.end():]
    path.write_text(new_text, encoding="utf-8")
    if errors := _model_errors(new_text):
        path.write_bytes(original)
        return errors
    return []


def migrate_legacy_task_states(root: Path) -> tuple[list[str], list[LegacyTaskState]]:
    """Write the table's fields into each migratable task; ``(lines, not migrated)``.

    The write goes to the file, not through sldb: sldb's untrack and model registration rebuild
    every document of the model and fail on any other invalid task, so the document route cannot
    write one task while another is still invalid. The new text is validated with ``TaskDoc``
    on its own; a task it still rejects is restored byte for byte and reported. The store's
    indexes are refreshed afterwards with the rest of ``desk update --apply``. Idempotent: a
    migrated task is coherent, so a second run finds nothing.
    """
    migratable, _ = legacy_task_states(root)
    lines: list[str] = []
    failed: list[LegacyTaskState] = []
    for state in migratable:
        if errors := rewrite_task_fields(state.path, state.written_fields()):
            failed.append(LegacyTaskState(state.path, state.rel, state.task_id, [f"not migrated, the result is still invalid: {'; '.join(errors)}"]))
            continue
        lines.extend(state.migration_lines())
    return lines, failed

FILE:deskops/cli/commands/desk.py
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from sldb.api import add_model
from sldb.api import remove_model
from sldb.api import track_document_file
from sldb.api import untrack_document
from sldb.api import update_store_indexes

from deskops.atom_tags import sync_tag_declaration
from deskops.workspace import ensure_target_directory
from deskops.workspace import inspect_desk
from deskops.workspace import legacy_task_states
from deskops.workspace import migrate_legacy_task_states
from deskops.doctor_findings import invalid_document_findings
from deskops.workspace import migrate_desk
from deskops.workspace import migrate_task_types
from deskops.workspace import apply_desk_includes
from deskops.workspace import pending_local_task_type_models
from deskops.workspace import pending_task_type_migration
from deskops.workspace import pending_desk_includes
from deskops.workspace import register_local_task_type_models
from deskops.workspace import seed_desk
from deskops.bootstrap import SLDBBootstrap, MODEL_REFS
from deskops.errors import DeskopsEnvironmentError
from deskops.paths import package_pythonpath
import deskops.models as models

#: The deskops FAQ model used to be registered with the same name sldb uses for its
#: own model. sldb federates models by name, so the old name must be migrated.
LEGACY_FAQ_MODEL = "FAQDoc"
LEGACY_FAQ_MODEL_REF = "deskops.models:FAQDoc"
FAQ_MODEL = "DeskFAQDoc"
FAQ_MODEL_REF = "deskops.models:DeskFAQDoc"


def legacy_faq_model_pending(entries: dict[str, Any]) -> bool:
    """Whether a store still registers the old deskops FAQ model name."""
    entry = entries.get(LEGACY_FAQ_MODEL)
    return entry is not None and getattr(entry, "model_ref", None) == LEGACY_FAQ_MODEL_REF


def moved_model_contracts(root: Path, entries: dict[str, Any]) -> list[str]:
    """Registered deskops models whose store contract no longer matches this checkout."""
    from sldb.store.hashing import hash_model_contract
    from sldb.store.io import load_models_index

    moved: list[str] = []
    for name, entry in sorted(entries.items()):
        model_ref = getattr(entry, "model_ref", "") or ""
        model_type = getattr(models, name, None)
        models_index = getattr(entry, "models_index", None)
        if not model_ref.startswith("deskops.models:") or model_type is None or not models_index:
            continue
        try:
            stored = load_models_index(root / models_index).contract_hash
        except Exception:
            continue
        if stored != hash_model_contract(model_type):
            moved.append(name)
    return moved


def migrate_legacy_faq_model(root: Path, *, pythonpath: str | None = None) -> list[str]:
    """Move an existing store from `FAQDoc` to `DeskFAQDoc`, keeping its documents.

    sldb exposes no model rename, so this registers the new name, retracks every
    document the old model owns, and removes the old entry with its document
    records. The Markdown files are never touched, so they stay byte-identical.
    """
    from sldb.store.io import load_documents_index
    from sldb.store.io import load_models_index

    store_dir = root / ".sldb"
    pythonpath = pythonpath or package_pythonpath()
    bootstrap = SLDBBootstrap()
    entries = bootstrap._registered_model_entries(store_dir)
    if not legacy_faq_model_pending(entries):
        return []

    changes: list[str] = []
    if FAQ_MODEL not in entries:
        add_model(store_dir, FAQ_MODEL_REF, pythonpath=pythonpath)
        changes.append(f"registered {FAQ_MODEL}")

    # The old class no longer exists, so its documents are read from the indexes
    # instead of resolving the model reference.
    legacy_entry = entries[LEGACY_FAQ_MODEL]
    legacy_index = load_models_index(root / legacy_entry.models_index)
    old_documents = load_documents_index(root / legacy_index.documents_index).documents
    tracked: set[str] = set()
    new_entry = bootstrap._registered_model_entries(store_dir).get(FAQ_MODEL)
    if new_entry is not None:
        new_index = load_models_index(root / new_entry.models_index)
        tracked = {document.name for document in load_documents_index(root / new_index.documents_index).documents}
    for document in old_documents:
        if document.name in tracked:
            continue
        track_document_file(store_dir, FAQ_MODEL, root / document.path, name=document.name, pythonpath=pythonpath, force=True)
        changes.append(f"tracked {document.name} as {FAQ_MODEL}")

    remove_model(store_dir, LEGACY_FAQ_MODEL, pythonpath=pythonpath, untrack_documents=True)
    changes.append(f"removed {LEGACY_FAQ_MODEL}")
    return changes


class DeskCLI:
    """Handle desk workspace scaffolding and rituals."""

    def run(self, args: Any) -> int:
        if args.desk_command == "install":
            return self.install(args)
        if args.desk_command == "migrate":
            return self.migrate(args)
        if args.desk_command == "replace":
            return self.replace(args)
        if args.desk_command == "update":
            return self.update(args)
        return 1

    def replace(self, args: Any) -> int:
        from deskops.services.replace import replace_text

        result = replace_text(
            Path(args.root),
            args.path,
            args.old,
            args.new,
            count=args.count,
        )
        print(f"Replaced {result.replacements} occurrence(s) in {result.path}")
        return 0

    def install(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        desk_dir = target_path / "desk"
        print(f"Scaffolding local desk at {desk_dir}...")
        result = seed_desk(target_path)
        for path in result.created_paths:
            print(f"Wrote {path}")
        for path in result.rewritten_paths:
            print(f"Rewrote {path}")

        if (target_path / ".sldb").exists():
            from deskops.lifecycle import write_lifecycle_graph

            for change in write_lifecycle_graph(target_path):
                print(f"Lifecycle graph: {change}")
        else:
            print("No .sldb store yet: run 'deskops init' to create it and the lifecycle graph that 'deskops advance' reads.")
        print("Scaffold complete.")
        print("Register the repo separately with 'deskops repo register ...' when you are ready.")
        return 0

    def migrate(self, args: Any) -> int:
        target_path = Path(args.root).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        result = migrate_desk(target_path)
        print(f"Desk migration report for {target_path}:")

        print("Adopted:")
        if result.adopted:
            for item in result.adopted:
                print(f"- {item}")
        else:
            print("- none")

        print("Preserved:")
        if result.preserved:
            for item in result.preserved:
                print(f"- {item}")
        else:
            print("- none")

        print("Still manual:")
        if result.still_manual:
            for item in result.still_manual:
                print(f"- {item}")
        else:
            print("- none")

        return 0

    def update(self, args: Any) -> int:
        root = Path(args.root).resolve()
        apply = getattr(args, "apply", False)

        desk_dir = root / "desk"
        store_dir = root / ".sldb"

        from deskops import lifecycle

        inspection = inspect_desk(root)

        # Tasks with a pre-CC31 lifecycle state: the model rejects them, and sldb with them every
        # other read of the store, so --apply migrates them first, from the frontmatter (d1).
        if apply and desk_dir.exists():
            migrated_lines, invalid_tasks = migrate_legacy_task_states(root)
            if migrated_lines:
                print("Migrating legacy task states...")
                for line in migrated_lines:
                    print(f"- {line}")
            legacy_pending: list = []
            invalid_tasks += legacy_task_states(root)[1]
            invalid_tasks.sort(key=lambda state: state.rel)
        else:
            legacy_pending, invalid_tasks = legacy_task_states(root) if desk_dir.exists() else ([], [])

        missing_desk_files: list[str] = []
        if inspection.classification == "absent":
            missing_desk_files.append("desk/")
        elif desk_dir.exists():
            if not (desk_dir / "tasks" / "Board.md").exists():
                missing_desk_files.append("desk/tasks/Board.md")
            if not (desk_dir / "drawer").exists():
                missing_desk_files.append("desk/drawer/")
            if not (desk_dir / "rituals" / "phase.md").exists():
                missing_desk_files.append("desk/rituals/phase.md")
            if not (desk_dir / "runtimes" / "runtime-pi-deepseek-flash.md").exists():
                missing_desk_files.append("desk/runtimes/runtime-pi-deepseek-flash.md")

        # The lifecycle graph's documents are managed seeds: a desk's copy that differs from the
        # package's is rewritten. A missing one is written with the rest of the scaffold.
        scaffold_plan = seed_desk(root, apply=False, restore_managed=True) if desk_dir.exists() else None
        lifecycle_rewrites = (
            [path.relative_to(root).as_posix() for path in scaffold_plan.rewritten_paths] if scaffold_plan else []
        )
        lifecycle_missing = bool(scaffold_plan) and any(
            path.relative_to(root).as_posix().startswith("desk/lifecycle/") for path in scaffold_plan.created_paths
        )

        bootstrap = SLDBBootstrap()
        registered_entries: dict[str, Any] = {}
        if store_dir.exists():
            try:
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception:
                pass

        legacy_faq_pending = legacy_faq_model_pending(registered_entries)
        if legacy_faq_pending and apply:
            print(f"Migrating the deskops FAQ model from {LEGACY_FAQ_MODEL} to {FAQ_MODEL}...")
            try:
                for change in migrate_legacy_faq_model(root):
                    print(f"- {change}")
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception as exc:
                print(f"Error: {exc}")
                return 1
            legacy_faq_pending = False

        moved_contracts = (
            moved_model_contracts(root, registered_entries) if store_dir.exists() else []
        )
        if moved_contracts and apply:
            pythonpath = package_pythonpath()
            for model_name in moved_contracts:
                print(f"Updating the {model_name} contract...")
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "sldb",
                        "models",
                        "update",
                        model_name,
                        "--store",
                        str(store_dir),
                        "--pythonpath",
                        pythonpath,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode != 0:
                    detail = result.stderr.strip() or result.stdout.strip()
                    print(f"Error: could not update the {model_name} contract: {detail}")
                    return 1
                print(f"Updated {model_name} contract.")
            registered_entries = bootstrap._registered_model_entries(store_dir)
            moved_contracts = moved_model_contracts(root, registered_entries)

        unregistered_models: list[str] = []
        copied_models: list[str] = []
        # A non-editable install has no owner store to inherit from; its directly
        # registered models are the expected state, not copies to convert.
        owner_store = bootstrap._deskops_owner_store()
        if owner_store is not None and store_dir.exists() and store_dir.resolve() == owner_store.resolve():
            # The owner store registers the deskops models directly; that is what
            # the other stores link to, not a copy of it.
            owner_store = None
        for model_name, model_ref in MODEL_REFS.items():
            entry = registered_entries.get(model_name)
            if entry is None:
                unregistered_models.append(model_name)
            elif (
                owner_store is not None
                and not getattr(entry, "origin", None)
                and getattr(entry, "model_ref", None) == model_ref
            ):
                copied_models.append(model_name)

        invalid_docs: list[str] = []
        missing_docs: list[str] = []
        store_invalid_docs: list[tuple[str, str]] = []
        all_store_invalid_docs: list[tuple[str, str]] = []
        missing_store = not store_dir.exists()
        if not missing_store:
            result = subprocess.run(
                [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_dir), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            payload = None
            if result.stdout and result.stdout.strip():
                try:
                    payload = json.loads(result.stdout)
                except json.JSONDecodeError as exc:
                    raise DeskopsEnvironmentError(
                        f"Could not parse 'sldb stores check' output for {store_dir}: {exc}"
                    ) from exc
            if payload is None and result.returncode != 0:
                reason = f": {result.stderr.strip()}" if result.stderr and result.stderr.strip() else ""
                raise DeskopsEnvironmentError(
                    f"'sldb stores check' failed for {store_dir} with exit code {result.returncode}{reason}"
                )
            if payload is None:
                raise DeskopsEnvironmentError(
                    f"'sldb stores check' produced no JSON output for {store_dir}"
                )
            for model in (payload or {}).get("models", []):
                for doc in model.get("documents", []):
                    doc_path = doc.get("path")
                    if not doc_path:
                        continue
                    if doc.get("note") not in ("ok", "doc_invalid"):
                        invalid_docs.append(f"{doc_path} ({doc.get('note')})")
                        if doc.get("note") == "missing":
                            missing_docs.append(doc.get("name") or Path(doc_path).stem)
            # The documents sldb names as store/doc-invalid, except the invalid tasks the
            # frontmatter listing above already reports (g3).
            reported_tasks = {state.rel for state in [*legacy_pending, *invalid_tasks]}
            all_store_invalid_docs = invalid_document_findings(payload or {})
            store_invalid_docs = [(rel, what) for rel, what in all_store_invalid_docs if rel not in reported_tasks]

        # The desk documents the package's declared includes name and the store does not
        # track yet, each with its declared model (deskops/data/desk_declaration.yaml).
        untracked_docs = pending_desk_includes(root) if desk_dir.exists() else []

        # The store declares the namespaces of desk/atoms/tag-namespaces.yaml for sldb's tag
        # family; the file wins (deskops.atom_tags.sync_tag_declaration).
        tag_declaration_pending = (
            desk_dir.exists() and not missing_store and sync_tag_declaration(root, apply=False)
        )

        pending_local_types = pending_local_task_type_models(root)
        pending_migration = pending_task_type_migration(root)
        # A task whose lifecycle TaskDoc's validator rejects is not retyped (CC37); it is listed
        # below as a legacy state to migrate or as an invalid task document.
        pending_migration = [line for line in pending_migration if not line.startswith("inconsistent ")]

        if not lifecycle_rewrites and not legacy_faq_pending and not missing_store and not missing_desk_files and not unregistered_models and not copied_models and not untracked_docs and not invalid_docs and not store_invalid_docs and not moved_contracts and not pending_local_types and not pending_migration and not legacy_pending and not invalid_tasks and not tag_declaration_pending:
            print("Desk is up to date.")
            return 0

        print("Desk divergence report:")
        if missing_store:
            print("- Missing store: .sldb")
        if legacy_faq_pending:
            print(
                f"- Legacy FAQ model: {LEGACY_FAQ_MODEL} ({LEGACY_FAQ_MODEL_REF}) should be {FAQ_MODEL}."
            )
        if moved_contracts:
            print(f"- Moved model contracts: {', '.join(moved_contracts)}")
        if lifecycle_rewrites:
            print(f"- Lifecycle documents to rewrite: {', '.join(lifecycle_rewrites)}")
        if missing_desk_files:
            print(f"- Missing desk structure: {', '.join(missing_desk_files)}")
        if unregistered_models:
            print(f"- Unregistered models: {', '.join(unregistered_models)}")
        if copied_models:
            print(f"- Copied deskops models: {', '.join(copied_models)}")
        if untracked_docs:
            print(f"- Untracked desk documents: {', '.join(path for _model, path in untracked_docs)}")
        if tag_declaration_pending:
            print("- Tag namespace declaration: .sldb/store.yaml differs from desk/atoms/tag-namespaces.yaml")
        if pending_local_types:
            print(f"- Unregistered desk-local task types: {', '.join(pending_local_types)}")
        if pending_migration:
            print(f"- Pending task type migration: {len(pending_migration)} task(s)")
        if invalid_docs:
            print(f"- Stale document hashes: {', '.join(invalid_docs)}")
        if store_invalid_docs:
            print(f"- Invalid documents (not written): {len(store_invalid_docs)} document(s)")
            for rel, what in store_invalid_docs:
                print(f"  - {rel}: {what}")
        if legacy_pending:
            print(f"- Legacy task states to migrate: {len(legacy_pending)} task(s)")
            for state in legacy_pending:
                for line in state.migration_lines():
                    print(f"  - {line}")
        if invalid_tasks:
            print(f"- Invalid task documents (not written): {len(invalid_tasks)} task(s)")
            for state in invalid_tasks:
                print(f"  - {state.finding()}")
        if not apply:
            print("\nRun with --apply to repair these issues.")
            return 1

        print("\nApplying repairs...")

        if missing_desk_files or lifecycle_rewrites or lifecycle_missing:
            scaffold = seed_desk(root, restore_managed=True)
            if missing_desk_files:
                print("Scaffolded missing desk structure.")
            for change in lifecycle.seed_changes(root, scaffold):
                print(f"Lifecycle graph: {change}")

        failed = False
        if unregistered_models or copied_models:
            if bootstrap.init_local_store(root) == 0:
                print("Registered missing models and converted copied deskops models.")
            else:
                print("Error: could not register the missing models (sldb rejects a tracked document; see the report above).")
                failed = True

        try:
            for change in register_local_task_type_models(root):
                print(f"- {change}")
        except Exception as exc:
            print(f"Error: {exc}")
            return 1
        try:
            for change in migrate_task_types(root):
                if not change.startswith("inconsistent "):
                    print(f"- {change}")
        except Exception as exc:
            print(f"Error: could not migrate the task types: {exc}")
            failed = True

        # Always: a store this --apply just created has no declaration yet (idempotent).
        try:
            declared_tags = sync_tag_declaration(root)
        except Exception as exc:
            print(f"Error: could not declare the tag namespaces: {exc}")
            return 1
        if declared_tags:
            print("Declared the tag namespaces of desk/atoms/tag-namespaces.yaml in .sldb/store.yaml.")

        # Recomputed: the scaffold may have written declared documents (the lifecycle graph).
        untracked_docs = pending_desk_includes(root) if desk_dir.exists() and store_dir.exists() else []
        if untracked_docs:
            declared_models = {path: model_name for model_name, path in untracked_docs}
            try:
                lifecycle.ensure_rule_model(root)
                tracked_paths = apply_desk_includes(root)
            except Exception as exc:
                # apply_includes tracks in order and stops at the first document sldb rejects, so
                # the first one still pending is the one the rule (named in ``exc``) refused.
                try:
                    refused = next(iter(pending_desk_includes(root)), None)
                except Exception:
                    refused = None
                where = f" ({refused[1]})" if refused else ""
                print(f"Error: could not track the declared desk documents{where}: {exc}")
                return 1
            for path in tracked_paths:
                model_name = declared_models.get(path, "its declared model")
                line = lifecycle.tracked_line(model_name, path)
                print(f"Lifecycle graph: {line}" if line else f"Tracked {path} as {model_name}.")

        if missing_docs:
            # A tracked document whose file is gone must be untracked, not
            # re-indexed: the store would keep describing something that is not there.
            pythonpath = package_pythonpath()
            for name in missing_docs:
                try:
                    untrack_document(root / ".sldb", name, pythonpath=pythonpath)
                    print(f"Untracked {name}: its file is gone.")
                except Exception as e:
                    print(f"Failed to untrack {name}: {e}")

        if invalid_docs or all_store_invalid_docs:
            pythonpath = package_pythonpath()
            update_store_indexes(root / ".sldb", pythonpath, wait=False)
            print("Updated store derived indexes.")

        # Exit 1 while a task or another document needs its owner's decision or a repair could not
        # run (the same as the dry-run, which exits 1 with any divergence).
        return 1 if invalid_tasks or store_invalid_docs or failed else 0

FILE:tests/test_legacy_task_states.py
"""Tasks with a lifecycle state from desks migrated before CC31 (task.debug of legacy states).

A terminal or drawer status with an empty history at ``ritual-execution`` is a state no
transition produces, so TaskDoc's validator (CC37) rejects it and sldb's store check stops at
the first such document. The seven fixtures are the five tasks of the shared_llm-gateway
reproduction (two superseded, one deferred, two draft after ``task_hands_to_closeout``) plus a
cancelled and a closed one (b6):

* ``deskops desk update`` (dry-run) lists what the table migrates and the tasks it does not
  decide, and writes nothing; ``--apply`` migrates (one ``<file>: <field> <before> -> <after>``
  line per field, b4), reports the rest with exit 1, and a second run migrates nothing (d1);
* ``deskops doctor`` reports each invalid task and goes on with every other check (d2, b9).

A non-terminal status with an empty history (``active``, ``ready_for_testing``; task.debug of
non-terminal tasks, decision of the overlord) is migrated to ``draft`` at the entry node with a
migration note in its summary (n1-n5).
"""
from __future__ import annotations

import contextlib
import difflib
import io
import json
from datetime import datetime
from datetime import timezone
import itertools
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]

from deskops.cli.commands.doctor import DoctorCLI
from deskops.cli.main import main
from deskops.models import TaskDoc
from deskops.models.task_lifecycle import UNMIGRATABLE_SUGGESTION
from deskops.models.task_lifecycle import legacy_state_migration
from deskops.models.task_lifecycle import lifecycle_errors
from deskops.models.task_lifecycle import lifecycle_table
from deskops.models.task_lifecycle import migration_note
from deskops.models.task_lifecycle import summary_with_migration_note
from deskops.operations import DeskopsOperations
from sldb.cli import main as sldb_main
from sldb.runtime.validation import extract_model_data

GOLDEN_DIR = Path(__file__).resolve().parent / "fixtures" / "golden" / "output"

#: (title, status, current_node, history): the b6 fixtures. The task id is the title's slug.
LEGACY = [
    ("Ci propio del gateway", "superseded", "ritual-execution", []),
    ("Workflow check obligatorio del gateway", "superseded", "ritual-execution", []),
    ("Tope por tipo y pedidos bloqueados", "deferred", "ritual-execution", []),
    ("Linea base de lint del gateway", "draft", "ritual-closeout", ["task_activates", "task_hands_to_closeout"]),
    ("Logs de llm gateway servir sin pii", "draft", "ritual-closeout", ["task_activates", "task_hands_to_closeout"]),
    ("Cancelada heredada", "cancelled", "ritual-execution", []),
    ("Cerrada heredada", "closed", "ritual-execution", []),
]
MIGRATION_LINES = [
    "desk/tasks/task-cancelada-heredada.md: current_node ritual-execution -> ''",
    "desk/tasks/task-cerrada-heredada.md: current_node ritual-execution -> ''",
    "desk/tasks/task-ci-propio-del-gateway.md: history [] -> [superseded]",
    "desk/tasks/task-tope-por-tipo-y-pedidos-bloqueados.md: current_node ritual-execution -> ''",
    "desk/tasks/task-workflow-check-obligatorio-del-gateway.md: history [] -> [superseded]",
]
UNMIGRATABLE = ["desk/tasks/task-linea-base-de-lint-del-gateway.md", "desk/tasks/task-logs-de-llm-gateway-servir-sin-pii.md"]
DRAFT_ERROR = "status: 'draft' does not follow history 'task_hands_to_closeout'; expected 'ready_for_testing'"


def _legacy_text(text: str, status: str, node: str, history: list[str]) -> str:
    """The task as a pre-CC31 desk left it: the three fields written by hand, nothing else."""
    history_text = "history: []" if not history else "history:\n" + "\n".join(f"- {h}" for h in history)
    assert text.count("status: draft\n") == 1 and text.count("current_node: ritual-execution\n") == 1
    assert text.count("history: []\n") == 1
    return (
        text.replace("status: draft\n", f"status: {status}\n")
        .replace("current_node: ritual-execution\n", f"current_node: {node}\n")
        .replace("history: []\n", history_text + "\n")
    )


def _make_tasks(root: Path, rows: list[tuple[str, str, str, list[str]]]) -> dict[str, Path]:
    """Create each task tracked (as ``deskops add task`` does), then give it its legacy state."""
    paths: dict[str, Path] = {}
    operations = DeskopsOperations(root)
    for title, status, node, history in rows:
        payload = {
            "title": title,
            "goal": "g",
            "scope": "s",
            "implementation_path": "i",
            "done_when": "d",
            "validation": ["pytest"],
            "task_type": "task.code",
        }
        task_id = operations.create_task_bundle(payload).task_id
        path = root / "desk" / "tasks" / f"{task_id}.md"
        path.write_text(_legacy_text(path.read_text(encoding="utf-8"), status, node, history), encoding="utf-8")
        paths[path.relative_to(root).as_posix()] = path
    return paths


@pytest.fixture
def legacy_desk(lifecycle_desk: Path) -> tuple[Path, dict[str, Path]]:
    return lifecycle_desk, _make_tasks(lifecycle_desk, LEGACY)


@pytest.fixture
def migratable_desk(lifecycle_desk: Path) -> tuple[Path, dict[str, Path]]:
    rows = [row for row in LEGACY if row[1] != "draft"]
    return lifecycle_desk, _make_tasks(lifecycle_desk, rows)


def _sldb_check(root: Path) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            return int(sldb_main(["stores", "check", "--store", str(root / ".sldb"), "--pythonpath", str(ROOT)]) or 0)
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else 1


def _store_doc_invalid_paths(root: Path) -> set[str]:
    """The desk documents `sldb stores check` names with the store/doc-invalid finding."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sldb",
            "stores",
            "check",
            "--store",
            str(root / ".sldb"),
            "--format",
            "json",
            "--pythonpath",
            str(ROOT),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    payload = json.loads(result.stdout or "{}")
    return {
        str(doc["path"])
        for model in payload.get("models") or []
        for doc in model.get("documents") or []
        if doc.get("note") == "doc_invalid"
    }


def _texts(paths: dict[str, Path]) -> dict[str, str]:
    return {rel: path.read_text(encoding="utf-8") for rel, path in paths.items()}


def _golden(name: str) -> str:
    return (GOLDEN_DIR / name).read_text(encoding="utf-8")


# ------------------------------------------------------------------ the table (d1, b7)
@pytest.mark.parametrize(
    ("status", "node", "expected"),
    [
        ("superseded", "ritual-execution", {"history": ([], ["superseded"])}),
        ("superseded", "", {"history": ([], ["superseded"])}),  # b7: an empty node gets it too
        ("superseded", "ritual-testing", {"history": ([], ["superseded"])}),
        *[(s, "ritual-execution", {"current_node": ("ritual-execution", "")}) for s in ("closed", "resolved", "done", "complete", "cancelled")],
        *[(s, "ritual-execution", {"current_node": ("ritual-execution", "")}) for s in ("deferred", "candidate")],
    ],
)
def test_the_table_migrates_each_legacy_status(status: str, node: str, expected: dict) -> None:
    assert lifecycle_errors(status, node, [])
    changes = legacy_state_migration(status, node, [])
    assert changes == expected
    after_node = changes.get("current_node", (node, node))[1]
    after_history = changes.get("history", ([], []))[1]
    assert lifecycle_errors(status, after_node, after_history) == []


@pytest.mark.parametrize("status", ["cancelled", "closed", "deferred", "candidate", "draft"])
def test_a_coherent_task_outside_the_lifecycle_is_not_touched(status: str) -> None:
    """b7: an empty node with a status of OUTSIDE_LIFECYCLE_STATUSES (cancelled added) is coherent."""
    assert legacy_state_migration(status, "", []) == {}
    payload = {"title": "T", "id": "task-t", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d"}
    assert TaskDoc(**payload, status=status, current_node="", history=[]).status == status


@pytest.mark.parametrize(
    ("status", "node", "history"),
    [
        ("ready_for_testing", "ritual-execution", ["task_activates"]),  # n4: a non-empty history stays with its owner
        ("draft", "ritual-closeout", ["task_activates", "task_hands_to_closeout"]),
        ("draft", "ritual-testing", []),
        ("closed", "ritual-testing", ["task_activates"]),
    ],
)
def test_any_other_incoherent_state_is_left_to_its_owner(status: str, node: str, history: list[str]) -> None:
    assert lifecycle_errors(status, node, history)
    assert legacy_state_migration(status, node, history) is None


# ------------------------------------------------------------------ non-terminal statuses (n1, n2)
@pytest.mark.parametrize(
    ("status", "node", "expected"),
    [
        ("active", "ritual-execution", {"status": ("active", "draft")}),
        ("ready_for_testing", "ritual-execution", {"status": ("ready_for_testing", "draft")}),
        ("active", "ritual-testing", {"status": ("active", "draft"), "current_node": ("ritual-testing", "ritual-execution")}),
        ("blocked", "ritual-closeout", {"status": ("blocked", "draft"), "current_node": ("ritual-closeout", "ritual-execution")}),
        ("in_progress", "", {"status": ("in_progress", "draft")}),  # an empty node stays empty
    ],
)
def test_the_table_migrates_a_non_terminal_status_with_an_empty_history_to_draft(status: str, node: str, expected: dict) -> None:
    assert lifecycle_table().entry_node == "ritual-execution"
    assert lifecycle_errors(status, node, [])
    changes = legacy_state_migration(status, node, [])
    assert changes == expected
    after_node = changes.get("current_node", (node, node))[1]
    assert lifecycle_errors("draft", after_node, []) == []


def test_the_migration_note_is_one_line_before_the_previous_summary() -> None:
    day = datetime(2026, 11, 11, tzinfo=timezone.utc).date()
    note = "Migrada a draft por deskops desk update: estado heredado 'active' sin history (2026-11-11)."
    assert migration_note("active", day) == note
    assert summary_with_migration_note("", "active", day) == note
    assert summary_with_migration_note("Antes.\nOtra línea.", "active", day) == f"{note} Antes. Otra línea."


#: (title, status, current_node, history): the reproduction's two tasks plus one at another node.
NON_TERMINAL = [
    ("Activa heredada", "active", "ritual-execution", []),
    ("Lista para testing heredada", "ready_for_testing", "ritual-execution", []),
    ("Activa en testing heredada", "active", "ritual-testing", []),
]


def test_desk_update_apply_migrates_non_terminal_tasks_to_draft_with_a_note(lifecycle_desk: Path, capsys) -> None:
    root = lifecycle_desk
    paths = _make_tasks(root, NON_TERMINAL)
    # One task carries a summary, which the note keeps after it.
    testing = root / "desk" / "tasks" / "task-activa-en-testing-heredada.md"
    text = testing.read_text(encoding="utf-8")
    assert text.count("summary: ''\n") == 1
    testing.write_text(text.replace("summary: ''\n", "summary: 'Resumen previo: con dos puntos.'\n"), encoding="utf-8")
    before = _texts(paths)
    assert _sldb_check(root) != 0
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root)]) == 1  # dry-run lists, writes nothing
    dry = capsys.readouterr().out
    assert "- Legacy task states to migrate: 3 task(s)" in dry
    assert "Invalid task documents" not in dry
    assert _texts(paths) == before

    today = datetime.now(timezone.utc).date()
    assert main(["desk", "update", "--root", str(root), "--apply"]) == 0
    out = capsys.readouterr().out
    lines = out.splitlines(keepends=True)
    block = lines[0] + "".join(itertools.takewhile(lambda line: line.startswith("- desk/tasks/"), lines[1:]))
    assert block == _golden("desk_update_nonterminal_migration.text")
    assert "Invalid task documents" not in out
    assert "Skipped the other repairs" not in out

    after = _texts(paths)
    for (title, status, _node, _history), (rel, path) in zip(NON_TERMINAL, paths.items()):
        data = extract_model_data(TaskDoc, after[rel])  # the model reads it now
        assert data["status"] == "draft"
        assert data["current_node"] == "ritual-execution"
        assert data["history"] == []
        note = migration_note(status, today)
        expected = f"{note} Resumen previo: con dos puntos." if path == testing else note
        assert data["summary"] == expected
        # Only status, summary and (when it moved) current_node changed.
        diff = [d[2:].split(":", 1)[0] for d in difflib.ndiff(before[rel].splitlines(), after[rel].splitlines()) if d[:1] in "+-"]
        assert set(diff) == ({"status", "summary", "current_node"} if path == testing else {"status", "summary"}), diff
    assert _sldb_check(root) == 0

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 0
    second = capsys.readouterr().out
    assert "Migrating legacy task states" not in second
    assert _texts(paths) == after


def test_doctor_points_a_non_terminal_task_to_desk_update(lifecycle_desk: Path, capsys) -> None:
    root = lifecycle_desk
    _make_tasks(root, NON_TERMINAL[:1])
    capsys.readouterr()
    assert main(["doctor", "--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert (
        "- Invalid task document: desk/tasks/task-activa-heredada.md: status: 'active' is not an entry status; "
        "a task with an empty history at 'ritual-execution' has status 'draft' (status changes only through "
        "deskops advance and deskops closeout). Migrate it with deskops desk update --apply.\n"
    ) in out
    assert UNMIGRATABLE_SUGGESTION not in out


# ------------------------------------------------------------------ desk update (d1, d2)
def test_desk_update_dry_run_lists_the_migration_and_the_undecided_tasks_and_writes_nothing(legacy_desk, capsys) -> None:
    root, paths = legacy_desk
    before = _texts(paths)
    assert _sldb_check(root) != 0  # sldb stops at the first invalid task: the reproduction
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert "- Legacy task states to migrate: 5 task(s)" in out
    for line in MIGRATION_LINES:
        assert f"  - {line}\n" in out
    assert "- Invalid task documents (not written): 2 task(s)" in out
    for rel in UNMIGRATABLE:
        assert f"  - {rel}: {DRAFT_ERROR}. To fix it, {UNMIGRATABLE_SUGGESTION}.\n" in out
    assert "- Invalid documents (not written)" not in out  # the frontmatter listing already names them
    assert "Migrating legacy task states" not in out
    assert _texts(paths) == before


def test_desk_update_apply_migrates_by_the_table_reports_the_rest_and_a_second_run_changes_nothing(legacy_desk, capsys) -> None:
    root, paths = legacy_desk
    before = _texts(paths)
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 1
    out = capsys.readouterr().out
    assert out.startswith("Migrating legacy task states...\n" + "".join(f"- {line}\n" for line in MIGRATION_LINES))
    assert "- Invalid task documents (not written): 2 task(s)" in out
    assert "Skipped the other repairs" not in out
    after = _texts(paths)
    for rel in UNMIGRATABLE:
        assert after[rel] == before[rel]
    for line in MIGRATION_LINES:
        rel = line.split(":", 1)[0]
        assert after[rel] != before[rel]
        extract_model_data(TaskDoc, after[rel])  # the model reads it now
        # Only the table's field moved.
        diff = [d for d in difflib.ndiff(before[rel].splitlines(), after[rel].splitlines()) if d[:1] in "+-"]
        assert diff in (
            ["- current_node: ritual-execution", "+ current_node: ''"],
            ["- history: []", "+ history:", "+ - superseded"],
        ), diff

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 1
    second = capsys.readouterr().out
    assert "Migrating legacy task states" not in second
    assert "Legacy task states to migrate" not in second
    assert not any(line in second for line in MIGRATION_LINES)
    for rel in UNMIGRATABLE:
        assert f"  - {rel}: {DRAFT_ERROR}. To fix it, {UNMIGRATABLE_SUGGESTION}.\n" in second
    assert _texts(paths) == after


def test_desk_update_apply_on_a_fully_migratable_desk_leaves_a_store_that_checks(migratable_desk, capsys) -> None:
    root, paths = migratable_desk
    assert _sldb_check(root) != 0
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 0
    out = capsys.readouterr().out
    lines = out.splitlines(keepends=True)
    block = lines[0] + "".join(itertools.takewhile(lambda line: line.startswith("- desk/tasks/"), lines[1:]))
    assert block == _golden("desk_update_legacy_migration.text")
    assert "Invalid task documents" not in out
    assert _sldb_check(root) == 0

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 0
    assert "Migrating legacy task states" not in capsys.readouterr().out


def test_desk_update_apply_repairs_everything_with_an_invalid_document(lifecycle_desk: Path, capsys, sldb_cache) -> None:
    """g2/g4b: with sldb naming the invalid task and going on, --apply keeps repairing the desk:
    the missing structure is scaffolded and the derived indexes are updated (no skipped repairs)."""
    root = lifecycle_desk
    paths = _make_tasks(root, [LEGACY[3]])
    rel = next(iter(paths))
    shutil.rmtree(root / "desk" / "drawer")
    sldb_cache(root)
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 1  # the task waits for its owner
    out = capsys.readouterr().out
    assert "- Invalid task documents (not written): 1 task(s)" in out
    assert "- Missing desk structure: desk/drawer/" in out
    assert "Scaffolded missing desk structure." in out
    assert (root / "desk" / "drawer").is_dir()
    assert "Updated store derived indexes." in out
    assert "Skipped the other repairs" not in out
    assert _store_doc_invalid_paths(root) == {rel}


def test_desk_update_and_doctor_name_a_store_invalid_document_once(lifecycle_desk: Path, capsys, sldb_cache) -> None:
    """g3: the sldb store/doc-invalid finding lists a non-task invalid document, while the task
    listing stays the frontmatter one and is not repeated from the finding."""
    root = lifecycle_desk
    paths = _make_tasks(root, [LEGACY[3]])
    task_rel = next(iter(paths))
    ritual = root / "desk" / "rituals" / "phase.md"
    text = ritual.read_text(encoding="utf-8")
    assert text.count("id: ritual-phase\n") == 1
    ritual.write_text(text.replace("id: ritual-phase\n", ""), encoding="utf-8")
    sldb_cache(root)
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert "- Invalid task documents (not written): 1 task(s)" in out
    assert "- Invalid documents (not written): 1 document(s)" in out
    assert "  - desk/rituals/phase.md: invalid: RitualDoc rejects desk/rituals/phase.md" in out
    assert f"  - {task_rel}: invalid: TaskCodeDoc rejects {task_rel}" not in out

    capsys.readouterr()
    assert main(["doctor", "--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert f"- Invalid task document: {task_rel}:" in out
    assert "- Invalid desk document: desk/rituals/phase.md: invalid: RitualDoc rejects desk/rituals/phase.md" in out
    assert f"- Invalid desk document: {task_rel}:" not in out
    assert "TaskCodeDoc:" not in out


# ------------------------------------------------------------------ doctor (d2, b9)
def test_doctor_reports_each_invalid_task_and_runs_every_other_check(legacy_desk, capsys, monkeypatch) -> None:
    root, _paths = legacy_desk
    ran: list[str] = []
    original = DoctorCLI._check_models

    def _check_models(self, *args, **kwargs):
        ran.append("models")
        return original(self, *args, **kwargs)

    monkeypatch.setattr(DoctorCLI, "_check_models", _check_models)
    capsys.readouterr()

    assert main(["doctor", "--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert out.startswith("Errors (the desk is broken):\n")
    findings = [line for line in out.splitlines() if line.startswith("- Invalid task document: ")]
    assert len(findings) == 7
    for line in MIGRATION_LINES:
        assert any(f.startswith(f"- Invalid task document: {line.split(':', 1)[0]}: ") and f.endswith("Migrate it with deskops desk update --apply.") for f in findings)
    unmigratable = [f for f in findings if UNMIGRATABLE_SUGGESTION in f]
    assert "\n".join(unmigratable) + "\n" == _golden("doctor_invalid_task.text")
    # sldb now reports the invalid tasks and goes on, and the frontmatter listing is not repeated
    # from its store/doc-invalid finding (g3).
    assert "SLDB store check crashed" not in out
    assert "- Invalid desk document: desk/tasks/" not in out
    assert "TaskCodeDoc:" not in out  # sldb's finding does not repeat the frontmatter listing
    assert ran == ["models"]


# ------------------------------------------------------------------ closeout retire with a store (d3)
def _git(root: Path, *argv: str) -> str:
    return subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def test_retire_closes_two_invalid_tasks_one_after_the_other(lifecycle_desk: Path, capsys, sldb_cache) -> None:
    """sldb names each invalid task with store/doc-invalid and no longer stops the store on it:
    retire closes one while the other is still invalid, then the other, and the store checks."""
    root = lifecycle_desk
    rows = [
        ("Cerrada con historia heredada", "closed", "ritual-closeout", ["task_activates"]),
        ("Cancelada con historia heredada", "cancelled", "ritual-closeout", ["task_activates"]),
    ]
    paths = _make_tasks(root, rows)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "two invalid retirable tasks")
    head = _git(root, "rev-parse", "HEAD")
    first, second = sorted(Path(rel).stem for rel in paths)
    sldb_cache(root)

    def retire(task_id: str) -> int:
        return main(["closeout", "retire", "--root", str(root), "--task", task_id, "--reason", "pre-CC31", "--ref", head])

    capsys.readouterr()
    assert _store_doc_invalid_paths(root) == {f"desk/tasks/{first}.md", f"desk/tasks/{second}.md"}
    assert retire(first) == 0, capsys.readouterr().out
    assert "Closeout-Mode: legacy-resolved" in _git(root, "log", "-1", "--format=%B")
    assert not (root / "desk" / "tasks" / f"{first}.md").exists()
    assert _store_doc_invalid_paths(root) == {f"desk/tasks/{second}.md"}

    assert retire(second) == 0, capsys.readouterr().out
    assert not (root / "desk" / "tasks" / f"{second}.md").exists()
    assert _store_doc_invalid_paths(root) == set()
    assert _sldb_check(root) == 0


def test_retire_closes_a_task_migrated_to_superseded_with_only_superseded_in_its_history(migratable_desk, capsys, sldb_cache) -> None:
    """After desk update --apply the legacy superseded task retires: its history is exactly
    [superseded], the closing commit is legacy-resolved and the store checks."""
    root, _paths = migratable_desk
    sldb_cache(root)
    capsys.readouterr()
    assert main(["desk", "update", "--root", str(root), "--apply"]) == 0, capsys.readouterr().out
    task = root / "desk" / "tasks" / "task-ci-propio-del-gateway.md"
    assert extract_model_data(TaskDoc, task.read_text(encoding="utf-8"))["history"] == ["superseded"]
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "migrated")
    head = _git(root, "rev-parse", "HEAD")
    capsys.readouterr()

    retire = ["closeout", "retire", "--root", str(root), "--task", task.stem, "--reason", "pre-CC31", "--ref", head]
    assert main(retire) == 0, capsys.readouterr().out
    assert "Closeout-Mode: legacy-resolved" in _git(root, "log", "-1", "--format=%B")
    assert not task.exists()
    assert _sldb_check(root) == 0


def test_desk_update_apply_exits_1_while_a_non_task_document_is_invalid(lifecycle_desk: Path, capsys, monkeypatch) -> None:
    """The dry-run and --apply agree: a store/doc-invalid document that is not a task keeps both at 1."""
    root = lifecycle_desk
    monkeypatch.setattr("deskops.cli.commands.desk.invalid_document_findings", lambda _payload: [("desk/notes/x.md", "rejected by model")])
    for argv in (["desk", "update", "--root", str(root)], ["desk", "update", "--root", str(root), "--apply"]):
        capsys.readouterr()
        assert main(argv) == 1
        assert "Invalid documents (not written): 1 document(s)" in capsys.readouterr().out


def test_desk_update_still_fails_when_stores_check_gives_no_json_and_exits_nonzero(lifecycle_desk: Path, capsys, monkeypatch) -> None:
    """The kept branch: a store check with no JSON and a failing exit code is an environment error."""
    import deskops.cli.commands.desk as desk_module
    real_run = subprocess.run

    def fake_run(argv, *args, **kwargs):
        if isinstance(argv, list) and "stores" in argv and "check" in argv:
            return subprocess.CompletedProcess(argv, 2, stdout="", stderr="boom")
        return real_run(argv, *args, **kwargs)

    monkeypatch.setattr(desk_module.subprocess, "run", fake_run)
    # main turns the DeskopsEnvironmentError into its message and a failing exit code.
    capsys.readouterr()
    assert main(["desk", "update", "--root", str(lifecycle_desk)]) != 0
    assert "'sldb stores check' failed for" in capsys.readouterr().err


# ------------------------------------------------------------------ closeout supersede of an undecided task
def test_supersede_closes_two_incoherent_tasks_one_after_the_other(lifecycle_desk: Path, capsys, sldb_cache) -> None:
    """The two gateway drafts after task_hands_to_closeout are both invalid under the same model:
    supersede reads each frontmatter, closes one while the other is still invalid, then the other."""
    root = lifecycle_desk
    rows = [row for row in LEGACY if row[1] == "draft"]
    paths = _make_tasks(root, rows)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "two incoherent drafts")
    head = _git(root, "rev-parse", "HEAD")
    first, second = sorted(Path(rel).stem for rel in paths)
    sldb_cache(root)

    def supersede(task_id: str) -> int:
        return main(["closeout", "supersede", "--root", str(root), "--task", task_id, "--reason", "replaced", "--ref", head])

    capsys.readouterr()
    assert _store_doc_invalid_paths(root) == {f"desk/tasks/{first}.md", f"desk/tasks/{second}.md"}
    assert supersede(first) == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert "Closeout-Mode: superseded" in message
    assert f"Task-Id: {first}" in message
    assert not (root / "desk" / "tasks" / f"{first}.md").exists()
    assert _store_doc_invalid_paths(root) == {f"desk/tasks/{second}.md"}

    assert supersede(second) == 0, capsys.readouterr().out
    assert not (root / "desk" / "tasks" / f"{second}.md").exists()
    assert _sldb_check(root) == 0


# ------------------------------------------------------------------ closeout resolved-by of an undecided task
def _resolved_by_desk(lifecycle_desk: Path, drafts: int) -> tuple[Path, list[str], str]:
    """``drafts`` gateway drafts after task_hands_to_closeout, plus a committed test: the work entered."""
    root = lifecycle_desk
    rows = [row for row in LEGACY if row[1] == "draft"][:drafts]
    paths = _make_tasks(root, rows)
    (root / "tests").mkdir(exist_ok=True)
    (root / "tests" / "test_gateway.py").write_text("def test_gateway():\n    assert True\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "incoherent drafts and their test")
    return root, sorted(Path(rel).stem for rel in paths), _git(root, "rev-parse", "HEAD")


def _resolved_by(root: Path, task_id: str, ref: str) -> int:
    return main(["closeout", "resolved-by", "--root", str(root), "--task", task_id, "--reason", "work entered", "--ref", ref, "--test", "tests/test_gateway.py"])


def test_resolved_by_closes_the_only_invalid_task_and_the_store_checks(lifecycle_desk: Path, capsys) -> None:
    root, (task_id,), head = _resolved_by_desk(lifecycle_desk, 1)
    capsys.readouterr()

    rc = _resolved_by(root, task_id, head)
    out = capsys.readouterr()
    assert rc == 0, out.out + out.err
    message = _git(root, "log", "-1", "--format=%B")
    assert "Closeout-Mode: resolved-by" in message
    assert f"Task-Id: {task_id}" in message
    assert f"Closeout-Ref: {head}" in message
    assert "Closeout-Test: tests/test_gateway.py" in message
    assert not (root / "desk" / "tasks" / f"{task_id}.md").exists()
    assert _git(root, "status", "--porcelain") == ""
    assert _sldb_check(root) == 0


def test_resolved_by_closes_two_invalid_tasks_one_after_the_other(lifecycle_desk: Path, capsys, sldb_cache) -> None:
    """The two invalid drafts of the same model: resolved-by closes one while the other is still
    invalid (sldb names it store/doc-invalid and goes on), then the other, and the store checks."""
    root, (first, second), head = _resolved_by_desk(lifecycle_desk, 2)
    sldb_cache(root)
    capsys.readouterr()

    assert _store_doc_invalid_paths(root) == {f"desk/tasks/{first}.md", f"desk/tasks/{second}.md"}
    assert _resolved_by(root, first, head) == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert "Closeout-Mode: resolved-by" in message
    assert f"Task-Id: {first}" in message
    assert not (root / "desk" / "tasks" / f"{first}.md").exists()
    assert _store_doc_invalid_paths(root) == {f"desk/tasks/{second}.md"}

    assert _resolved_by(root, second, head) == 0, capsys.readouterr().out
    assert not (root / "desk" / "tasks" / f"{second}.md").exists()
    assert _sldb_check(root) == 0

FILE:instruccion
Cold-bundle de la tarea task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_legacy_task_states.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas, cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea


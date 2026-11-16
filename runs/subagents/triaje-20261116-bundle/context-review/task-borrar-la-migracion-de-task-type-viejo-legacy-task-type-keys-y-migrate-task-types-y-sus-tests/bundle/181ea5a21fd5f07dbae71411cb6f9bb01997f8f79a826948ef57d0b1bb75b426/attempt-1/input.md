FILE:desk/tasks/task-borrar-la-migracion-de-task-type-viejo-legacy-task-type-keys-y-migrate-task-types-y-sus-tests.md
---
sldb:
  by: agent
  at: '2026-11-16T05:04:28Z'
  authority: generated
  via: save_document_payload
id: task-borrar-la-migracion-de-task-type-viejo-legacy-task-type-keys-y-migrate-task-types-y-sus-tests
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply
pills: []
files:
- deskops/workspace.py
- deskops/cli/commands/desk.py
- tests/test_task_types.py
- tests/test_task_lifecycle_validator.py
- docs/workflow-policy-reference.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-retirar-caminos-legacy-migrar-los-datos-y-borrar-el-c-digo-de-compatibilidad.md
---

# Borrar la migracion de task_type viejo (LEGACY_TASK_TYPE_KEYS y migrate_task_types) y sus tests

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (punto 1). Por DK3 de deskops-como-config, un camino de compatibilidad se borra cuando sus consumidores migraron. Sigue vivo: LEGACY_TASK_TYPE_KEYS en deskops/workspace.py:520, migrate_task_types en :712 y su llamada en deskops/cli/commands/desk.py:452; tests en tests/test_task_types.py:107 y 149.

## Goal

_Describe the concrete result this task must produce._

El mapa, la funcion, la llamada y los tests legacy desaparecen; desk update ya no migra task_type viejos.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/workspace.py, deskops/cli/commands/desk.py, tests/test_task_types.py, tests/test_task_lifecycle_validator.py (casos legacy) y docs/workflow-policy-reference.md (la frase de migracion). No entra: otros caminos legacy. Precisiones del preflight 1: la dependencia externa esta cerrada cuando deskops show task task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply --root . da status closed. Casos legacy = los tests que nombran LEGACY_TASK_TYPE_KEYS, migrate_task_types o un task_type viejo sin prefijo (code, implementation, test, docs, spec, design, external, vacio) como valor a migrar, p. ej. test_task_lifecycle_validator.py alrededor de 177 y 290-303. La frase de la doc es la oracion de docs/workflow-policy-reference.md linea 75 que empieza con 'A desk adds its own subtypes' en su parte 'and migrates legacy task_type strings (...)'. Despues del borrado, una tarea con task_type viejo se trata como cualquier task_type desconocido hoy (el validador la reporta); no se agrega comportamiento nuevo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Confirmar que la dependencia externa cerro. 2) Borrar. 3) `grep -rn 'LEGACY_TASK_TYPE\|migrate_task_types' deskops tests docs` vacio. 4) Tests.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rn 'LEGACY_TASK_TYPE\|migrate_task_types' deskops tests docs
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_task_types.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_task_lifecycle_validator.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El grep queda vacio y la suite no tiene fallas nuevas.

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
            if not (desk_dir / "reviews").exists():
                missing_desk_files.append("desk/reviews/")
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

FILE:tests/test_task_types.py
"""GC01: task types as models with a hierarchy and type-declared closeout evidence.

Covers each Done When line of task-gc01: the seven factory subclasses and their declared
evidence (the activation receipts are the RuleDoc seeds of CC32), `add task --task-type` (registered-only + default + envelope note), the
store family ``model <= TaskCodeDoc``, closeout reading evidence from the type, `--evidence`
as a floor, the desk-local type registration (DC7), the legacy ``task_type`` migration, and
the removal of ``TASK_TYPE_EVIDENCE``.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import yaml

from deskops import doc_access
from deskops.models import TaskAggregateDoc
from deskops.models import TaskCodeDoc
from deskops.models import TaskDebugDoc
from deskops.models import TaskDecisionDoc
from deskops.models import TaskDoc
from deskops.models import TaskDocsDoc
from deskops.models import TaskExternalDoc
from deskops.models import TaskRefactorDoc
from deskops.models.task_types import canonical_task_type_name
from deskops.models.task_types import closeout_evidence_kinds
from deskops.models.task_types import TASK_TYPE_MODELS

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
SLDB = [sys.executable, "-m", "sldb"]


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _cli(root: Path, *argv: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([*CLI, *argv, "--root", str(root)], cwd=root, capture_output=True, text=True)
    if check:
        assert result.returncode == 0, f"deskops {' '.join(argv)} failed:\n{result.stdout}\n{result.stderr}"
    return result


def _init(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([*CLI, "init", str(root)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def _sldb(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*SLDB, *argv], cwd=root, capture_output=True, text=True)


def _frontmatter(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]) or {}


def _write_task(root: Path, task_id: str, *, task_type: str, references: list[str] | None = None, files: list[str] | None = None) -> Path:
    path = root / "desk" / "tasks" / f"{task_id}.md"
    path.write_text(
        f"""---
id: {task_id}
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: {references or []}
depends_on: []
pills: []
files: {files or []}
task_type: {task_type}
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# {task_id}

## Rationale

## Goal

Migrate.

## Scope

## Implementation Path

## Validation

## Done When

""",
        encoding="utf-8",
    )
    return path


def _write_legacy_task(root: Path, task_id: str, task_type: str) -> Path:
    return _write_task(root, task_id, task_type=task_type)


# ------------------------------------------------------------------ models
def test_factory_type_declarations_match_the_normative_table() -> None:
    """The closeout evidence of each type is data (``closeout-evidence.yaml``, CC33b c3), not a
    class attribute; ``task.aggregate`` has no children kind until a children field exists."""
    expected = {
        TaskCodeDoc: ("task.code", ("tests", "commit", "atom", "materialization")),
        TaskDocsDoc: ("task.docs", ("commit", "document")),
        TaskDebugDoc: ("task.debug", ("tests", "commit", "atom", "materialization")),
        TaskRefactorDoc: ("task.refactor", ("tests", "commit", "atom", "materialization", "goldens")),
        TaskDecisionDoc: ("task.decision", ("commit", "document")),
        TaskAggregateDoc: ("task.aggregate", ("commit",)),
        TaskExternalDoc: ("task.external", ("external",)),
    }
    for model, (name, kinds) in expected.items():
        assert model.model_fields["task_type"].default == name
        assert closeout_evidence_kinds(model) == kinds
        assert "__closeout_evidence__" not in vars(model)


def test_type_hierarchy_keeps_refactor_in_code_and_debug_out_of_it() -> None:
    assert issubclass(TaskRefactorDoc, TaskCodeDoc)
    assert not issubclass(TaskDebugDoc, TaskCodeDoc)
    assert issubclass(TaskDebugDoc, TaskDoc)
    assert issubclass(TaskDocsDoc, TaskDoc)


def test_taskdoc_declares_the_contract_fields() -> None:
    assert TaskDoc.__contract__ == [
        "title",
        "goal",
        "scope",
        "implementation_path",
        "files",
        "validation",
        "done_when",
    ]


def test_legacy_task_type_map_matches_the_migration() -> None:
    assert canonical_task_type_name("code") == "task.code"
    assert canonical_task_type_name("implementation") == "task.code"
    assert canonical_task_type_name("test") == "task.code"
    assert canonical_task_type_name("docs") == "task.docs"
    assert canonical_task_type_name("spec") == "task.docs"
    assert canonical_task_type_name("design") == "task.docs"
    assert canonical_task_type_name("external") == "task.external"
    assert canonical_task_type_name("") == "task.code"
    assert canonical_task_type_name("task.code") == "task.code"
    assert canonical_task_type_name("reflection") == "task.code"


# ------------------------------------------------------------------ add task
def test_add_task_with_task_type_tracks_under_the_type_model(lifecycle_desk: Path) -> None:
    result = _cli(lifecycle_desk, "add", "task", "--title", "Typed", "--goal", "g", "--scope", "s", "--task-type", "task.code")
    assert "Created task bundle task-typed" in result.stdout
    frontmatter = _frontmatter(lifecycle_desk / "desk" / "tasks" / "task-typed.md")
    assert frontmatter["task_type"] == "task.code"

    found = _sldb(lifecycle_desk, "find", "task-typed", "--in", "physical", "--type", "doc", "--where", "model <= TaskCodeDoc", "--store", ".sldb", "--format", "json")
    results = json.loads(found.stdout)["results"]
    assert [(r["name"], r["model"]) for r in results] == [("task-typed", "TaskCodeDoc")]


def test_add_task_without_task_type_defaults_to_code_with_a_note(lifecycle_desk: Path) -> None:
    result = _cli(lifecycle_desk, "add", "task", "--title", "Defaulted", "--goal", "g", "--scope", "s")
    assert "no --task-type given; defaulting to task.code" in result.stdout
    frontmatter = _frontmatter(lifecycle_desk / "desk" / "tasks" / "task-defaulted.md")
    assert frontmatter["task_type"] == "task.code"
    assert frontmatter.get("closeout_evidence") is None


def test_add_task_with_an_unregistered_type_lists_the_types(lifecycle_desk: Path) -> None:
    result = _cli(lifecycle_desk, "add", "task", "--title", "Bad", "--goal", "g", "--scope", "s", "--task-type", "foo", check=False)
    assert result.returncode == 1
    assert "'foo' is not a registered task type" in result.stdout
    for name in TASK_TYPE_MODELS:
        assert name in result.stdout
    assert not (lifecycle_desk / "desk" / "tasks" / "task-bad.md").exists()


# ------------------------------------------------------------------ evidence floor
def test_add_task_evidence_can_add_but_not_remove_a_type_kind(lifecycle_desk: Path) -> None:
    removed = _cli(
        lifecycle_desk,
        "add", "task", "--title", "Removed", "--goal", "g", "--scope", "s",
        "--task-type", "task.code", "--evidence", "commit", "document",
        check=False,
    )
    assert removed.returncode == 1
    assert "--evidence removes closeout evidence the task type requires" in removed.stdout

    added = _cli(
        lifecycle_desk,
        "add", "task", "--title", "Added", "--goal", "g", "--scope", "s",
        "--task-type", "task.code",
        "--evidence", "tests", "commit", "atom", "materialization", "document",
    )
    assert added.returncode == 0
    frontmatter = _frontmatter(lifecycle_desk / "desk" / "tasks" / "task-added.md")
    assert frontmatter["closeout_evidence"] == ["tests", "commit", "atom", "materialization", "document"]


# ------------------------------------------------------------------ family query
def test_model_family_query_includes_refactor_and_not_debug_or_docs(lifecycle_desk: Path) -> None:
    for title in ("Code", "Refactor", "Debug", "Docs"):
        _cli(lifecycle_desk, "add", "task", "--title", title, "--goal", "g", "--scope", "s", "--task-type", f"task.{title.lower()}")

    found = _sldb(lifecycle_desk, "find", "task-", "--in", "physical", "--type", "doc", "--where", "model <= TaskCodeDoc", "--store", ".sldb", "--format", "json")
    names = {r["name"] for r in json.loads(found.stdout)["results"]}
    assert "task-code" in names
    assert "task-refactor" in names
    assert "task-debug" not in names
    assert "task-docs" not in names


# ------------------------------------------------------------------ closeout reads the type
def test_closeout_verify_reads_evidence_from_the_type(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "api.md").write_text("# API\n", encoding="utf-8")
    _git(root, "add", "docs")
    _git(root, "commit", "-q", "-m", "docs")
    commit = _git(root, "rev-parse", "HEAD")

    path = _write_task(root, "task-doc-task", task_type="task.docs", references=[commit, "docs/api.md"])
    # Tasks resolve through the store (CC35b a7): track the hand-written task under its type.
    doc_access.track_created_document(root, TaskDocsDoc, path, "task-doc-task")

    result = _cli(root, "closeout", "verify", "--task", "task-doc-task")
    report = json.loads(result.stdout)
    assert report["ok"], report
    assert report["declared"] == ["commit", "document"]
    assert report["found"] == ["commit", "document"]
    assert report["implicit_code"] is False


def test_closeout_verify_of_an_aggregate_declares_only_commit(lifecycle_desk: Path) -> None:
    """No children kind (TaskAggregateDoc has no children field, b4): the aggregate closes with
    a commit receipt, and verify names nothing it cannot check."""
    _cli(lifecycle_desk, "add", "task", "--title", "Aggregate", "--goal", "g", "--scope", "s", "--task-type", "task.aggregate")
    result = _cli(lifecycle_desk, "closeout", "verify", "--task", "task-aggregate", check=False)
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["declared"] == ["commit"]
    assert {item["code"] for item in report["findings"]} == {"missing_commit_evidence"}
    assert "children" not in result.stdout


# ------------------------------------------------------------------ local types (DC7)
def test_desk_update_apply_registers_a_local_type_and_add_task_uses_it(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _init(root)
    models_dir = root / "desk" / "models"
    models_dir.mkdir()
    (models_dir / "local_types.py").write_text(
        """from typing import Literal
from pydantic import Field
from deskops.models import TaskCodeDoc


class TaskCliDoc(TaskCodeDoc):
    task_type: Literal["task.code.cli"] = Field(default="task.code.cli", description="CLI subtype.")
""",
        encoding="utf-8",
    )

    _cli(root, "desk", "update", "--apply")

    registered = _sldb(root, "models", "list", "--store", ".sldb", "--format", "json")
    assert "TaskCliDoc" in {m["name"] for m in json.loads(registered.stdout)["models"]}

    result = _cli(root, "add", "task", "--title", "CLI", "--goal", "g", "--scope", "s", "--task-type", "task.code.cli")
    assert "Created task bundle task-cli" in result.stdout
    frontmatter = _frontmatter(root / "desk" / "tasks" / "task-cli.md")
    assert frontmatter["task_type"] == "task.code.cli"

    found = _sldb(root, "find", "task-cli", "--in", "physical", "--type", "doc", "--where", "model <= TaskCodeDoc", "--store", ".sldb", "--pythonpath", str(root / "desk"), "--format", "json")
    results = json.loads(found.stdout)["results"]
    assert [(r["name"], r["model"]) for r in results] == [("task-cli", "TaskCliDoc")]

    # The local subtype reads its factory ancestor's evidence (task.code) from the table.
    verify = _cli(root, "closeout", "verify", "--task", "task-cli", check=False)
    assert json.loads(verify.stdout)["declared"] == ["tests", "commit", "atom", "materialization"]


def test_desk_update_apply_declares_the_types_it_registers_so_a_clean_clone_rebuilds(tmp_path: Path) -> None:
    """`desk update --apply` registered GC01's task types in sldb's index but not in its
    store.yaml, and the CI rebuild said `Model 'TaskCodeDoc' not registered.` (sldb 8b60e889).
    A declared desk that gains a type keeps rebuilding from its declaration."""
    root = tmp_path / "repo"
    _init(root)
    _git(root, "init", "-q")
    declared = _sldb(root, "stores", "declare", "--write", "--store", ".sldb")
    assert declared.returncode == 0, declared.stdout + declared.stderr
    models_dir = root / "desk" / "models"
    models_dir.mkdir()
    (models_dir / "local_types.py").write_text(
        """from typing import Literal
from pydantic import Field
from deskops.models import TaskCodeDoc


class TaskCliDoc(TaskCodeDoc):
    task_type: Literal["task.code.cli"] = Field(default="task.code.cli", description="CLI subtype.")
""",
        encoding="utf-8",
    )

    _cli(root, "desk", "update", "--apply")
    _cli(root, "add", "task", "--title", "CLI", "--goal", "g", "--scope", "s", "--task-type", "task.code.cli")

    declaration = yaml.safe_load((root / ".sldb" / "store.yaml").read_text(encoding="utf-8"))
    assert "TaskCliDoc" in {m["name"] for m in declaration["models"]}
    check = _sldb(root, "stores", "build", "--check", "--store", ".sldb")
    assert check.returncode == 0, check.stdout + check.stderr


# ------------------------------------------------------------------ migration
def test_legacy_task_type_migrates_idempotently(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _init(root)
    path = _write_legacy_task(root, "task-legacy", "implementation")

    _cli(root, "desk", "update", "--apply")
    assert _frontmatter(path)["task_type"] == "task.code"

    found = _sldb(root, "find", "task-legacy", "--in", "physical", "--type", "doc", "--where", "model <= TaskCodeDoc", "--store", ".sldb", "--format", "json")
    assert [r["model"] for r in json.loads(found.stdout)["results"]] == ["TaskCodeDoc"]

    before = path.read_bytes()
    second = _cli(root, "desk", "update", "--apply")
    assert "Desk is up to date." in second.stdout
    assert path.read_bytes() == before


def test_unknown_legacy_task_type_migrates_to_code_with_a_report(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _init(root)
    path = _write_legacy_task(root, "task-weird", "reflection")

    result = _cli(root, "desk", "update", "--apply")
    assert _frontmatter(path)["task_type"] == "task.code"
    assert "unknown legacy task_type 'reflection'" in result.stdout
    assert "migrated to task.code" in result.stdout


# ------------------------------------------------------------------ no flat mapping left
def test_task_type_evidence_mapping_is_gone() -> None:
    for path in (ROOT / "deskops").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "TASK_TYPE_EVIDENCE" not in text, path

FILE:tests/test_task_lifecycle_validator.py
"""CC37: a task's lifecycle is a validator of TaskDoc, so no write leaves it outside the rules.

``status``, ``current_node`` and ``history`` must form a state the lifecycle graph (the
``RelationDoc`` seeds of ``deskops/data/lifecycle/``) or closeout can produce, and
``task_type`` must match the document's model. sldb builds the model on every write, so
``sldb fields update``, ``sldb docs update`` and ``sldb serve``'s ``/save`` reject an
inconsistent task with the validator's message.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]

from deskops.cli.main import main
from deskops.models import TaskDoc
from deskops.models.task_lifecycle import CLOSEOUT_STATES, DRAWER_STATUSES, ENTRY_STATUSES, lifecycle_table
from deskops.models.task_types import TaskCodeDoc, TaskDocsDoc
from deskops.models.validation import validation_messages
from deskops.operations import DeskopsOperations
from sldb.cli import main as sldb_main

BASE = {"title": "T", "id": "task-t", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d"}
ENTRY = {**BASE, "status": "draft", "current_node": "ritual-execution", "history": []}
ENTRY_ERROR = (
    "status: 'closed' is not an entry status; a task with an empty history at 'ritual-execution' has "
    "status 'draft' (status changes only through deskops advance and deskops closeout)"
)


def _rejects(model, payload: dict, *texts: str) -> str:
    with pytest.raises(ValidationError) as excinfo:
        model(**payload)
    [message] = validation_messages(excinfo.value)
    for text in texts:
        assert text in message
    return message


# ------------------------------------------------------------------ the table
def test_the_table_is_read_from_the_package_relation_docs() -> None:
    table = lifecycle_table()
    assert table.entry_node == "ritual-execution"
    edges = {name: (edge.target, edge.status) for name, edge in table.edges.items()}
    assert edges == {
        "task_activates": ("ritual-testing", "active"),
        "task_hands_to_closeout": ("ritual-closeout", "ready_for_testing"),
        "task_completes": ("complete", "closed"),
    }
    assert ENTRY_STATUSES == {"draft"}
    assert DRAWER_STATUSES == {"deferred", "candidate"}
    assert {s: h for s, (h, _) in CLOSEOUT_STATES.items()} == {
        "closed": "task_completes",
        "superseded": "superseded",
        "resolved": "resolved-by",
    }


# ------------------------------------------------------------------ (i) entry state
def test_entry_state_is_valid() -> None:
    assert TaskCodeDoc(**ENTRY).status == "draft"
    # An empty current_node is the entry node (deskops advance reads it so).
    assert TaskCodeDoc(**{**ENTRY, "current_node": ""}).current_node == ""


def test_a_drawer_task_outside_the_lifecycle_may_be_deferred() -> None:
    """``promote inbox-to-drawer-task`` writes ``deferred`` with no current_node and no history."""
    assert TaskDoc(**{**ENTRY, "status": "deferred", "current_node": ""}).status == "deferred"
    # The drawer candidates of the workspace-documental plan (CC37 c4, revisable).
    assert TaskDoc(**{**ENTRY, "status": "candidate", "current_node": ""}).status == "candidate"
    _rejects(TaskDoc, {**ENTRY, "status": "deferred"}, "status: 'deferred' is not an entry status")
    _rejects(TaskDoc, {**ENTRY, "status": "active", "current_node": ""}, "status: 'active' is not an entry status; a task with an empty history and no current_node has status 'cancelled', 'candidate', 'closed', 'complete', 'deferred', 'done', 'draft', 'resolved'")


@pytest.mark.parametrize("status", ["resolved", "closed", "done", "complete", "cancelled"])
def test_a_task_resolved_before_the_lifecycle_is_valid_only_outside_it(status: str) -> None:
    """``closeout retire`` removes tasks resolved before the lifecycle: no current_node, no history."""
    assert TaskDoc(**{**ENTRY, "status": status, "current_node": ""}).status == status
    _rejects(TaskDoc, {**ENTRY, "status": status}, f"status: '{status}' is not an entry status")


def test_entry_state_rejects_a_status_outside_the_entry_set() -> None:
    _rejects(TaskCodeDoc, {**ENTRY, "status": "closed"}, "Task task-t lifecycle is inconsistent:", ENTRY_ERROR)
    _rejects(TaskCodeDoc, {**ENTRY, "status": "active"}, "status: 'active' is not an entry status")


def test_entry_state_rejects_a_later_node_without_history() -> None:
    _rejects(
        TaskCodeDoc,
        {**ENTRY, "current_node": "ritual-testing"},
        "current_node: 'ritual-testing' needs a history; with an empty history a task is at the entry node 'ritual-execution'",
    )


# ------------------------------------------------------------------ (ii) after transitions
@pytest.mark.parametrize(
    ("history", "node", "status"),
    [
        (["task_activates"], "ritual-testing", "active"),
        (["task_activates", "task_hands_to_closeout"], "ritual-closeout", "ready_for_testing"),
        (["task_activates", "task_hands_to_closeout", "task_completes"], "complete", "closed"),
    ],
)
def test_state_after_each_transition_is_valid(history: list[str], node: str, status: str) -> None:
    task = TaskCodeDoc(**{**BASE, "status": status, "current_node": node, "history": history})
    assert (task.status, task.current_node) == (status, node)


def test_status_must_be_the_sets_status_of_the_last_transition() -> None:
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "draft", "current_node": "ritual-testing", "history": ["task_activates"]},
        "status: 'draft' does not follow history 'task_activates'; expected 'active'",
    )


def test_current_node_must_be_the_target_of_the_last_transition() -> None:
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "active", "current_node": "ritual-closeout", "history": ["task_activates"]},
        "current_node: 'ritual-closeout' does not follow history 'task_activates'; expected 'ritual-testing'",
    )


def test_last_history_item_must_be_a_transition_or_a_closeout_record() -> None:
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "active", "current_node": "ritual-testing", "history": ["jumped"]},
        "history: last item 'jumped' is neither a lifecycle transition",
    )


# ------------------------------------------------------------------ (iii) closed by closeout
@pytest.mark.parametrize(("status", "record"), [("superseded", "superseded"), ("resolved", "resolved-by")])
@pytest.mark.parametrize("node", ["ritual-execution", "ritual-testing", "ritual-closeout"])
def test_closeout_records_are_valid_from_any_node(status: str, record: str, node: str) -> None:
    history = [] if node == "ritual-execution" else ["task_activates"]
    task = TaskCodeDoc(**{**BASE, "status": status, "current_node": node, "history": [*history, record]})
    assert task.history[-1] == record


def test_closeout_status_needs_its_own_record() -> None:
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "resolved", "current_node": "ritual-execution", "history": ["superseded"]},
        "history: last item 'superseded' is neither",
    )
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "superseded", "current_node": "ritual-execution", "history": []},
        "status: 'superseded' is not an entry status",
    )


def test_closed_needs_the_terminal_transition_and_the_complete_node() -> None:
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "closed", "current_node": "ritual-closeout", "history": ["task_activates", "task_completes"]},
        "current_node: 'ritual-closeout' does not follow history 'task_completes'; expected 'complete'",
    )


# ------------------------------------------------------------------ (iv) task_type matches the model
def test_task_type_matches_the_typed_model() -> None:
    assert TaskDocsDoc(**ENTRY).task_type == "task.docs"
    with pytest.raises(ValidationError) as excinfo:
        TaskCodeDoc(**{**ENTRY, "task_type": "task.docs"})
    assert excinfo.value.errors()[0]["loc"] == ("task_type",)


@pytest.mark.parametrize("task_type", ["", "code", "implementation", "task.code"])
def test_generic_task_doc_accepts_empty_legacy_or_any_task_type(task_type: str) -> None:
    assert TaskDoc(**{**ENTRY, "task_type": task_type}).task_type == task_type


# ------------------------------------------------------------------ sldb applies it on every write
def _sldb_run(argv: list[str]) -> tuple[int, str]:
    try:
        return int(sldb_main(argv) or 0), ""
    except SystemExit as exc:
        if isinstance(exc.code, int) or exc.code is None:
            return int(exc.code or 0), ""
        return 1, str(exc.code)


@pytest.fixture
def task_desk(lifecycle_desk: Path) -> tuple[Path, Path]:
    payload = {
        "title": "Probe",
        "goal": "g",
        "scope": "s",
        "implementation_path": "i",
        "done_when": "d",
        "validation": ["pytest"],
        "task_type": "task.code",
    }
    task_id = DeskopsOperations(lifecycle_desk).create_task_bundle(payload).task_id  # tracked as TaskCodeDoc
    return lifecycle_desk, lifecycle_desk / "desk" / "tasks" / f"{task_id}.md"


def _store_args(root: Path) -> list[str]:
    return ["--store", str(root / ".sldb"), "--pythonpath", str(ROOT)]


def _current_payload(root: Path) -> dict:
    """The task's payload as sldb holds it (what ``/save``'s ``expected`` guard compares)."""
    from sldb.cli.model_utils import resolve_model_ref
    from sldb.store.query import load_runtime_documents

    [doc] = [d for d in load_runtime_documents(root / ".sldb", resolve_model_ref, str(ROOT)) if d.name == "task-probe"]
    return dict(doc.payload)


def test_sldb_fields_update_of_status_to_closed_at_ritual_execution_is_rejected(task_desk, capsys) -> None:
    root, task = task_desk
    before = task.read_text(encoding="utf-8")
    code, message = _sldb_run(["fields", "update", "docs/TaskCodeDoc/task-probe/status", '"closed"', *_store_args(root)])
    out = capsys.readouterr()
    assert code != 0
    assert ENTRY_ERROR in message + out.out + out.err
    assert task.read_text(encoding="utf-8") == before


def test_sldb_fields_update_of_current_node_without_a_coherent_status_is_rejected(task_desk, capsys) -> None:
    root, task = task_desk
    before = task.read_text(encoding="utf-8")
    code, message = _sldb_run(
        ["fields", "update", "docs/TaskCodeDoc/task-probe/current_node", '"ritual-closeout"', *_store_args(root)]
    )
    out = capsys.readouterr()
    assert code != 0
    assert (
        "current_node: 'ritual-closeout' needs a history; with an empty history a task is at the entry node "
        "'ritual-execution'"
    ) in message + out.out + out.err
    assert task.read_text(encoding="utf-8") == before


def test_sldb_docs_update_with_the_inconsistent_payload_is_rejected(task_desk, capsys) -> None:
    root, task = task_desk
    before = task.read_text(encoding="utf-8")
    payload = json.dumps({**_current_payload(root), "status": "closed"})
    code, message = _sldb_run(["docs", "update", "task-probe", payload, *_store_args(root)])
    out = capsys.readouterr()
    assert code != 0
    assert ENTRY_ERROR in message + out.out + out.err
    assert task.read_text(encoding="utf-8") == before


@pytest.mark.parametrize("batched", [False, True])
def test_sldb_serve_save_with_the_inconsistent_payload_is_rejected(task_desk, batched: bool) -> None:
    """``save_request`` is what ``sldb serve`` runs for ``POST /save`` (single and batched)."""
    from sldb.cli.serve.save_routes import save_request

    root, task = task_desk
    before = task.read_text(encoding="utf-8")
    current = _current_payload(root)
    payload = {**current, "status": "closed"}
    if batched:
        change = {"id": "task-probe", "action": "update", "model": "TaskCodeDoc", "payload": payload, "expected": current}
        request = {"changes": [change]}
    else:
        request = {"doc": "task-probe", "payload": payload}
    try:
        response, code = save_request(request, root / ".sldb", root, str(ROOT))
        message = json.dumps(response, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001 - the single route raises what the HTTP layer turns into a 4xx
        code, message = 400, str(exc)
    assert code >= 400
    assert ENTRY_ERROR in message
    assert task.read_text(encoding="utf-8") == before


def test_a_consistent_direct_write_is_accepted(task_desk, capsys) -> None:
    """DA6: no "transition only" field; a coherent state written without a transition is fine."""
    root, task = task_desk
    code, _ = _sldb_run(["fields", "update", "docs/TaskCodeDoc/task-probe/summary", '"probe"', *_store_args(root)])
    capsys.readouterr()
    assert code == 0
    assert "summary: probe" in task.read_text(encoding="utf-8")


# ------------------------------------------------------------------ desk update reports, never writes
#: A non-empty history with an incoherent status: the migration table leaves it to its owner (an
#: empty history with a non-terminal status is migrated to draft instead, task.debug of
#: non-terminal tasks).
ACTIVE_ERROR = "status: 'ready_for_testing' does not follow history 'task_activates'; expected 'active'"


def test_desk_update_reports_an_inconsistent_task_and_does_not_write_it(lifecycle_desk: Path, capsys) -> None:
    """An untracked task with a legacy task_type (a pending migration) and a status no transition
    wrote nor the legacy table decides: desk update lists it and --apply neither migrates nor
    tracks it, and exits 1 while it waits for its owner."""
    from deskops.models.task_lifecycle import UNMIGRATABLE_SUGGESTION

    root = lifecycle_desk
    text = (
        "---\nid: task-legacy\nstatus: ready_for_testing\ncurrent_node: ritual-testing\nhistory:\n- task_activates\ntask_type: code\n---\n\n"
        "# Legacy\n\n## Goal\n\ng\n"
    )
    task = root / "desk" / "tasks" / "task-legacy.md"
    task.write_text(text, encoding="utf-8")
    line = f"  - desk/tasks/task-legacy.md: {ACTIVE_ERROR}. To fix it, {UNMIGRATABLE_SUGGESTION}."

    assert main(["desk", "update", "--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert "- Invalid task documents (not written): 1 task(s)" in out
    assert line in out
    assert "Pending task type migration" not in out

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 1
    assert line in capsys.readouterr().out
    assert task.read_text(encoding="utf-8") == text
    code, _ = _sldb_run(["docs", "list", "--store", str(root / ".sldb")])
    assert "task-legacy" not in capsys.readouterr().out


def test_desk_update_names_a_tracked_inconsistent_task_and_writes_nothing(task_desk, capsys, sldb_cache) -> None:
    """A tracked task edited by hand outside the rules: sldb names it store/doc-invalid and goes
    on, so desk update reports the validator's message, writes nothing to the task, and keeps the
    other repairs instead of skipping them (g2)."""
    root, task = task_desk
    sldb_cache(root)
    text = task.read_text(encoding="utf-8")
    assert text.count("status: draft\n") == 1 and text.count("current_node: ritual-execution\n") == 1
    assert text.count("history: []\n") == 1
    text = (
        text.replace("status: draft\n", "status: ready_for_testing\n")
        .replace("current_node: ritual-execution\n", "current_node: ritual-testing\n")
        .replace("history: []\n", "history:\n- task_activates\n")
    )
    task.write_text(text, encoding="utf-8")
    capsys.readouterr()
    assert main(["desk", "update", "--root", str(root), "--apply"]) == 1
    out = capsys.readouterr().out
    rel = task.relative_to(root).as_posix()
    assert f"  - {rel}: {ACTIVE_ERROR}." in out
    assert "- Store check failed" not in out
    assert "Skipped the other repairs" not in out
    assert task.read_text(encoding="utf-8") == text

FILE:docs/workflow-policy-reference.md
---
atoms:
- id: atom-cheap-zero-context-reviews-test-the-brief-recursively
  role: documents
- id: atom-docs-are-human-facing-atom-materializations
  role: documents
- id: atom-phase-gates-prevent-agent-skipping
  role: documents
- id: atom-code-changes-close-with-tests-and-commit
  role: documents
- id: atom-available-tasks-are-board-routed-work
  role: documents
- id: atom-drawers-feed-tasks-through-promotion
  role: documents
- id: atom-pills-carry-transitional-task-knowledge
  role: documents
- id: atom-pills-are-reusable-across-tasks
  role: documents
- id: atom-pills-end-as-atoms-docs-or-deletion
  role: documents
- id: atom-phases-are-dependency-layers-of-tasks
  role: documents
- id: atom-phase-closeout-reconciles-pills-and-next-work
  role: documents
- id: atom-tasks-enable-zero-context-subagents
  role: documents
- id: atom-task-board-phases
  role: documents
- id: atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
  role: documents
---
# Workflow Policy Reference

Source atoms are declared in the YAML frontmatter.

This reference summarizes the current workflow policy used by `deskops`.

> **No task is complete without the closeout evidence it declared at creation and its own closing commit. No phase is complete without integration validation and pill reconciliation.**

## Quick Links

- [Task Management](../desk/tasks/Board.md) - Active tasks
- [Pills Reference](../desk/contexts/pills.md) - Context pill format
- [Deferred Work](../desk/drawer/README.md) - Waiting items
- [Context Review Ritual](../desk/rituals/context-review.md) - Cheap recursive brief comprehension
- [Phase Ritual](../desk/rituals/phase.md) - Dependency-layer execution and closeout

---

## Core Model

### Tasks

A task is the atomic workflow unit.

- One coherent deliverable.
- May depend on other tasks.
- Executes in a fresh subagent context.
- Declares how it activates and how it closes by choosing a task type (`deskops add task --task-type`); the type's activation rule names the review receipts it needs, the type's closeout rule names the evidence receipts it closes with, and the task closes only when `deskops closeout verify` has written them accepted and intact, with its own atomic closing commit. `--evidence` only adds kinds to the type's floor, never removes one the type requires.

#### Task types

A task type is a model: a `TaskDoc` subclass registered in the store. `model <= <Tipo>` names the type's family (including its subtypes); a subtype inherits the gates of its ancestors and can only add, never remove.

| Type | Extends | Activation receipts | Closeout evidence |
|---|---|---|---|
| `task.code` | `TaskDoc` | `preflight` + `bundle` | `tests` + `commit` + `atom\|materialization` |
| `task.docs` | `TaskDoc` | `preflight` | `commit` + `document` |
| `task.debug` | `TaskDoc` | `preflight` + `reproduction` | `tests` + `commit` + `atom\|materialization` |
| `task.refactor` | `task.code` | `preflight` + `bundle` + `goldens` | `task.code` + `goldens` |
| `task.decision` | `TaskDoc` | `owner` | `commit` + `document` |
| `task.aggregate` | `TaskDoc` | none (its dependencies closed; `children` is not a field yet) | `commit` (no `children` clause until `TaskAggregateDoc` has a children field) |
| `task.external` | `TaskDoc` | `preflight` | `external` (URL) |

`atom|materialization` is one gate with two alternatives. `commit` means a commit reachable from `HEAD`. The closeout column is data, `deskops/data/rules/closeout-evidence.yaml` (task type -> kinds): `deskops closeout verify` reads it to choose the producers it runs and `deskops add task` reads it as the floor `--evidence` adds to; a desk subtype reads its nearest factory ancestor's entry. A desk adds its own subtypes in `desk/models/*.py`; `deskops desk update --apply` registers them and migrates legacy `task_type` strings (`code`/`implementation`/`test` → `task.code`; `docs`/`spec`/`design` → `task.docs`; `external` → `task.external`; empty → `task.code`).

#### Activation rules

The activation gate of a type is not Python: it is a `RuleDoc` (sldb GO06/GO08) the desk carries under `desk/lifecycle/rule-activation-<type>.md`, a managed seed of the deskops package (`deskops/data/rules/`, declared in `deskops/data/desk_declaration.yaml` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply`; a desk's copy that differs is rewritten and a second run changes nothing). Every rule is `on_transition`, `severity: error`, applies `where current_node = "ritual-execution"` and has the subject `model <= <TypeDoc>`, so a desk subtype (`desk/models/*.py`) inherits it without code and a desk can add its own `RuleDoc` with a narrower subject to add a clause. A receipt counts when a `ReviewDoc` of that `kind` has the task as `subject`, `verdict: accepted` and `anchor_state: intact` (sldb pins `subject` with the task's contract hash when the receipt is saved and recomputes the state on every read: editing `goal`, `scope`, `files`, `validation`, `done_when`, `title` or `implementation_path` leaves it `changed`).

| Rule | Subject | Condition | Message |
|---|---|---|---|
| `rule-activation-task-code` | `model <= TaskCodeDoc` | `any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") and any(^subject: … kind = "bundle") and all(depends_on: status = "closed")` | Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. |
| `rule-activation-task-docs` | `model <= TaskDocsDoc` | `any(^subject: … kind = "preflight") and all(depends_on: status = "closed")` | Una tarea task.docs se activa con un recibo preflight aceptado e intacto y sus dependencias cerradas. |
| `rule-activation-task-debug` | `model <= TaskDebugDoc` | `any(^subject: … kind = "preflight") and any(^subject: … kind = "reproduction") and all(depends_on: status = "closed")` | Una tarea task.debug se activa con recibos preflight y reproduction aceptados e intactos y sus dependencias cerradas. |
| `rule-activation-task-refactor` | `model <= TaskRefactorDoc` | `any(^subject: … kind = "goldens")` (the `task.code` rule already applies to the family) | Una tarea task.refactor se activa, además de lo que pide task.code, con un recibo goldens aceptado e intacto. |
| `rule-activation-task-decision` | `model <= TaskDecisionDoc` | `any(^subject: … kind = "owner") and all(depends_on: status = "closed")` | Una tarea task.decision se activa con un recibo owner aceptado e intacto y sus dependencias cerradas. |
| `rule-activation-task-aggregate` | `model <= TaskAggregateDoc` | `all(depends_on: status = "closed")` | Una tarea task.aggregate se activa con sus dependencias cerradas. |
| `rule-activation-task-external` | `model <= TaskExternalDoc` | `any(^subject: … kind = "preflight") and all(depends_on: status = "closed")` | Una tarea task.external se activa con un recibo preflight aceptado e intacto y sus dependencias cerradas. |

`…` abbreviates `anchor_state = "intact" and verdict = "accepted" and`. A dependency that closed no longer exists as a task document, so `all(depends_on: …)` omits it. `deskops review` writes `preflight`, `bundle` and `node` receipts; `reproduction`, `goldens` and `owner` have no command yet.

`deskops advance` passes the task to sldb as the `document` of its `on_transition` rules: when an `error` finding holds the edge back, the message lists each finding (`error: [rules/<rule>] <Model>:<task>: <message> | <clause> (seen: {...}) (witness: ...)`) instead of the edge's condition; a gate held back only by its own condition (`ritual-testing`, `ritual-closeout`) keeps the message `Gate <node> is not complete (...)`. `deskops show task` prints the same findings under each lifecycle gate (`blocked by:`; `findings` in `--format json`) and `deskops next` under `Blocked by:`. A blocked task is not a status: it stays `draft` at `ritual-execution` with the blocked edge visible in `show` and `next`.

#### Closeout rules

The closeout gate of a type is a `RuleDoc` too (CC33b): `desk/lifecycle/rule-closeout-<type>.md`, a managed seed of `deskops/data/rules/` declared and tracked like the activation rules. Every rule is `on_transition`, `severity: error`, applies `where current_node = "ritual-closeout"` (the source of `task_completes`, whose own condition is only `status = "ready_for_testing"`) and has the subject `model <= <TypeDoc>`. It asks, per kind of the table, for an evidence receipt `deskops closeout verify` writes (CC33a): `any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted")`, with `atom|materialization` as an `or` of the two.

| Rule | Subject | Clauses (receipts accepted and intact) |
|---|---|---|
| `rule-closeout-task-code` | `model <= TaskCodeDoc` | `tests`, `commit`, `atom` or `materialization` |
| `rule-closeout-task-docs` | `model <= TaskDocsDoc` | `commit`, `document` |
| `rule-closeout-task-debug` | `model <= TaskDebugDoc` | `tests`, `commit`, `atom` or `materialization` |
| `rule-closeout-task-refactor` | `model <= TaskRefactorDoc` | `any(^subject: kind = "goldens" and anchor_state = "intact" and verdict = "accepted")` (the receipt of `deskops review record --kind goldens`; the `task.code` rule already applies to the family) |
| `rule-closeout-task-decision` | `model <= TaskDecisionDoc` | `commit`, `document` |
| `rule-closeout-task-aggregate` | `model <= TaskAggregateDoc` | `commit` |
| `rule-closeout-task-external` | `model <= TaskExternalDoc` | `external` |

The closing order is fixed: `deskops closeout verify` runs the producers and writes the receipts (`accepted` or `rejected`); `deskops closeout commit` writes none and evaluates the rule on the task read at `ritual-closeout`. When an error finding holds it back the commit is not made and the output lists each finding (`- error: [rules/rule-closeout-<type>] ...`) and says to run `deskops closeout verify --task <id>`; editing a contract field after verify leaves the receipts `changed`, so the rule blocks again until verify writes new ones. `deskops show task` and `deskops next` show the same findings on the `task_completes` gate. The board view runs verify read-only.

When the atom|materialization gate passes without a linking document (a desk without local atoms, coverage only by a routed follow-up, or a skill guard test), verify writes an accepted `atom` receipt whose `value` is `exempt: <why the gate passed>`, so the rule needs no special case. `--evidence` (the task's `closeout_evidence`) only adds kinds (DA5): an added kind is verified and gets its receipt, and when it fails verify reports it as the alert `added_closeout_evidence_not_verified` without blocking; an added kind outside the vocabulary is the alert `unknown_closeout_evidence`.

Two rules over the task's own fields are `on_write` alerts, `subject: model <= TaskDoc`: `rule-closeout-alert-implicit-code` (`has(task_type) or nonempty(closeout_evidence)`: a task that predates types is gated as code) and `rule-closeout-alert-pill-graduation` (`not nonempty(pills) or any(references: model <= AtomDoc)`: a task that binds pills references the atom they graduate to). The other field checks stay in verify because the rule language has no quantifier over the elements of a list value: the closeout evidence vocabulary (`deskops add task --evidence` refuses an unknown kind), `python_changes_without_declared_tests` and the http(s) shape of an `external` reference.

### Task lifecycle graph

A task moves through the desk's lifecycle graph, which lives in the desk's sldb store: every state is a tracked ritual (`RitualDoc:ritual-execution`, `ritual-testing`, `ritual-closeout`) and every transition is a `RelationDoc` under `desk/lifecycle/`, typed by a `RelationTypeDoc` named by the verb (`task_activates`, `task_hands_to_closeout`, `task_completes`). Each `RelationDoc` declares the whole transition: its `condition` (an sldb `--where` predicate over the task, such as `nonempty(validation)`) and its effects in `attributes`, following sldb's transition convention (GO09): `sets` names the task fields the transition writes (`status: active`, `ready_for_testing`, `closed`) and `terminal: true` marks the transition that closes the task (`task_completes`).

`deskops advance task` asks sldb which edges leaving the task's current node hold (`sldb.api.edges_holding`, with the task as `document` so its activation rule runs), takes that edge, applies its effects with `sldb.api.apply_effects` (validated against the task type's model), sets `current_node: complete` when the edge is terminal and appends the relation type to the task's `history`. One edge leaves each ritual, so nothing depends on the order sldb returns edges in. A blocked task stays where it is with the gate named. The terminal transition is never persisted by `advance`: the only closing entry point is `deskops closeout commit`. `deskops next` reads only the states of `deskops/spec/workflows/task_lifecycle.yaml` (ritual, next actions, `advance_when`); `deskops next --diagram` draws the desk's graph.

The six lifecycle documents and the seven activation rules are managed seeds of the deskops package (`deskops/data/desk_declaration.yaml`, templates in `deskops/data/lifecycle/` and `deskops/data/rules/`). `deskops init` and `deskops desk update --apply` write them, track them (with the three lifecycle rituals by their ids) and rewrite a desk's copy that differs from the package's: `desk update` lists it under `Lifecycle documents to rewrite`, `--apply` reports `Lifecycle graph: rewrote <path>`, and a second run changes nothing. Every other scaffold only creates what is missing. Changing a transition's effect means changing the `RelationDoc` through sldb; no YAML of deskops has to change, and the next `desk update --apply` restores the package's version.

#### Lifecycle consistency (CC37)

A task's `status`, `current_node`, `history` and `task_type` are checked together by a validator of the `TaskDoc` model (`deskops/models/task_lifecycle.py`). sldb applies it on every write: `deskops` itself, `sldb fields update`, `sldb docs update`, `sldb serve` `/save` and transactions. So a write that leaves a task inconsistent is refused with the validator's message, whatever path it takes. A task is consistent in one of these states:

- **Entry:** `current_node` is the entry node, `history` is empty and `status` is `draft`.
- **After transitions:** the last `history` item is the transition that leads to `current_node`, and `status` is what that transition `sets` (`active`, then `ready_for_testing`). The table comes from the package's `RelationDoc`s, not from the desk's store.
- **Closed by closeout:** `superseded` after `superseded`, `resolved` after `resolved-by`, and `closed` after `task_completes`. `closeout supersede` and `closeout resolved-by` record the first two from any node, also on a task the model rejects (they write its frontmatter), and a store lets them close one invalid task while another of the same model remains (sldb names it `store/doc-invalid` and goes on). `closed` is never persisted by `advance`; `closeout commit` removes the task.
- **Outside the lifecycle**, with no `current_node` and empty history: `draft`, a drawer task's `deferred`, and the pre-lifecycle statuses that `closeout retire` removes (`resolved`, `closed`, `done`, `complete`).

`task_type` matches the document's model: each typed model accepts only its own type, and the generic `TaskDoc` accepts an empty or unregistered type. `deskops desk update --apply` does not write an inconsistent task. It reports the task with the reason sldb gives. Only `deskops advance` and `deskops closeout` change a task's lifecycle fields; `deskops edit task` refuses them (GC06).

### Phases

Tasks form an execution dependency graph.

A **phase** is one horizontal dependency layer in that graph:

- task prerequisites are already satisfied
- tasks are ready at the same time
- planned operational changes do not overlap
- tasks may run in parallel when the environment supports it

A phase has execution meaning, not business meaning. It is the workflow unit above individual tasks and below the whole board.

### Boards

The board is the routing surface for active work.

- It names the active tasks.
- It routes board-wide pills and rituals.
- Its current ready dependency layer is the current phase.

---

## Cheap Context Review and Fresh Subagents

Before promoting or executing a draft, plan, package or leaf, run the [context-review ritual](../desk/rituals/context-review.md). It tests the quality of the written question with a cheap reviewer: faithful reformulation, explicit ambiguities and a detailed dry-run of proposed readings, changes, validation and dependencies. The reviewer names intended commands without executing them or editing sources.

Supply the exact versioned brief and only necessary explicit references. Use a new ephemeral process for every attempt, without chat history, earlier reviews, oral fixes, persistent memory, automatic context/skills or tools. Record the chosen cheap provider/model/profile and reason; an expert cannot rescue a failed cheap comprehension gate. The ritual specifies the verified Pi isolation profile and per-node evidence layout.

The coordinator compares understanding with intent, corrects the written brief and recursively decomposes large nodes into children and explicit edges. Review root, packages, every leaf and dependency interfaces before selecting ready leaves. A root-only review does not cover descendants. Unresolved ambiguity blocks execution. Changed input or a changed dependency contract invalidates affected reviews; retries use a new process. Technical transport/quota failures are recorded separately from ambiguity.

Before Executor dispatch, preserve two distinct cheap roles: TaskDoc-only preflight (also saved in `runs/subagents/<run-dir>/preflight.md`) and cold-bundle coverage. The explicit execution bundle contains task, board-routed instructions/rituals, bound pills, linked atoms/files and validation targets. Neither review executes implementation. Expert council review, Executor work, independent Tester validation and human product approval remain separate gates; a word such as APTO or structural PASS grants none of them.

Evidence lives at `runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/`: exact input bytes/hash, model/profile/selection, command/isolation, reformulation/ambiguities/dry-run, coordinator comparison and required edits. These are process records, not runtime enforcement or a new lifecycle state. Each active task then executes in its own fresh context, and an independent Tester validates implementation. The coordinator integrates outputs and enforces task/phase closeout. Do not carry unrelated tasks through one long-lived context.

---

## Pill Lifecycle

Pills are temporary execution aids, but they are not task-specific instances. Correction: pills are not 1:1 with tasks.

```text
Draft or refresh reusable pills -> bind pills to tasks opportunistically -> execute tasks ->
close tasks -> reconcile pills at phase closeout ->
keep / delete / merge / graduate to atoms -> prepare next phase pills
```

At phase closeout, classify touched pills explicitly:

- **still active** - keep for the next phase
- **stale** - delete or retire
- **redundant** - merge or remove duplicates
- **durable** - promote the stabilized residue into atoms first
- **materialization-worthy** - land resulting changes in code, specs, or docs as needed

Do not let durable knowledge remain pill-only once it stabilizes. Do not create a new pill just because a new task exists; create or update a pill only when there is a reusable atomic truth worth rebinding.

---

## Ritual Stack

### 1. Phase Ritual

Before starting a ready dependency layer:

```text
0. REVIEW   -> Review root/packages/leaves and edges cheaply; correct briefs and decompose.
1. IDENTIFY -> Select reviewed ready non-overlapping leaves.
2. BUNDLE   -> Confirm each task has its fresh context bundle.
3. EXECUTE  -> Run the execution ritual per task.
4. CLOSE    -> Require each task to close with its declared evidence and a task commit.
5. VALIDATE -> Run phase-level integration or end-to-end checks.
6. REGRESS  -> Fix interaction regressions.
7. RECONCILE-> Audit pills; delete, merge, or graduate them.
8. SURFACE  -> Capture newly discovered tasks and next-phase pills.
9. COMMIT   -> Make the phase-closing commit.
```

### 2. Task Execution Ritual

For each task in the phase:

```text
1. INIT   -> Confirm task scope, files, pills, validation, and declared closeout evidence.
2. REVIEW -> Accept cheap TaskDoc-only preflight, then separate cheap cold-bundle coverage.
3. BIND   -> Bind every relevant pill.
4. IMPLEMENT -> Make only task-scoped changes.
5. HANDOFF   -> Open an explicit testing handoff.
```

### 3. Task Testing Ritual

```text
1. CHECK  -> Confirm the intended contract and pill guardrails.
2. UPDATE -> Fix stale tests or add missing ones.
3. RUN    -> Execute the smallest relevant scope first.
4. EXPAND -> Run broader checks when shared behavior changed.
5. HANDOFF-> Open an explicit closeout handoff.
```

### 4. Task Closeout Ritual

```text
1. VERIFY -> Run `deskops closeout verify`: it checks the type's evidence (declared X;
             found Y) and writes the evidence receipts the closeout rule reads.
2. CLEAN  -> Remove stale task-local context when appropriate.
3. DELETE -> Remove the resolved task from active routing.
4. COMMIT -> Close with `deskops closeout commit`: it evaluates the type's closeout rule
             on those receipts and writes none; `closeout supersede` when the
             subject no longer exists, `closeout retire` for a pre-lifecycle resolution.
5. WAIT   -> If this was the last task in the phase, do not start the next phase until phase closeout passes.
```

---

## Commit Rules

### Task commit

Every closed task gets its own atomic commit, made by `deskops closeout commit`, `closeout supersede`, or `closeout retire`. The evidence it must show is its type's (plus any kind `--evidence` added at creation), as receipts `deskops closeout verify` wrote and the type's closeout rule accepts.

### Phase commit

When all tasks in a phase are closed, make one separate descriptive phase commit for:

- integration fixes
- pill reconciliation
- captured next work
- board/phase bookkeeping

Do not hide unfinished task work inside a phase commit.

---

## Anti-Patterns

- Starting implementation before identifying the ready phase.
- Treating semantic milestones as phases when tasks still depend on each other.
- Running multiple unrelated tasks through one stale context.
- Closing tasks without the evidence they declared or without a dedicated task commit.
- Starting the next phase after isolated green task tests without integration validation.
- Carrying stale or overlapping pills forward because each task passed independently.
- Leaving durable rules only in pills instead of promoting them into atoms.
- Skipping newly discovered task capture at phase closeout.

FILE:instruccion
Cold-bundle de la tarea task-borrar-la-migracion-de-task-type-viejo-legacy-task-type-keys-y-migrate-task-types-y-sus-tests: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rn 'LEGACY_TASK_TYPE\|migrate_task_types' deskops tests docs
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_task_types.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_task_lifecycle_validator.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea


FILE:desk/tasks/task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis.md
---
sldb:
  by: agent
  at: '2026-11-23T04:39:24Z'
  authority: generated
  via: create_document
id: task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-234848-suggestion-deskops-init-fija-project-identity-con-el-nombre-de-la-carpeta-y-no-hay-comando-para-cambiarlo.md
- desk/inbox/20261122-222005-unclear-de-labchile-chatbots-no-hay-verbo-para-cambiar-project-identity-editar-la-portada-de-pills-ni-fusionar-dos-desks.md
depends_on: []
pills: []
files:
- deskops/workspace.py
- deskops/cli/registry.py
- deskops/cli/commands/repo.py
- tests/test_repo_identity.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops init --id fija project_identity, deskops repo whoami --set la cambia por CLI y repo register avisa si --id no coincide con la identidad del desk

## Rationale

_Explain why this task exists or the business driver behind it._

Dos notas con el mismo hueco. Nota 20261122-234848 (desk de workflow, scion-coordination, 2026-11-23): deskops init /mnt/ssd/proyectos/wf-desks dejó project_identity wf-desks en desk/config.json; después deskops repo register workflow <ruta> --id workflow registró el repo como workflow, y deskops repo whoami en ese desk responde wf-desks. Nota 20261122-222005 (labchile_chatbots, punto 2): al fusionar dos desks no hubo verbo para cambiar project_identity y se editó desk/config.json a mano. Hoy deskops/workspace.py (alrededor de la línea 366) hace data.setdefault("project_identity", root.name) y no hay otra forma. Relacionada, no se duplica: task-init-en-un-worktree-usa-el-nombre-del-repo-y-doctor-lee-el-pythonpath-del-store (cómo se deriva la identidad por defecto en un worktree); esta tarea agrega la forma explícita.

## Goal

_Describe the concrete result this task must produce._

(1) deskops init [path] --id <identidad>: escribe project_identity = <identidad> en desk/config.json (sin --id, igual que hoy); si el desk ya existe con otra identidad, no la pisa y avisa que se use repo whoami --set. (2) deskops repo whoami --set <identidad> --root <desk>: valida que <identidad> sea un slug (minúsculas, dígitos, guiones), reescribe solo project_identity en desk/config.json (como set_job_field de deskops/queue.py, sin tocar el resto del archivo) e imprime "project_identity: <vieja> -> <nueva>". (3) deskops repo register <nombre> <ruta> --id X avisa en stderr cuando el desk de <ruta> tiene project_identity distinto de X: "el desk de <ruta> dice project_identity <Y>; alinéalo con deskops repo whoami --set X --root <ruta>".

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/workspace.py, deskops/cli/registry.py (argumentos de init), deskops/cli/commands/repo.py, goldens de ayuda y tests/test_repo_identity.py. No entra: los puntos 1 y 3 de la nota 20261122-222005 (editar la portada de pills y fusionar desks), que esperan decisión de JP; renombrar referencias a la identidad vieja en otros desks.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_repo_identity.py: test_init_with_id_sets_project_identity, test_whoami_set_rewrites_only_project_identity (el resto de desk/config.json queda byte a byte), test_whoami_set_rejects_non_slug, test_register_warns_when_id_differs_from_desk_identity. p2: implementar. p3: goldens de ayuda. p4: suite con -n 4. p5: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_repo_identity.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_scaffold_golden.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los cuatro tests nuevos pasan y deskops init sin --id deja el mismo desk/config.json que hoy (test existente de scaffold verde).

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
    if restore_managed:
        declaration = _keep_desk_hooks(target_path, declaration)
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


def _keep_desk_hooks(target_path: Path, declaration: Any) -> Any:
    """The declaration with each lifecycle seed carrying the desk's own ``attributes.hooks``.

    The hooks of a transition belong to the desk: rewriting a managed seed copies the whole
    list, in order, from the desk's file (the package declares none, so nothing is merged)."""
    from sldb.api import Seed
    from sldb.api import StoreDeclaration

    from deskops import lifecycle

    prefix = lifecycle.LIFECYCLE_DIR.as_posix() + "/"
    seeds = []
    for seed in declaration.seeds:
        desk_file = target_path / seed.path
        if seed.path.startswith(prefix) and seed.text is not None and desk_file.is_file():
            desk_text = desk_file.read_text(encoding="utf-8")
            hooks = lifecycle.hooks_from_text(desk_text)
            if hooks is not None:
                text = lifecycle.with_hooks(seed.text, hooks, lifecycle.provenance_from_text(desk_text))
                seed = Seed(path=seed.path, mode=seed.mode, text=text)
        seeds.append(seed)
    return StoreDeclaration(folders=declaration.folders, seeds=seeds, include=declaration.include)


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
        try:
            raw = _frontmatter_task_type(path)
        except (yaml.YAMLError, UnicodeDecodeError):
            continue  # legacy_task_states reports it as an invalid task; nothing here writes it
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


# Frontmatter keys of tasks written before the TaskDoc migration that TaskDoc does not declare:
# the model ignores them on read, but every model write (``write_doc``) refuses to erase them.
# The list is closed; any other undeclared key keeps that refusal.
LEGACY_FRONTMATTER_KEYS = ("checklists", "routine")


@dataclass(frozen=True)
class LegacyFrontmatterKey:
    """One legacy key in the frontmatter of a task under ``desk/tasks``."""

    path: Path
    rel: str
    key: str
    value: Any

    def pending_line(self) -> str:
        return f"{self.rel}: legacy frontmatter key {self.key}"

    def removed_line(self) -> str:
        previous = json.dumps(self.value, ensure_ascii=False, default=str, separators=(",", ":"))
        return f"{self.rel}: removed {self.key} = {previous}"


def legacy_frontmatter_keys(root: Path) -> list[LegacyFrontmatterKey]:
    """The legacy keys of each task's frontmatter, in path order and, within a file, in the
    order of ``LEGACY_FRONTMATTER_KEYS``. A task whose frontmatter cannot be read is skipped:
    ``legacy_task_states`` already reports it as an invalid task."""
    found: list[LegacyFrontmatterKey] = []
    for path in _task_files(root):
        try:
            parsed = _task_frontmatter(path)
        except (yaml.YAMLError, UnicodeDecodeError):
            continue
        if parsed is None:
            continue
        data = parsed[0]
        rel = path.relative_to(root).as_posix()
        found.extend(LegacyFrontmatterKey(path, rel, key, data[key]) for key in LEGACY_FRONTMATTER_KEYS if key in data)
    return found


def _without_top_level_keys(frontmatter: str, keys: set[str]) -> str:
    """The frontmatter text without the blocks of ``keys``: each one's ``key:`` line plus the
    lines under it (indented, ``- `` items, and blank lines inside an indented block). Every
    other line keeps its text and order."""
    lines = frontmatter.split("\n")
    kept: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not any(line.startswith(f"{key}:") for key in keys):
            kept.append(line)
            index += 1
            continue
        index += 1
        while index < len(lines):
            current = lines[index]
            if current[:1] in (" ", "-"):
                index += 1
                continue
            if current == "":
                following = next((rest for rest in lines[index:] if rest != ""), "")
                if following[:1] in (" ", "-"):
                    index += 1
                    continue
            break
    return "\n".join(kept)


def migrate_legacy_frontmatter_keys(root: Path) -> tuple[list[str], list[LegacyTaskState]]:
    """Remove the legacy keys from each task's frontmatter; ``(lines, not migrated)``.

    The edit is textual: only the keys' blocks go, the rest of the file is kept byte for byte.
    A file is written only when its frontmatter, read back, is the previous one without exactly
    those keys; otherwise it is left as it was and reported. Idempotent.
    """
    by_path: dict[Path, list[LegacyFrontmatterKey]] = {}
    for item in legacy_frontmatter_keys(root):
        by_path.setdefault(item.path, []).append(item)
    lines: list[str] = []
    failed: list[LegacyTaskState] = []
    for path, items in by_path.items():
        rel = items[0].rel
        text = path.read_text(encoding="utf-8")
        match = _FRONTMATTER_RE.match(text)
        keys = {item.key for item in items}
        before = (yaml.safe_load(match.group(1)) or {}) if match else None
        new_frontmatter = _without_top_level_keys(match.group(1), keys) if match else ""
        try:
            after = yaml.safe_load(new_frontmatter) or {}
        except yaml.YAMLError:
            after = None
        expected = {k: v for k, v in before.items() if k not in keys} if isinstance(before, dict) else None
        if expected is None or after != expected:
            task_id = str(before.get("id") or path.stem) if isinstance(before, dict) else path.stem
            failed.append(
                LegacyTaskState(path, rel, task_id, [f"legacy frontmatter keys not removed ({', '.join(sorted(keys))}): the textual edit would change other fields"])
            )
            continue
        path.write_text("---\n" + new_frontmatter + "\n---\n" + text[match.end():], encoding="utf-8")
        lines.extend(item.removed_line() for item in items)
    return lines, failed

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

    Without this, `deskops message ack` and `deskops next` inside such a repo
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

FILE:instruccion
Cold-bundle de la tarea task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_repo_identity.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_scaffold_golden.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)


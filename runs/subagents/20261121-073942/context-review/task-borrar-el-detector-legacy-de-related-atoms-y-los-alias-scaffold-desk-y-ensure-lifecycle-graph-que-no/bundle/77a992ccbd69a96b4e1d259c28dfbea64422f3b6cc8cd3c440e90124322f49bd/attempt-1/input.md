FILE:desk/tasks/task-borrar-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph-que-no.md
---
sldb:
  by: agent
  at: '2026-11-16T06:05:08Z'
  authority: generated
  via: save_document_payload
id: task-borrar-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph-que-no
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/atom_references.py
- deskops/graph/checks.py
- deskops/workspace.py
- deskops/lifecycle.py
- tests/test_atom_reference_convention.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-retirar-caminos-legacy-migrar-los-datos-y-borrar-el-c-digo-de-compatibilidad.md
---

# Borrar el detector legacy de related_atoms y los alias scaffold_desk y ensure_lifecycle_graph, que no tienen consumidores

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (puntos 3 y 5, verificados el 2026-11-16). LEGACY_FIELD_VIOLATION vive en deskops/atom_references.py:23 y se usa en deskops/graph/checks.py:13 y 196; ningun desk usa related_atoms. Los alias scaffold_desk (deskops/workspace.py:754) y ensure_lifecycle_graph (deskops/lifecycle.py:431) se agregaron contra DK3 en b11a5282; graph_ui ya usa seed_desk y write_lifecycle_graph fuera de runs/. El punto 2 (snapshot en ruta vieja) ya se resolvio en CC33c (120bb672).

## Goal

_Describe the concrete result this task must produce._

Desaparecen: en deskops/atom_references.py LEGACY_FIELDS, LEGACY_FIELD_VIOLATION y la frase del docstring que presenta related_atoms como alias legacy; en deskops/graph/checks.py los imports (lineas 13-14) y el bloque que los usa (alrededor de 188-196); las asignaciones de alias scaffold_desk = seed_desk (deskops/workspace.py:754) y ensure_lifecycle_graph = write_lifecycle_graph (deskops/lifecycle.py:431); y en tests/test_atom_reference_convention.py los tests que esperan el hallazgo legacy_atom_reference_field. test_fenced_yaml_examples_are_not_scanned se conserva (prueba que los bloques de ejemplo no se escanean, sigue siendo valido).

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/atom_references.py, deskops/graph/checks.py, deskops/workspace.py, deskops/lifecycle.py, tests/test_atom_reference_convention.py (casos legacy) y los tests que importen los alias. Verificar antes con `grep -rn 'scaffold_desk\|ensure_lifecycle_graph' /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui --include=*.py | grep -v /runs/` vacio. No entra: scripts viejos en UIs/graph_ui/runs/. Precisiones del preflight 1: hoy solo tests/test_atom_reference_convention.py nombra related_atoms o LEGACY_FIELD_VIOLATION, y ningun test importa scaffold_desk ni ensure_lifecycle_graph (solo los definen deskops/workspace.py y deskops/lifecycle.py); casos legacy = los tests de ese archivo que usan esos nombres. La busqueda de consumidores cubre todo /mnt/ssd/proyectos/SLDB_1 excepto directorios runs/ y .git: grep -rn --include=*.py 'scaffold_desk\|ensure_lifecycle_graph\|LEGACY_FIELD_VIOLATION' /mnt/ssd/proyectos/SLDB_1 | grep -v '/runs/'. test_graph_checks.py y test_cli.py solo se corren.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Greps de consumidores. 2) Borrar. 3) Greps de validacion vacios. 4) Tests.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rnE 'LEGACY_FIELDS|LEGACY_FIELD_VIOLATION|scaffold_desk|ensure_lifecycle_graph' deskops tests
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_reference_convention.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_checks.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los greps quedan vacios y la suite no tiene fallas nuevas.

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

FILE:deskops/atom_references.py
"""Canonical atom reference metadata.

One artifact field carries structured atom references: ``atoms``. A reference is
either a bare atom id or a mapping with an ``id`` and an optional ``role``. The
role vocabulary is deliberately small; ``related_atoms`` is a legacy alias that
``deskops drift check`` reports, and ``source_atoms`` remains the
``MaterializationContractDoc`` field.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


CANONICAL_FIELD = "atoms"
LEGACY_FIELDS = ("related_atoms",)
MATERIALIZATION_FIELD = "source_atoms"
ALLOWED_ROLES = ("references", "documents", "specifies", "constrains", "validates")
DEFAULT_ROLE = "references"

INVALID_ROLE_VIOLATION = "invalid_atom_reference_role"
LEGACY_FIELD_VIOLATION = "legacy_atom_reference_field"


@dataclass(frozen=True)
class ParsedAtomReference:
    """One declared atom reference.

    ``role`` keeps the declared value even when it is invalid; ``violation``
    names the problem so extractors can fall back to ``DEFAULT_ROLE`` while the
    drift validator reports the declaration instead of hiding it.
    """

    atom_id: str
    role: str
    field_name: str
    violation: str | None = None

    def as_tuple(self) -> tuple[str, str, str]:
        return (self.atom_id, self.role, self.field_name)


def parse_atom_reference(
    value: Any,
    field_name: str = CANONICAL_FIELD,
) -> ParsedAtomReference | None:
    """Parse a string or ``{id, role}`` mapping into an atom reference.

    Returns ``None`` when the value is not a reference shape. An unknown role is
    returned as an explicit ``invalid_atom_reference_role`` violation; it is
    never silently rewritten here.
    """
    if isinstance(value, str):
        atom_id = value.strip()
        if not atom_id:
            return None
        return ParsedAtomReference(atom_id=atom_id, role=DEFAULT_ROLE, field_name=field_name)

    if not isinstance(value, dict):
        return None

    atom_id = value.get("id")
    if not isinstance(atom_id, str) or not atom_id.strip():
        return None

    role = value.get("role")
    if not isinstance(role, str) or not role.strip():
        return ParsedAtomReference(
            atom_id=atom_id.strip(),
            role=DEFAULT_ROLE,
            field_name=field_name,
        )

    role = role.strip()
    violation = None if role in ALLOWED_ROLES else INVALID_ROLE_VIOLATION
    return ParsedAtomReference(
        atom_id=atom_id.strip(),
        role=role,
        field_name=field_name,
        violation=violation,
    )


def iter_atom_reference_values(value: Any) -> list[Any]:
    """Normalize a declared field value to the reference shapes to parse."""
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]

FILE:deskops/graph/checks.py
from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from sldb.api.edges.project_graph import MissingProjectTarget as MissingGraphTarget

from deskops.atom_references import ALLOWED_ROLES
from deskops.atom_references import CANONICAL_FIELD
from deskops.atom_references import LEGACY_FIELD_VIOLATION
from deskops.atom_references import LEGACY_FIELDS
from deskops.atom_references import MATERIALIZATION_FIELD
from deskops.atom_references import iter_atom_reference_values
from deskops.atom_references import parse_atom_reference


from deskops.graph.desk_graph import extract_declared_edges
from deskops.graph.desk_graph import extract_doc_nodes
from deskops.graph.view import GraphReadError
from deskops.graph.view import GraphView
from deskops.graph.view import read_graph_file


class GraphMissingCheckError(RuntimeError):
    """Raised when graph missing checks cannot read their input."""


@dataclass(frozen=True)
class GraphMissingFinding:
    kind: str
    source_id: str
    target_id: str
    reason: str
    role: str | None = None
    provenance_path: str | None = None
    provenance_locator: str | None = None
    extractor: str | None = None
    record: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


def find_missing_graph_references(root: Path, graph_path: Path | None = None) -> list[GraphMissingFinding]:
    """Missing references of sldb's project graph (GD21), plus the dangling edges of a ``--graph`` file."""
    findings = [
        _finding_from_missing_target(missing)
        for missing in extract_declared_edges(root).missing_targets
        if not declared_target_is_a_file(root, missing.target_id)
    ]
    if graph_path is not None:
        try:
            snapshot = read_graph_file(graph_path)
        except GraphReadError as exc:
            raise GraphMissingCheckError(str(exc)) from exc
        findings.extend(find_missing_snapshot_targets(snapshot))
    return sorted(findings, key=lambda finding: (finding.kind, finding.source_id, finding.target_id))


def declared_target_is_a_file(root: Path, target_id: str) -> bool:
    """Whether a declared target the graph has no node for is still an existing file of the repo.

    The project graph makes nodes only for the files its surfaces extract, so an existing
    ``.yaml`` or ``.json`` (the plan's ``dag.yaml`` in the drawer, a test fixture) is reported as
    a missing target although it is there. sldb's ``DeclaredFileTargets`` (GD21) makes nodes only
    for a top-level scalar frontmatter field of a glob of documents, outside the exclusions; the
    desk already declares the one it can (``MATERIALIZATION_TARGETS``). None of the targets this
    exception covers fits it: a task's ``references:`` list (inbox notes), a path mentioned in a
    task's body (``dag.yaml``, an e2e scenario), and a materialization target under the excluded
    ``tests/fixtures``. So the exception stays (reported to sldb): such a target is not missing
    when, without its ``kind:`` prefix, it names a file inside ``root``. An atom reference, a
    path that does not exist, and a path that leaves ``root`` (absolute, or through ``..``) are
    still reported.
    """
    if target_id.startswith("atom:"):
        return False
    prefix, sep, rest = target_id.partition(":")
    relative = rest if sep and "/" not in prefix else target_id
    if not relative or Path(relative).is_absolute():
        return False
    base = Path(root).resolve()
    candidate = (base / relative).resolve()
    return candidate.is_relative_to(base) and candidate.is_file()


def find_missing_snapshot_targets(snapshot: GraphView) -> list[GraphMissingFinding]:
    """Return edges whose target id is absent from the graph's nodes."""
    node_ids = {node.id for node in snapshot.nodes}
    findings: list[GraphMissingFinding] = []
    seen: set[tuple[str, str, str | None]] = set()
    for edge in snapshot.edges:
        if edge.target in node_ids:
            continue
        key = (edge.source, edge.target, edge.role)
        if key in seen:
            continue
        seen.add(key)
        findings.append(
            GraphMissingFinding(
                kind="missing_edge_target",
                source_id=edge.source,
                target_id=edge.target,
                role=edge.role,
                provenance_path=edge.provenance_path,
                provenance_locator=edge.provenance_locator,
                extractor=edge.extractor,
                reason="edge target was not found among graph nodes",
            )
        )
    return sorted(findings, key=lambda finding: (finding.source_id, finding.target_id, finding.role or ""))


def _finding_from_missing_target(missing: MissingGraphTarget) -> GraphMissingFinding:
    kind = "dangling_source_atom_reference" if missing.target_id.startswith("atom:") else "missing_declared_target"
    return GraphMissingFinding(
        kind=kind,
        source_id=missing.source_id,
        target_id=missing.target_id,
        provenance_path=missing.provenance_path,
        provenance_locator=missing.provenance_locator,
        extractor=missing.extractor,
        reason=missing.reason,
        record=missing.record,
    )


@dataclass(frozen=True)
class AtomReferenceFinding:
    kind: str
    path: str
    locator: str
    reason: str
    atom_id: str | None = None
    role: str | None = None
    field_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


def find_atom_reference_violations(root: Path) -> list[AtomReferenceFinding]:
    """Report invalid roles and legacy atom reference fields in Markdown frontmatter.

    The documents are the project graph's (sldb, GD21) under ``desk/`` and ``docs/``; only
    their frontmatter is a declaration. Fenced YAML blocks are examples, so they are not read.
    """
    project_root = Path(root)
    findings: list[AtomReferenceFinding] = []
    paths = {node.path for node in extract_doc_nodes(project_root) if node.path.endswith(".md") and node.path.split("/", 1)[0] in ("desk", "docs")}
    for relative_path in sorted(paths):
        if any(part.startswith(".") for part in Path(relative_path).parts):
            continue
        try:
            text = (project_root / relative_path).read_text(encoding="utf-8")
        except OSError:
            continue
        frontmatter = _frontmatter_mapping(text)
        if frontmatter is not None:
            findings.extend(_atom_reference_findings(frontmatter, relative_path))

    return sorted(findings, key=lambda finding: (finding.path, finding.locator, finding.kind))


def _frontmatter_mapping(text: str) -> dict[Any, Any] | None:
    if not text.startswith("---\n"):
        return None
    try:
        _, rest = text.split("---\n", 1)
        block, _body = rest.split("\n---", 1)
    except ValueError:
        return None
    try:
        loaded = yaml.safe_load(block)
    except yaml.YAMLError:
        return None
    return loaded if isinstance(loaded, dict) else None


def _atom_reference_findings(mapping: dict[Any, Any], path: str) -> list[AtomReferenceFinding]:
    findings: list[AtomReferenceFinding] = []
    fields: list[tuple[str, Any]] = []
    for field_name in (CANONICAL_FIELD, MATERIALIZATION_FIELD):
        if field_name in mapping:
            fields.append((field_name, mapping[field_name]))
    materialization = mapping.get("materialization")
    if isinstance(materialization, dict) and MATERIALIZATION_FIELD in materialization:
        fields.append(
            (f"materialization.{MATERIALIZATION_FIELD}", materialization[MATERIALIZATION_FIELD])
        )
    for field_name in LEGACY_FIELDS:
        if field_name in mapping:
            fields.append((field_name, mapping[field_name]))

    for field_name, value in fields:
        if field_name in LEGACY_FIELDS:
            findings.append(
                AtomReferenceFinding(
                    kind=LEGACY_FIELD_VIOLATION,
                    path=path,
                    locator=f"frontmatter:{field_name}",
                    field_name=field_name,
                    reason=(
                        f"uses legacy atom reference field {field_name}; "
                        f"declare atom references in {CANONICAL_FIELD}"
                    ),
                )
            )

        for index, item in enumerate(iter_atom_reference_values(value)):
            parsed = parse_atom_reference(item, field_name)
            if parsed is None or parsed.violation is None:
                continue
            findings.append(
                AtomReferenceFinding(
                    kind=parsed.violation,
                    path=path,
                    locator=f"frontmatter:{field_name}[{index}]",
                    atom_id=parsed.atom_id,
                    role=parsed.role,
                    field_name=field_name,
                    reason=(
                        f"atom {parsed.atom_id} declares invalid role {parsed.role!r}; "
                        f"allowed roles: {', '.join(ALLOWED_ROLES)}"
                    ),
                )
            )

    return findings

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

FILE:deskops/lifecycle.py
"""The task lifecycle as a graph in the desk's sldb store.

States are the desk's tracked rituals (``RitualDoc:ritual-execution`` and its siblings).
Transitions are sldb ``RelationDoc`` edges between those rituals, typed by a
``RelationTypeDoc`` whose name is the verb (``task_activates``), with a ``condition``
written as an sldb ``--where`` predicate over the task and the transition's effects in
``attributes``: ``sets`` (the task fields the transition writes, ``status`` today) and
``terminal`` (the task closes), the convention sldb reads (GO09). The six documents are
managed seeds of the package (``deskops/data/desk_declaration.yaml``, templates in
``deskops/data/lifecycle/``): ``deskops init`` and ``deskops desk update --apply`` write
them under ``desk/lifecycle/`` and rewrite a desk's copy that differs.

The activation gate of each factory task type is a ``RuleDoc`` (sldb GO06/GO08), also a
managed seed (``deskops/data/rules/``, written to ``desk/lifecycle/rule-activation-<type>.md``):
``on_transition`` over ``ritual-execution``, with subject ``model <= <TypeDoc>`` so a desk's
subtype inherits it without code, requiring the review receipts the type asks for
(``any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")``) and
the task's dependencies closed (``all(depends_on: status = "closed")``). sldb evaluates those
rules when ``edges_holding`` receives the task as ``document``; an ``error`` finding blocks
every edge and ``edges_blocked`` returns them with the findings ``deskops advance``, ``next``
and ``show`` print.

deskops keeps three things: the states ``deskops next`` describes
(``deskops/spec/workflows/task_lifecycle.yaml``), the call to sldb for the edges whose
condition holds (``sldb.api.edges_holding``) and their effects (``sldb.api.apply_effects``),
and the task's ``history``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from deskops.paths import data_path
from deskops.paths import package_pythonpath

SPEC_PATH = data_path("spec", "workflows", "task_lifecycle.yaml")
LIFECYCLE_DIR = Path("desk") / "lifecycle"
COMPLETE = "complete"
RELATION_TYPE_MODEL = "RelationTypeDoc"
RELATION_MODEL = "RelationDoc"
RITUAL_MODEL = "RitualDoc"
RULE_MODEL = "RuleDoc"
RULE_MODEL_REF = "sldb.models.rule_doc:RuleDoc"


class LifecycleGraphMissing(RuntimeError):
    """The desk's store has no lifecycle graph, or it does not cover a task's state."""


class LifecycleSeedOutOfDate(LifecycleGraphMissing):
    """The edge ``deskops advance`` would take does not carry the package's effect (a desk's
    lifecycle seed older than CC31, ``attributes: {}``): applying it would write a state the
    ``TaskDoc`` validator rejects. Raised before any effect is applied; the fix is
    ``deskops desk update --apply``, which restores the managed seed."""


class HookDefinitionError(RuntimeError):
    """A transition's ``attributes.hooks`` entry is malformed; ``deskops advance`` fails with it
    before persisting anything."""


#: Seconds a post-hook may run unless its entry carries its own ``timeout``.
DEFAULT_HOOK_TIMEOUT = 300


@dataclass(frozen=True, slots=True)
class Hook:
    """One post-hook of a transition: a command (argument list, no shell) run after the transition is persisted."""

    name: str
    run: tuple[str, ...]
    timeout: int = DEFAULT_HOOK_TIMEOUT

    def as_dict(self) -> dict[str, Any]:
        return {"name": self.name, "run": list(self.run), "timeout": self.timeout}


def parse_hooks(raw: Any, relation_doc: str) -> tuple[Hook, ...]:
    """The hooks of ``attributes.hooks`` of the edge authored by ``relation_doc``; raises
    ``HookDefinitionError`` naming the RelationDoc when an entry has no ``name``, no ``run``, a
    ``run`` that is not a list of texts, or a ``timeout`` that is not an integer above zero."""
    if raw in (None, ""):
        return ()
    where = f"{LIFECYCLE_DIR.as_posix()}/{relation_doc}.md"

    def bad(why: str) -> HookDefinitionError:
        return HookDefinitionError(f"Malformed attributes.hooks in {where}: {why}.")

    if not isinstance(raw, list):
        raise bad("hooks must be a list")
    hooks: list[Hook] = []
    for index, entry in enumerate(raw, start=1):
        if not isinstance(entry, dict):
            raise bad(f"entry {index} is not a mapping")
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            raise bad(f"entry {index} has no name")
        run = entry.get("run")
        if not isinstance(run, list) or not run or not all(isinstance(a, str) for a in run):
            raise bad(f"hook '{name}' needs run as a non-empty list of texts")
        timeout = entry.get("timeout", DEFAULT_HOOK_TIMEOUT)
        if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout <= 0:
            raise bad(f"hook '{name}' has a timeout that is not an integer above zero")
        hooks.append(Hook(name=name, run=tuple(run), timeout=timeout))
    return tuple(hooks)


def _frontmatter_of(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def hooks_from_text(text: str) -> Any:
    """``attributes.hooks`` of a lifecycle seed's frontmatter text; None when it declares none."""
    attributes = _frontmatter_of(text).get("attributes")
    return attributes.get("hooks") if isinstance(attributes, dict) else None


def provenance_from_text(text: str) -> Any:
    """The ``sldb`` write provenance of a document's frontmatter text; None without it."""
    return _frontmatter_of(text).get("sldb")


def with_hooks(text: str, hooks: Any, provenance: Any = None) -> str:
    """The seed ``text`` with ``attributes.hooks`` set to ``hooks`` (the whole list, in order) and,
    when given, the desk copy's ``sldb`` write provenance (sldb adds it to a document it edits, so
    a copy carrying the hooks has it); the text unchanged when the seed has no frontmatter."""
    front = _frontmatter_of(text)
    if not front:
        return text
    attributes = dict(front.get("attributes") or {})
    attributes["hooks"] = hooks
    front["attributes"] = attributes
    if provenance is not None:
        front = {"sldb": provenance, **front}
    rest = text.split("---", 2)[2]
    return "---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True) + "---" + rest


@dataclass(frozen=True, slots=True)
class Transition:
    """One edge of the lifecycle graph leaving ``source``, with its effects as the edge declares them."""

    relation_type: str
    source: str
    target: str
    condition: str
    sets: dict[str, Any] = field(default_factory=dict)
    terminal: bool = False
    #: The name of the ``RelationDoc`` that authors the edge (its file is ``desk/lifecycle/<name>.md``).
    relation_doc: str = ""
    #: The findings of the task's ``on_transition`` rules (sldb GO08), as ``finding_dict`` gives
    #: them: every finding on a blocked edge, only alerts on a holding one, none without a document.
    findings: tuple[dict[str, Any], ...] = ()
    #: ``attributes.hooks`` as the edge declares them, unvalidated (``parse_hooks`` validates).
    raw_hooks: Any = None
    #: ``attributes.manual``: the edge is never taken by the normal advance, only by ``advance --back``.
    manual: bool = False

    @property
    def hooks(self) -> tuple[Hook, ...]:
        return parse_hooks(self.raw_hooks, self.relation_doc or self.relation_type)

    def hooks_listing(self) -> list[dict[str, Any]]:
        """The declared hooks as plain mappings for display; a malformed entry is shown as far as it reads."""
        raw = self.raw_hooks if isinstance(self.raw_hooks, list) else []
        return [
            {
                "name": str(e.get("name") or ""),
                "run": [str(a) for a in e["run"]] if isinstance(e.get("run"), list) else [],
                "timeout": e.get("timeout", DEFAULT_HOOK_TIMEOUT),
            }
            for e in raw
            if isinstance(e, dict)
        ]

    @property
    def effects(self) -> dict[str, Any]:
        return {"sets": dict(self.sets), "terminal": self.terminal}


@dataclass(frozen=True, slots=True)
class LifecycleSpec:
    """The states of ``task_lifecycle.yaml``: what ``deskops next`` says at each node."""

    entry_node: str
    states: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    @property
    def rituals(self) -> list[str]:
        return [node for node in (str(state.get("current_node") or "") for state in self.states) if node and node != COMPLETE]


@dataclass(slots=True)
class ReadSnapshot:
    """Reads shared by every task of one read-only pass.

    ``DeskopsOperations.read_snapshot`` opens one; ``transitions_from`` keeps the transitions
    leaving each node in it, ``transition_findings`` the store's rule graph (sldb loads the
    whole index for it, ~3 s on a small desk), the closure service the closeout graph context
    and the operations facade the path, model payload and normalized payload of each task.
    Nothing outlives the pass: the snapshot is dropped when the block closes.
    """

    transitions: dict[str, list["Transition"]] = field(default_factory=dict)
    graph_context: Any = None
    rule_graph: Any = None
    has_rules: bool | None = None
    #: Cache key (resolved path or task id) -> (path, model payload, payload with effective fields).
    task_records: dict[str, tuple[Path, dict[str, Any], dict[str, Any]]] = field(default_factory=dict)
    #: Normalized task payloads, keyed by task id, shared by a task's inherited parents.
    task_payloads: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: Resolved task path -> the ``Model:name`` its on_transition rules use.
    task_documents: dict[str, str | None] = field(default_factory=dict)


@dataclass(slots=True)
class TransitionResult:
    current_node: str
    status: str
    progressed: bool
    blocked: bool
    message: str
    #: The transition taken (set when ``progressed``); ``advance_task`` runs its hooks after persisting it.
    transition: Transition | None = None


def load_lifecycle_spec(path: Path = SPEC_PATH) -> LifecycleSpec:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    states = tuple(state for state in payload.get("states") or [] if isinstance(state, dict))
    if not states:
        raise ValueError(f"Lifecycle spec declares no states: {path}")
    return LifecycleSpec(entry_node=str(payload.get("entry_node") or states[0].get("current_node") or ""), states=states)


# ---------------------------------------------------------------- conditions
def condition_holds(condition: str, payload: dict[str, Any]) -> bool:
    """Whether an sldb ``--where`` condition (predicates joined by `` and ``) holds on a task payload."""
    from sldb.api import where_matches

    return where_matches(condition, payload)


# ---------------------------------------------------------------- the graph
def _store(root: Path) -> Path:
    return root / ".sldb"


def ritual_export_id(ritual_id: str) -> str:
    return f"{RITUAL_MODEL}:{ritual_id}"


def finding_dict(finding: Any) -> dict[str, Any]:
    """An sldb ``Finding`` as the plain mapping ``show --format json`` prints."""
    return {"level": finding.level, "code": finding.code, "subject": finding.subject, "what": finding.what}


def finding_line(finding: dict[str, Any]) -> str:
    """One finding as sldb prints it: ``<level>: [<code>] <node>: <message> | <clause> (seen: ...)``."""
    return f"{finding['level']}: [{finding['code']}] {finding['subject']}: {finding['what']}"


def _transition(node: str, edge: Any) -> Transition:
    """The edge as a transition; ``effects`` (filled by ``edges_holding``) else the declared attributes."""
    attributes = edge.metadata.get("attributes") or {}
    effects = edge.effects or {"sets": attributes.get("sets") or {}, "terminal": attributes.get("terminal")}
    return Transition(
        relation_type=edge.relation,
        source=node,
        target=edge.target.rsplit(":", 1)[-1],
        condition=str(edge.metadata.get("condition") or ""),
        sets=dict(effects.get("sets") or {}),
        terminal=bool(effects.get("terminal")),
        relation_doc=str(edge.metadata.get("relation_doc") or ""),
        findings=tuple(finding_dict(f) for f in (getattr(edge, "findings", None) or ())),
        raw_hooks=attributes.get("hooks"),
        manual=bool(attributes.get("manual")),
    )


def _is_lifecycle_edge(edge: Any) -> bool:
    """An authored edge (a RelationDoc) whose target is a ritual (`sldb://document/RitualDoc:<id>`)."""
    return edge.metadata.get("origin") == "relation_doc" and edge.target.rsplit("/", 1)[-1].startswith(f"{RITUAL_MODEL}:")


def _lifecycle_edges(node: str, edges: list[Any], *, manual: bool = False) -> list[Transition]:
    """The authored edges between rituals, in the order sldb returns them: the manual ones
    (``attributes.manual``) when ``manual``, else the ones the normal advance may take."""
    found = [_transition(node, e) for e in edges if _is_lifecycle_edge(e)]
    return [t for t in found if t.manual is manual]


def transitions_from(root: Path, node: str, *, snapshot: ReadSnapshot | None = None, manual: bool = False) -> list[Transition]:
    """The lifecycle transitions leaving ``node``, as the desk's graph declares them.

    Topology, conditions and effects all come from the graph. The lifecycle graph lives in the
    desk's own store, so only that store's edge index is read (sldb keeps it composed while
    its shards do not move), not the index composed with every linked store.

    With a ``snapshot``, the transitions leaving a node are read once and reused. Manual
    transitions (``attributes.manual``) are left out unless ``manual``.
    """
    if manual:
        from sldb.api import edges_from as manual_edges_from

        return _lifecycle_edges(node, manual_edges_from(_store(root), ritual_export_id(node), include_linked=False), manual=True)
    if snapshot is not None:
        if node not in snapshot.transitions:
            snapshot.transitions[node] = transitions_from(root, node)
        return snapshot.transitions[node]
    from sldb.api import edges_from

    return _lifecycle_edges(node, edges_from(_store(root), ritual_export_id(node), include_linked=False))


def transitions_holding(root: Path, node: str, payload: dict[str, Any], document: str | None = None) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` (``sldb.api.edges_holding``),
    each with its effects resolved for that payload. With ``document`` (the task's ``Model:name``
    in the store) the task's ``on_transition`` rules run too: an error finding holds every edge back."""
    from sldb.api import edges_holding

    return _lifecycle_edges(node, edges_holding(_store(root), ritual_export_id(node), payload, include_linked=False, document=document))


def transitions_blocked(root: Path, node: str, payload: dict[str, Any], document: str) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` but that an error
    finding of the task's ``on_transition`` rules blocks (``sldb.api.edges_blocked``), each
    carrying every finding."""
    from sldb.api import edges_blocked

    return _lifecycle_edges(node, edges_blocked(_store(root), ritual_export_id(node), payload, include_linked=False, document=document))


def transition_findings(root: Path, document: str, payload: dict[str, Any], *, snapshot: ReadSnapshot | None = None) -> list[dict[str, Any]]:
    """The findings of the task's ``on_transition`` rules read as ``payload`` (``sldb.api.transition_findings``).

    With a ``snapshot``, the store's rule graph is loaded once and shared by every task read of
    the pass (what ``sldb.api.transition_findings`` does on each call); a store without
    ``RuleDoc`` has no findings and loads nothing."""
    if snapshot is None:
        from sldb.api import transition_findings as sldb_transition_findings

        return [finding_dict(f) for f in sldb_transition_findings(_store(root), document, payload)]
    from sldb.api.rules.rule_graph import rule_graph
    from sldb.api.rules.rule_subjects import resolve_subject
    from sldb.api.rules.rules_on_transition import has_rules
    from sldb.api.rules.rules_on_transition import payload_findings

    if snapshot.has_rules is None:
        snapshot.has_rules = has_rules(_store(root))
    if not snapshot.has_rules:
        return []
    if snapshot.rule_graph is None:
        # The same graph sldb's transition_findings builds: its own index unless the rules
        # may read a linked store (``rule_graph(store, None)``).
        snapshot.rule_graph = rule_graph(_store(root), None)
    graph = snapshot.rule_graph
    return [finding_dict(f) for f in payload_findings(graph, "on_transition", resolve_subject(graph, document), payload)]


def task_document(root: Path, task_path: Path) -> str | None:
    """The ``Model:name`` the desk's store tracks ``task_path`` under (the subject of its rules);
    None for an untracked task or a desk without a store, where no rule runs.

    Reads the store indexes deskops already keeps for the pass (``doc_access.index_entries``)
    instead of opening the store once more for every task.
    """
    from deskops import doc_access

    if not (_store(root) / "core").exists():
        return None
    try:
        entry = doc_access.index_entry(root, task_path)
    except Exception:
        return None
    if entry is None or not entry.model or not entry.name:
        return None
    return f"{entry.model}:{entry.name}"


def lifecycle_transitions(root: Path, spec: LifecycleSpec | None = None) -> list[Transition]:
    """Every transition of the desk's lifecycle graph, ritual by ritual; empty without a store."""
    if not (_store(root) / "core").exists():
        return []
    spec = spec or load_lifecycle_spec()
    return [t for node in spec.rituals for t in transitions_from(root, node)]


def advance(
    root: Path,
    payload: dict[str, Any],
    model: type[Any],
    spec: LifecycleSpec | None = None,
    document: str | None = None,
    *,
    back_reason: str | None = None,
) -> TransitionResult:
    """Take the first transition out of the task's current node whose condition holds.

    The edge's effects are applied with ``sldb.api.apply_effects`` (``sets`` replaces the
    payload's top-level keys; the result validates against ``model``, the task type's model)
    and, when the edge is ``terminal``, ``current_node`` becomes ``complete``; the relation type
    is appended to ``history``. Mutates ``payload`` and reports what happened; one call takes
    at most one transition. The graph has one edge leaving each ritual, so the order sldb
    returns the holding edges in decides nothing (k4).

    With ``document`` (``task_document``) the task's ``on_transition`` rules run: when an error
    finding holds the edges back, the message lists each finding (rule, clause, node and value
    seen) instead of the edges' conditions.

    With ``back_reason`` the task takes the manual transition leaving its node instead (the
    return from testing to execution); the history entry is ``<relation_type>: <reason>``.
    """
    from sldb.api import apply_effects

    spec = spec or load_lifecycle_spec()
    node = str(payload.get("current_node") or spec.entry_node)
    status = str(payload.get("status") or "")
    if node == COMPLETE:
        return TransitionResult(COMPLETE, status, False, False, "Task already complete.")
    if not (_store(root) / "core").exists():
        raise LifecycleGraphMissing(
            f"No sldb store at {_store(root)}: run 'deskops init' (or 'deskops desk update --apply' on an "
            "existing store) to create the lifecycle graph that 'deskops advance' reads."
        )
    if back_reason is not None:
        manual = transitions_from(root, node, manual=True)
        if not manual:
            return TransitionResult(node, status, False, True, f"no hay transicion de vuelta desde {node}")
        transition = manual[0]
        target = COMPLETE if transition.terminal else transition.target
        _check_against_package(payload, transition, target)
        transition.hooks
        history = [str(item) for item in payload.get("history") or []]
        sets = {**transition.sets, "history": [*history, f"{transition.relation_type}: {back_reason}"], "current_node": target}
        payload.update(apply_effects(payload, {**transition.effects, "sets": sets}, model))
        return TransitionResult(target, str(payload.get("status") or ""), True, False, f"Returned to {target} via {transition.relation_type}.", transition)
    transitions = transitions_from(root, node)
    if not transitions:
        raise LifecycleGraphMissing(
            f"No lifecycle transition leaves '{node}' in the graph of {_store(root)}. "
            "Run 'deskops desk update --apply' to write the lifecycle graph."
        )
    holding = transitions_holding(root, node, payload, document)
    if not holding:
        payload["current_node"] = node
        blocked = transitions_blocked(root, node, payload, document) if document else []
        findings = [f for t in blocked for f in t.findings if f["level"] == "error"]
        if findings:
            lines = "; ".join(finding_line(f) for f in findings)
            return TransitionResult(node, status, False, True, f"Gate {node} is blocked by its rules: {lines}")
        gates = "; ".join(f"{t.relation_type}: {t.condition}" for t in transitions)
        return TransitionResult(node, status, False, True, f"Gate {node} is not complete ({gates}).")
    transition = holding[0]
    target = COMPLETE if transition.terminal else transition.target
    _check_against_package(payload, transition, target)
    transition.hooks  # a malformed hook entry fails here, before the payload changes
    # The model validates the whole new state (TaskDoc's lifecycle coherence): the edge's
    # ``sets``, the history it appends to and the node it leads to are applied together.
    history = [str(item) for item in payload.get("history") or []]
    sets = {**transition.sets, "history": [*history, transition.relation_type], "current_node": target}
    payload.update(apply_effects(payload, {**transition.effects, "sets": sets}, model))
    verb = "Completed" if transition.terminal else "Advanced to"
    return TransitionResult(target, str(payload.get("status") or ""), True, False, f"{verb} {target} via {transition.relation_type}.", transition)


UPDATE_SEEDS = "deskops desk update --apply"


def _check_against_package(payload: dict[str, Any], transition: Transition, target: str) -> None:
    """Refuse an edge whose effect differs from the package's lifecycle table (b6).

    The ``TaskDoc`` validator checks the new state against ``lifecycle_table()``, the package's
    edges; the desk's edge is what ``advance`` applies. When the two differ (a desk seed older
    than CC31 has no ``attributes.sets``), the write would fail inside pydantic without naming
    the edge, so the edge is compared first: same ``relation_type``, same target, same
    ``sets.status``. The table is cached; no file is read here.
    """
    from deskops.models.task_lifecycle import lifecycle_table

    task_id = str(payload.get("id") or "")
    edge_file = f"{LIFECYCLE_DIR.as_posix()}/{transition.relation_doc or transition.relation_type}.md"
    head = f"Cannot advance {task_id} via {transition.relation_type}: the edge {edge_file}"
    tail = f" The desk's lifecycle seeds are out of date: run '{UPDATE_SEEDS}'."
    expected = lifecycle_table().edges.get(transition.relation_type)
    if expected is None:
        raise LifecycleSeedOutOfDate(f"{head} is not a transition of the deskops package lifecycle.{tail}")
    seen = transition.sets.get("status")
    if str(seen or "") != expected.status:
        shown = "missing" if seen in (None, "") else str(seen)
        raise LifecycleSeedOutOfDate(
            f"{head} does not set status {expected.status} (attributes.sets.status is {shown}).{tail}"
        )
    if target != expected.target:
        raise LifecycleSeedOutOfDate(f"{head} does not lead to {expected.target} (it leads to {target}).{tail}")


# ---------------------------------------------------------------- writing the graph
def seed_changes(root: Path, result: Any) -> list[str]:
    """What a desk scaffold did to the lifecycle graph: ``wrote <path>`` and ``rewrote <path>`` lines."""
    root = root.resolve()
    prefix = LIFECYCLE_DIR.as_posix() + "/"
    created = [path.resolve().relative_to(root).as_posix() for path in result.created_paths]
    rewritten = [path.resolve().relative_to(root).as_posix() for path in result.rewritten_paths]
    return [f"wrote {rel}" for rel in created if rel.startswith(prefix)] + [f"rewrote {rel}" for rel in rewritten]


def _ritual_paths(spec: LifecycleSpec) -> dict[str, str]:
    return {f"desk/rituals/{node.removeprefix('ritual-')}.md": node for node in spec.rituals}


def tracked_line(model: str, path: str, spec: LifecycleSpec | None = None) -> str | None:
    """The change line for a lifecycle document the declared includes tracked; None for any other."""
    if path.startswith(LIFECYCLE_DIR.as_posix() + "/"):
        return f"tracked {path}"
    ritual = _ritual_paths(spec or load_lifecycle_spec()).get(path)
    if model == RITUAL_MODEL and ritual:
        return f"tracked {path} as {ritual_export_id(ritual)}"
    return None


def ensure_rule_model(root: Path) -> bool:
    """Register sldb's ``RuleDoc`` in the desk's store when it lacks it (``sldb.api.add_model``);
    True when it was registered now. Tracking an activation rule needs the model, and each
    ``model <= <TypeDoc>`` of a rule's subject needs the type registered, which the deskops
    models always are."""
    from sldb.api import add_model
    from sldb.api import is_model_registered

    if is_model_registered(_store(root), RULE_MODEL):
        return False
    add_model(_store(root), RULE_MODEL_REF, pythonpath=package_pythonpath())
    return True


def write_lifecycle_graph(root: Path) -> list[str]:
    """Make the desk's store carry the lifecycle graph; return what was written or tracked.

    Idempotent: writes the managed lifecycle seeds (the graph and the activation rules) and
    restores one the desk changed (``workspace.seed_desk``), registers sldb's relation models
    and ``RuleDoc`` when the store lacks them and tracks the declared desk documents
    (``workspace.apply_desk_includes``): the lifecycle documents and the lifecycle rituals by
    their ids. Any other declared document pending is tracked too and reported in the same way.
    """
    from sldb.api import init_relations
    from sldb.api import is_model_registered

    from deskops.workspace import apply_desk_includes
    from deskops.workspace import pending_desk_includes
    from deskops.workspace import seed_desk

    root = root.resolve()
    changes = seed_changes(root, seed_desk(root, restore_managed=True))
    if not all(is_model_registered(_store(root), name) for name in (RELATION_MODEL, RELATION_TYPE_MODEL)):
        init_relations(_store(root), pythonpath=package_pythonpath())
    ensure_rule_model(root)
    spec = load_lifecycle_spec()
    pending = {path: model for model, path in pending_desk_includes(root)}
    for path in apply_desk_includes(root):
        model = pending.get(path, "")
        changes.append(tracked_line(model, path, spec) or f"tracked {path} as {model}")
    return changes


# Alias de compatibilidad hacia atrás
ensure_lifecycle_graph = write_lifecycle_graph

FILE:tests/test_atom_reference_convention.py
from __future__ import annotations

from pathlib import Path

from deskops.atom_references import ALLOWED_ROLES
from deskops.atom_references import CANONICAL_FIELD
from deskops.atom_references import DEFAULT_ROLE
from deskops.atom_references import LEGACY_FIELD_VIOLATION
from deskops.atom_references import parse_atom_reference
from deskops.graph.checks import find_atom_reference_violations


def test_valid_roles_pass(tmp_path: Path) -> None:
    roles = "".join(f"  - {{id: atom-{role}, role: {role}}}\n" for role in ALLOWED_ROLES)
    write(
        tmp_path / "docs/guide.md",
        f"""---
{CANONICAL_FIELD}:
{roles}  - atom-bare
---
# Guide
""",
    )

    assert find_atom_reference_violations(tmp_path) == []


def test_unknown_role_produces_one_finding(tmp_path: Path) -> None:
    write(
        tmp_path / "docs/guide.md",
        """---
atoms:
  - id: atom-known
    role: documents
  - id: atom-unknown
    role: explains
---
# Guide
""",
    )

    findings = find_atom_reference_violations(tmp_path)

    assert [finding.to_dict() for finding in findings] == [
        {
            "kind": "invalid_atom_reference_role",
            "path": "docs/guide.md",
            "locator": "frontmatter:atoms[1]",
            "reason": "atom atom-unknown declares invalid role 'explains'; allowed roles: references, documents, specifies, constrains, validates",
            "atom_id": "atom-unknown",
            "role": "explains",
            "field_name": "atoms",
        }
    ]


def test_related_atoms_produces_one_legacy_finding(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/atoms/atom-source.md",
        """---
id: atom-source
related_atoms:
  - atom-first
  - atom-second
---
# Source
""",
    )

    findings = find_atom_reference_violations(tmp_path)

    assert [finding.to_dict() for finding in findings] == [
        {
            "kind": LEGACY_FIELD_VIOLATION,
            "path": "desk/atoms/atom-source.md",
            "locator": "frontmatter:related_atoms",
            "reason": "uses legacy atom reference field related_atoms; declare atom references in atoms",
            "field_name": "related_atoms",
        }
    ]


def test_bare_string_maps_to_references() -> None:
    parsed = parse_atom_reference("atom-bare")

    assert parsed is not None
    assert parsed.as_tuple() == ("atom-bare", DEFAULT_ROLE, CANONICAL_FIELD)
    assert parsed.violation is None


def test_mapping_without_role_maps_to_references() -> None:
    parsed = parse_atom_reference({"id": "atom-bare"})

    assert parsed is not None
    assert parsed.as_tuple() == ("atom-bare", DEFAULT_ROLE, CANONICAL_FIELD)
    assert parsed.violation is None


def test_fenced_yaml_examples_are_not_scanned(tmp_path: Path) -> None:
    write(
        tmp_path / "docs/guide.md",
        """---
title: Guide
---
# Guide

```yaml
atoms:
  - id: atom-example
    role: explains
related_atoms:
  - atom-example
```
""",
    )

    assert find_atom_reference_violations(tmp_path) == []


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

FILE:instruccion
Cold-bundle de la tarea task-borrar-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph-que-no: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rnE 'LEGACY_FIELDS|LEGACY_FIELD_VIOLATION|scaffold_desk|ensure_lifecycle_graph' deskops tests
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_reference_convention.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_checks.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea


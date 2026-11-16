FILE:desk/tasks/task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y.md
---
sldb:
  by: agent
  at: '2026-11-16T06:16:26Z'
  authority: generated
  via: save_document_payload
id: task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-012942-suggestion-project-graph-de-deskops-sldb-ya-ofrece-closed-como-predicado-y-declared-file-targets-desv-os-h1-h2-de-cc33c.md
depends_on: []
pills: []
files:
- deskops/graph/desk_graph.py
- deskops/graph/checks.py
- tests/test_graph_checks.py
- tests/test_graph_declared_edges.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-knowledge-graph-connects-desk-and-source-files
---

# deskops declara su project_graph con closed y declared_file_targets de sldb y borra los desvios H1 y H2 de CC33c

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de sldb del 2026-11-16 (triaje de su drawer). Desde GD21 (a2a0174f) sldb ofrece dos capacidades que deskops emula con codigo propio desde CC33c: H2, la superficie de documentos de project_graph acepta closed: como predicado del lenguaje de reglas (sldb src/sldb/api/edges/project_graph/document_surface.py:25, evaluado en project_texts.py:41-48; config_to_mapping rechaza un callable y apunta a closed:, project_graph_config_mapping.py:18 y 32-33); H1, declared_file_targets convierte en nodos los archivos existentes que no son documento (project_graph_config.py:38, declared_file_targets.py, declared_target_nodes.py; test tests/api/test_project_graph.py:60). deskops todavia usa declared_target_is_a_file (deskops/graph/checks.py:63) y closed_document=_closed_issue (deskops/graph/desk_graph.py:204).

## Goal

_Describe the concrete result this task must produce._

La configuracion de project_graph que deskops arma en deskops/graph/desk_graph.py usa closed: (predicado del lenguaje de reglas de sldb, con la misma condicion que hoy evalua _closed_issue) en lugar de closed_document=_closed_issue, y declara declared_file_targets para los archivos existentes que no son documento; declared_target_is_a_file y _closed_issue desaparecen. `deskops graph missing --root .` da el mismo resultado que antes del cambio en el desk de deskops (misma lista de faltantes). Si algun destino que hoy cubre declared_target_is_a_file (p. ej. dag.yaml o tests/fixtures/model_contract_hashes.json) no se puede declarar con declared_file_targets porque no sale de un campo de frontmatter de un glob de documentos, se manda deskops message send --to sldb con el caso y ese destino conserva su tratamiento actual.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/graph/desk_graph.py, deskops/graph/checks.py y sus tests (tests/test_graph_checks.py, tests/test_graph_declared_edges.py). Antes de cambiar, guardar la salida de deskops graph missing --root . en runs/subagents/<run>/graph-missing-antes.txt para comparar. No entra: cambiar sldb, declarar project_graph en .sldb/store.yaml a mano (la config se arma en codigo como hoy). Precisiones del preflight 1: la condicion de _closed_issue se lee en desk_graph.py y se traduce a la sintaxis closed: que documenta sldb (docs/architecture del repo sldb y tests/api/test_project_graph.py). DeclaredFileTargets de sldb exige directory y field: se declara uno por cada carpeta del desk cuyos documentos nombran archivos en un campo de frontmatter (al menos desk/materializations con field target_identity). Un destino es no declarable si no sale de un campo de frontmatter de documentos de una carpeta (p. ej. dag.yaml, tests/fixtures/model_contract_hashes.json): para esos se manda la nota a sldb con la ruta y quien la referencia, y conservan el tratamiento actual. La corrida se llama runs/subagents/project-graph-<AAAAMMDD>/. La comparacion de graph missing es por conjunto de lineas (orden indistinto).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer los archivos de sldb citados y desk_graph.py:180-215, checks.py:55-90. 2) Traducir _closed_issue a una condicion closed:. 3) Armar declared_file_targets. 4) Borrar el codigo viejo. 5) Comparar graph missing antes y despues (diff vacio). 6) Tests.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_checks.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_declared_edges.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (mismo conjunto de lineas que graph-missing-antes.txt)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rn 'declared_target_is_a_file\|_closed_issue' deskops
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas = cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El grep queda vacio, graph missing da la misma salida que antes y los tests pasan (o hay nota a sldb por un destino no declarable).

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

FILE:desk/atoms/knowledge-model/atom-knowledge-graph-connects-desk-and-source-files.md
---
id: atom-knowledge-graph-connects-desk-and-source-files
title: Knowledge graph connects desk and source files
five_wh_one_plus: what
tags:
- system:deskops
- system:sldb
- topic:knowledge-graph
- topic:source-code
---

# Knowledge graph connects desk and source files

## Answer

The project knowledge graph should connect desk artifacts such as atoms, tasks, docs, specs, diagrams, issues, and rituals with source files such as modules, tests, CLI entrypoints, model definitions, fixtures, and configuration files.

FILE:deskops/graph/desk_graph.py
"""The desk's graph as configuration over sldb's project graph.

sldb (``sldb.api.edges.project_graph``) reads the nodes, the store's edge index and the
declarations; this module only says what a desk is made of: where its documents live, which
files are nodes, which fields and sections declare references, and which documents are history.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from sldb.api.edges.project_graph import DeclaredFileTargets
from sldb.api.edges.project_graph import DocumentNode
from sldb.api.edges.project_graph import DocumentSurface
from sldb.api.edges.project_graph import FileExclusions
from sldb.api.edges.project_graph import FileNode
from sldb.api.edges.project_graph import FileRule
from sldb.api.edges.project_graph import LineMentions
from sldb.api.edges.project_graph import MentionPattern
from sldb.api.edges.project_graph import MissingTargetKind
from sldb.api.edges.project_graph import ProjectGraph
from sldb.api.edges.project_graph import ProjectGraphConfig
from sldb.api.edges.project_graph import ProjectGraphExtraction
from sldb.api.edges.project_graph import ReferenceField
from sldb.api.edges.project_graph import SectionMentions
from sldb.api.edges.project_graph import extract_document_nodes
from sldb.api.edges.project_graph import extract_file_nodes

from deskops.atom_references import ALLOWED_ROLES
from deskops.atom_references import CANONICAL_FIELD
from deskops.atom_references import DEFAULT_ROLE
from deskops.atom_references import LEGACY_FIELDS
from deskops.atom_references import MATERIALIZATION_FIELD


DOC_NODE_EXTRACTOR = "desk_doc_nodes_v1"
SOURCE_FILE_NODE_EXTRACTOR = "desk_source_file_nodes_v1"
DECLARED_EDGE_EXTRACTOR = "desk_declared_edges_v1"

# Declared fields that record where a document came from. They link to the source while it
# exists; once it is deleted the provenance stays recorded as text and is not a reference.
PROVENANCE_FIELDS = ("from_drawer",)

_MD = (".md",)
SURFACES = (
    DocumentSurface(kind="atom", directory="desk/atoms", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="materialization", directory="desk/materializations", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="role", directory="desk/roles", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="runtime_profile", directory="desk/runtimes", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="run", directory="desk/runs", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="pill", directory="desk/contexts", pattern="*.md", identity="document_id"),
    DocumentSurface(kind="task", directory="desk/tasks", pattern="*.md", excluded_names=("Board.md",), identity="document_id"),
    DocumentSurface(kind="issue", directory="desk/drawer/issues", pattern="*.md", identity="document_id_or_slug"),
    DocumentSurface(kind="question", directory="desk/drawer/questions", pattern="*.md"),
    DocumentSurface(kind="task", directory="desk/drawer/tasks", pattern="*.md", excluded_names=("Board.md",), identity="document_id"),
    DocumentSurface(kind="feature", directory="desk/drawer/features", pattern="*.md"),
    DocumentSurface(kind="use_case", directory="desk/drawer/use-cases", pattern="*.md"),
    DocumentSurface(kind="stress_test", directory="desk/drawer/stress-tests", pattern="**/*.md"),
    DocumentSurface(kind="diagram", directory="docs/diagrams", pattern="**/*", suffixes=(".md", ".mmd")),
    DocumentSurface(kind="doc", directory="docs", pattern="**/*.md", excluded_parts=("diagrams",)),
    DocumentSurface(kind="doc", directory="", pattern="README.md"),
    DocumentSurface(kind="doc", directory="deskops/data", pattern="**/*.md"),
    DocumentSurface(kind="spec", directory="spec", pattern="**/*", suffixes=(".md", ".yaml", ".yml")),
    DocumentSurface(kind="board", directory="desk/tasks", pattern="Board.md", identity="document_id"),
    DocumentSurface(kind="drawer_board", directory="desk/drawer/tasks", pattern="Board.md"),
    DocumentSurface(kind="ritual", directory="desk/rituals", pattern="*.md", identity="document_id"),
    DocumentSurface(kind="step", directory="desk/steps", pattern="*.md", identity="document_id"),
)

_SPEC = (".md", ".yaml", ".yml")
_DATA = (".json", ".yaml", ".yml")
FILE_RULES = (
    FileRule(kind="spec", file_kind="spec", path_prefixes=("spec", "docs/architecture/spec2viz"), suffixes=_SPEC),
    FileRule(kind="test_file", file_kind="test", path_prefixes=("tests",), suffixes=(".py",)),
    FileRule(kind="config_file", file_kind="config", suffixes=(".cfg", ".ini", ".toml")),
    FileRule(kind="config_file", file_kind="config", suffixes=_DATA, hidden_name=True),
    FileRule(kind="config_file", file_kind="config", suffixes=_DATA, stem_keywords=("config", "namespace", "registry")),
    FileRule(kind="source_file", file_kind="source", path_prefixes=("desk", "deskops"), suffixes=(".py",)),
)

EXCLUSIONS = FileExclusions(
    directories=(".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tmp", ".venv", "__pycache__", "build", "dist", "node_modules", "tools", "venv"),
    path_prefixes=(".sldb/runtime", ".sldb/core/documents", ".sldb_cache", "tests/fixtures"),
    suffixes=(".pyc", ".pyo"),
    path_endings=(".graph.json", ".kgdb.json", ".snapshot.json"),
)

MATERIALIZATION_TARGETS = DeclaredFileTargets(
    directory="desk/materializations", field="target_identity", kind="source_file", file_kind="source",
    source_kind="declared_materialization_target",
)


def _atom_field(*path: str, index_owned: bool = False) -> ReferenceField:
    return ReferenceField(path=path, target_prefix="atom:", default_role=DEFAULT_ROLE, allowed_roles=ALLOWED_ROLES, index_owned=index_owned)


def _target_field(*path: str) -> ReferenceField:
    return ReferenceField(path=path, default_role=DEFAULT_ROLE, scalar_only=True)


REFERENCE_FIELDS = (
    *(_atom_field(field, index_owned=True) for field in (CANONICAL_FIELD, MATERIALIZATION_FIELD, *LEGACY_FIELDS)),
    _atom_field("materialization", "source_atoms"),
    _target_field("materialization", "target_identity"),
    _target_field("target_identity"),
)

# A slug like `atom-pills-carry-transitional-task-knowledge` contains `task-knowledge`, which is
# part of an atom name, not a task reference; a real reference starts at a non-word, non-hyphen.
TASK_OR_ISSUE = MentionPattern(regex=r"(?<![\w-])(?P<kind>task|issue)-[a-z0-9][a-z0-9-]*\b", target="{kind}:{0}")
ATOM = MentionPattern(regex=r"\batom-[a-z0-9][a-z0-9-]*\b", target="atom:{0}")
# The same atom named with its kind, `atom:atom-<slug>`, as a whole token: `xatom:atom-a`,
# `atom:atom-a.b` and `atom:atom-a/b` name nothing (the token is longer than the atom id).
ATOM_ID = MentionPattern(regex=r"(?<![\w:./-])atom:atom-[a-z0-9][a-z0-9-]*(?![\w:/-]|\.\w)", target="{0}")
# A bullet of the drawer Board names one drawer entry: `- `tasks/<id>.md``, `- `<id>``.
DRAWER_BULLET = MentionPattern(
    regex=r"(?<=^- `)(?:tasks/|issues/)?(?P<id>(?P<kind>task|issue)-[^`\s/]+?)(?:\.md)?(?=`)", target="{kind}:{id}",
)
SOURCE_PATH = MentionPattern(
    regex=r"(?<![\w/.-])(?P<path>(?:deskops|desk|tests|spec|docs)/[A-Za-z0-9_./-]+\.(?:py|yaml|yml|md|toml|json|mmd))(?![\w/.-])",
    target="{path}",
)
SECTION_MENTIONS = (
    SectionMentions(
        headings=("related atoms", "source atoms", "related tasks", "related issues", "related task", "related issue"),
        patterns=(ATOM_ID, ATOM, TASK_OR_ISSUE), role=DEFAULT_ROLE,
    ),
    SectionMentions(headings=("source", "sources", "diagram source", "diagram sources"), patterns=(SOURCE_PATH,), role=DEFAULT_ROLE, kinds=("diagram",)),
)
# Drawer tasks keep the extraction they had as `drawer_task` nodes: their lines are not scanned.
LINE_MENTIONS = (
    LineMentions(
        kinds=("task", "issue"), excluded_path_prefixes=("desk/drawer/tasks",), skipped_frontmatter_fields=PROVENANCE_FIELDS,
        patterns=(SOURCE_PATH,), role=DEFAULT_ROLE, locator="source-file-reference",
    ),
    # `atom:atom-<slug>` anywhere in a task or issue: what `atoms merge` rewrites in prose.
    LineMentions(
        kinds=("task", "issue"), excluded_path_prefixes=("desk/drawer/tasks",), skipped_frontmatter_fields=PROVENANCE_FIELDS,
        patterns=(ATOM_ID,), role=DEFAULT_ROLE, locator="atom-mention",
    ),
    LineMentions(kinds=("drawer_board",), patterns=(DRAWER_BULLET,), role=DEFAULT_ROLE, locator="drawer-bullet"),
)
MISSING_TARGET_KINDS = (
    MissingTargetKind(parts=("docs", "diagrams"), kind="diagram"),
    MissingTargetKind(parts=("docs",), kind="doc"),
    MissingTargetKind(parts=("tests",), kind="test_file"),
    MissingTargetKind(parts=("spec",), kind="spec"),
    MissingTargetKind(parts=(), one_of_first=("desk", "deskops"), ending=".py", kind="source_file"),
)


def _closed_issue(kind: str, text: str) -> bool:
    """A closed issue is history, like a ``record: true`` document."""
    if kind != "issue":
        return False
    from deskops.services.issues import issue_status

    return issue_status(text) == "closed"


def _model_classes() -> dict[str, Any]:
    from deskops import models

    return {name: value for name, value in vars(models).items() if isinstance(value, type)}


def _declared_fields(model: Any) -> tuple[str, ...]:
    return (*getattr(model, "__containment__", {}).keys(), *getattr(model, "__references__", []))


def _model_kind(model: Any) -> str | None:
    types = (getattr(model, "__semantics__", None) or {}).get("type") or []
    return types[-1] if types else None


def _fields_by_kind() -> dict[str, tuple[str, ...]]:
    """Model-declared reference fields per surface kind: the first model (in ``models.__all__``) of that type."""
    from deskops import models

    fields: dict[str, tuple[str, ...]] = {}
    for kind in {surface.kind for surface in SURFACES}:
        normalized = kind.removeprefix("drawer_")
        model = next((getattr(models, name) for name in models.__all__ if _model_kind(getattr(models, name)) == normalized), None)
        if model is not None:
            fields[kind] = _declared_fields(model)
    return fields


@lru_cache(maxsize=1)
def desk_graph_config() -> ProjectGraphConfig:
    """What a desk's graph is made of."""
    classes = _model_classes()
    kinds = {name: _model_kind(model) for name, model in classes.items()}
    return ProjectGraphConfig(
        document_extractor=DOC_NODE_EXTRACTOR, file_extractor=SOURCE_FILE_NODE_EXTRACTOR, edge_extractor=DECLARED_EDGE_EXTRACTOR,
        surfaces=SURFACES, file_rules=FILE_RULES, exclusions=EXCLUSIONS, declared_file_targets=(MATERIALIZATION_TARGETS,),
        reference_fields=REFERENCE_FIELDS, fields_by_kind=_fields_by_kind(),
        fields_by_model={name: _declared_fields(model) for name, model in classes.items()},
        kind_by_model={name: "materialization" if kind == "materialization_contract" else kind for name, kind in kinds.items() if kind},
        provenance_fields=PROVENANCE_FIELDS, section_mentions=SECTION_MENTIONS, line_mentions=LINE_MENTIONS,
        missing_target_kinds=MISSING_TARGET_KINDS, closed_document=_closed_issue,
    )


@lru_cache(maxsize=1)
def _desk_graph_config_without_runs() -> ProjectGraphConfig:
    """The graph configuration with ``runs/`` left out of the file walk.

    Run evidence is not a graph surface: no document surface or file rule reads it. The
    walk still visits every one of its files (tens of thousands in this desk) for nothing,
    so the closeout graph is built without it when no materialization declares a target
    there (``_declares_target_under`` then returns False and the full configuration is used).
    """
    base = desk_graph_config()
    exclusions = base.exclusions.model_copy(
        update={"path_prefixes": (*base.exclusions.path_prefixes, "runs")}
    )
    return base.model_copy(update={"exclusions": exclusions})


def _declares_target_under(root: Path, prefix: str) -> bool:
    """Whether a materialization declares ``target_identity`` under ``prefix``."""
    from sldb.api.edges.project_graph.frontmatter_mapping import frontmatter_mapping

    directory = root / MATERIALIZATION_TARGETS.directory
    if not directory.exists():
        return False
    for path in directory.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        target = str((frontmatter_mapping(text) or {}).get(MATERIALIZATION_TARGETS.field) or "").strip()
        normalized = target.removeprefix("./")
        if normalized == prefix or normalized.startswith(f"{prefix}/"):
            return True
    return False


def desk_graph(root: Path) -> ProjectGraph:
    """The desk's declared-edge graph, read source by source."""
    root = Path(root).resolve()
    config = desk_graph_config() if _declares_target_under(root, "runs") else _desk_graph_config_without_runs()
    return ProjectGraph(root, config)


def extract_doc_nodes(root: Path) -> list[DocumentNode]:
    """Every desk document as a node."""
    return extract_document_nodes(root, desk_graph_config())


def extract_source_file_nodes(root: Path) -> list[FileNode]:
    """Every source, test, config and spec file (and declared materialization target) as a node."""
    return extract_file_nodes(root, desk_graph_config())


def extract_declared_edges(root: Path) -> ProjectGraphExtraction:
    """Every declared edge of the desk and every declared target that does not resolve."""
    return desk_graph(root).extraction()

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
    a missing target although it is there. CC33c read ``graph`` from sldb's project graph (GD21)
    and found it still makes no node for them, so the exception stays: such a target is not
    missing when, without its ``kind:`` prefix, it names a file inside ``root``. An atom reference, a path that does not exist, and a
    path that leaves ``root`` (absolute, or through ``..``) are still reported.
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

FILE:tests/test_graph_checks.py
from __future__ import annotations

from pathlib import Path

from deskops.graph.checks import find_missing_graph_references
from deskops.graph.checks import find_missing_snapshot_targets
from deskops.graph.view import Edge
from deskops.graph.view import GraphView as GraphSnapshot
from deskops.graph.view import Node


def test_find_missing_snapshot_targets_reports_dangling_edge() -> None:
    snapshot = GraphSnapshot(
        nodes=[Node(id="task:source", kind="task", label="Source")],
        edges=[
            Edge(
                source="task:source",
                target="atom:missing",
                role="references",
                provenance_path="desk/tasks/source.md",
                provenance_locator="Related Atoms",
            )
        ],
    )

    findings = find_missing_snapshot_targets(snapshot)

    assert [finding.to_dict() for finding in findings] == [
        {
            "kind": "missing_edge_target",
            "source_id": "task:source",
            "target_id": "atom:missing",
            "reason": "edge target was not found among graph nodes",
            "role": "references",
            "provenance_path": "desk/tasks/source.md",
            "provenance_locator": "Related Atoms",
        }
    ]


def test_find_missing_snapshot_targets_accepts_clean_graph_fixture() -> None:
    snapshot = GraphSnapshot(
        nodes=[
            Node(id="task:source", kind="task", label="Source"),
            Node(id="atom:target", kind="atom", label="Target"),
        ],
        edges=[Edge(source="task:source", target="atom:target", role="references")],
    )

    assert find_missing_snapshot_targets(snapshot) == []


def test_find_missing_graph_references_reports_dangling_source_atom(tmp_path: Path) -> None:
    write(
        tmp_path / "docs/guide.md",
        """# Guide

```yaml
source_atoms:
  - atom-missing
```
""",
    )

    findings = find_missing_graph_references(tmp_path)

    assert [finding.to_dict() for finding in findings] == [
        {
            "kind": "dangling_source_atom_reference",
            "source_id": "doc:docs/guide.md",
            "target_id": "atom:atom-missing",
            "reason": "declared target was not found among extracted graph nodes",
            "provenance_path": "docs/guide.md",
            "provenance_locator": "line:3:yaml",
            "extractor": "desk_declared_edges_v1",
        }
    ]


def test_find_missing_graph_references_accepts_task_pill_references(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/tasks/task-template-docs.md",
        """---
id: task-template-docs
references:
- desk/contexts/pill-template-docs.md
---

# Template docs
""",
    )
    write(
        tmp_path / "desk/contexts/pill-template-docs.md",
        """# Template docs pill

ID: pill-template-docs
""",
    )

    assert find_missing_graph_references(tmp_path) == []


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

FILE:tests/test_graph_declared_edges.py
"""Declared model metadata is a graph input.

TaskDoc declares current_node, pills and atoms as references, and also its
references, depends_on and inherits_from. `from_drawer` is provenance, not a
declared reference. BoardDoc declares tasks, pills and rituals. Those
declarations only reach the snapshot as prose unless the declared fields are
read from the model, which is what these tests pin down.
"""

from __future__ import annotations

from pathlib import Path

from deskops.cli.main import main
from deskops.graph.checks import find_missing_graph_references
from deskops.graph.desk_graph import extract_declared_edges


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


TASK = """---
id: task-do-the-thing
status: active
current_node: ritual-execution
pills:
- desk/contexts/pill-guardrail.md
atoms:
- atom-do-the-thing
references:
- task-something-else
depends_on: []
inherits_from: []
from_drawer: desk/drawer/tasks/task-do-the-thing.md
---

# Do the thing
"""


def _build_desk(root: Path) -> None:
    write(root / "desk/tasks/task-do-the-thing.md", TASK)
    write(
        root / "desk/rituals/execution.md",
        "---\nid: ritual-execution\n---\n\n# Execution\n",
    )
    write(
        root / "desk/contexts/pill-guardrail.md",
        "---\nid: pill-guardrail\n---\n\n# Pill\n",
    )
    write(
        root / "desk/atoms/atom-do-the-thing.md",
        "---\nid: atom-do-the-thing\nfive_wh_one_plus: what\n---\n\n# Atom\n",
    )
    write(
        root / "desk/tasks/task-something-else.md",
        "---\nid: task-something-else\n---\n\n# Other\n",
    )
    write(
        root / "desk/tasks/Board.md",
        "---\nid: board-001\ntasks:\n- desk/tasks/task-do-the-thing.md\n---\n\n# Board\n",
    )


def test_declared_references_become_edges_with_the_field_as_role(tmp_path: Path) -> None:
    _build_desk(tmp_path)

    extraction = extract_declared_edges(tmp_path)
    task_edges = {
        (edge.role, edge.target_id)
        for edge in extraction.edges
        if edge.source_id == "task:task-do-the-thing"
    }

    assert ("current_node", "ritual:ritual-execution") in task_edges, "a task's lifecycle node is a ritual"
    assert ("pills", "pill:pill-guardrail") in task_edges
    assert ("atoms", "atom:atom-do-the-thing") in task_edges
    assert ("references", "task:task-something-else") in task_edges


def test_board_task_reference_resolves_to_the_task_node(tmp_path: Path) -> None:
    _build_desk(tmp_path)

    extraction = extract_declared_edges(tmp_path)

    assert any(
        edge.source_id == "board:board-001"
        and edge.role == "tasks"
        and edge.target_id == "task:task-do-the-thing"
        for edge in extraction.edges
    )


def test_a_declared_field_holding_prose_is_not_an_unresolved_reference(tmp_path: Path) -> None:
    """Ritual steps are instruction text; edge targets are workflow node names."""
    write(
        tmp_path / "desk/rituals/ritual-phase.md",
        "---\n"
        "id: ritual-phase\n"
        "steps:\n"
        "- Identify the ready dependency layer of tasks whose prerequisites are satisfied.\n"
        "- '1. Store the reformulation at `runs/subagents/<run-dir>/preflight.md`.'\n"
        "- '1. Run a gate: give one fresh subagent only the TaskDoc.'\n"
        "---\n\n# Phase\n",
    )
    write(
        tmp_path / "desk/primitives/edges/edge-task-x-close-to-complete.md",
        "---\n"
        "id: edge-task-x-close-to-complete\n"
        "source: task-x\n"
        "target: complete\n"
        "---\n\n# Edge\n",
    )

    extraction = extract_declared_edges(tmp_path)

    assert extraction.missing_targets == []
    assert all(
        "prerequisites" not in edge.target_id for edge in extraction.edges
    )
    assert not any(
        edge.source_id == "ritual:ritual-phase" and edge.role == "steps"
        for edge in extraction.edges
    ), "Ritual steps are prose, not StepDoc containment"


def test_from_drawer_is_provenance_not_a_declared_reference(tmp_path: Path) -> None:
    _build_desk(tmp_path)
    write(tmp_path / "desk/drawer/tasks/task-do-the-thing.md", "---\nid: task-do-the-thing\n---\n\n# Drawer\n")

    present = extract_declared_edges(tmp_path)
    assert not any(
        edge.source_id == "task:task-do-the-thing" and edge.role == "from_drawer"
        for edge in present.edges
    ), "from_drawer is provenance and contributes no declared edge"

    (tmp_path / "desk/drawer/tasks/task-do-the-thing.md").unlink()

    deleted = extract_declared_edges(tmp_path)
    assert [m for m in deleted.missing_targets if "drawer" in m.target_id] == []


LIVE_ISSUE = """# Live issue

## Kind

bug

This issue names `deskops/missing.py`.
"""


def test_live_issue_with_a_dangling_path_still_fails(tmp_path: Path, capsys) -> None:
    write(tmp_path / "desk/drawer/issues/issue-live.md", LIVE_ISSUE)

    findings = find_missing_graph_references(tmp_path)

    assert [(finding.target_id, finding.record) for finding in findings] == [
        ("source_file:deskops/missing.py", None)
    ]
    result = main(["graph", "missing", "--root", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 1
    assert "Missing graph references:" in captured.out
    assert "1 missing, 0 informational" in captured.out


def test_record_issue_with_the_same_dangling_path_is_informational(tmp_path: Path, capsys) -> None:
    write(
        tmp_path / "desk/drawer/issues/issue-archived.md",
        "---\nrecord: true\n---\n\n" + LIVE_ISSUE,
    )

    findings = find_missing_graph_references(tmp_path)

    assert [(finding.target_id, finding.record) for finding in findings] == [
        ("source_file:deskops/missing.py", True)
    ]
    result = main(["graph", "missing", "--root", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 0
    assert "Informational (archived records):" in captured.out
    assert "0 missing, 1 informational" in captured.out

FILE:instruccion
Cold-bundle de la tarea task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_checks.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_declared_edges.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (mismo conjunto de lineas que graph-missing-antes.txt)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rn 'declared_target_is_a_file\|_closed_issue' deskops
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas = cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea


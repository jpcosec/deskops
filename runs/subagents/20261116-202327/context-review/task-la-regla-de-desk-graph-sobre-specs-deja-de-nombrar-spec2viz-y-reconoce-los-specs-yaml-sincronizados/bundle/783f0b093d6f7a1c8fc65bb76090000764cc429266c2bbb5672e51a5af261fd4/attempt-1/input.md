FILE:desk/tasks/task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados.md
---
sldb:
  by: agent
  at: '2026-11-16T20:07:00Z'
  authority: generated
  via: save_document_payload
id: task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados
status: draft
summary: La FileRule de specs de desk_graph.py reconoce docs/architecture en vez de
  docs/architecture/spec2viz (pedido IR13, decision de JP G7).
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-224757-suggestion-ir13-pide-migrar-las-habilidades-y-el-script-de-deskops-de-spec2viz-a-specir.md
depends_on: []
pills: []
files:
- deskops/graph/desk_graph.py
- tests/test_graph_extract_sources.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# La regla de desk_graph sobre specs deja de nombrar spec2viz y reconoce los specs YAML sincronizados con sldb notations sync

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15 (G7 aceptada y recomendación del coordinador aceptada): el YAML del spec queda subordinado al grafo y spec2viz se archiva cuando specir retirement check salga con 0; deskops/graph/desk_graph.py:75 es la última regla de deskops que espera a G7.

## Goal

_Describe the concrete result this task must produce._

La regla de desk_graph.py reconoce los specs YAML como artefactos de autoría que se sincronizan al store con sldb notations sync, sin nombrar ni depender de spec2viz.

## Scope

_State what is in scope and what is out of scope._

Entra: la FileRule de kind spec en deskops/graph/desk_graph.py (hoy path_prefixes=("spec", "docs/architecture/spec2viz")) y su test en tests/test_graph_extract_sources.py. La regla pasa a path_prefixes=("spec", "docs/architecture"): un YAML de spec en cualquier subdirectorio de docs/architecture es un nodo de file_kind spec, sin nombrar ninguna herramienta; los sufijos (_SPEC: .md, .yaml, .yml) y el orden de las FILE_RULES no cambian. Decision de JP 2026-11-15 (repo IR, documento fuente-de-verdad-del-diagrama de su carpeta de decisiones, punto 4): los specs YAML se quedan como formato de autoria, se validan con sldb y se sincronizan con sldb notations sync --spec; la ruta docs/architecture/spec2viz se renombra o generaliza por pedido al desk de deskops. Sale: las habilidades de agente y el script render_diagram.py del drawer (tarea aparte de IR13), el DocumentSurface de kind spec (directory spec) y cualquier deteccion semantica de si un YAML esta sincronizado con sldb (el reconocimiento es por ruta).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer FILE_RULES y la clasificacion de archivos en deskops/graph/desk_graph.py. 2) Cambiar el path_prefix docs/architecture/spec2viz por docs/architecture. 3) En tests/test_graph_extract_sources.py, sobre un desk sandbox (tmp_path) como los tests existentes de ese archivo: un YAML creado en un subdirectorio de docs/architecture del sandbox se extrae como nodo de kind spec con file_kind spec, y la asercion existente sobre el atom.yaml de la carpeta spec/artifacts sigue en verde. 4) Correr los tests de la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_extract_sources.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_missing_existing_files.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -n spec2viz deskops/graph/desk_graph.py (sin coincidencias, rc 1)

## Done When

_Name the observable condition that makes the task complete._

grep de spec2viz en deskops/graph/desk_graph.py no da coincidencias, un YAML bajo docs/architecture/ de un desk sandbox se extrae como nodo de file_kind spec y los tres archivos de test de la Validation pasan.

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

FILE:tests/test_graph_extract_sources.py
from __future__ import annotations

from pathlib import Path

from deskops.graph.desk_graph import extract_source_file_nodes


def test_extract_source_file_nodes_reads_file_level_source_surfaces(tmp_path: Path) -> None:
    write(tmp_path / "deskops/operations.py", "def run() -> None:\n    pass\n")
    write(tmp_path / "deskops/cli/commands/atoms.py", "def main() -> None:\n    pass\n")
    write(tmp_path / "tests/test_atom_materialization.py", "def test_atom() -> None:\n    pass\n")
    write(tmp_path / "pyproject.toml", "[project]\nname = \"deskops\"\n")
    write(tmp_path / "desk/atoms/tag-namespaces.yaml", "namespaces: []\n")
    write(tmp_path / "spec/artifacts/atom.yaml", "id: artifact.atom\n")
    write(tmp_path / "spec/contracts/source-node.md", "# Source Node Contract\n")
    write(tmp_path / "desk/tasks/006-extract-source-file-graph-nodes.md", "# Task doc\n")
    write(tmp_path / "docs/knowledge-graph/desk-source-graph-vocabulary.md", "# Vocabulary doc\n")

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    assert set(by_id) == {
        "config_file:desk/atoms/tag-namespaces.yaml",
        "config_file:pyproject.toml",
        "source_file:deskops/cli/commands/atoms.py",
        "source_file:deskops/operations.py",
        "spec:spec/artifacts/atom.yaml",
        "spec:spec/contracts/source-node.md",
        "test_file:tests/test_atom_materialization.py",
    }
    assert by_id["source_file:deskops/operations.py"].kind == "source_file"
    assert by_id["source_file:deskops/operations.py"].identity == "deskops/operations.py"
    assert by_id["source_file:deskops/operations.py"].path == "deskops/operations.py"
    assert by_id["source_file:deskops/operations.py"].file_kind == "source"
    assert by_id["test_file:tests/test_atom_materialization.py"].file_kind == "test"
    assert by_id["config_file:pyproject.toml"].file_kind == "config"
    assert by_id["spec:spec/artifacts/atom.yaml"].file_kind == "spec"
    assert by_id["config_file:desk/atoms/tag-namespaces.yaml"].provenance.model_dump() == {
        "path": "desk/atoms/tag-namespaces.yaml",
        "source_kind": "path_rule",
        "extractor": "desk_source_file_nodes_v1",
    }


def test_extract_source_file_nodes_excludes_generated_runtime_outputs_by_default(
    tmp_path: Path,
) -> None:
    write(tmp_path / "deskops/operations.py", "# source\n")
    write(tmp_path / "deskops/__pycache__/operations.cpython-313.pyc", "compiled\n")
    write(tmp_path / ".sldb/runtime/source-graph.json", "{}\n")
    write(tmp_path / "tests/fixtures/knowledge_graph/static_desk_source_graph.json", "{}\n")
    write(tmp_path / "runtime.snapshot.json", "{}\n")

    nodes = extract_source_file_nodes(tmp_path)

    assert [node.id for node in nodes] == ["source_file:deskops/operations.py"]


def test_extract_source_file_nodes_skips_vendored_tools_and_tmp_trees(tmp_path: Path) -> None:
    write(tmp_path / "deskops/operations.py", "# source\n")
    write(tmp_path / "tools/x/deskops/impl.py", "# vendored source\n")
    write(tmp_path / "tools/x/pyproject.toml", "[project]\nname = \"vendored\"\n")
    write(tmp_path / ".tmp/scratch/deskops/impl.py", "# scratch source\n")

    nodes = extract_source_file_nodes(tmp_path)

    assert [node.id for node in nodes] == ["source_file:deskops/operations.py"]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_materialization(path: Path, target_identity: str) -> None:
    """Write a minimal MaterializationContractDoc with the given target_identity."""
    write(
        path,
        f"""---
id: {path.stem}
title: Test Materialization
source_atoms:
- atom-test
target_kind: source_file
target_identity: {target_identity}
validation:
- pytest
tags: []
---

# Test Materialization

## Intent

Test materialization.
""",
    )


def test_declared_target_src_file_becomes_source_node(tmp_path: Path) -> None:
    """A declared target src/vsm/organs/links.py becomes a source_file node."""
    write(tmp_path / "src/vsm/organs/links.py", "# links\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-links.md",
        "src/vsm/organs/links.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    assert "source_file:src/vsm/organs/links.py" in by_id
    node = by_id["source_file:src/vsm/organs/links.py"]
    assert node.kind == "source_file"
    assert node.identity == "src/vsm/organs/links.py"
    assert node.path == "src/vsm/organs/links.py"
    assert node.file_kind == "source"
    assert node.provenance.source_kind == "declared_materialization_target"


def test_declared_target_github_workflow_becomes_source_node(tmp_path: Path) -> None:
    """A declared target .github/workflows/pulse.yml becomes a source_file node."""
    write(tmp_path / ".github/workflows/pulse.yml", "name: Pulse\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-pulse.md",
        ".github/workflows/pulse.yml",
    )

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    assert "source_file:.github/workflows/pulse.yml" in by_id
    node = by_id["source_file:.github/workflows/pulse.yml"]
    assert node.provenance.source_kind == "declared_materialization_target"


def test_declared_target_doc_surface_produces_no_source_node(tmp_path: Path) -> None:
    """A declared Markdown target under docs produces no source_file node."""
    write(tmp_path / "docs/guide.md", "# Guide\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-guide.md",
        "docs/guide.md",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    # No source_file node for the doc surface
    assert "source_file:docs/guide.md" not in ids


def test_declared_target_already_matched_by_path_rule_not_duplicated(tmp_path: Path) -> None:
    """A target already matched by a path rule is not duplicated."""
    write(tmp_path / "deskops/operations.py", "# operations\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-operations.md",
        "deskops/operations.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    # Should appear exactly once, from path_rule
    assert ids.count("source_file:deskops/operations.py") == 1
    node = next(n for n in nodes if n.id == "source_file:deskops/operations.py")
    assert node.provenance.source_kind == "path_rule"


def test_declared_target_leading_dotslash_is_stripped(tmp_path: Path) -> None:
    """A leading './' in target_identity is stripped."""
    write(tmp_path / "src/app.py", "# app\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-app.md",
        "./src/app.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    assert "source_file:src/app.py" in by_id


def test_declared_target_absolute_path_produces_no_node(tmp_path: Path) -> None:
    """An absolute path target produces no source_file node."""
    write(tmp_path / "src/app.py", "# app\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-absolute.md",
        "/etc/passwd",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    assert not any("passwd" in id_ for id_ in ids)


def test_declared_target_dotdot_path_produces_no_node(tmp_path: Path) -> None:
    """A path with '..' segments produces no source_file node."""
    write(tmp_path / "src/app.py", "# app\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-escape.md",
        "../outside/file.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    assert not any("outside" in id_ for id_ in ids)


def test_declared_target_kind_id_produces_no_node(tmp_path: Path) -> None:
    """A kind:id target produces no source_file node (handled by extract_edges)."""
    write(tmp_path / "src/app.py", "# app\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-kindid.md",
        "source_file:src/app.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    # No source_file node should be created from a kind:id target
    assert "source_file:source_file:src/app.py" not in ids


def test_declared_target_nonexistent_produces_no_node(tmp_path: Path) -> None:
    """A nonexistent target produces no source_file node."""
    write_materialization(
        tmp_path / "desk/materializations/materialization-missing.md",
        "src/missing.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    assert "source_file:src/missing.py" not in ids


def test_declared_target_excluded_tmp_produces_no_node(tmp_path: Path) -> None:
    """A target under .tmp/ produces no source_file node."""
    write(tmp_path / ".tmp/scratch.py", "# scratch\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-tmp.md",
        ".tmp/scratch.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    assert "source_file:.tmp/scratch.py" not in ids


def test_declared_target_excluded_tools_produces_no_node(tmp_path: Path) -> None:
    """A target under tools/ produces no source_file node."""
    write(tmp_path / "tools/helper.py", "# helper\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-tools.md",
        "tools/helper.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    assert "source_file:tools/helper.py" not in ids


def test_declared_target_dotslash_github_workflow_yields_correct_node(tmp_path: Path) -> None:
    """'./.github/workflows/pulse.yml' yields node 'source_file:.github/workflows/pulse.yml'.

    Regression test: lstrip("./") was incorrectly stripping every leading '.' and '/',
    so './.github' became 'github'. This verifies removeprefix("./") is used.
    """
    write(tmp_path / ".github/workflows/pulse.yml", "name: Pulse\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-dotslash-github.md",
        "./.github/workflows/pulse.yml",
    )

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    # Must include the leading dot in .github
    assert "source_file:.github/workflows/pulse.yml" in by_id
    # And NOT strip the dot incorrectly
    assert "source_file:github/workflows/pulse.yml" not in by_id

    node = by_id["source_file:.github/workflows/pulse.yml"]
    assert node.identity == ".github/workflows/pulse.yml"
    assert node.path == ".github/workflows/pulse.yml"
    assert node.provenance.path == ".github/workflows/pulse.yml"


def test_declared_target_symlink_yields_link_path_not_resolved_target(tmp_path: Path) -> None:
    """A symlink inside root declared as target yields a node for the link path.

    Regression test: the node path was computed from the symlink-resolved path,
    so 'link.py' pointing to 'real.py' would create a node for 'real.py' instead
    of 'link.py'. This verifies the declared normalized path is used.
    """
    # Create the real file
    write(tmp_path / "src/real.py", "# real implementation\n")
    # Create a symlink pointing to it
    link_path = tmp_path / "src/link.py"
    link_path.symlink_to(tmp_path / "src/real.py")

    # Declare the symlink as the materialization target
    write_materialization(
        tmp_path / "desk/materializations/materialization-link.md",
        "src/link.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    # Must create a node for the declared link path
    assert "source_file:src/link.py" in by_id
    node = by_id["source_file:src/link.py"]
    assert node.identity == "src/link.py"
    assert node.path == "src/link.py"
    assert node.provenance.path == "src/link.py"
    assert node.provenance.source_kind == "declared_materialization_target"

FILE:instruccion
Cold-bundle de la tarea task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_extract_sources.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_missing_existing_files.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -n spec2viz deskops/graph/desk_graph.py (sin coincidencias, rc 1)


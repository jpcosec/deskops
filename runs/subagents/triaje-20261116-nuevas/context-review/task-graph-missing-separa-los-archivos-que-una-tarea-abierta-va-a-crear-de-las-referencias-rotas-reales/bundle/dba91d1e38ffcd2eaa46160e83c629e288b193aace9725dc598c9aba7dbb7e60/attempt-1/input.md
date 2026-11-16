FILE:desk/tasks/task-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas-reales.md
---
sldb:
  by: agent
  at: '2026-11-16T06:11:09Z'
  authority: generated
  via: create_document
id: task-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas-reales
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-010912-unclear-graph-missing-no-distingue-archivos-que-la-tarea-va-a-crear-ya-borrados-o-de-otro-repo.md
depends_on: []
pills: []
files:
- deskops/graph/checks.py
- deskops/cli/commands/graph.py
- tests/test_graph_checks.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-knowledge-graph-connects-desk-and-source-files
---

# graph missing separa los archivos que una tarea abierta va a crear de las referencias rotas reales

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de deskops del 2026-11-16 (triaje). SOURCE_PATH (deskops/graph/desk_graph.py:122-125) convierte en arista toda mencion deskops|desk|tests|spec|docs/<ruta>.<ext> del texto de un TaskDoc, y graph missing la reporta como missing_declared_target si el archivo no existe. Hoy hay unos 30 faltantes asi en desk/tasks: archivos que la tarea va a crear (tests/test_ascii_ids.py, docs/configuration.md, deskops/graph/paths.py...), archivos citados como ya borrados (deskops/specs/loader.py) y rutas de otro repo (docs/spec/spec-procesos-modelables.md de Governance). graph missing da rc 0 igual. Reescribir las rutas para esquivar el detector falsea la evidencia, asi que quedan tal cual.

## Goal

_Describe the concrete result this task must produce._

Cuando el origen de un missing_declared_target es un TaskDoc abierto (status distinto de closed, superseded, cancelled o retired) y el destino es un source_file, test_file o doc inexistente, graph missing lo reporta como informational con el codigo planned_target, separado de la lista de faltantes; los mismos destinos desde documentos que no son tareas abiertas siguen como missing. La salida dice cuantos son de cada tipo.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/graph/checks.py (donde se arma la lista de missing y de informational; buscar MISSING_TARGET_KINDS y 'informational'), la salida de deskops graph missing en deskops/cli/commands/graph.py y tests/test_graph_checks.py. No entra: cambiar SOURCE_PATH ni el extractor, ni ocultar los planned_target (se siguen listando).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer checks.py y graph.py (comando missing). 2) Clasificar por estado del TaskDoc de origen. 3) Tests: tarea en draft que cita tests/test_nuevo.py da planned_target informational; un atomo que cita el mismo archivo da missing; una tarea cerrada (en history) no aplica porque ya no esta en desk/tasks.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_checks.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (los faltantes de tareas abiertas salen como planned_target informational)
- {'cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas': 'cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea'}

## Done When

_Name the observable condition that makes the task complete._

Los tres casos del paso 3 pasan y graph missing en el desk de deskops separa planned_target de missing.

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

FILE:deskops/cli/commands/graph.py
from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.errors import UsageError


class GraphCLI:
    def run(self, args: Any) -> int:
        if args.graph_command == "build":
            return self._build(args)
        if args.graph_command == "neighbors":
            return self._neighbors(args)
        if args.graph_command == "missing":
            return self._missing(args)
        if args.graph_command == "reflect":
            return self._reflect(args)
        raise UsageError(f"Unknown graph command: {args.graph_command}")

    def _build(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if not root.exists() or not root.is_dir():
            print(f"Error: graph root is not a directory: {root}")
            return 1

        from deskops.graph.export import GraphSnapshotCapabilityError
        from deskops.graph.export import networkx_path_for_snapshot
        from deskops.graph.export import write_graph_snapshot

        try:
            requested_output = Path(args.output) if args.output else None
            if requested_output is not None and not requested_output.is_absolute():
                requested_output = root / requested_output
            output_path = (
                write_graph_snapshot(root, requested_output)
                if requested_output is not None
                else write_graph_snapshot(root)
            )

            from sldb.api.graph.snapshot import snapshot_load
            from sldb.store.graph.graph_io import save_graph

            save_graph(snapshot_load(output_path), networkx_path_for_snapshot(output_path))

        except GraphSnapshotCapabilityError as exc:
            print(f"Error: {exc}")
            return 1

        print(f"Graph snapshot written: {output_path}")
        return 0

    def _neighbors(self, args: Any) -> int:
        root = Path(args.root).resolve()
        from deskops.graph.view import GraphReadError
        from deskops.graph.view import graph_neighbors
        from deskops.graph.view import graph_view

        graph_path = Path(args.graph).resolve() if args.graph else None
        try:
            neighbors = graph_neighbors(graph_view(root, graph_path), args.id)
        except GraphReadError as exc:
            print(f"Error: {exc}")
            return 1

        self._print_neighbors(args.id, neighbors)
        return 0

    def _missing(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if not root.exists() or not root.is_dir():
            print(f"Error: graph root is not a directory: {root}")
            return 1

        # Imported outside the try: a failing import must surface as itself,
        # not as an unbound name in the except clause.
        from deskops.graph.checks import GraphMissingCheckError
        from deskops.graph.checks import find_missing_graph_references

        graph_path = Path(args.graph).resolve() if args.graph else None
        try:
            findings = find_missing_graph_references(root, graph_path)
        except GraphMissingCheckError as exc:
            print(f"Error: {exc}")
            return 1

        if not findings:
            print("No missing graph references found.")
            return 0

        failing = [finding for finding in findings if not finding.record]
        informational = [finding for finding in findings if finding.record]

        if failing:
            print("Missing graph references:")
            for finding in failing:
                self._print_missing_finding(finding)
        if informational:
            print("Informational (archived records):")
            for finding in informational:
                self._print_missing_finding(finding)

        print(f"{len(failing)} missing, {len(informational)} informational")
        return 1 if failing else 0

    def _print_missing_finding(self, finding: Any) -> None:
        print(f"- {finding.kind}: {finding.source_id} -> {finding.target_id}")
        if finding.role:
            print(f"  role: {finding.role}")
        if finding.provenance_path:
            locator = f":{finding.provenance_locator}" if finding.provenance_locator else ""
            print(f"  provenance: {finding.provenance_path}{locator}")
        print(f"  reason: {finding.reason}")

    def _reflect(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if not root.exists() or not root.is_dir():
            print(f"Error: graph root is not a directory: {root}")
            return 1

        from deskops.graph.checks import GraphMissingCheckError
        from deskops.graph.self_reflection import build_self_reflection_report
        from deskops.graph.self_reflection import write_self_reflection_report
        from deskops.graph.view import GraphReadError
        from deskops.graph.view import graph_view

        graph_path = Path(args.graph).resolve() if args.graph else None
        try:
            report = build_self_reflection_report(graph_view(root, graph_path))
            output_path = write_self_reflection_report(root, report)
        except (GraphReadError, GraphMissingCheckError) as exc:
            print(f"Error: {exc}")
            return 1

        summary = report["summary"]
        print(f"Self-reflection report written: {output_path}")
        print(f"Findings: {summary['finding_count']}")
        print(f"Suppressed duplicates: {summary['suppressed_duplicate_count']}")
        return 0

    def _print_neighbors(self, node_id: str, neighbors: dict[str, Any]) -> None:
        nodes = neighbors["nodes"]
        node = neighbors["node"]
        print(f"Node: {node_id} ({_graph_node_label(node)})")
        print("Outgoing:")
        if neighbors["outgoing"]:
            for edge in neighbors["outgoing"]:
                target = nodes.get(edge["target"], {"id": edge["target"]})
                print(f"- {edge['role']} -> {edge['target']} ({_graph_node_label(target)})")
        else:
            print("- none")

        print("Incoming:")
        if neighbors["incoming"]:
            for edge in neighbors["incoming"]:
                source = nodes.get(edge["source"], {"id": edge["source"]})
                print(f"- {edge['source']} ({_graph_node_label(source)}) -> {edge['role']}")
        else:
            print("- none")


def _graph_node_label(node: dict[str, Any]) -> str:
    return str(node.get("label") or node.get("title") or node.get("id"))

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

FILE:instruccion
Cold-bundle de la tarea task-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas-reales: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_checks.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (los faltantes de tareas abiertas salen como planned_target informational)
- {'cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas': 'cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea'}


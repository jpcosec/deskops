FILE:desk/tasks/task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime.md
---
sldb:
  by: agent
  at: '2026-11-16T05:51:41Z'
  authority: generated
  via: save_document_payload
id: task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261104-233657-suggestion-sldb-el-store-pasa-a-sldb-versionado-y-sldb-cache-ignorada-journal-retirado.md
depends_on: []
pills:
- desk/contexts/pill-010-graph-runtime-output-policy.md
files:
- deskops/graph/export.py
- deskops/graph/self_reflection.py
- tests/test_graph_snapshot.py
- tests/test_graph_self_reflection.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# graph export y self_reflection escriben su salida derivada en .sldb_cache y no en .sldb/runtime

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de sldb (c420809c, 2026-11-04): el store es .sldb/ versionado y lo derivado vive en .sldb_cache/, ignorada. deskops todavia escribe salidas derivadas en la ruta vieja .sldb/runtime/, que ya no esta ignorada: deskops/graph/export.py:22 y deskops/graph/self_reflection.py:17-18 y 39.

## Goal

_Describe the concrete result this task must produce._

Las salidas de graph export y self_reflection van a .sldb_cache/ (DERIVED_ROOT = Path('.sldb_cache') en un modulo nuevo deskops/graph/paths.py; cada salida conserva la ruta relativa que hoy tiene bajo .sldb/runtime/). Ningun codigo de deskops/ ESCRIBE en .sldb/runtime/; las menciones que solo excluyen o leen esa ruta vieja (p. ej. EXCLUDED_SOURCE_PREFIXES) se conservan. La pill pill-010-graph-runtime-output-policy, que hoy dice que se prefiera .sldb/runtime/, quedo vieja con la decision de sldb c420809c: se actualiza con deskops edit pill para que diga .sldb_cache/ (ignorada por .gitignore). Consumidores: grep -rnF '.sldb/runtime' en /mnt/ssd/proyectos/SLDB_1 excluyendo runs/ y .git; si alguno fuera de deskops lee la ruta vieja, deskops message send --to <repo> con titulo 'deskops mueve sus salidas derivadas a .sldb_cache', las rutas viejas y nuevas y el hash del commit de esta tarea.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/graph/export.py, deskops/graph/self_reflection.py, sus tests (tests/test_graph_snapshot.py, tests/test_graph_self_reflection.py) y tests/test_gitignore_policy.py si hace falta. Consumidores a revisar con `grep -rn '.sldb/runtime' /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui --include=*.py --include=*.js` (excluyendo runs/); si hay, `deskops message send --to graph_ui`. No entra: migrar archivos viejos ya escritos (se borran a mano solo si no estan versionados), tocar sldb. Precisiones del preflight 1: la constante es DERIVED_ROOT = Path('.sldb_cache') en un modulo nuevo deskops/graph/paths.py, importada por export.py y self_reflection.py; cada salida conserva la ruta relativa que hoy tiene bajo .sldb/runtime/ pero bajo .sldb_cache/. tests/test_gitignore_policy.py se toca solo si afirma algo sobre .sldb/runtime. La busqueda es del literal '.sldb/runtime' (grep -rnF). Si hay consumidor en graph_ui, la nota dice: titulo 'deskops mueve sus salidas derivadas a .sldb_cache', cuerpo con las rutas viejas y nuevas y el hash. No se borra ningun archivo existente.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) `grep -rn 'sldb/runtime\|"runtime"' deskops/graph deskops/services`. 2) Cambiar las rutas a una constante comun que apunte a .sldb_cache. 3) Ajustar los tests. 4) Revisar consumidores en graph_ui.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_self_reflection.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_gitignore_policy.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -rnF '.sldb/runtime' deskops/ --include=*.py (solo menciones de exclusion o lectura, ninguna escritura)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Ningun codigo de deskops/ escribe en .sldb/runtime (el grep solo muestra menciones de exclusion o lectura); pill-010 dice .sldb_cache/; los tests listados pasan; consumidores avisados si los hubo.

FILE:desk/contexts/pill-010-graph-runtime-output-policy.md
---
# pill-xxx
id: pill-010
# e.g., language:python, library:pydantic
tags:
- system:deskops
- system:sldb
- pill-type:guardrail
- topic:runtime
- topic:drift-control
---

# Guardrail: generated graph output is runtime state

## What

_Define the context or guardrail this pill carries._

Generated graph snapshots and query indexes are runtime artifacts unless a task explicitly promotes a fixture or contract example into versioned test data.

## Why

_Explain why this context matters for safe execution._

Graph outputs can become large, noisy, and stale. Keeping generated outputs in runtime prevents the repository from confusing source knowledge with derived graph projections.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task writes deskops graph snapshot JSON, generated indexes, query results, or self-reflection reports.

## Where

_Name the files, surfaces, or scope this pill applies to._

Generated outputs should prefer `.sldb/runtime/` or another agreed ignored runtime location. Versioned fixtures belong under tests or contracts only when they prove behavior.

## How

_Describe the correct way to apply this guidance._

Separate source specs/adapters from generated graph outputs. Add or update ignore rules when a new runtime path is introduced. Keep small golden fixtures only for tests.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not commit full generated graph snapshots as documentation. Do not use generated graph output as the only source of relation truth.

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

FILE:deskops/graph/export.py
"""``deskops graph build``: sldb's project graph of the desk written as a KGDB GraphSnapshot file.

The graph is sldb's (``desk_graph``); this module only lays its nodes and edges out in the
KGDB node-link shape (``sldb.api.graph.snapshot.GraphSnapshot`` validates it) at the ignored
runtime path, for tools that read a graph file. The graph commands do not read it back.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from deskops.graph.desk_graph import DECLARED_EDGE_EXTRACTOR
from deskops.graph.desk_graph import DOC_NODE_EXTRACTOR
from deskops.graph.desk_graph import SOURCE_FILE_NODE_EXTRACTOR
from deskops.graph.desk_graph import desk_graph


SNAPSHOT_SCHEMA = "deskops_kgdb_graph_snapshot_v1"
SNAPSHOT_EXTRACTOR = "deskops_kgdb_snapshot_v1"
DEFAULT_SNAPSHOT_PATH = Path(".sldb/runtime/graphs/deskops.kg.json")


class GraphSnapshotCapabilityError(RuntimeError):
    """Raised when sldb graph snapshot validation support is unavailable."""


def networkx_path_for_snapshot(snapshot_path: Path) -> Path:
    """Return the sibling NetworkX path for a GraphSnapshot destination."""
    without_json = snapshot_path.with_suffix("")
    if without_json.suffix == ".kg":
        return without_json.with_suffix(".nx.json")
    return snapshot_path.with_suffix(".nx.json")


def build_graph_snapshot(root: Path) -> dict[str, Any]:
    """The desk's project graph as a KGDB GraphSnapshot payload: one node per id, its edges nested."""
    graph = desk_graph(root.resolve())
    nodes: dict[str, dict[str, Any]] = {}
    for node in (*graph.nodes.documents, *graph.nodes.files):
        item = node.to_dict()
        merged = nodes.setdefault(item["id"], {**item, "provenance": []})
        merged["provenance"].append(item["provenance"])
        for key, value in item.items():
            if key != "provenance" and value is not None:
                merged.setdefault(key, value)
    edges = graph.extraction().edges
    by_source: dict[str, list[dict[str, Any]]] = {}
    for edge in edges:
        by_source.setdefault(edge.source_id, []).append(
            {
                "target_id": edge.target_id,
                "relation_type": edge.role,
                "metadata": {
                    "role": edge.role, "source_kind": edge.source_kind, "confidence": edge.confidence,
                    "provenance_path": edge.provenance_path, "provenance_locator": edge.provenance_locator,
                    "extractor": edge.extractor,
                },
            }
        )
    snapshot_nodes = [
        {
            "identity": {"node_id": node_id, "node_type": node["kind"]},
            "edges": by_source.get(node_id, []),
            "semantics": {key: value for key, value in node.items() if key not in {"id", "kind", "provenance"} and value is not None},
            "source": {"extractor": SNAPSHOT_EXTRACTOR, "provenance": node["provenance"]},
        }
        for node_id, node in sorted(nodes.items())
    ]
    return {
        "version": "1.0",
        "nodes": snapshot_nodes,
        "metadata": {
            "schema": SNAPSHOT_SCHEMA,
            "extractor": SNAPSHOT_EXTRACTOR,
            "runtime_output_path": DEFAULT_SNAPSHOT_PATH.as_posix(),
            "source_extractors": [DOC_NODE_EXTRACTOR, SOURCE_FILE_NODE_EXTRACTOR, DECLARED_EDGE_EXTRACTOR],
            "node_count": len(snapshot_nodes),
            "edge_count": len(edges),
        },
    }


def write_graph_snapshot(root: Path, output_path: Path | None = None) -> Path:
    """Write the graph snapshot to the ignored runtime output path (or ``output_path``)."""
    destination = output_path or root / DEFAULT_SNAPSHOT_PATH
    snapshot = build_graph_snapshot(root)
    try:
        from sldb.api.graph.snapshot import GraphSnapshot
    except ImportError as exc:
        raise GraphSnapshotCapabilityError(
            "sldb graph API unavailable (sldb.api.graph.snapshot); upgrade structuredLanguageDB before running `deskops graph build`."
        ) from exc
    GraphSnapshot.model_validate(snapshot)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return destination

FILE:deskops/graph/self_reflection.py
from __future__ import annotations

import json
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from deskops.graph.checks import GraphMissingFinding
from deskops.graph.checks import find_missing_snapshot_targets
from deskops.graph.view import GraphView
from deskops.graph.view import Node


REPORT_SCHEMA = "deskops_self_reflection_report_v2"
DECISIONS_SCHEMA = "deskops_self_reflection_decisions_v1"
DEFAULT_REPORT_PATH = Path(".sldb/runtime/self_reflection_findings.json")
DEFAULT_DECISIONS_PATH = Path(".sldb/runtime/self_reflection_decisions.json")

ATOM_REFERENCE_ROLES = {"references", "documents", "specifies", "constrains", "validates"}
SOURCE_LINK_ROLES = {
    "references",
    "documents",
    "specifies",
    "constrains",
    "supports",
    "uses",
    "materializes",
    "implements",
    "validates",
    "tests",
    "violates",
    "invokes",
    "defines",
    "routes",
    "configures",
}
EXCLUDED_SOURCE_PREFIXES = (
    ".sldb/runtime/",
    "tests/fixtures/",
)
EXCLUDED_SOURCE_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}
EXCLUDED_SOURCE_SUFFIXES = (
    ".graph.json",
    ".kgdb.json",
    ".snapshot.json",
)


@dataclass(frozen=True)
class SelfReflectionFinding:
    question_id: str
    kind: str
    source_id: str
    target_id: str | None
    role: str | None
    provenance_path: str
    provenance_locator: str
    confidence: str
    reason: str
    later_action: str
    dedupe_key: str
    promotion_targets: list[str]
    duplicate_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_self_reflection_report(
    snapshot: GraphView,
    missing_findings: list[GraphMissingFinding] | None = None,
) -> dict[str, Any]:
    """Return review-only self-reflection findings for a graph (sldb's project graph, or a ``--graph`` file)."""
    findings = [
        *_missing_atom_reference_findings(snapshot, missing_findings or []),
        *_dangling_generated_artifact_findings(snapshot, missing_findings or []),
        *_unlinked_source_file_findings(snapshot),
    ]
    grouped_findings = _group_duplicate_findings(findings)
    return {
        "schema": REPORT_SCHEMA,
        "runtime_only": True,
        "mutation_policy": "review_only_no_source_artifact_mutation",
        "review_loop": {
            "decision_storage": {
                "schema": DECISIONS_SCHEMA,
                "runtime_output_path": DEFAULT_DECISIONS_PATH.as_posix(),
                "allowed_statuses": ["pending", "accepted", "rejected"],
            },
            "promotion_paths": {
                "task": "accepted finding -> create or promote a desk task when remediation work is clear",
                "question": "accepted finding -> route a desk question when owner intent or source of truth is unclear",
                "atom": "accepted finding -> update or create an atom when the durable knowledge gap is understood",
            },
        },
        "summary": {
            "finding_count": len(grouped_findings),
            "suppressed_duplicate_count": sum(finding.duplicate_count for finding in grouped_findings),
        },
        "findings": [finding.to_dict() for finding in grouped_findings],
    }


def write_self_reflection_report(
    root: Path,
    report: dict[str, Any],
    output_path: Path | None = None,
) -> Path:
    """Write a generated report to runtime storage, not to desk source artifacts."""
    destination = output_path or root / DEFAULT_REPORT_PATH
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_self_reflection_decisions_store(root, report_path=destination)
    return destination


def write_self_reflection_decisions_store(
    root: Path,
    report_path: Path,
    output_path: Path | None = None,
) -> Path:
    """Persist the review-loop decision ledger alongside the generated findings report."""
    destination = output_path or root / DEFAULT_DECISIONS_PATH
    payload = _read_existing_decisions(destination)
    payload.update(
        {
            "schema": DECISIONS_SCHEMA,
            "runtime_only": True,
            "report_path": report_path.relative_to(root).as_posix() if report_path.is_absolute() else report_path.as_posix(),
            "allowed_statuses": ["pending", "accepted", "rejected"],
        }
    )
    payload.setdefault("decisions", [])
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return destination


def _read_existing_decisions(path: Path) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {}
    loaded = json.loads(path.read_text(encoding="utf-8"))
    return loaded if isinstance(loaded, dict) else {}


def _missing_atom_reference_findings(
    snapshot: GraphView,
    missing_findings: list[GraphMissingFinding],
) -> list[SelfReflectionFinding]:
    findings = [_missing_atom_finding_from_snapshot(edge) for edge in _missing_atom_edges(snapshot)]
    findings.extend(
        _missing_atom_finding_from_check(finding)
        for finding in missing_findings
        if finding.kind == "dangling_source_atom_reference" and finding.target_id.startswith("atom:")
    )
    return findings


def _missing_atom_edges(snapshot: GraphView) -> list[dict[str, str]]:
    return [
        edge
        for edge in _snapshot_missing_targets(snapshot)
        if edge.target_id.startswith("atom:") and (edge.role or "") in ATOM_REFERENCE_ROLES
        for edge in [_missing_finding_to_edge(edge)]
    ]


def _snapshot_missing_targets(snapshot: GraphView) -> list[GraphMissingFinding]:
    return find_missing_snapshot_targets(snapshot)


def _missing_finding_to_edge(finding: GraphMissingFinding) -> dict[str, str]:
    return {
        "source_id": finding.source_id,
        "target_id": finding.target_id,
        "role": finding.role or "references",
        "provenance_path": finding.provenance_path or _path_from_node_id(finding.source_id),
        "provenance_locator": finding.provenance_locator or f"edge:{finding.source_id}:{finding.target_id}",
    }


def _missing_atom_finding_from_snapshot(edge: dict[str, str]) -> SelfReflectionFinding:
    return SelfReflectionFinding(
        question_id="missing-atom-references",
        kind="dangling_source_atom_reference",
        source_id=edge["source_id"],
        target_id=edge["target_id"],
        role=edge.get("role"),
        provenance_path=edge["provenance_path"],
        provenance_locator=edge["provenance_locator"],
        confidence="high",
        reason="declared atom reference target was not found among graph nodes",
        later_action="atom_candidate",
        dedupe_key=_dedupe_key("missing-atom-references", edge["source_id"], edge["target_id"], edge.get("role")),
        promotion_targets=["atom", "question"],
    )


def _missing_atom_finding_from_check(finding: GraphMissingFinding) -> SelfReflectionFinding:
    role = finding.role or "references"
    return SelfReflectionFinding(
        question_id="missing-atom-references",
        kind="dangling_source_atom_reference",
        source_id=finding.source_id,
        target_id=finding.target_id,
        role=role,
        provenance_path=finding.provenance_path or _path_from_node_id(finding.source_id),
        provenance_locator=finding.provenance_locator or f"missing:{finding.source_id}:{finding.target_id}",
        confidence="high",
        reason="declared atom reference target was not found among graph nodes",
        later_action="atom_candidate",
        dedupe_key=_dedupe_key("missing-atom-references", finding.source_id, finding.target_id, role),
        promotion_targets=["atom", "question"],
    )


def _dangling_generated_artifact_findings(
    snapshot: GraphView,
    missing_findings: list[GraphMissingFinding],
) -> list[SelfReflectionFinding]:
    findings: list[SelfReflectionFinding] = []
    nodes = snapshot.nodes
    node_ids = {node.id for node in nodes}
    linked_pairs = {
        (edge.source, edge.target)
        for edge in snapshot.edges
        if edge.role in {"references", "generated_from", "materializes", "renders", "source_for"}
    }

    for finding in [*_snapshot_missing_targets(snapshot), *missing_findings]:
        if not finding.source_id.startswith("diagram:"):
            continue
        if not finding.target_id.startswith("diagram:"):
            continue
        source_path = _path_from_node_id(finding.source_id)
        target_path = _path_from_node_id(finding.target_id)
        if not (source_path.startswith("docs/diagrams/") and source_path.endswith(".md") and target_path.endswith(".mmd")):
            continue
        findings.append(
            SelfReflectionFinding(
                question_id="dangling-generated-artifacts",
                kind="dangling_generated_artifact",
                source_id=finding.source_id,
                target_id=finding.target_id,
                role=finding.role or "references",
                provenance_path=finding.provenance_path or source_path,
                provenance_locator=finding.provenance_locator or f"missing:{finding.source_id}:{finding.target_id}",
                confidence="high",
                reason="rendered diagram declares a source artifact that is missing from the graph snapshot",
                later_action="issue_candidate",
                dedupe_key=_dedupe_key("dangling-generated-artifacts", finding.source_id, finding.target_id, finding.role or "references"),
                promotion_targets=["task", "question"],
            )
        )

    for node in nodes:
        if node.kind != "diagram":
            continue
        path = _node_path(node)
        if not (path.startswith("docs/diagrams/") and path.endswith(".md")):
            continue
        source_id = f"diagram:{path[:-3]}.mmd"
        if source_id not in node_ids or (node.id, source_id) in linked_pairs:
            continue
        findings.append(
            SelfReflectionFinding(
                question_id="dangling-generated-artifacts",
                kind="dangling_generated_artifact",
                source_id=node.id,
                target_id=source_id,
                role="source_for",
                provenance_path=path,
                provenance_locator=f"sibling-source:{source_id}",
                confidence="medium",
                reason="rendered diagram has a sibling Mermaid source file but no declared graph edge linking them",
                later_action="issue_candidate",
                dedupe_key=_dedupe_key("dangling-generated-artifacts", node.id, source_id, "source_for"),
                promotion_targets=["task", "question"],
            )
        )
    return findings


def _unlinked_source_file_findings(snapshot: GraphView) -> list[SelfReflectionFinding]:
    nodes = snapshot.nodes
    linked_source_ids = _linked_source_ids(snapshot)
    findings: list[SelfReflectionFinding] = []
    for node in nodes:
        if node.kind != "source_file" or node.id in linked_source_ids:
            continue
        path = _node_path(node)
        if _is_excluded_source_path(path):
            continue
        findings.append(
            SelfReflectionFinding(
                question_id="unlinked-source-files",
                kind="unlinked_source_file",
                source_id=node.id,
                target_id=None,
                role=None,
                provenance_path=path,
                provenance_locator=f"node:{node.id}",
                confidence="medium",
                reason="source file has no graph edge connecting it to a desk knowledge surface",
                later_action="issue_candidate",
                dedupe_key=f"unlinked-source-files:{node.id}",
                promotion_targets=["task", "question"],
            )
        )
    return findings


def _linked_source_ids(snapshot: GraphView) -> set[str]:
    linked: set[str] = set()
    for edge in snapshot.edges:
        if edge.role not in SOURCE_LINK_ROLES:
            continue
        for node_id in (edge.source, edge.target):
            if node_id.startswith("source_file:"):
                linked.add(node_id)
    return linked


def _node_path(node: Node) -> str:
    if node.path:
        return str(node.path)
    if isinstance(node.identity, str) and node.identity:
        return node.identity
    return _path_from_node_id(node.id)


def _group_duplicate_findings(findings: list[SelfReflectionFinding]) -> list[SelfReflectionFinding]:
    grouped: dict[str, SelfReflectionFinding] = {}
    duplicate_counts: dict[str, int] = {}
    for finding in sorted(findings, key=lambda item: (item.dedupe_key, item.provenance_path, item.provenance_locator)):
        if finding.dedupe_key not in grouped:
            grouped[finding.dedupe_key] = finding
            duplicate_counts[finding.dedupe_key] = 0
            continue
        duplicate_counts[finding.dedupe_key] += 1
    return [
        SelfReflectionFinding(**{**finding.to_dict(), "duplicate_count": duplicate_counts[finding.dedupe_key]})
        for finding in grouped.values()
    ]


def _dedupe_key(question_id: str, source_id: str, target_id: str | None, role: str | None) -> str:
    return f"{question_id}:{source_id}:{target_id or ''}:{role or ''}"


def _path_from_node_id(node_id: str) -> str:
    return node_id.split(":", 1)[1] if ":" in node_id else node_id


def _is_excluded_source_path(path: str) -> bool:
    parts = Path(path).parts
    if any(part in EXCLUDED_SOURCE_PARTS for part in parts):
        return True
    if any(path.startswith(prefix) for prefix in EXCLUDED_SOURCE_PREFIXES):
        return True
    return any(path.endswith(suffix) for suffix in EXCLUDED_SOURCE_SUFFIXES)


def drift_check_knowledge_surfaces(root: Path) -> list[str]:
    from deskops.graph.checks import find_atom_reference_violations
    from deskops.graph.checks import find_missing_graph_references
    from deskops.graph.view import project_graph_view

    snapshot = project_graph_view(root)
    missing = sorted(
        [*find_missing_graph_references(root), *find_missing_snapshot_targets(snapshot)],
        key=lambda finding: (finding.kind, finding.source_id, finding.target_id),
    )

    report: list[str] = []
    
    # 1. an atom whose declared targets or materializations no longer resolve
    for finding in missing:
        if finding.source_id.startswith("atom:"):
            loc = f"{finding.provenance_path}#{finding.provenance_locator}" if finding.provenance_path else finding.source_id
            report.append(f"stale-atom: {loc} declares target {finding.target_id} which no longer resolves")
            
    # 2a. a document that points at atoms with no inbound trace (dangling reference)
    for finding in missing:
        if finding.target_id.startswith("atom:") and not finding.source_id.startswith("atom:"):
            loc = f"{finding.provenance_path}#{finding.provenance_locator}" if finding.provenance_path else finding.source_id
            report.append(f"dangling-atom-reference: {loc} points at missing {finding.target_id}")

    # 3. a graph finding that no atom and no issue covers
    covering_sources = set()
    for edge in snapshot.edges:
        if edge.source.startswith("atom:") or edge.source.startswith("issue:"):
            covering_sources.add(edge.target)
            
    for finding in missing:
        if finding.source_id.startswith("atom:") or finding.source_id.startswith("issue:"):
            continue
        if finding.source_id in covering_sources:
            continue
        loc = f"{finding.provenance_path}#{finding.provenance_locator}" if finding.provenance_path else finding.source_id
        report.append(f"unrouted-finding: {loc} (missing {finding.target_id}) is not covered by any atom or issue")

    # 4. atom reference metadata that does not follow the canonical convention
    for violation in find_atom_reference_violations(root):
        loc = f"{violation.path}#{violation.locator}"
        report.append(f"atom-reference: {loc} {violation.reason}")

    # 5. a task body that restates global workflow policy instead of referencing it
    from deskops.task_policy import scan_task_policy_leaks

    for leak in scan_task_policy_leaks(root):
        report.append(
            f"task-policy-leak: {leak.path}:{leak.line} repeats global policy phrase "
            f"'{leak.phrase}'; reference desk/rituals/closeout.md or a pill instead"
        )

    return report

FILE:tests/test_graph_snapshot.py
from __future__ import annotations

import json
from pathlib import Path

import pytest
from sldb.api.graph.snapshot import GraphSnapshot

from deskops.graph.export import DEFAULT_SNAPSHOT_PATH
from deskops.graph.export import build_graph_snapshot
from deskops.graph.export import networkx_path_for_snapshot
from deskops.graph.export import write_graph_snapshot
from deskops.graph.view import GraphReadError as GraphSnapshotReadError
from deskops.graph.view import project_graph_view
from deskops.graph.view import read_graph_file as read_graph_snapshot


def test_build_graph_snapshot_combines_nodes_and_declared_edges(tmp_path: Path) -> None:
    write_atom(tmp_path / "desk/atoms/atom-existing.md", "atom-existing", "Existing Atom")
    write(tmp_path / "deskops/operations.py", "def run() -> None:\n    pass\n")
    write(
        tmp_path / "desk/tasks/008-write-kgdb-graph-snapshot.md",
        """# Write KGDB graph snapshot

ID: task-008-write-kgdb-graph-snapshot

## Related Atoms

- atom-existing

## Notes

Explicit source file reference: `deskops/operations.py`.
""",
    )

    snapshot = build_graph_snapshot(tmp_path)
    validated = GraphSnapshot.model_validate(snapshot)
    nodes_by_id = {node.identity.node_id: node for node in validated.nodes}

    assert snapshot["metadata"]["schema"] == "deskops_kgdb_graph_snapshot_v1"
    assert snapshot["metadata"]["runtime_output_path"] == ".sldb/runtime/graphs/deskops.kg.json"
    assert snapshot["metadata"]["node_count"] >= 3
    assert snapshot["metadata"]["edge_count"] >= 2

    task_node = nodes_by_id["task:task-008-write-kgdb-graph-snapshot"]
    assert task_node.identity.node_type == "task"
    assert [(edge.target_id, edge.relation_type) for edge in task_node.edges] == [
        ("atom:atom-existing", "references"),
        ("source_file:deskops/operations.py", "references"),
    ]
    assert task_node.edges[0].metadata == {
        "role": "references",
        "source_kind": "declared",
        "confidence": "high",
        "provenance_path": "desk/tasks/008-write-kgdb-graph-snapshot.md",
        "provenance_locator": "line:7:related atoms",
        "extractor": "desk_declared_edges_v1",
    }


def test_write_graph_snapshot_uses_ignored_runtime_path(tmp_path: Path) -> None:
    write_atom(tmp_path / "desk/atoms/atom-existing.md", "atom-existing", "Existing Atom")

    output_path = write_graph_snapshot(tmp_path)

    assert DEFAULT_SNAPSHOT_PATH.as_posix() == ".sldb/runtime/graphs/deskops.kg.json"
    assert output_path == tmp_path / DEFAULT_SNAPSHOT_PATH
    GraphSnapshot.model_validate(json.loads(output_path.read_text(encoding="utf-8")))


def test_snapshot_path_helpers_keep_projections_separate(tmp_path: Path) -> None:
    preferred = tmp_path / DEFAULT_SNAPSHOT_PATH

    assert networkx_path_for_snapshot(preferred) == (
        tmp_path / ".sldb/runtime/graphs/deskops.nx.json"
    )


def test_the_project_graph_view_is_what_the_built_snapshot_reads_back(tmp_path: Path) -> None:
    """The graph commands read sldb's project graph directly; it is the graph `graph build` writes."""
    write_atom(tmp_path / "desk/atoms/atom-existing.md", "atom-existing", "Existing Atom")
    write(
        tmp_path / "desk/tasks/task-source.md",
        "# Source task\n\n## Related Atoms\n\n- atom-existing\n- atom-missing\n",
    )
    write(tmp_path / "deskops/tool.py", "VALUE = 1\n")

    live = project_graph_view(tmp_path)
    built = read_graph_snapshot(write_graph_snapshot(tmp_path))

    def nodes(view):
        return [(node.id, node.kind, node.path, node.label) for node in view.nodes]

    assert nodes(live) == nodes(built)
    assert live.edges == built.edges
    assert ("task:desk/tasks/task-source.md", "atom:atom-existing", "references") in {(e.source, e.target, e.role) for e in live.edges}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_atom(path: Path, atom_id: str, title: str) -> None:
    write(
        path,
        f"""---
id: {atom_id}
title: {title}
five_wh_one_plus: what
tags: []
---

# {title}

## Answer

Existing knowledge.
""",
    )


def test_read_graph_snapshot_flattens_nested_edges() -> None:
    path = Path(__file__).parent / "fixtures/golden/graph_snapshot.kg.json"

    snapshot = read_graph_snapshot(path)

    atom = next(node for node in snapshot.nodes if node.id == "atom:atom-golden-one")
    assert atom.kind == "atom"
    assert atom.path == "desk/atoms/atom-golden-one.md"
    assert isinstance(atom.identity, dict)
    assert atom.identity["node_id"] == "atom:atom-golden-one"
    assert atom.label == "Golden atom one"

    edge = next(edge for edge in snapshot.edges if edge.source == "task:task-golden-alpha")
    assert edge.target == "atom:atom-golden-one"
    assert edge.role == "references"
    assert edge.provenance_path == "desk/tasks/task-golden-alpha.md"
    assert edge.provenance_locator == "line:43:related atoms"
    assert edge.extractor == "desk_declared_edges_v1"


def test_read_graph_snapshot_accepts_top_level_edges_and_id_identity(tmp_path: Path) -> None:
    snapshot = {
        "nodes": [{"identity": {"node_id": "task:source", "node_type": "task"}, "semantics": {"title": "Source"}}],
        "edges": [{"source": "task:source", "target": "atom:missing", "role": "references"}],
    }
    path = _write(tmp_path, json.dumps(snapshot))

    result = read_graph_snapshot(path)

    assert [(node.id, node.kind, node.label) for node in result.nodes] == [("task:source", "task", "Source")]
    assert [(edge.source, edge.target, edge.role) for edge in result.edges] == [
        ("task:source", "atom:missing", "references")
    ]


def test_read_graph_snapshot_rejects_missing_file(tmp_path: Path) -> None:
    path = tmp_path / "missing.json"

    with pytest.raises(GraphSnapshotReadError, match="graph snapshot not found"):
        read_graph_snapshot(path)


def test_read_graph_snapshot_rejects_invalid_json(tmp_path: Path) -> None:
    path = _write(tmp_path, "{not json")

    with pytest.raises(GraphSnapshotReadError, match="not valid JSON"):
        read_graph_snapshot(path)


def test_read_graph_snapshot_rejects_missing_key(tmp_path: Path) -> None:
    path = _write(tmp_path, json.dumps({"version": "1.0"}))

    with pytest.raises(GraphSnapshotReadError, match="missing the nodes list"):
        read_graph_snapshot(path)

    path = _write(tmp_path, json.dumps({"nodes": [{"kind": "atom"}]}))

    with pytest.raises(GraphSnapshotReadError, match="missing its id"):
        read_graph_snapshot(path)


def test_read_graph_snapshot_rejects_malformed_shape(tmp_path: Path) -> None:
    path = _write(tmp_path, json.dumps({"nodes": {}}))

    with pytest.raises(GraphSnapshotReadError, match="missing the nodes list"):
        read_graph_snapshot(path)

    path = _write(tmp_path, json.dumps({"nodes": ["node"]}))

    with pytest.raises(GraphSnapshotReadError, match="non-object node"):
        read_graph_snapshot(path)

    path = _write(tmp_path, json.dumps({"nodes": [{"id": "task:source", "edges": {}}]}))

    with pytest.raises(GraphSnapshotReadError, match="node edges must be a list"):
        read_graph_snapshot(path)


def _write(path: Path, content: str) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    target = path / "snapshot.json"
    target.write_text(content, encoding="utf-8")
    return target

FILE:tests/test_graph_self_reflection.py
from __future__ import annotations

import json
from pathlib import Path

from deskops.graph.checks import GraphMissingFinding
from deskops.graph.self_reflection import DEFAULT_DECISIONS_PATH
from deskops.graph.self_reflection import DEFAULT_REPORT_PATH
from deskops.graph.self_reflection import build_self_reflection_report
from deskops.graph.self_reflection import write_self_reflection_report
from deskops.graph.view import read_graph_file as read_graph_snapshot


FIXTURE_GRAPH = Path(__file__).parent / "fixtures/knowledge_graph/static_desk_source_graph.json"


def test_self_reflection_report_generates_findings_and_writes_runtime_report(tmp_path: Path) -> None:
    snapshot = json.loads(FIXTURE_GRAPH.read_text(encoding="utf-8"))
    snapshot["nodes"].extend(
        [
            {
                "id": "source_file:deskops/unlinked.py",
                "kind": "source_file",
                "label": "Unlinked source",
                "identity": "deskops/unlinked.py",
                "path": "deskops/unlinked.py",
            },
            {
                "id": "diagram:docs/diagrams/example/rendered.md",
                "kind": "diagram",
                "label": "Rendered diagram",
                "identity": "docs/diagrams/example/rendered.md",
                "path": "docs/diagrams/example/rendered.md",
            },
            {
                "id": "diagram:docs/diagrams/example/rendered.mmd",
                "kind": "diagram",
                "label": "Rendered diagram source",
                "identity": "docs/diagrams/example/rendered.mmd",
                "path": "docs/diagrams/example/rendered.mmd",
            },
        ]
    )
    snapshot["edges"].append(
        {
            "source": "task:task-004-create-static-graph-fixture",
            "target": "atom:atom-missing-reflection",
            "role": "references",
            "provenance_path": "desk/tasks/004-create-static-graph-fixture.md",
            "provenance_locator": "Related Atoms",
        }
    )

    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(snapshot), encoding="utf-8")
    report = build_self_reflection_report(read_graph_snapshot(graph_path))
    report_path = write_self_reflection_report(tmp_path, report)
    decisions_path = tmp_path / DEFAULT_DECISIONS_PATH

    assert report_path == tmp_path / DEFAULT_REPORT_PATH
    assert report_path.exists()
    assert decisions_path.exists()
    assert json.loads(decisions_path.read_text(encoding="utf-8")) == {
        "allowed_statuses": ["pending", "accepted", "rejected"],
        "decisions": [],
        "report_path": ".sldb/runtime/self_reflection_findings.json",
        "runtime_only": True,
        "schema": "deskops_self_reflection_decisions_v1",
    }
    assert not (tmp_path / "desk").exists()
    assert report["schema"] == "deskops_self_reflection_report_v2"
    assert report["runtime_only"] is True
    assert report["mutation_policy"] == "review_only_no_source_artifact_mutation"
    assert report["review_loop"] == {
        "decision_storage": {
            "schema": "deskops_self_reflection_decisions_v1",
            "runtime_output_path": ".sldb/runtime/self_reflection_decisions.json",
            "allowed_statuses": ["pending", "accepted", "rejected"],
        },
        "promotion_paths": {
            "task": "accepted finding -> create or promote a desk task when remediation work is clear",
            "question": "accepted finding -> route a desk question when owner intent or source of truth is unclear",
            "atom": "accepted finding -> update or create an atom when the durable knowledge gap is understood",
        },
    }
    assert report["summary"] == {"finding_count": 3, "suppressed_duplicate_count": 0}
    assert report["findings"] == [
        {
            "question_id": "dangling-generated-artifacts",
            "kind": "dangling_generated_artifact",
            "source_id": "diagram:docs/diagrams/example/rendered.md",
            "target_id": "diagram:docs/diagrams/example/rendered.mmd",
            "role": "source_for",
            "provenance_path": "docs/diagrams/example/rendered.md",
            "provenance_locator": "sibling-source:diagram:docs/diagrams/example/rendered.mmd",
            "confidence": "medium",
            "reason": "rendered diagram has a sibling Mermaid source file but no declared graph edge linking them",
            "later_action": "issue_candidate",
            "dedupe_key": "dangling-generated-artifacts:diagram:docs/diagrams/example/rendered.md:diagram:docs/diagrams/example/rendered.mmd:source_for",
            "promotion_targets": ["task", "question"],
            "duplicate_count": 0,
        },
        {
            "question_id": "missing-atom-references",
            "kind": "dangling_source_atom_reference",
            "source_id": "task:task-004-create-static-graph-fixture",
            "target_id": "atom:atom-missing-reflection",
            "role": "references",
            "provenance_path": "desk/tasks/004-create-static-graph-fixture.md",
            "provenance_locator": "Related Atoms",
            "confidence": "high",
            "reason": "declared atom reference target was not found among graph nodes",
            "later_action": "atom_candidate",
            "dedupe_key": "missing-atom-references:task:task-004-create-static-graph-fixture:atom:atom-missing-reflection:references",
            "promotion_targets": ["atom", "question"],
            "duplicate_count": 0,
        },
        {
            "question_id": "unlinked-source-files",
            "kind": "unlinked_source_file",
            "source_id": "source_file:deskops/unlinked.py",
            "target_id": None,
            "role": None,
            "provenance_path": "deskops/unlinked.py",
            "provenance_locator": "node:source_file:deskops/unlinked.py",
            "confidence": "medium",
            "reason": "source file has no graph edge connecting it to a desk knowledge surface",
            "later_action": "issue_candidate",
            "dedupe_key": "unlinked-source-files:source_file:deskops/unlinked.py",
            "promotion_targets": ["task", "question"],
            "duplicate_count": 0,
        },
    ]


def test_self_reflection_report_suppresses_duplicate_findings(tmp_path: Path) -> None:
    snapshot = {
        "nodes": [{"id": "task:source", "kind": "task", "label": "Source"}],
        "edges": [
            {
                "source": "task:source",
                "target": "atom:missing",
                "role": "references",
                "provenance_path": "desk/tasks/source.md",
                "provenance_locator": "Related Atoms",
            },
            {
                "source": "task:source",
                "target": "atom:missing",
                "role": "references",
                "provenance_path": "desk/tasks/source.md",
                "provenance_locator": "YAML metadata",
            },
        ],
    }
    missing_findings = [
        GraphMissingFinding(
            kind="dangling_source_atom_reference",
            source_id="task:source",
            target_id="atom:missing",
            reason="declared target was not found among extracted graph nodes",
            role="references",
            provenance_path="desk/tasks/source.md",
            provenance_locator="line:3:yaml",
        )
    ]

    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(snapshot), encoding="utf-8")
    report = build_self_reflection_report(read_graph_snapshot(graph_path), missing_findings)

    assert report["summary"] == {"finding_count": 1, "suppressed_duplicate_count": 1}
    assert report["findings"][0]["dedupe_key"] == "missing-atom-references:task:source:atom:missing:references"
    assert report["findings"][0]["promotion_targets"] == ["atom", "question"]
    assert report["findings"][0]["duplicate_count"] == 1

FILE:instruccion
Cold-bundle de la tarea task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_self_reflection.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_gitignore_policy.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -rnF '.sldb/runtime' deskops/ --include=*.py (solo menciones de exclusion o lectura, ninguna escritura)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea


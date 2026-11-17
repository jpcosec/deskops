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


def test_existing_files_sldb_cannot_declare_are_not_missing(tmp_path: Path) -> None:
    """H1 of CC33c: targets outside ``DeclaredFileTargets`` keep the existing-file exception.

    A task's ``references:`` list (an inbox note), a path in a task's body (a plan's
    ``dag.yaml``) and a materialization target under the excluded ``tests/fixtures`` are no
    graph nodes, but they exist, so they are not reported; a target that does not exist is.
    """
    write(tmp_path / "desk/inbox/20261116-note.md", "# A note\n")
    write(tmp_path / "desk/drawer/plans/p/dag.yaml", "nodes: []\n")
    write(tmp_path / "tests/fixtures/golden.json", "{}\n")
    write(
        tmp_path / "desk/tasks/task-a.md",
        "---\nid: task-a\nreferences:\n- desk/inbox/20261116-note.md\n---\n\n# A\n\n"
        "Plan: desk/drawer/plans/p/dag.yaml and desk/drawer/plans/p/gone.yaml\n",
    )
    write(
        tmp_path / "desk/materializations/materialization-golden.md",
        "---\nid: materialization-golden\ntarget_identity: tests/fixtures/golden.json\n---\n\n# Golden\n",
    )

    assert [finding.target_id for finding in find_missing_graph_references(tmp_path)] == [
        "desk/drawer/plans/p/gone.yaml"
    ]

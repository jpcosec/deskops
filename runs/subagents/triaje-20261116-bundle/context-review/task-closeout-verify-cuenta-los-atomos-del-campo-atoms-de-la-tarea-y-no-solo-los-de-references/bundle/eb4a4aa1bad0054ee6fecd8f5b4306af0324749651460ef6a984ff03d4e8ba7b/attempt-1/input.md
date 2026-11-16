FILE:desk/tasks/task-closeout-verify-cuenta-los-atomos-del-campo-atoms-de-la-tarea-y-no-solo-los-de-references.md
---
sldb:
  by: agent
  at: '2026-11-16T05:02:04Z'
  authority: generated
  via: save_document_payload
id: task-closeout-verify-cuenta-los-atomos-del-campo-atoms-de-la-tarea-y-no-solo-los-de-references
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
files:
- deskops/services/closeout_gates.py
- deskops/services/closure.py
- tests/test_closeout_gates.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-closeout-verify-ignora-el-campo-atoms-de-la-tarea-y-solo-lee-references.md
---

# closeout verify cuenta los atomos del campo atoms de la tarea y no solo los de references

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (2026-10-29): closeout verify falla con missing_atom_or_materialization_link aunque la tarea tenga atoms: [atom-...] en su frontmatter. Reproduccion: `deskops edit task T atoms '["atom-x"]'` -> verify falla; `deskops edit task T references '[..., "atom-x"]'` -> verify pasa. Sigue igual hoy: deskops/services/closeout_gates.py:100-113 solo recorre references y deskops/services/closure.py:1241 y 1288-1293 usan reference_evidence['atom'].

## Goal

_Describe the concrete result this task must produce._

La compuerta atom|materialization de closeout verify y de closeout commit cuenta como evidencia los ids del campo atoms de la tarea, igual que los atom-* de references.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/closeout_gates.py, deskops/services/closure.py y sus tests. No entra: cambiar otras compuertas ni el formato del reporte. Precisiones del preflight 1: se cuentan todos los valores del campo atoms (es una lista tipada de AtomDoc; no se filtra por prefijo). La compuerta de materialization no cambia. Los tests de Validation que no esten en files pueden editarse solo si el cambio los rompe por una razon legitima. El status draft de la tarea no le toca al ejecutor.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Unir task.atoms a los atom-* de references al armar la evidencia de atomo. 2) Test en tests/test_closeout_gates.py: tarea con atoms y sin atom-* en references pasa la compuerta; tarea sin ninguno sigue fallando.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los dos casos del test pasan y la reproduccion del item ya no falla.

FILE:desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
---
# pill-xxx
id: pill-closeout-knowledge-gates-require-traceable-evidence
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:closeout
- topic:knowledge
---

# Guardrail: closeout knowledge gates require traceable evidence

## What

_Define the context or guardrail this pill carries._

Treat knowledge-oriented closeout gates as evidence checks over real atoms, materializations, graph links, tests, cleanup actions, and commits.

## Why

_Explain why this context matters for safe execution._

A closeout gate is only meaningful if it proves that the changed work is still connected to durable knowledge and not merely accompanied by free-form claims.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task changes closeout validation, graph/atom traceability checks, materialization verification, or commit-evidence requirements.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to task closeout readiness, evidence verification helpers, generated artifact provenance checks, and future graph-backed closeout commands.

## How

_Describe the correct way to apply this guidance._

Verify evidence against real resolvable surfaces, fail clearly when a required knowledge link is missing, and route uncovered gaps into explicit follow-up work.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not let closeout accept empty or unverifiable references. Do not confuse a narrative summary with durable evidence.

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

FILE:deskops/services/closeout_gates.py
"""Closeout evidence gates.

Closeout verification accepts only real evidence: a lowercase commit id naming
a commit in HEAD's history, and a Python test file inside the repository's
``tests/`` directory. A front-matter string that merely looks like evidence is
not evidence.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
from typing import Any
from typing import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from deskops.identity import RegisteredRepository


COMMIT_ID_PATTERN = re.compile(r"[0-9a-f]{7,40}")
URL_PATTERN = re.compile(r"https?://\S+")

# Closed vocabulary for a task's declared closeout evidence. `atom` and
# `materialization` are alternatives of one gate: either link satisfies it.
CLOSEOUT_EVIDENCE_VOCABULARY = ("tests", "commit", "atom", "materialization", "document", "external")

CODE_EVIDENCE = ("tests", "commit", "atom", "materialization")
DOCUMENT_EVIDENCE = ("commit", "document")
EXTERNAL_EVIDENCE = ("external",)

DOCUMENT_SUFFIXES = frozenset({".md", ".rst", ".txt", ".adoc", ".yaml", ".yml"})


class CloseoutEvidenceError(ValueError):
    """The declared closeout evidence is invalid or missing."""


def normalize_declared_evidence(value: Any) -> list[str]:
    """Validate a declared evidence list against the closed vocabulary, keeping order."""
    if value in (None, ""):
        return []
    items = value if isinstance(value, (list, tuple)) else [value]
    declared: list[str] = []
    for item in items:
        kind = str(item).strip().lower()
        if not kind:
            continue
        if kind not in CLOSEOUT_EVIDENCE_VOCABULARY:
            raise CloseoutEvidenceError(
                f"Unknown closeout evidence '{item}'. Allowed: {', '.join(CLOSEOUT_EVIDENCE_VOCABULARY)}."
            )
        if kind not in declared:
            declared.append(kind)
    return declared


def order_evidence_kinds(kinds: list[str]) -> list[str]:
    """Deduplicate a declared evidence list in the vocabulary order, keeping the kinds that
    are declared on a type but not in the CLI vocabulary (``children``, ``goldens``) last.
    """
    seen: list[str] = []
    for kind in [*CLOSEOUT_EVIDENCE_VOCABULARY, *kinds]:
        if kind in kinds and kind not in seen:
            seen.append(kind)
    return seen


def collapse_link_kinds(kinds: list[str]) -> list[str]:
    """Show atom and materialization as the one alternative gate they are."""
    if "atom" in kinds and "materialization" in kinds:
        out: list[str] = []
        for kind in kinds:
            label = "atom|materialization" if kind in {"atom", "materialization"} else kind
            if label not in out:
                out.append(label)
        return out
    return list(kinds)


def gate_summary(declared: list[str], found: list[str]) -> str:
    declared_text = ", ".join(collapse_link_kinds(declared)) or "nada"
    found_text = ", ".join(found) or "nada"
    return f"esta tarea declaró {declared_text}; encontré {found_text}"


class CloseoutGatesService:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def closeout_reference_evidence(
        self,
        payload: dict[str, Any],
        *,
        points_to_atom: Callable[[str], bool],
        points_to_routed_follow_up: Callable[[str], bool],
    ) -> dict[str, list[str]]:
        evidence = {"tests": [], "atom": [], "commit": [], "follow_up": [], "document": [], "external": []}
        references = payload.get("references") or []
        if not isinstance(references, list):
            references = [references]
        files = payload.get("files") or []
        if not isinstance(files, list):
            files = [files]
        for reference in references:
            ref = str(reference).strip()
            if not ref:
                continue
            if self.reference_points_to_test(ref, files=files):
                evidence["tests"].append(ref)
            if points_to_atom(ref):
                evidence["atom"].append(ref)
            if self.reference_points_to_commit(ref):
                evidence["commit"].append(ref)
            if points_to_routed_follow_up(ref):
                evidence["follow_up"].append(ref)
            if self.reference_points_to_url(ref):
                evidence["external"].append(ref)
        for candidate in [*references, *files]:
            ref = str(candidate).strip()
            if ref and self.reference_points_to_document(ref) and ref not in evidence["document"]:
                evidence["document"].append(ref)
        return evidence

    @staticmethod
    def reference_points_to_url(reference: str) -> bool:
        """True for an http(s) URL: the record of work done outside this repository."""
        return bool(URL_PATTERN.fullmatch(reference.strip()))

    def reference_points_to_document(self, reference: str) -> bool:
        """True only for an existing document file inside the repository.

        Documents are prose or spec files (``DOCUMENT_SUFFIXES``). Test sources and
        the task bundle itself, which closure removes, are not documents.
        """
        path = Path(reference.split("::", 1)[0].strip())
        if not str(path) or path.is_absolute():
            return False
        resolved = (self.root / path).resolve()
        if resolved.suffix.lower() not in DOCUMENT_SUFFIXES or not resolved.is_file():
            return False
        if not resolved.is_relative_to(self.root):
            return False
        excluded = ((self.root / "tests").resolve(), (self.root / "desk" / "tasks").resolve())
        return not any(resolved.is_relative_to(parent) for parent in excluded)

    def reference_points_to_test(self, reference: str, files: list[Any] | None = None) -> bool:
        """True only for an existing .py file inside the repository that is a test location.

        After dropping an optional ``::node`` suffix (the node is not validated) and the
        ``pytest <path>`` form, the reference must name an existing file, relative to the
        root, whose suffix is exactly ``.py`` and which resolves inside the root. It counts
        when one of its directories (relative to the root) is named ``tests`` (``tests/``,
        ``runtime/foo/tests/``, ``ops/tests/sub/``) or when its path is declared in
        ``files``, the evaluated TaskDoc's ``files``: they widen where tests may live but
        are not evidence by themselves. Absolute paths, paths that leave the root through
        ``..`` or a symlink, and files under a directory starting with ``.`` or named
        ``site-packages`` or ``node_modules`` (third-party code) are not evidence. Each
        reference is checked on its own; the disk is not walked.
        """
        for candidate in self._test_path_candidates(reference):
            path_text = candidate.split("::", 1)[0]
            path = Path(path_text)
            if not path_text or path.is_absolute():
                continue
            resolved = (self.root / path).resolve()
            if resolved.suffix != ".py" or not resolved.is_file():
                continue
            if not resolved.is_relative_to(self.root):
                continue
            directories = resolved.relative_to(self.root).parts[:-1]
            if any(part.startswith(".") or part in {"site-packages", "node_modules"} for part in directories):
                continue
            if "tests" in directories:
                return True
            for entry in files or []:
                declared = str(entry).strip()
                if declared and not Path(declared).is_absolute() and (self.root / declared).resolve() == resolved:
                    return True
        return False

    def full_commit_sha(self, reference: str) -> str:
        """The full id of a commit reference that passes ``reference_points_to_commit``, else ''."""
        if not self.reference_points_to_commit(reference):
            return ""
        resolved = subprocess.run(
            ["git", "rev-parse", "--verify", f"{reference.strip()}^{{commit}}"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        return resolved.stdout.strip() if resolved.returncode == 0 else ""

    def reference_points_to_commit(self, reference: str) -> bool:
        """True only for a lowercase hex id resolving to HEAD or an ancestor.

        The pattern rejects symbolic names such as ``HEAD`` or ``main``; an
        ambiguous abbreviation fails ``rev-parse --verify``; an unrelated or
        descendant commit fails the ancestor check.
        """
        candidate = reference.strip()
        if not COMMIT_ID_PATTERN.fullmatch(candidate):
            return False
        try:
            resolved = subprocess.run(
                ["git", "rev-parse", "--verify", f"{candidate}^{{commit}}"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
            if resolved.returncode != 0:
                return False
            full_sha = resolved.stdout.strip()
            if not full_sha:
                return False
            ancestor = subprocess.run(
                ["git", "merge-base", "--is-ancestor", full_sha, "HEAD"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            return False
        return ancestor.returncode == 0

    def build_closeout_graph_context(self) -> "CloseoutGraph":
        """The declared-edge graph the closeout link gate reads, built lazily.

        Nodes come from one pass over the repository's document surfaces and file tree,
        tracked documents and schema edges from one read of the sldb index; the declared
        edges of a document are read only when the gate asks about it.
        """
        from deskops.graph.desk_graph import desk_graph

        return CloseoutGraph(desk_graph(self.root))

    def _test_path_candidates(self, reference: str) -> list[str]:
        candidates: list[str] = []
        stripped = reference.strip()
        if stripped.startswith("pytest "):
            for token in stripped.split()[1:]:
                token = token.strip("\"'")
                if token.startswith("-"):
                    continue
                if ".py" in token:
                    candidates.append(token)
        elif ".py" in stripped:
            candidates.append(stripped)
        return candidates


class RepositoryReferences:
    """Split closeout references qualified by a registered repository: ``<repo-id>:<value>``.

    The reference is cut at its first ``:``. When what comes before it is the id of a
    repository in the desk's own registry (``desk/registry/repo-*.md``), the rest is the
    value (a commit id or a test path, which may carry a pytest ``::node``) and it is
    checked in that repository's root. Otherwise the whole reference is what it was
    before: a local commit, a local test path or an http(s) URL. A prefix naming the desk
    itself (its ``project_identity`` or a registered repository whose root is the desk's
    root) is local: the value is checked as an unqualified reference.
    """

    def __init__(
        self,
        root: Path,
        entries: "list[RegisteredRepository]",
        *,
        own_identity: str | None = None,
    ) -> None:
        self.root = root.resolve()
        self.entries = {entry.id: entry for entry in entries}
        self.own_identity = (own_identity or "").strip() or None
        self._gates: dict[Path, CloseoutGatesService] = {}

    def split(self, reference: str) -> "tuple[RegisteredRepository | None, str]":
        """(the other repository, the value) for a qualified reference, else (None, the local reference)."""
        text = reference.strip()
        if CloseoutGatesService.reference_points_to_url(text) or ":" not in text:
            return None, text
        prefix, value = text.split(":", 1)
        if self.own_identity is not None and prefix == self.own_identity:
            return None, value.strip()
        entry = self.entries.get(prefix)
        if entry is None:
            return None, text
        if entry.repo_root is not None and entry.repo_root.resolve() == self.root:
            return None, value.strip()
        return entry, value.strip()

    @staticmethod
    def missing_root_message(entry: "RegisteredRepository") -> str | None:
        """The refusal for a registered repository whose root is not on this machine, else None."""
        if entry.repo_root is not None and entry.repo_root.is_dir():
            return None
        location = entry.repo_root if entry.repo_root is not None else entry.relative_path or "(no path)"
        return f"Registered repository {entry.id} is not at {location} on this machine."

    def gates(self, entry: "RegisteredRepository") -> CloseoutGatesService:
        """The evidence gates of a registered repository, rooted at its registered root."""
        assert entry.repo_root is not None
        root = entry.repo_root.resolve()
        if root not in self._gates:
            self._gates[root] = CloseoutGatesService(root)
        return self._gates[root]


class CloseoutGraph:
    """What the closeout link gate asks of the declared-edge graph.

    The gate needs, for a changed file, the edges leaving its node and the edges a
    materialization points at it, plus the edges that link test files to atoms or
    materializations. Only the materialization documents and the documents the gate asks
    about are read; ``edges_around`` and ``test_link_edges`` return supersets of what the
    gate keeps, in the order a full scan of the sorted edge list would visit them, so the
    gate's own conditions produce the same evidence in the same order.
    """

    def __init__(self, graph: Any) -> None:
        self.graph = graph
        lookup = graph.nodes.lookup
        self.node_ids_by_path = {path: node.id for path, node in lookup.by_path.items()}
        materializations = sorted(
            node_id for node_id in lookup.existing_ids | graph.node_ids() if node_id.startswith("materialization:")
        )
        self.invalid_materializations = {node_id for node_id in materializations if graph.missing_from(node_id)}
        self._materialization_edges_to: dict[str, list[Any]] = {}
        for node_id in materializations:
            for edge in graph.edges_from(node_id):
                self._materialization_edges_to.setdefault(edge.target_id, []).append(edge)

    def node_id(self, relative_path: str) -> str | None:
        return self.node_ids_by_path.get(relative_path)

    def edges_around(self, node_id: str) -> list[Any]:
        """Edges leaving ``node_id`` and materialization edges into it, sorted and unique."""
        return _sorted_unique([*self.graph.edges_from(node_id), *self._materialization_edges_to.get(node_id, [])])

    def test_link_edges(self) -> list[Any]:
        """Edges leaving a test file, and materialization edges into a test file."""
        edges = [
            edge
            for node_id in sorted(self.graph.node_ids())
            if node_id.startswith("test_file:")
            for edge in self.graph.edges_from(node_id)
        ]
        edges += [
            edge
            for target_id, into in self._materialization_edges_to.items()
            if target_id.startswith("test_file:")
            for edge in into
        ]
        return _sorted_unique(edges)


def _sorted_unique(edges: list[Any]) -> list[Any]:
    unique = {(edge.source_id, edge.target_id, edge.role, edge.provenance_locator): edge for edge in edges}
    return [unique[key] for key in sorted(unique)]

FILE:tests/test_closeout_gates.py
"""The closeout graph and the lifecycle transitions read from sldb.

`build_closeout_graph_context` reads sldb's project graph of the desk (GD21). These tests
run the closeout gate over temporary desks that exercise each case it distinguishes. The
frozen full-scan extractors (`tests/graph_oracle_v1`) were compared with the project graph
over the real desk of this repository and removed by CC33c once they matched (neighbors and
missing, as sets). `lifecycle.transitions_from` reads the desk's own store;
`tests/closeout_graph_oracle.py` keeps the linked-index reading it replaced, and the
transitions must be the same.
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import shutil
import subprocess

import pytest
import yaml

from deskops import lifecycle
from deskops.operations import DeskopsOperations

from tests.closeout_graph_oracle import transitions_from_v1


ATOM = "atom-closeout-graph-equivalence"
GUARD_TEST = "tests/test_skill_cli_drift.py"
CHANGED_SKILL = ".pi/skills/use-deskops/SKILL.md"

# task id -> changed files. Together they cover: a file covered by a valid
# materialization (source and test targets), a file whose only materialization is
# invalid, a file with no materialization, a changed document that declares atoms, a
# changed atom, a skill file covered through a guard test, and a path outside the repo.
TASKS: dict[str, list[str]] = {
    "task-valid-materialization": ["deskops/covered.py", "tests/test_covered.py"],
    "task-invalid-materialization": ["deskops/covered_by_invalid.py"],
    "task-no-materialization": ["deskops/uncovered.py", "docs/notes.md"],
    "task-changed-documents": [
        "desk/tasks/task-valid-materialization.md",
        f"desk/atoms/{ATOM}.md",
        "docs/design.md",
    ],
    "task-skill-guard": [CHANGED_SKILL],
    "task-mixed": ["deskops/covered.py", "deskops/uncovered.py", "../outside.py", "config/app-config.yaml"],
}


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _materialization(name: str, atoms: list[str], target_kind: str, target: str) -> str:
    return (
        "---\n"
        + yaml.safe_dump(
            {
                "id": name,
                "title": name.replace("-", " "),
                "source_atoms": atoms,
                "target_kind": target_kind,
                "target_identity": target,
                "validation": [f"python -m pytest {GUARD_TEST} -q"],
                "tags": [],
            },
            sort_keys=False,
        )
        + f"---\n\n# {name}\n\n## Intent\n\nCover {target}.\n"
    )


def _task(task_id: str, files: list[str], atoms: list[str]) -> str:
    front = {
        "id": task_id,
        "status": "active",
        "current_node": "ritual-testing",
        "history": ["task_activates"],
        "references": [GUARD_TEST],
        "depends_on": [],
        "pills": [],
        "atoms": atoms,
        "files": files,
        "task_type": "code",
        "closeout_evidence": ["tests", "commit", "atom", "materialization"],
        "tags": [],
    }
    return (
        "---\n"
        + yaml.safe_dump(front, sort_keys=False)
        + f"---\n\n# {task_id}\n\n## Rationale\n\nEquivalence.\n\n## Goal\n\nSame answers.\n\n"
        "## Related atoms\n\n"
        f"- {ATOM}\n- atom-that-does-not-exist\n\n"
        "## Implementation Path\n\nTouch deskops/covered.py and tests/test_covered.py.\n\n"
        "## Validation\n\n- pytest\n\n## Done When\n\nDone.\n"
    )


def _populate(root: Path) -> None:
    """The shared desk content: atom, materializations (valid and invalid), sources, tasks."""
    _write(
        root / "desk" / "atoms" / f"{ATOM}.md",
        f"---\nid: {ATOM}\ntitle: Equivalence atom\nfive_wh_one_plus: what\ntags: []\n---\n\n"
        "# Equivalence atom\n\n## Answer\n\nThe closeout graph reads what it needs.\n",
    )
    _write(root / "deskops" / "covered.py", "COVERED = 1\n")
    _write(root / "deskops" / "covered_by_invalid.py", "INVALID = 1\n")
    _write(root / "deskops" / "uncovered.py", "UNCOVERED = 1\n")
    _write(root / "tests" / "test_covered.py", "def test_covered() -> None:\n    assert True\n")
    _write(
        root / GUARD_TEST,
        'SKILL_TREES = (".pi/skills", ".agents/skills", ".opencode/skills")\nSKILL_FILE = "SKILL.md"\n',
    )
    _write(root / CHANGED_SKILL, "# Use deskops\n")
    _write(root / "config" / "app-config.yaml", "key: value\n")
    _write(root / "runs" / "subagents" / "run-1" / "registry.json", "{}\n")
    _write(root / "runs" / "subagents" / "run-1" / "summary.md", "# Run\n")
    _write(root / "docs" / "notes.md", "# Notes\n\nPlain notes.\n")
    _write(
        root / "docs" / "design.md",
        f"---\ntitle: Design\natoms:\n- {ATOM}\n---\n\n# Design\n\n## Related atoms\n\n- {ATOM}\n",
    )
    materializations = root / "desk" / "materializations"
    _write(
        materializations / "materialization-covered-source.md",
        _materialization("materialization-covered-source", [ATOM], "source_file", "deskops/covered.py"),
    )
    _write(
        materializations / "materialization-covered-test.md",
        _materialization("materialization-covered-test", [ATOM], "test_file", "tests/test_covered.py"),
    )
    _write(
        materializations / "materialization-guard-test.md",
        _materialization("materialization-guard-test", [ATOM], "test_file", GUARD_TEST),
    )
    # Invalid: one of its source atoms does not exist.
    _write(
        materializations / "materialization-broken-atom.md",
        _materialization(
            "materialization-broken-atom",
            [ATOM, "atom-missing-from-the-desk"],
            "source_file",
            "deskops/covered_by_invalid.py",
        ),
    )
    # Invalid: its target is not a file of the repository.
    _write(
        materializations / "materialization-missing-target.md",
        _materialization("materialization-missing-target", [ATOM], "source_file", "deskops/gone.py"),
    )
    for task_id, files in TASKS.items():
        _write(root / "desk" / "tasks" / f"{task_id}.md", _task(task_id, files, [ATOM]))


def _commit(root: Path) -> None:
    _git(root, "add", "--", "deskops", "tests", "docs", "config", ".pi")
    _git(root, "commit", "-q", "-m", "work")
    sha = _git(root, "rev-parse", "--short", "HEAD")
    for task_id, files in TASKS.items():
        path = root / "desk" / "tasks" / f"{task_id}.md"
        text = path.read_text(encoding="utf-8").replace(f"- {GUARD_TEST}\n", f"- {GUARD_TEST}\n- '{sha}'\n", 1)
        path.write_text(text, encoding="utf-8")


@pytest.fixture
def bare_desk(tmp_path: Path) -> Path:
    """A repository with a desk and no sldb store: every document is read locally."""
    root = tmp_path / "bare"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed")
    _populate(root)
    _commit(root)
    return root


@pytest.fixture
def store_desk(lifecycle_desk: Path) -> Path:
    """An initialized desk whose store tracks the atom, the tasks and the materializations."""
    from sldb.api import track_document_file

    root = lifecycle_desk
    _populate(root)
    _commit(root)
    pythonpath = str(Path(__file__).resolve().parents[1])
    track_document_file(root / ".sldb", "AtomDoc", root / "desk" / "atoms" / f"{ATOM}.md", name=ATOM, pythonpath=pythonpath, force=True)
    for path in sorted((root / "desk" / "materializations").glob("materialization-*.md")):
        track_document_file(root / ".sldb", "MaterializationContractDoc", path, name=path.stem, pythonpath=pythonpath, force=True)
    for task_id in TASKS:
        track_document_file(root / ".sldb", "TaskDoc", root / "desk" / "tasks" / f"{task_id}.md", name=task_id, pythonpath=pythonpath, force=True)
    return root


@pytest.mark.parametrize("desk", ["bare_desk", "store_desk"])
def test_closeout_reports_cover_each_gate_case(desk: str, request: pytest.FixtureRequest) -> None:
    root: Path = request.getfixturevalue(desk)
    reports = {
        task_id: DeskopsOperations(root).verify_task_closeout(task_id)["gates"]["atom_or_materialization_link"]
        for task_id in TASKS
    }

    # The desk exercises each case the gate distinguishes.
    valid = reports["task-valid-materialization"]
    assert valid["ok"] is True
    assert "materialization:materialization:materialization-covered-source->deskops/covered.py" in valid["evidence"]
    invalid = reports["task-invalid-materialization"]
    assert invalid["ok"] is False
    assert [f["code"] for f in invalid["findings"]] == ["missing_changed_file_link"]
    absent = reports["task-no-materialization"]
    assert {f["path"] for f in absent["findings"]} == {"deskops/uncovered.py", "docs/notes.md"}
    assert any(item.startswith("graph:") for item in reports["task-changed-documents"]["evidence"])
    assert reports["task-skill-guard"]["evidence"] == [f"guard-test:{GUARD_TEST} -> {CHANGED_SKILL}"]
    assert any(f["code"] == "changed_file_missing" for f in reports["task-mixed"]["findings"])

    context = DeskopsOperations(root).closeout_gates.build_closeout_graph_context()
    assert context.invalid_materializations == {
        "materialization:materialization-broken-atom",
        "materialization:materialization-missing-target",
    }


def _lifecycle_nodes() -> list[str]:
    return sorted(set(lifecycle.load_lifecycle_spec().rituals) | {"ritual-unknown"})


def test_transitions_match_the_linked_index(lifecycle_desk: Path, tmp_path: Path) -> None:
    """Reading the desk's own store gives the transitions the linked composition gave,
    also when the desk links another store that carries a lifecycle graph of its own."""
    from sldb.api import link_store

    for node in _lifecycle_nodes():
        assert lifecycle.transitions_from(lifecycle_desk, node) == transitions_from_v1(lifecycle_desk, node), node

    other = tmp_path / "other"
    shutil.copytree(lifecycle_desk, other)
    with contextlib.redirect_stdout(io.StringIO()):
        link_store(lifecycle_desk / ".sldb", other / ".sldb", name="other")
    for node in _lifecycle_nodes():
        assert lifecycle.transitions_from(lifecycle_desk, node) == transitions_from_v1(lifecycle_desk, node), node
    assert lifecycle.transitions_from(lifecycle_desk, "ritual-testing")

FILE:instruccion
Cold-bundle de la tarea task-closeout-verify-cuenta-los-atomos-del-campo-atoms-de-la-tarea-y-no-solo-los-de-references: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea


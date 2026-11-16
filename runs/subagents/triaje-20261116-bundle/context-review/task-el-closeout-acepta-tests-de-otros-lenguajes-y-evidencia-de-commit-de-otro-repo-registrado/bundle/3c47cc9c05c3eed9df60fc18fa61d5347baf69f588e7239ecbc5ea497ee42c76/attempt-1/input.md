FILE:desk/tasks/task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado.md
---
sldb:
  by: agent
  at: '2026-11-16T05:06:01Z'
  authority: generated
  via: save_document_payload
id: task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-005144-suggestion-closeout-el-gate-de-tests-solo-acepta-py-y-el-de-commit-solo-el-repo-del-desk-tareas-go-bash-o-con-c-digo-en-otro.md
depends_on: []
pills: []
files:
- deskops/services/closeout_gates.py
- deskops/services/closure.py
- docs/workflow-policy-reference.md
- tests/test_closeout_gates.py
- tests/test_closeout_resolved_by.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# El closeout acepta tests de otros lenguajes y evidencia de commit de otro repo registrado

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de scion del 2026-11-16 (triaje del desk de scion). Tres tareas de la fase 0 del piloto scion estan hechas y verificadas pero closeout commit las bloquea: (1) el test es Go (cmd/build_context_test.go, commit f6e623c69 en scion) y reference_points_to_test en deskops/services/closeout_gates.py (linea 148; el chequeo de sufijo .py esta en la 168) exige .py; (2) un hook bash (hooks/pre-start-deskops.sh) validado con docker run no tiene forma de declarar su test; (3) una tarea del desk de scion cuyo codigo entro en deskops (4a7707a5, 4c745c18, 881e177a) e IR (5b8ce32): reference_points_to_commit (linea 196) solo resuelve ancestros del repo del desk. resolved-by tambien exige .py.

## Goal

_Describe the concrete result this task must produce._

(1) reference_points_to_test acepta, ademas de test_*.py, archivos de test de otros lenguajes con convencion reconocible (*_test.go, *.test.sh, *.bats) que existan en el repo; (2) una referencia de validacion de la forma runs/<run>/validation.log (archivo existente con el comando y su salida) cuenta como evidencia de tests para artefactos sin framework de tests; (3) una referencia repo:<nombre>@<sha> cuenta como evidencia de commit si <nombre> esta en el registro de repos (deskops repo / registro del ecosistema), su raiz existe en esta maquina y <sha> es ancestro de su HEAD. Lo mismo vale para closeout resolved-by.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/closeout_gates.py, deskops/services/closure.py (rama resolved-by), la doc de evidencia en docs/workflow-policy-reference.md y tests nuevos en tests/test_closeout_gates.py y tests/test_closeout_resolved_by.py. No entra: cerrar las tres tareas de scion (lo hace su coordinador despues), cambiar que evidencia exige cada tipo. Precisiones del preflight 1: la lista de sufijos es cerrada: *_test.go, *.test.sh, *.bats, y el archivo debe estar en files o references de la tarea y existir en el repo. Log de validacion: archivo bajo runs/ cuya primera linea empieza con '$ ' (el comando) y cuya ultima linea es 'rc=0'; se acepta para cualquier tarea, no hay que detectar 'sin framework'. La nota a scion es deskops message send --to scion con el hash del commit.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer closeout_gates.py:140-260. 2) Tabla de sufijos de test por lenguaje. 3) Validacion por log en runs/. 4) Resolver repo:<nombre>@<sha> con la misma funcion que usa message send --to (registro propio y luego el del ecosistema) y `git -C <raiz> merge-base --is-ancestor <sha> HEAD`. 5) Tests: un _test.go en files pasa; un .txt cualquiera no; un validation.log en runs/ pasa; repo:sldb@<sha ancestro> pasa y un sha inexistente no. 6) Nota a scion con el hash.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_resolved_by.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_test_paths.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los casos del paso 5 pasan, la doc de evidencia describe las tres formas nuevas y la nota a scion esta enviada con el hash.

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

FILE:tests/test_closeout_resolved_by.py
"""``deskops closeout resolved-by``: close a task whose work already entered the history."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.cli.main import main
from deskops.operations import DeskopsOperations
from deskops.services.closure import ClosureService

PR_URL = "https://github.com/example/repo/pull/42"
TEST_REF = "tests/test_thing.py"


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


BOARD = """---
id: board-tasks
scope: desk
tasks:
- desk/tasks/task-x.md
pills: []
rituals: []
tags: []
---

# Repo Board

## Purpose

Route the active task.

## Notes

No additional notes.

## Task Details
"""


def _task(files: list[str]) -> str:
    files_yaml = "files: []" if not files else "files:\n" + "".join(f"- {entry}\n" for entry in files).rstrip("\n")
    return f"""---
id: task-x
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
{files_yaml}
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Task X

## Rationale

The work entered main through a PR before the closeout.

## Goal

Close it honestly.

## Scope

Stay scoped.

## Implementation Path

Already merged.

## Validation

- pytest

## Done When

Closed.
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A git repo whose history already holds the task's work and its test."""
    return _make_repo(tmp_path / "repo")


def _make_repo(root: Path, task_text: str | None = None) -> Path:
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _write(root / ".gitignore", ".deskops.log\n")
    _write(root / "pkg" / "thing.py", "VALUE = 1\n")
    _write(root / "pkg" / "other.py", "def test_other():\n    assert True\n")
    _write(root / TEST_REF, "def test_thing():\n    assert True\n")
    _write(root / "checks" / "check_thing.py", "def test_check():\n    assert True\n")
    _git(root, "add", ".gitignore", "pkg", "tests", "checks")
    _git(root, "commit", "-q", "-m", "work merged through the PR")
    _write(root / "desk" / "tasks" / "Board.md", BOARD)
    _write(root / "desk" / "tasks" / "task-x.md", task_text or _task(["pkg/thing.py", "checks/check_thing.py"]))
    _git(root, "add", "desk/tasks")
    _git(root, "commit", "-q", "-m", "add task and board")
    return root


def _work_commit(root: Path) -> str:
    return _git(root, "rev-parse", "HEAD~1")


def _resolved_by(root: Path, *argv: str) -> int:
    return main(["closeout", "resolved-by", "--root", str(root), "--task", "task-x", *argv])


def _snapshot(root: Path) -> tuple[str, str, str]:
    """sha256 over desk/ (paths and bytes), git status and HEAD."""
    digest = hashlib.sha256()
    for path in sorted(p for p in (root / "desk").rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes() + b"\0")
    status = _git(root, "status", "--porcelain", "--untracked-files=all")
    return digest.hexdigest(), status, _git(root, "rev-parse", "HEAD")


def _capture_task_before_close(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """Record the task file as the closing commit sees it, before it is removed."""
    seen: dict[str, str] = {}
    original = ClosureService._close

    def spy(self: ClosureService, task_id: str, **kwargs):  # type: ignore[no-untyped-def]
        seen["task"] = self._task_path(task_id).read_text(encoding="utf-8")
        seen["route"] = kwargs["route"]
        return original(self, task_id, **kwargs)

    monkeypatch.setattr(ClosureService, "_close", spy)
    return seen


def test_resolved_by_closes_with_an_ancestor_commit_and_an_accepted_test(
    repo: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    seen = _capture_task_before_close(monkeypatch)
    ref = _work_commit(repo)
    head_before = _git(repo, "rev-parse", "HEAD")

    rc = _resolved_by(repo, "--reason", "Merged through PR 42", "--ref", ref, "--test", TEST_REF)

    out = capsys.readouterr().out
    assert rc == 0, out
    assert "resolved-by mode: Merged through PR 42" in out

    assert seen["route"] == "resolved-by"
    assert "status: resolved" in seen["task"]
    assert "- resolved-by" in seen["task"]

    assert _git(repo, "rev-parse", "HEAD~1") == head_before
    message = _git(repo, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: task-x"
    assert "Task-Id: task-x" in message
    assert "Closeout-Mode: resolved-by" in message
    assert "Closeout-Reason: Merged through PR 42" in message
    assert f"Closeout-Ref: {ref}" in message
    assert f"Closeout-Test: {TEST_REF}" in message
    assert _git(repo, "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)") == "resolved-by"

    assert not (repo / "desk" / "tasks" / "task-x.md").exists()
    assert "desk/tasks/task-x.md" not in (repo / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert _git(repo, "status", "--porcelain") == ""

    entry = json.loads((repo / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry == {
        "task_id": "task-x",
        "run_id": None,
        "run_dir": None,
        "commit": None,
        "session_sha256": None,
        "mode": "resolved-by",
    }
    assert sorted(_git(repo, "show", "--name-only", "--format=", "HEAD").splitlines()) == [
        "desk/tasks/Board.md",
        "desk/tasks/task-x.md",
        "runs/subagents/index.jsonl",
    ]


def test_resolved_by_accepts_a_pr_url_as_an_additional_ref(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    ref = _work_commit(repo)

    rc = _resolved_by(
        repo, "--reason", "Merged through PR 42", "--ref", ref, "--ref", PR_URL, "--test", TEST_REF
    )

    assert rc == 0, capsys.readouterr().out
    message = _git(repo, "log", "-1", "--format=%B")
    assert f"Closeout-Ref: {ref}" in message
    assert f"Closeout-Ref: {PR_URL}" in message
    refs = _git(repo, "log", "-1", "--format=%(trailers:key=Closeout-Ref,valueonly)").splitlines()
    assert refs == [ref, PR_URL]


def test_resolved_by_accepts_a_test_declared_in_the_task_files_and_several_tests(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rc = _resolved_by(
        repo,
        "--reason",
        "Merged through PR 42",
        "--ref",
        _work_commit(repo),
        "--test",
        TEST_REF,
        "--test",
        "checks/check_thing.py",
    )

    assert rc == 0, capsys.readouterr().out
    tests = _git(repo, "log", "-1", "--format=%(trailers:key=Closeout-Test,valueonly)").splitlines()
    assert tests == [TEST_REF, "checks/check_thing.py"]


def test_resolved_by_passes_paths_and_message_to_the_closing_commit(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write(repo / "notes.txt", "closing note\n")

    rc = _resolved_by(
        repo,
        "--reason",
        "Merged through PR 42",
        "--ref",
        _work_commit(repo),
        "--test",
        TEST_REF,
        "--message",
        "closeout: work merged in PR 42",
        "--paths",
        "notes.txt",
    )

    assert rc == 0, capsys.readouterr().out
    assert _git(repo, "log", "-1", "--format=%s") == "closeout: work merged in PR 42"
    assert "notes.txt" in _git(repo, "show", "--name-only", "--format=", "HEAD").splitlines()
    assert _git(repo, "status", "--porcelain") == ""


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        pytest.param(
            ["--reason", "Merged", "--ref", PR_URL, "--test", TEST_REF],
            "at least one --ref naming a commit",
            id="no-commit-ref-only-url",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "{commit}", "--ref", "desk/tasks/Board.md", "--test", TEST_REF],
            "Unresolvable --ref: desk/tasks/Board.md",
            id="ref-is-a-path-not-commit-or-url",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "not-a-ref", "--test", TEST_REF],
            "Unresolvable --ref: not-a-ref",
            id="ref-is-neither-commit-nor-url",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "0" * 40, "--test", TEST_REF],
            "Unresolvable --ref",
            id="ref-is-an-unknown-commit",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "{commit}", "--test", "tests/test_missing.py"],
            "Unresolvable --test: tests/test_missing.py",
            id="test-does-not-exist",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "{commit}", "--test", "pkg/other.py"],
            "Unresolvable --test: pkg/other.py",
            id="test-is-not-a-test-location",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "{commit}", "--test", TEST_REF, "--test", "tests/test_missing.py"],
            "Unresolvable --test: tests/test_missing.py",
            id="one-test-does-not-exist",
        ),
        pytest.param(
            ["--reason", "   ", "--ref", "{commit}", "--test", TEST_REF],
            "Resolved-by needs a non-empty --reason",
            id="blank-reason",
        ),
    ],
)
def test_resolved_by_refuses_and_writes_nothing(
    repo: Path, capsys: pytest.CaptureFixture[str], argv: list[str], expected: str
) -> None:
    commit = _work_commit(repo)
    argv = [commit if item == "{commit}" else item for item in argv]
    before = _snapshot(repo)

    rc = _resolved_by(repo, *argv)

    assert rc == 1
    assert expected in capsys.readouterr().out
    assert _snapshot(repo) == before
    assert not (repo / "runs").exists()


@pytest.mark.parametrize(
    ("argv", "flag"),
    [
        pytest.param(["--ref", "{commit}", "--test", TEST_REF], "--reason", id="no-reason"),
        pytest.param(["--reason", "Merged", "--test", TEST_REF], "--ref", id="no-ref"),
        pytest.param(["--reason", "Merged", "--ref", "{commit}"], "--test", id="no-test"),
    ],
)
def test_resolved_by_requires_reason_ref_and_test_flags(
    repo: Path, capsys: pytest.CaptureFixture[str], argv: list[str], flag: str
) -> None:
    commit = _work_commit(repo)
    argv = [commit if item == "{commit}" else item for item in argv]
    before = _snapshot(repo)

    rc = _resolved_by(repo, *argv)

    assert rc == 2
    assert flag in capsys.readouterr().err
    assert _snapshot(repo) == before


@pytest.mark.parametrize(
    ("refs", "tests", "expected"),
    [
        pytest.param(None, [TEST_REF], "at least one --ref naming a commit", id="service-no-refs"),
        pytest.param(["{commit}"], None, "at least one --test", id="service-no-tests"),
        pytest.param(["{commit}"], ["  "], "at least one --test", id="service-blank-test"),
    ],
)
def test_resolved_by_service_refuses_missing_evidence_and_writes_nothing(
    repo: Path, refs: list[str] | None, tests: list[str] | None, expected: str
) -> None:
    commit = _work_commit(repo)
    refs = None if refs is None else [commit if item == "{commit}" else item for item in refs]
    before = _snapshot(repo)

    outcome = ClosureService(repo, DeskopsOperations(repo)).close_resolved_by(
        "task-x", reason="Merged", refs=refs, tests=tests
    )

    assert outcome.exit_code == 1
    assert any(expected in line for line in outcome.messages)
    assert _snapshot(repo) == before


def test_resolved_by_refuses_an_unknown_task_and_writes_nothing(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    before = _snapshot(repo)

    rc = main(
        [
            "closeout",
            "resolved-by",
            "--root",
            str(repo),
            "--task",
            "task-missing",
            "--reason",
            "Merged",
            "--ref",
            _work_commit(repo),
            "--test",
            TEST_REF,
        ]
    )

    assert rc == 1
    assert "Task not found: task-missing" in capsys.readouterr().out
    assert _snapshot(repo) == before


def _incoherent_task(files: list[str]) -> str:
    """A legacy draft the model rejects: its history already handed it to closeout."""
    text = _task(files)
    return (
        text.replace("status: active\n", "status: draft\n")
        .replace("current_node: ritual-testing\n", "current_node: ritual-closeout\n")
        .replace("history:\n- task_activates\n", "history:\n- task_activates\n- task_hands_to_closeout\n")
    )


def _close_and_describe(root: Path, seen: dict[str, str]) -> dict[str, object]:
    """Close task-x by resolved-by and describe the closing commit, independent of the repo's hashes."""
    ref = _work_commit(root)
    rc = _resolved_by(root, "--reason", "Merged through PR 42", "--ref", ref, "--test", "checks/check_thing.py")
    return {
        "rc": rc,
        "message": _git(root, "log", "-1", "--format=%B").replace(ref, "<ref>"),
        "files": sorted(_git(root, "show", "--name-only", "--format=", "HEAD").splitlines()),
        "status": _git(root, "status", "--porcelain"),
        "index": (root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1],
        "task_status": yaml.safe_load(seen["task"].split("---\n")[1])["status"],
        "history": yaml.safe_load(seen["task"].split("---\n")[1])["history"],
    }


def test_resolved_by_closes_a_task_the_model_rejects_like_a_valid_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A legacy draft after task_hands_to_closeout is read from its frontmatter, as supersede
    does: the tests gate uses its declared files, and the closing commit, its trailers, the
    board, the index entry and the recorded status equal those of a valid task (no store)."""
    files = ["pkg/thing.py", "checks/check_thing.py"]
    from deskops import doc_access
    from deskops.models import TaskDoc

    invalid = _make_repo(tmp_path / "invalid", _incoherent_task(files))
    with pytest.raises(Exception, match="lifecycle is inconsistent"):
        doc_access.read_doc(invalid / "desk" / "tasks" / "task-x.md", TaskDoc)
    valid = _make_repo(tmp_path / "valid", _task(files))

    seen = _capture_task_before_close(monkeypatch)
    got = _close_and_describe(invalid, seen)
    assert got["rc"] == 0, capsys.readouterr().out
    expected = _close_and_describe(valid, seen)
    assert expected["rc"] == 0, capsys.readouterr().out

    # The history differs only by the legacy event the invalid task carried.
    assert expected["history"] == ["task_activates", "resolved-by"]
    assert {k: v for k, v in got.items() if k != "history"} == {k: v for k, v in expected.items() if k != "history"}
    assert got["task_status"] == "resolved"
    assert got["history"] == ["task_activates", "task_hands_to_closeout", "resolved-by"]
    assert "Closeout-Mode: resolved-by" in str(got["message"])
    assert "Closeout-Test: checks/check_thing.py" in str(got["message"])
    assert got["status"] == ""
    assert not (invalid / "desk" / "tasks" / "task-x.md").exists()

FILE:instruccion
Cold-bundle de la tarea task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_resolved_by.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_test_paths.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea


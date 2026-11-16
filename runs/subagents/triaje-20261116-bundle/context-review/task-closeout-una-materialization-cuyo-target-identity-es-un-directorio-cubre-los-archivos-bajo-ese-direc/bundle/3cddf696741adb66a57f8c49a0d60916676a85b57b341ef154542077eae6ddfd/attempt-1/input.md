FILE:desk/tasks/task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc.md
---
sldb:
  by: agent
  at: '2026-11-16T05:02:10Z'
  authority: generated
  via: save_document_payload
id: task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc
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
- desk/contexts/pill-materialization-contracts-declare-source-intent-and-target.md
files:
- deskops/services/closure.py
- tests/test_materialization_targets_outside_package.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
- atom-materializations-declare-source-atoms
from_drawer: desk/drawer/tasks/task-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md
---

# closeout: una materialization cuyo target_identity es un directorio cubre los archivos bajo ese directorio

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (cierre de SV01-SV04 en sldb, 2026-11-06): la compuerta atom|materialization exige un enlace por archivo; una materialization con target_identity src/sldb/notations (directorio) no cubrio ninguno de sus archivos y hubo que crear 62 materializations para 66 archivos. Hoy deskops/services/closure.py:1325-1340 busca la ruta exacta, y en sldb src/sldb/api/edges/project_graph/declared_target_nodes.py:52 exige is_file().

## Goal

_Describe the concrete result this task must produce._

En deskops, un archivo cambiado queda cubierto si alguna materialization de la tarea tiene un target_identity que es el mismo archivo o un directorio que lo contiene (comparacion por prefijo de ruta normalizada, con separador). Si `deskops graph missing` reporta missing_declared_target para un target que es directorio, se manda una nota a sldb pidiendo que declared_target_nodes acepte directorios, y esta tarea no espera esa respuesta.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/closure.py (alrededor de 1325-1340) y tests. No entra: modificar sldb (solo la nota), cambiar la compuerta de atomos. Precisiones del preflight 1: la funcion se llama target_covers(target, path) y vive junto a la cobertura de materializations en closure.py (se ubica por nombre, los numeros de linea son orientativos). Normalizacion: rutas POSIX relativas a la raiz del repo, sin resolver symlinks, sin barra final, sensibles a mayusculas; un target cubre un archivo si es igual o si path empieza con target + '/'. No hace falta que el directorio exista. La nota a sldb: titulo 'declared_target_nodes: aceptar un directorio como target declarado', cuerpo con la salida de graph missing y el caso; exito = nota entregada.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Funcion covers(target, path) por prefijo. 2) Usarla en la cobertura. 3) Test en tests/test_materialization_targets_outside_package.py: materialization con target 'pkg/sub' cubre 'pkg/sub/a.py' y no 'pkg/subzero.py'. 4) Correr graph missing en un desk sandbox con target directorio y, si falla, `deskops message send --to sldb`.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_materialization_targets_outside_package.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El test del paso 3 pasa; si el paso 4 fallo, la nota a sldb esta enviada y citada en el commit.

FILE:desk/contexts/pill-materialization-contracts-declare-source-intent-and-target.md
---
# pill-xxx
id: pill-materialization-contracts-declare-source-intent-and-target
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:materialization
- topic:provenance
---

# Guardrail: materialization contracts declare source, intent, and target

## What

_Define the context or guardrail this pill carries._

Treat materialization as an explicit contract from source atoms to target artifacts, with declared intent, target identity, and validation expectations.

## Why

_Explain why this context matters for safe execution._

Without an explicit contract, docs and projections drift away from their source atoms and become hard to audit or regenerate safely.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task defines materialization models, CLI commands, validation checks, or generated/projection metadata.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to source atom references, target artifact paths, projection metadata, and query surfaces for materialization status.

## How

_Describe the correct way to apply this guidance._

Require declared source references, stable target identity, and validation rules that can prove the target still matches the intended source contract.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not treat generated or derived docs as self-justifying. Do not leave target paths or source provenance implicit.

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

FILE:desk/atoms/knowledge-model/atom-materializations-declare-source-atoms.md
---
id: atom-materializations-declare-source-atoms
title: Materializations declare source atoms
five_wh_one_plus: how
tags:
- system:deskops
- topic:atoms
- topic:materialization
- topic:traceability
---

# Materializations declare source atoms

## Answer

Docs, specs, diagrams, tests, tasks, and other materialized artifacts should declare the atoms they use so readers and tools can trace a durable artifact back to the distilled project knowledge it expresses.

FILE:tests/test_materialization_targets_outside_package.py
"""Tests for materialization targets outside the indexed package.

These tests verify that MaterializationContractDoc.target_identity values pointing
to repo-relative paths outside desk/ and deskops/ become source_file graph nodes.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv],
        cwd=root,
        capture_output=True,
        text=True,
    )


def _sldb_cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sldb", *argv],
        cwd=root,
        capture_output=True,
        text=True,
    )


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    (root / ".gitignore").write_text(".deskops.log\n", encoding="utf-8")
    _git(root, "add", "seed.txt", ".gitignore")
    _git(root, "commit", "-q", "-m", "seed")
    return root


# --- Graph missing tests ---


def test_declared_target_outside_package_becomes_graph_node(tmp_path: Path) -> None:
    """A materialization target outside desk/ and deskops/ becomes a source_file node."""
    root = _make_repo(tmp_path)

    # Initialize deskops
    result = _cli(root, "init", str(root))
    assert result.returncode == 0, result.stderr

    # Create real target files
    _write(root / "src/vsm/organs/links.py", "# Source\n")
    _write(root / ".github/workflows/pulse.yml", "name: Pulse\n")

    # Create an atom
    result = _cli(
        root,
        "add", "atom",
        "--root", str(root),
        "--title", "CI/CD workflow",
        "--five-wh-one-plus", "how",
        "--answer", "The CI/CD workflow is defined by the pulse and ci YAML files.",
        "--tags", "topic:ci",
    )
    assert result.returncode == 0, result.stderr

    # Create materializations pointing to those files
    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Links implementation",
        "--source-atoms", "atom-ci-cd-workflow",
        "--target-kind", "source_file",
        "--target-identity", "src/vsm/organs/links.py",
        "--intent", "The links module implements the CI/CD workflow.",
    )
    assert result.returncode == 0, result.stderr

    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Pulse workflow",
        "--source-atoms", "atom-ci-cd-workflow",
        "--target-kind", "config_file",
        "--target-identity", ".github/workflows/pulse.yml",
        "--intent", "The pulse workflow defines CI/CD.",
    )
    assert result.returncode == 0, result.stderr

    # graph missing should exit 0 (no missing targets)
    result = _cli(root, "graph", "missing", "--root", str(root))
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"


def test_declared_target_missing_file_stays_missing(tmp_path: Path) -> None:
    """A materialization target pointing to a nonexistent file is missing_declared_target."""
    root = _make_repo(tmp_path)

    result = _cli(root, "init", str(root))
    assert result.returncode == 0, result.stderr

    # Create an atom
    result = _cli(
        root,
        "add", "atom",
        "--root", str(root),
        "--title", "Missing file test",
        "--five-wh-one-plus", "what",
        "--answer", "Test for missing target.",
        "--tags", "topic:test",
    )
    assert result.returncode == 0, result.stderr

    # Create a materialization pointing to a nonexistent file
    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Missing target",
        "--source-atoms", "atom-missing-file-test",
        "--target-kind", "source_file",
        "--target-identity", "src/missing.py",
        "--intent", "This target does not exist.",
    )
    assert result.returncode == 0, result.stderr

    # graph missing should exit 1 with missing_declared_target
    result = _cli(root, "graph", "missing", "--root", str(root))
    assert result.returncode == 1, f"stdout: {result.stdout}\nstderr: {result.stderr}"
    assert "missing_declared_target" in result.stdout
    assert "src/missing.py" in result.stdout


# --- Materialization tracking tests ---


def test_add_materialization_tracks_document_in_store(tmp_path: Path) -> None:
    """deskops add materialization tracks the created document in the .sldb store."""
    root = _make_repo(tmp_path)

    result = _cli(root, "init", str(root))
    assert result.returncode == 0, result.stderr

    # Create an atom first
    result = _cli(
        root,
        "add", "atom",
        "--root", str(root),
        "--title", "Tracking test atom",
        "--five-wh-one-plus", "what",
        "--answer", "Test for store tracking.",
        "--tags", "topic:test",
    )
    assert result.returncode == 0, result.stderr

    # Create a target file
    _write(root / "src/tracked.py", "# Source\n")

    # Create a materialization
    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Tracked materialization",
        "--source-atoms", "atom-tracking-test-atom",
        "--target-kind", "source_file",
        "--target-identity", "src/tracked.py",
        "--intent", "Test that materializations are tracked.",
    )
    assert result.returncode == 0, result.stderr

    # Check store tracking with sldb stores check
    result = _sldb_cli(root, "stores", "check", "--store", str(root / ".sldb"), "--format", "json")
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"

    check_data = json.loads(result.stdout)
    models = check_data.get("models", [])

    # Find MaterializationContractDoc in models
    materialization_model = next(
        (m for m in models if m.get("name") == "MaterializationContractDoc"),
        None,
    )
    assert materialization_model is not None, f"MaterializationContractDoc not found in {models}"

    # The materialization should be tracked
    documents = materialization_model.get("documents", [])
    assert any(
        "materialization-tracked-materialization" in str(doc)
        for doc in documents
    ), f"Materialization not tracked: {documents}"


# --- Closeout tests ---


def test_closeout_verify_accepts_materialization_coverage(tmp_path: Path) -> None:
    """closeout verify accepts materializations as changed-file coverage."""
    root = _make_repo(tmp_path)

    result = _cli(root, "init", str(root))
    assert result.returncode == 0, result.stderr

    # Create target files
    _write(root / "src/vsm/organs/links.py", "# Links source\n")
    _write(root / ".github/workflows/pulse.yml", "name: Pulse\n")

    # Create an atom
    result = _cli(
        root,
        "add", "atom",
        "--root", str(root),
        "--title", "Closeout test atom",
        "--five-wh-one-plus", "how",
        "--answer", "Atom for closeout verification.",
        "--tags", "topic:closeout",
    )
    assert result.returncode == 0, result.stderr

    # Create materializations for those files
    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Links materialization",
        "--source-atoms", "atom-closeout-test-atom",
        "--target-kind", "source_file",
        "--target-identity", "src/vsm/organs/links.py",
        "--intent", "Links implementation materialization.",
    )
    assert result.returncode == 0, result.stderr

    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Pulse materialization",
        "--source-atoms", "atom-closeout-test-atom",
        "--target-kind", "config_file",
        "--target-identity", ".github/workflows/pulse.yml",
        "--intent", "Pulse workflow materialization.",
    )
    assert result.returncode == 0, result.stderr

    # Create a task that lists those files
    _write(
        root / "desk/tasks/task-closeout-test.md",
        """---
id: task-closeout-test
status: active
current_node: ritual-testing
history:
- task_activates
references:
- tests/test_materialization_targets_outside_package.py
depends_on: []
pills: []
files:
- src/vsm/organs/links.py
- .github/workflows/pulse.yml
tags: []
---

# Closeout Test Task

## Rationale

Test closeout verification.

## Goal

Verify closeout works.

## Scope

In scope.

## Implementation Path

Implement.

## Validation

- pytest

## Done When

Done.
""",
    )
    # Since CC35b the task selector resolves through the store only: a task written by hand
    # is tracked as `deskops add task` would track it (the CC35b a7 adaptation).
    from deskops import doc_access
    from deskops.models import TaskDoc

    doc_access.track_created_document(
        root, TaskDoc, root / "desk/tasks/task-closeout-test.md", "task-closeout-test"
    )

    # Create board
    _write(
        root / "desk/tasks/Board.md",
        """---
id: Board
title: Board
scope: test
purpose: test
tasks:
- desk/tasks/task-closeout-test.md
tags: []
---

# Board
""",
    )

    # Commit everything so we have a commit reference
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "setup closeout test")
    commit_sha = _git(root, "rev-parse", "HEAD")

    # Add commit to task references
    _write(
        root / "desk/tasks/task-closeout-test.md",
        f"""---
id: task-closeout-test
status: active
current_node: ritual-testing
history:
- task_activates
references:
- tests/test_materialization_targets_outside_package.py
- {commit_sha}
depends_on: []
pills: []
files:
- src/vsm/organs/links.py
- .github/workflows/pulse.yml
tags: []
---

# Closeout Test Task

## Rationale

Test closeout verification.

## Goal

Verify closeout works.

## Scope

In scope.

## Implementation Path

Implement.

## Validation

- pytest

## Done When

Done.
""",
    )

    # Copy test file as evidence
    import shutil
    (root / "tests").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(__file__, root / "tests" / Path(__file__).name)

    # Commit the task update
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "add commit reference")

    # closeout verify should have no missing_changed_file_link
    result = _cli(
        root,
        "closeout", "verify",
        "--root", str(root),
        "--task", "task-closeout-test",
    )
    output = json.loads(result.stdout)

    # Check that there's no missing_changed_file_link finding
    findings = output.get("findings", [])
    missing_link_findings = [
        f for f in findings
        if f.get("code") == "missing_changed_file_link"
    ]
    assert not missing_link_findings, f"Unexpected missing_changed_file_link: {missing_link_findings}"

FILE:instruccion
Cold-bundle de la tarea task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_materialization_targets_outside_package.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea


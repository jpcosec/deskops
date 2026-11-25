FILE:desk/tasks/task-closeout-verify-no-trata-como-artefacto-generado-un-golden-json-que-tiene-un-golden-yaml-hermano-baj.md
---
sldb:
  by: agent
  at: '2026-11-17T13:34:18Z'
  authority: generated
  via: create_document
id: task-closeout-verify-no-trata-como-artefacto-generado-un-golden-json-que-tiene-un-golden-yaml-hermano-baj
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/closure.py
- tests/test_closeout_declared_evidence.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# closeout verify no trata como artefacto generado un golden json que tiene un golden yaml hermano bajo tests/fixtures

## Rationale

_Explain why this task exists or the business driver behind it._

Al cerrar la tarea de ack --reason (97649c61), closeout verify dio generated_artifact_missing_declared_sources para tests/fixtures/golden/output/message_ack.json y message_read.json: _generated_artifact_source_finding en deskops/services/closure.py (alrededor de la linea 1583) trata un .json o .md con un .yaml, .yml o .mmd hermano como proyeccion renderizada que debe declarar source_atoms o provenance. Bajo tests/fixtures/golden/output/ el json y el yaml son dos goldens independientes (la misma salida en dos formatos), no uno generado del otro, y un golden no puede llevar provenance sin cambiar su contenido. El hallazgo bloquea el gate atom|materialization del cierre.

## Goal

_Describe the concrete result this task must produce._

closeout verify no da generated_artifact_missing_declared_sources para archivos bajo tests/fixtures/ (goldens y fixtures de test); fuera de tests/fixtures/ el chequeo sigue igual.

## Scope

_State what is in scope and what is out of scope._

Entra: _generated_artifact_source_finding (o _find_generated_artifact_source_sibling) en deskops/services/closure.py y tests en tests/test_closeout_declared_evidence.py. Sale: la regla para docs, diagramas y artefactos fuera de tests/fixtures/.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer _generated_artifact_source_finding y donde se llama. 2) Excluir las rutas bajo tests/fixtures/. 3) Tests en desk sandbox (tmp_path): un par json/yaml bajo tests/fixtures/golden/output/ en files de la tarea no da el hallazgo; un .md con un .yaml hermano fuera de tests/fixtures/ lo sigue dando.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos pasan (golden bajo tests/fixtures sin hallazgo; artefacto fuera de tests/fixtures con hallazgo) y los dos archivos de la Validation pasan.

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

FILE:tests/test_closeout_declared_evidence.py
"""Closeout evidence is the task type's, and closeout checks exactly that (CC33b).

The kinds come from the type (``closeout-evidence.yaml``); ``closeout_evidence`` only adds
kinds, and an added kind only alerts when it fails (DA5). ``closeout verify`` writes the
evidence receipts and ``closeout commit`` evaluates the type's closeout rule on them. Four
classes of task (code, docs, spec/design, external), the task without a type gated as code,
the never-silent .py alert, the 'esta tarea declaró X; encontré Y' line, and the add-task
failure without a declaration.
"""
from __future__ import annotations

from pathlib import Path
import json
import shutil
import subprocess
import sys

import pytest
import yaml

from closeout_desk import store_repo
from closeout_desk import track_task
from test_closeout import _git, _write, _write_board

CLI = [sys.executable, "-m", "deskops"]
TASK_ID = "task-x"
TASK_REL = f"desk/tasks/{TASK_ID}.md"
URL = "https://linear.app/example/issue/LIN-1"
IMPLICIT_RULE = Path(__file__).resolve().parents[1] / "deskops" / "data" / "rules" / "rule-closeout-alert-implicit-code.md"


@pytest.fixture
def repo(lifecycle_desk: Path) -> Path:
    return store_repo(lifecycle_desk)


def _write_declared_task(
    root: Path,
    *,
    task_type: str | None,
    references: list[str],
    files: list[str],
    evidence: list[str] | None = None,
) -> None:
    """A routed, committed, tracked task; ``task_type=None`` writes a task that predates types."""
    payload: dict = {
        "id": TASK_ID,
        "status": "active",
        "current_node": "ritual-testing",
        "history": ["task_activates"],
        "references": references,
        "depends_on": [],
        "pills": [],
        "files": files,
        "tags": [],
    }
    if task_type is not None:
        payload["task_type"] = task_type
    if evidence is not None:
        payload["closeout_evidence"] = evidence
    _write(
        root / TASK_REL,
        "---\n" + yaml.safe_dump(payload, sort_keys=False) + "---\n\n# Task X\n\n"
        "## Rationale\n\nNot provided.\n\n## Goal\n\nClose.\n\n## Scope\n\nScoped.\n\n"
        "## Implementation Path\n\nDo it.\n\n## Validation\n\n- pytest\n\n## Done When\n\nClosed.\n",
    )
    _write_board(root, TASK_ID)
    track_task(root, TASK_ID)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "route task")


def _cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*CLI, *argv, "--root", str(root)], cwd=root, capture_output=True, text=True)


def _verify(root: Path) -> tuple[dict, subprocess.CompletedProcess[str]]:
    result = _cli(root, "closeout", "verify", "--task", TASK_ID)
    assert result.stdout.strip(), result.stderr
    return json.loads(result.stdout), result


def _commit_no_run(root: Path, *paths: str) -> subprocess.CompletedProcess[str]:
    argv = ["closeout", "commit", "--task", TASK_ID, "--no-run", "--reason", "closed by the supervisor"]
    if paths:
        argv += ["--paths", *paths]
    return _cli(root, *argv)


# ---------------------------------------------------------------- external
def test_external_task_with_a_url_closes_with_no_run(repo: Path) -> None:
    root = repo
    _write_declared_task(root, task_type="task.external", references=[URL], files=[])

    report, result = _verify(root)
    assert report["ok"], report
    assert report["declared"] == ["external"]
    assert report["found"] == ["external"]
    assert set(report["gates"]) == {"external"}
    assert report["alerts"] == []
    assert "Closeout gate: esta tarea declaró external; encontré external" in result.stderr

    closed = _commit_no_run(root, TASK_REL)
    assert closed.returncode == 0, closed.stdout + closed.stderr
    assert "esta tarea declaró external; encontré external" in closed.stdout
    assert not (root / TASK_REL).exists()
    message = _git(root, "log", "-1", "--format=%B")
    assert f"Task-Id: {TASK_ID}" in message and "Closeout-Mode: manual" in message


def test_external_task_without_a_url_stays_blocked(repo: Path) -> None:
    root = repo
    _write_declared_task(root, task_type="task.external", references=["not a url"], files=[])
    before = _git(root, "rev-parse", "HEAD")

    report, _ = _verify(root)
    assert not report["ok"]
    assert report["found"] == []
    assert report["summary"] == "esta tarea declaró external; encontré nada"
    assert [item["code"] for item in report["findings"]] == ["missing_external_evidence"]

    closed = _commit_no_run(root, TASK_REL)
    assert closed.returncode == 1
    assert "esta tarea declaró external; encontré nada" in closed.stdout
    assert "[rules/rule-closeout-task-external]" in closed.stdout and 'fact = "external"' in closed.stdout
    assert _git(root, "rev-parse", "HEAD") == before
    assert (root / TASK_REL).exists()


# ---------------------------------------------------------------- code
def test_code_task_without_tests_stays_blocked(repo: Path) -> None:
    root = repo
    _write(root / "feature.py", "x = 1\n")
    commit = _git(root, "rev-parse", "HEAD")
    _write_declared_task(root, task_type="task.code", references=[commit], files=["feature.py"])
    before = _git(root, "rev-parse", "HEAD")

    report, _ = _verify(root)
    assert not report["ok"]
    assert report["declared"] == ["tests", "commit", "atom", "materialization"]
    assert "tests" not in report["found"] and "commit" in report["found"]
    assert not report["gates"]["tests"]["ok"]
    assert "missing_tests_evidence" in {item["code"] for item in report["findings"]}
    assert "esta tarea declaró tests, commit, atom|materialization; encontré " in report["summary"]

    closed = _commit_no_run(root, "feature.py", TASK_REL)
    assert closed.returncode == 1
    assert "[rules/rule-closeout-task-code]" in closed.stdout and 'fact = "tests"' in closed.stdout
    assert "esta tarea declaró tests, commit, atom|materialization" in closed.stdout
    assert _git(root, "rev-parse", "HEAD") == before


def test_code_task_with_its_evidence_closes(repo: Path) -> None:
    root = repo
    (root / "tests").mkdir(exist_ok=True)
    shutil.copyfile(__file__, root / "tests" / Path(__file__).name)
    _write(root / "feature.py", "x = 1\n")
    _git(root, "add", "tests", "feature.py")
    _git(root, "commit", "-q", "-m", "feature")
    refs = [f"tests/{Path(__file__).name}", _git(root, "rev-parse", "HEAD")]
    _write_declared_task(root, task_type="task.code", references=refs, files=["feature.py"])

    report, _ = _verify(root)
    assert report["ok"], report
    assert report["found"] == ["tests", "atom|materialization (exento: sin atoms locales)", "commit"]
    assert report["alerts"] == []

    closed = _commit_no_run(root, TASK_REL)
    assert closed.returncode == 0, closed.stdout + closed.stderr
    assert "esta tarea declaró tests, commit, atom|materialization; encontré tests" in closed.stdout


def test_python_changes_without_declared_tests_alert_but_do_not_block(repo: Path) -> None:
    root = repo
    _write_declared_task(root, task_type="task.external", references=[URL], files=["feature.py"])

    report, result = _verify(root)
    assert report["ok"], report
    assert set(report["gates"]) == {"external"}
    assert [alert["code"] for alert in report["alerts"]] == ["python_changes_without_declared_tests"]
    assert "feature.py" in report["alerts"][0]["message"]
    assert "ALERTA python_changes_without_declared_tests" in result.stderr

    _write(root / "feature.py", "x = 1\n")
    closed = _commit_no_run(root, "feature.py", TASK_REL)
    assert closed.returncode == 0, closed.stdout + closed.stderr
    assert "ALERTA python_changes_without_declared_tests" in closed.stdout


def test_task_without_a_type_is_gated_as_code_and_the_implicit_rule_names_it(repo: Path) -> None:
    from sldb.api import where_matches

    from deskops import doc_access
    from deskops.models import TaskDoc

    root = repo
    _write_declared_task(root, task_type=None, references=[], files=["seed.txt"])

    report, _ = _verify(root)
    assert not report["ok"]
    assert report["implicit_code"] is True
    assert report["declared"] == ["tests", "commit", "atom", "materialization"]
    assert "missing_tests_evidence" in {item["code"] for item in report["findings"]}
    # The alert is the on_write rule rule-closeout-alert-implicit-code, not a verify alert.
    assert "closeout_evidence_not_declared" not in {alert["code"] for alert in report["alerts"]}
    condition = yaml.safe_load(IMPLICIT_RULE.read_text(encoding="utf-8").split("---", 2)[1])["condition"]
    assert not where_matches(condition, doc_access.read_doc(root / TASK_REL, TaskDoc))


# ---------------------------------------------------------------- docs, spec, design
@pytest.mark.parametrize("suffix", ["docs", "spec", "design"])
def test_document_class_task_closes_with_commit_and_document(repo: Path, suffix: str) -> None:
    root = repo
    _write(root / "docs" / f"{suffix}.md", f"# {suffix}\n")
    _git(root, "add", "docs")
    _git(root, "commit", "-q", "-m", suffix)
    refs = [_git(root, "rev-parse", "HEAD"), f"docs/{suffix}.md"]
    _write_declared_task(root, task_type="task.docs", references=refs, files=[f"docs/{suffix}.md"])

    report, _ = _verify(root)
    assert report["ok"], report
    assert set(report["gates"]) == {"commit", "document"}
    assert report["found"] == ["commit", "document"]
    assert report["alerts"] == []

    closed = _commit_no_run(root, TASK_REL)
    assert closed.returncode == 0, closed.stdout + closed.stderr
    assert "esta tarea declaró commit, document; encontré commit, document" in closed.stdout


def test_document_task_without_a_document_stays_blocked(repo: Path) -> None:
    root = repo
    commit = _git(root, "rev-parse", "HEAD")
    # A test source and a missing path are not documents.
    _write(root / "tests" / "test_a.py", "")
    _write_declared_task(
        root, task_type="task.docs", references=[commit, "tests/test_a.py", "docs/missing.md"], files=[]
    )

    report, _ = _verify(root)
    assert not report["ok"]
    assert report["found"] == ["commit"]
    assert [item["code"] for item in report["findings"]] == ["missing_document_evidence"]


def test_an_added_kind_outside_the_vocabulary_is_an_alert(repo: Path) -> None:
    root = repo
    _write_declared_task(root, task_type="task.external", references=[URL], files=[], evidence=["external", "vibes"])

    report, _ = _verify(root)
    assert report["ok"], report
    assert "unknown_closeout_evidence" in {alert["code"] for alert in report["alerts"]}
    assert report["findings"] == []


# ---------------------------------------------------------------- add task
@pytest.fixture
def desk_repo(lifecycle_desk: Path) -> Path:
    return lifecycle_desk


def _declared(root: Path, task_id: str) -> list[str]:
    frontmatter = (root / "desk" / "tasks" / f"{task_id}.md").read_text(encoding="utf-8").split("---", 2)[1]
    return yaml.safe_load(frontmatter).get("closeout_evidence") or []


def test_add_task_without_evidence_nor_task_type_defaults_to_code(desk_repo: Path) -> None:
    result = _cli(desk_repo, "add", "task", "--title", "Undeclared")
    assert result.returncode == 0
    assert "defaulting to task.code" in result.stdout
    assert _declared(desk_repo, "task-undeclared") == []


def test_add_task_with_an_unknown_task_type_fails_listing_types(desk_repo: Path) -> None:
    result = _cli(desk_repo, "add", "task", "--title", "Odd", "--task-type", "reflection")
    assert result.returncode == 1
    assert "'reflection' is not a registered task type" in result.stdout
    assert "task.code" in result.stdout


def test_add_task_rejects_evidence_outside_the_vocabulary(desk_repo: Path) -> None:
    result = _cli(desk_repo, "add", "task", "--title", "Bad", "--evidence", "vibes")
    assert result.returncode == 1
    assert "Unknown closeout evidence 'vibes'" in result.stdout


@pytest.mark.parametrize(
    "task_type,slug",
    [
        ("task.code", "task-typed-task-code"),
        ("task.docs", "task-typed-task-docs"),
        ("task.external", "task-typed-task-external"),
    ],
)
def test_add_task_type_leaves_closeout_evidence_to_the_type(desk_repo: Path, task_type: str, slug: str) -> None:
    result = _cli(desk_repo, "add", "task", "--title", f"Typed {task_type}", "--task-type", task_type)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _declared(desk_repo, slug) == []


def test_evidence_can_only_add_to_the_type_floor(desk_repo: Path) -> None:
    result = _cli(desk_repo, "add", "task", "--title", "Explicit", "--task-type", "task.code", "--evidence", "commit", "document")
    assert result.returncode == 1
    assert "--evidence removes closeout evidence the task type requires" in result.stdout

    added = _cli(desk_repo, "add", "task", "--title", "Added", "--task-type", "task.code", "--evidence", "tests", "commit", "atom", "materialization", "document")
    assert added.returncode == 0, added.stdout + added.stderr
    assert _declared(desk_repo, "task-added") == ["tests", "commit", "atom", "materialization", "document"]


def test_evidence_alone_defaults_to_code_floor(desk_repo: Path) -> None:
    result = _cli(desk_repo, "add", "task", "--title", "Only evidence", "--evidence", "external")
    assert result.returncode == 1
    assert "--evidence removes closeout evidence the task type requires" in result.stdout


# ---------------------------------------------------------------- verify --run-dir
RUN_DIR_REL = "runs/subagents/20260101-000000-task-x"
RUN_EVIDENCE = ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]


def _run_dir(root: Path, *names: str) -> Path:
    run_dir = root / RUN_DIR_REL
    run_dir.mkdir(parents=True, exist_ok=True)
    for name in names:
        _write(run_dir / name, f"{name}\n")
    return run_dir


def test_verify_with_an_incomplete_run_dir_names_the_missing_file_like_commit(repo: Path) -> None:
    root = repo
    _write_declared_task(root, task_type="task.external", references=[URL], files=[])
    run_dir = _run_dir(root, *(name for name in RUN_EVIDENCE if name != "task.txt"))

    result = _cli(root, "closeout", "verify", "--task", TASK_ID, "--run-dir", RUN_DIR_REL)
    assert result.stdout.strip(), result.stderr
    report = json.loads(result.stdout)
    assert result.returncode == 1
    assert report["ok"] is False
    expected = f"Missing required evidence in {run_dir.resolve()}: task.txt"
    assert {"code": "missing_run_evidence", "message": expected} in report["findings"]
    # The declared evidence itself was found; only the run dir is short.
    assert report["found"] == ["external"]

    before = _git(root, "rev-parse", "HEAD")
    closed = _cli(root, "closeout", "commit", "--task", TASK_ID, "--run-dir", RUN_DIR_REL, "--paths", TASK_REL)
    assert closed.returncode != 0
    assert expected in closed.stdout + closed.stderr
    assert _git(root, "rev-parse", "HEAD") == before


def test_verify_with_a_complete_run_dir_is_ok(repo: Path) -> None:
    root = repo
    _write_declared_task(root, task_type="task.external", references=[URL], files=[])
    _run_dir(root, *RUN_EVIDENCE)

    result = _cli(root, "closeout", "verify", "--task", TASK_ID, "--run-dir", RUN_DIR_REL)
    assert result.stdout.strip(), result.stderr
    report = json.loads(result.stdout)
    assert result.returncode == 0, result.stdout + result.stderr
    assert report["ok"] is True
    assert report["findings"] == []


def test_verify_without_run_dir_ignores_run_evidence(repo: Path) -> None:
    root = repo
    _write_declared_task(root, task_type="task.external", references=[URL], files=[])
    _run_dir(root)  # an empty run dir exists, but verify was not pointed at it

    report, result = _verify(root)
    assert result.returncode == 0
    assert report["ok"] is True
    assert all(finding.get("code") != "missing_run_evidence" for finding in report["findings"])


def test_commit_and_verify_share_the_run_evidence_helper(tmp_path: Path) -> None:
    from deskops.services.closure import ClosureService

    (tmp_path / "board.txt").write_text("b\n", encoding="utf-8")
    assert ClosureService.missing_run_evidence(tmp_path) == ["task.txt", "git-status.txt", "result-summary.md"]
    source = (Path(__file__).resolve().parents[1] / "deskops" / "services" / "closure.py").read_text(encoding="utf-8")
    assert source.count("self.missing_run_evidence(resolved_run_dir)") == 2


# ---------------------------------------------------------------- receipts follow the verdict
def _evidence_receipts(root: Path, fact: str) -> list[dict]:
    directory = root / "desk" / "reviews" / TASK_ID
    receipts = []
    for path in sorted(directory.glob(f"evidence-{fact}-*.md")):
        receipts.append(yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]))
    return receipts


def _code_task_with_its_evidence(root: Path) -> None:
    (root / "tests").mkdir(exist_ok=True)
    shutil.copyfile(__file__, root / "tests" / Path(__file__).name)
    _write(root / "feature.py", "x = 1\n")
    _git(root, "add", "tests", "feature.py")
    _git(root, "commit", "-q", "-m", "feature")
    refs = [f"tests/{Path(__file__).name}", _git(root, "rev-parse", "HEAD")]
    _write_declared_task(root, task_type="task.code", references=refs, files=["feature.py"])


def test_a_changed_verdict_on_the_same_input_writes_a_new_receipt_and_unblocks_closeout(repo: Path) -> None:
    from deskops.operations import DeskopsOperations

    root = repo
    _code_task_with_its_evidence(root)
    closure = DeskopsOperations(root).closure
    green = closure.verify_task_closeout(TASK_ID)["gates"]
    red = json.loads(json.dumps(green))
    red["tests"].update(ok=False, findings=[{"code": "tests_failed", "message": "the suite is red"}])
    # The gate in red: same tests items, verdict rejected.
    written = closure._write_evidence_receipts(root / TASK_REL, TASK_ID, ["tests"], red)
    assert written == [f"review-{TASK_ID}-evidence-tests-1"]
    assert [r["verdict"] for r in _evidence_receipts(root, "tests")] == ["rejected"]

    # Fixed without changing the fact's input: verify writes the accepted receipt.
    report, _ = _verify(root)
    assert report["ok"], report
    receipts = _evidence_receipts(root, "tests")
    assert [r["verdict"] for r in receipts] == ["rejected", "accepted"]
    assert receipts[0]["input_sha256"] == receipts[1]["input_sha256"]

    closed = _commit_no_run(root, TASK_REL)
    assert closed.returncode == 0, closed.stdout + closed.stderr
    assert "[rules/rule-closeout-task-code]" not in closed.stdout

    # Symmetric: back to rejected on the same input writes yet another receipt.
    assert closure._write_evidence_receipts(root / TASK_REL, TASK_ID, ["tests"], red) == [
        f"review-{TASK_ID}-evidence-tests-3"
    ]


def test_two_green_verifies_do_not_duplicate_receipts(repo: Path) -> None:
    root = repo
    _code_task_with_its_evidence(root)
    first, _ = _verify(root)
    assert first["ok"], first
    directory = root / "desk" / "reviews" / TASK_ID
    before = sorted(path.name for path in directory.glob("evidence-*.md"))
    assert before
    second, _ = _verify(root)
    assert second["ok"], second
    assert sorted(path.name for path in directory.glob("evidence-*.md")) == before

FILE:instruccion
Cold-bundle de la tarea task-closeout-verify-no-trata-como-artefacto-generado-un-golden-json-que-tiene-un-golden-yaml-hermano-baj: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py


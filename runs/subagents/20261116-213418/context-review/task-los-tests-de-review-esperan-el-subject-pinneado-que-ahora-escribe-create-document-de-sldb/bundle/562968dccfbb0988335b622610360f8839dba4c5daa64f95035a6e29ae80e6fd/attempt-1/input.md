FILE:desk/tasks/task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb.md
---
sldb:
  by: agent
  at: '2026-11-16T21:32:42Z'
  authority: generated
  via: create_document
id: task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb
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
- tests/test_review_record.py
- tests/test_review_command.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# los tests de review esperan el subject pinneado que ahora escribe create_document de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

sldb 477d1bc0 (closeout aacb03cc, task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload) hizo que create_document pinnee las anclas a documentos (doc:<Modelo>:<id>@sha256:<hash>) igual que save_document_payload. Desde entonces la suite de deskops sobre origin/main da 3 fallas (integrador wA:p1, 2026-11-16): tests/test_review_record.py::test_subject_is_pinned_and_the_anchor_is_intact, tests/test_review_record.py::test_a_short_selector_keys_and_anchors_receipts_on_the_full_task_id y tests/test_review_command.py::test_preflight_writes_attempt_evidence_and_receipt esperan el subject sin pin ('doc:TaskCodeDoc:task-x'). sldb ajusto sus propias expectativas igual (tests/api/test_doc_anchors.py de sldb).

## Goal

_Describe the concrete result this task must produce._

Los tres tests esperan el subject pinneado que escribe hoy create_document al registrar un recibo, y pasan contra el sldb de origin/main; el codigo de deskops no cambia.

## Scope

_State what is in scope and what is out of scope._

Entra: solo las aserciones sobre el campo subject de los recibos (y el docstring que dice que create_document no pinnea) en tests/test_review_record.py y tests/test_review_command.py. Cada aserccion de igualdad exacta con 'doc:TaskCodeDoc:<id>' sobre un recibo recien creado pasa a exigir el valor pinneado con la misma forma que ya usa la aserccion de la linea 266 de tests/test_review_record.py: re.fullmatch(r'doc:TaskCodeDoc:<id>@sha256:[0-9a-f]{64}', subject). El docstring de test_subject_is_pinned_and_the_anchor_is_intact se corrige: sldb pinnea al crear y al guardar. Sale: el codigo de deskops (deskops/), sldb, otros tests y cualquier aserccion que no sea sobre subject. Si un test falla por otra causa, el ejecutor para y lo informa.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr los dos archivos de test y confirmar que fallan solo por el subject sin pin (guardar la salida). 2) Cambiar cada aserccion de subject sin pin por el fullmatch con @sha256:[0-9a-f]{64}; donde el test ya compara con el id completo de la tarea, usar re.escape del valor esperado. 3) Corregir el docstring. 4) Correr la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_record.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && git diff --stat (solo los dos archivos de test)

## Done When

_Name the observable condition that makes the task complete._

Los dos archivos de test pasan contra el sldb instalado (origin/main con 477d1bc0) y git diff solo toca tests/test_review_record.py y tests/test_review_command.py.

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

FILE:tests/test_review_record.py
"""``deskops review record``: reproduction, goldens and owner receipts without a model call.

Follow-up of CC32 (decisions r1-r8, precisions b1-b4 of the TaskDoc). The receipt is written
by whoever operates the desk with the evidence they checked: ``verdict: pending``,
``engine: human``, ``actor`` from the desk identity, ``input_sha256`` over the sorted evidence
(b1) and the evidence paths in ``summary`` (b4). ``deskops review dispose`` gives the verdict.
A ``pi`` that only logs its calls is first on ``PATH``, so a test would see a model call.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from sldb.api import check_doc_anchors
from sldb.runtime.validation import extract_model_data

from deskops.models import ReviewDoc


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
SHA256 = re.compile(r"^[0-9a-f]{64}$")

LOGGING_PI = """#!/usr/bin/env python3
import os
import sys

with open(os.environ["FAKE_PI_LOG"], "a", encoding="utf-8") as handle:
    handle.write(" ".join(sys.argv[1:]) + "\\n")
sys.exit(1)
"""


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    return env


def _deskops(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*CLI, *argv, "--root", str(root)], cwd=root, env=_env(), capture_output=True, text=True
    )


@pytest.fixture
def pi_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pi = bin_dir / "pi"
    pi.write_text(LOGGING_PI, encoding="utf-8")
    pi.chmod(0o755)
    log = tmp_path / "pi.log"
    monkeypatch.setenv("FAKE_PI_LOG", str(log))
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return log


@pytest.fixture
def desk(lifecycle_desk: Path, pi_log: Path) -> Path:
    result = _deskops(
        lifecycle_desk,
        "add",
        "task",
        "--title",
        "X",
        "--goal",
        "record goal",
        "--scope",
        "record scope",
        "--validation",
        "pytest",
        "--task-type",
        "task.code",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return lifecycle_desk


def _review_files(root: Path) -> list[Path]:
    reviews = root / "desk" / "reviews"
    return sorted(reviews.rglob("*.md")) if reviews.exists() else []


def _review(root: Path, review_id: str) -> dict:
    docs = [
        doc
        for doc in (extract_model_data(ReviewDoc, path.read_text(encoding="utf-8")) for path in _review_files(root))
        if doc["id"] == review_id
    ]
    assert len(docs) == 1, review_id
    return docs[0]


def _evidence(root: Path, rel: str, text: str) -> str:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return rel


def test_reproduction_with_evidence_writes_a_pending_well_formed_receipt(desk: Path, pi_log: Path) -> None:
    root = desk
    b = _evidence(root, "runs/repro/b.log", "second\n")
    a = _evidence(root, "runs/repro/a.log", "first\n")

    result = _deskops(
        root,
        "review",
        "record",
        "task-x",
        "--kind",
        "reproduction",
        "--evidence",
        b,
        "--evidence",
        a,
        "--evidence",
        str(root / b),  # the same file again, absolute: counted once (b1)
        "--reason",
        "reproduced on main",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "review: review-task-x-reproduction-1" in result.stdout

    doc = _review(root, "review-task-x-reproduction-1")
    expected = hashlib.sha256(
        b"runs/repro/a.log\nfirst\n" + b"\n" + b"runs/repro/b.log\nsecond\n" + b"\n"
    ).hexdigest()
    assert doc["kind"] == "reproduction"
    assert doc["verdict"] == "pending"
    assert doc["engine"] == "human"
    assert doc["actor"] == "repo"
    assert doc["reason"] == "reproduced on main"
    assert doc["run_dir"] == ""
    assert doc["output_sha256"] == ""
    assert doc["input_sha256"] == expected
    assert doc["summary"] == "reproduction receipt recorded by repo; evidence: runs/repro/a.log, runs/repro/b.log"
    assert doc["disposed_at"] == "" and doc["disposed_by"] == ""
    assert doc["subject_ref"] == ""
    assert (root / "desk" / "reviews" / "task-x" / "reproduction-1.md").is_file()
    assert not (root / "runs" / "subagents").exists()
    assert not pi_log.exists()


def test_goldens_with_evidence_is_numbered_by_its_kind(desk: Path) -> None:
    root = desk
    rel = _evidence(root, "tests/fixtures/golden/out.txt", "golden\n")
    result = _deskops(root, "review", "record", "task-x", "--kind", "goldens", "--evidence", rel, "--reason", "goldens unchanged")
    assert result.returncode == 0, result.stdout + result.stderr
    doc = _review(root, "review-task-x-goldens-1")
    assert doc["kind"] == "goldens"
    assert SHA256.match(doc["input_sha256"])


# preflight and bundle are recorded by hand since main en verde (decision B of the project
# coordinator, with the overlord's conditions): see the human-receipt tests below.
@pytest.mark.parametrize("kind", ["node"])
def test_model_kinds_are_refused_and_nothing_is_written(desk: Path, pi_log: Path, kind: str) -> None:
    root = desk
    rel = _evidence(root, "runs/repro/a.log", "first\n")
    result = _deskops(root, "review", "record", "task-x", "--kind", kind, "--evidence", rel, "--reason", "r")
    assert result.returncode == 2
    assert "invalid choice" in result.stderr
    assert _review_files(root) == []
    assert not pi_log.exists()


@pytest.mark.parametrize("kind", ["reproduction", "goldens"])
def test_reproduction_and_goldens_require_evidence(desk: Path, kind: str) -> None:
    root = desk
    result = _deskops(root, "review", "record", "task-x", "--kind", kind, "--reason", "no evidence")
    assert result.returncode == 2
    assert f"--kind {kind} requires at least one --evidence" in result.stdout
    assert _review_files(root) == []


def test_missing_evidence_fails_without_writing(desk: Path) -> None:
    root = desk
    good = _evidence(root, "runs/repro/a.log", "first\n")
    result = _deskops(
        root, "review", "record", "task-x", "--kind", "reproduction",
        "--evidence", good, "--evidence", "runs/repro/missing.log", "--reason", "r",
    )
    assert result.returncode == 1
    assert "Error: evidence not found: runs/repro/missing.log" in result.stdout
    assert _review_files(root) == []


@pytest.mark.parametrize("where", ["dotdot", "absolute", "symlink", "directory"])
def test_evidence_outside_the_root_or_not_a_file_fails_without_writing(desk: Path, tmp_path: Path, where: str) -> None:
    root = desk
    outside = tmp_path / "outside.log"
    outside.write_text("outside\n", encoding="utf-8")
    if where == "dotdot":
        ref = "../outside.log"
    elif where == "absolute":
        ref = str(outside)
    elif where == "symlink":
        (root / "runs").mkdir(exist_ok=True)
        (root / "runs" / "link.log").symlink_to(outside)
        ref = "runs/link.log"
    else:
        (root / "runs" / "dir").mkdir(parents=True)
        ref = "runs/dir"
    result = _deskops(root, "review", "record", "task-x", "--kind", "goldens", "--evidence", ref, "--reason", "r")
    assert result.returncode == 1
    assert f"Error: evidence not found: {ref}" in result.stdout
    assert _review_files(root) == []


def test_owner_without_evidence_records_the_reason_alone(desk: Path) -> None:
    root = desk
    result = _deskops(root, "review", "record", "task-x", "--kind", "owner", "--reason", "approved by the owner")
    assert result.returncode == 0, result.stdout + result.stderr
    doc = _review(root, "review-task-x-owner-1")
    assert doc["kind"] == "owner"
    assert doc["verdict"] == "pending"
    assert doc["engine"] == "human"
    assert doc["input_sha256"] == ""
    assert doc["reason"] == "approved by the owner"
    assert doc["summary"] == "owner receipt recorded by repo; evidence: (none)"


def test_record_requires_a_reason(desk: Path) -> None:
    root = desk
    result = _deskops(root, "review", "record", "task-x", "--kind", "owner")
    assert result.returncode == 2
    assert _review_files(root) == []


def test_dispose_accepts_a_recorded_receipt(desk: Path) -> None:
    root = desk
    rel = _evidence(root, "runs/repro/a.log", "first\n")
    assert _deskops(root, "review", "record", "task-x", "--kind", "reproduction", "--evidence", rel, "--reason", "r").returncode == 0

    disposed = _deskops(
        root, "review", "dispose", "review-task-x-reproduction-1", "--verdict", "accepted", "--reason", "reproduction checked",
    )
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr
    doc = _review(root, "review-task-x-reproduction-1")
    assert doc["verdict"] == "accepted"
    assert doc["reason"] == "reproduction checked"
    assert doc["disposed_at"]
    assert doc["disposed_by"] == "repo"
    assert doc["engine"] == "human"


def test_subject_is_pinned_and_the_anchor_is_intact(desk: Path) -> None:
    """sldb pins `__doc_anchors__` on save (`save_document_payload`), not on
    `create_document`: the recorded receipt carries the bare anchor, like every other
    receipt, and the disposition write pins it against the task's contract."""
    root = desk
    result = _deskops(root, "review", "record", "task-x", "--kind", "owner", "--reason", "approved")
    assert result.returncode == 0, result.stdout + result.stderr
    assert _review(root, "review-task-x-owner-1")["subject"] == "doc:TaskCodeDoc:task-x"

    disposed = _deskops(root, "review", "dispose", "review-task-x-owner-1", "--verdict", "accepted", "--reason", "ok")
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr
    doc = _review(root, "review-task-x-owner-1")
    assert re.fullmatch(r"doc:TaskCodeDoc:task-x@sha256:[0-9a-f]{64}", doc["subject"]), doc["subject"]

    findings = check_doc_anchors(root / ".sldb", pythonpath=str(ROOT))
    assert [f for f in findings if f.subject.endswith("review-task-x-owner-1")] == []


def test_json_output_reports_the_receipt(desk: Path) -> None:
    import json

    root = desk
    rel = _evidence(root, "runs/repro/a.log", "first\n")
    result = _deskops(
        root, "review", "record", "task-x", "--kind", "reproduction", "--evidence", rel, "--reason", "r", "--format", "json",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    payload = data.get("data", data)
    assert payload["review_id"] == "review-task-x-reproduction-1"
    assert payload["evidence"] == ["runs/repro/a.log"]


@pytest.mark.parametrize("kind", ["preflight", "bundle"])
def test_human_preflight_and_bundle_require_an_operator_and_write_nothing_without_one(
    desk: Path, pi_log: Path, kind: str
) -> None:
    root = desk
    rel = _evidence(root, "runs/review/notes.md", "read the contract\n")
    result = _deskops(root, "review", "record", "task-x", "--kind", kind, "--evidence", rel, "--reason", "r")
    assert result.returncode != 0
    assert "--operator" in result.stdout + result.stderr
    assert _review_files(root) == []
    assert not pi_log.exists()


@pytest.mark.parametrize("kind", ["preflight", "bundle"])
def test_human_preflight_and_bundle_receipts_show_engine_operator_and_no_model_reason(
    desk: Path, pi_log: Path, kind: str
) -> None:
    root = desk
    rel = _evidence(root, "runs/review/notes.md", "read the contract\n")
    result = _deskops(
        root, "review", "record", "task-x", "--kind", kind, "--operator", "Ana", "--evidence", rel, "--reason", "contract read",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "engine: human; operator: Ana; no model available" in result.stdout

    doc = _review(root, f"review-task-x-{kind}-1")
    assert doc["kind"] == kind
    assert doc["engine"] == "human"
    assert doc["actor"] == "Ana"
    assert doc["verdict"] == "pending"
    assert doc["run_dir"] == "" and doc["output_sha256"] == ""
    assert "operator Ana" in doc["summary"] and "no model available" in doc["summary"]
    assert "no model available" in doc["title"]
    assert not (root / "runs" / "subagents").exists()
    assert not pi_log.exists()

    disposed = _deskops(root, "review", "dispose", f"review-task-x-{kind}-1", "--verdict", "accepted", "--reason", "ok")
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr
    doc = _review(root, f"review-task-x-{kind}-1")
    assert doc["engine"] == "human" and doc["actor"] == "Ana"
    assert "no model available" in doc["summary"]


def test_human_preflight_and_bundle_activate_a_task_code(desk: Path, pi_log: Path) -> None:
    """The documented path for a desk without a model (CI scenarios, the quickstart)."""
    root = desk
    rel = _evidence(root, "runs/review/notes.md", "read the contract\n")
    blocked = _deskops(root, "advance", "task", "task-x")
    assert blocked.returncode != 0 and "rule-activation-task-code" in blocked.stdout + blocked.stderr
    for kind in ("preflight", "bundle"):
        recorded = _deskops(
            root, "review", "record", "task-x", "--kind", kind, "--operator", "Ana", "--evidence", rel, "--reason", "r",
        )
        assert recorded.returncode == 0, recorded.stdout + recorded.stderr
        disposed = _deskops(root, "review", "dispose", f"review-task-x-{kind}-1", "--verdict", "accepted", "--reason", "ok")
        assert disposed.returncode == 0, disposed.stdout + disposed.stderr
    advanced = _deskops(root, "advance", "task", "task-x")
    assert advanced.returncode == 0, advanced.stdout + advanced.stderr
    assert "Current node: ritual-testing" in advanced.stdout
    assert not pi_log.exists()


def test_a_short_selector_keys_and_anchors_receipts_on_the_full_task_id(desk: Path, pi_log: Path) -> None:
    """`review record|preflight` with a prefix of the task id: the receipt carries the full id
    (review id, path and subject), or no activation rule would ever see it (main en verde)."""
    root = desk
    added = _deskops(
        root, "add", "task", "--title", "Long name for a selector", "--goal", "g", "--scope", "s",
        "--validation", "pytest", "--task-type", "task.code",
    )
    assert added.returncode == 0, added.stdout + added.stderr
    full = "task-long-name-for-a-selector"

    recorded = _deskops(root, "review", "record", "task-long", "--kind", "owner", "--reason", "approved")
    assert recorded.returncode == 0, recorded.stdout + recorded.stderr
    assert f"review: review-{full}-owner-1" in recorded.stdout
    assert _review(root, f"review-{full}-owner-1")["subject"] == f"doc:TaskCodeDoc:{full}"
    assert (root / "desk" / "reviews" / full / "owner-1.md").is_file()

    # The model review too: the logging `pi` fails, so the receipt is a technical failure,
    # but it is still written under the full id.
    _deskops(root, "review", "preflight", "task-long")
    assert pi_log.exists()
    doc = _review(root, f"review-{full}-preflight-1")
    assert doc["subject"] == f"doc:TaskCodeDoc:{full}"
    assert not (root / "desk" / "reviews" / "task-long").exists()

FILE:tests/test_review_command.py
"""GC03: ``deskops review`` — cold context reviews and their disposition.

Each test runs in a temporary desk with a fake ``pi`` executable placed first on
``PATH``. The fake prints a ``REFORMULACION`` section (or fails) and counts its
invocations, so no test ever calls the real model or touches the network.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from sldb.runtime.validation import extract_model_data

from deskops.models import ReviewDoc


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
PLAN_SRC = ROOT / "desk" / "drawer" / "plans" / "gates-por-tipo"


FAKE_PI = """#!/usr/bin/env python3
import os
import sys
import time

log = os.environ.get("FAKE_PI_LOG")
if log:
    with open(log, "a", encoding="utf-8") as handle:
        handle.write(" ".join(sys.argv[1:]) + "\\n")

mode = os.environ.get("FAKE_PI_MODE", "ok")
if mode == "fail":
    sys.exit(1)
if mode == "no-reformulacion":
    print("sin seccion")
    sys.exit(0)
if mode == "sleep":
    time.sleep(5)
    print("REFORMULACION\\nDRY-RUN: nada.")
    sys.exit(0)
print(
    "REFORMULACION\\n"
    "Propósito: revisar el encargo.\\n"
    "AMBIGUEDADES: ninguna.\\n"
    "DRY-RUN: leer, proponer, validar, sin ejecutar.\\n"
    "FUTURO: otro nodo o un humano."
)
sys.exit(0)
"""


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(filter(None, (str(ROOT), env.get("PYTHONPATH"))))
    return env


def _run(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*argv], cwd=root, env=env or _env(), capture_output=True, text=True)


def _deskops(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return _run(root, *CLI, *argv, "--root", str(root), env=env)


@pytest.fixture
def fake_pi(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pi = bin_dir / "pi"
    pi.write_text(FAKE_PI, encoding="utf-8")
    pi.chmod(0o755)
    log = tmp_path / "pi.log"
    monkeypatch.setenv("FAKE_PI_LOG", str(log))
    monkeypatch.setenv("FAKE_PI_MODE", "ok")
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return bin_dir, log


def _pi_calls(log: Path) -> int:
    if not log.exists():
        return 0
    return len([line for line in log.read_text(encoding="utf-8").splitlines() if line.strip()])


def _add_task(root: Path, *, title: str = "X", task_type: str = "task.code") -> str:
    result = _deskops(
        root,
        "add",
        "task",
        "--title",
        title,
        "--goal",
        "review goal",
        "--scope",
        "review scope",
        "--validation",
        "pytest",
        "--task-type",
        task_type,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return f"task-{title.lower().replace(' ', '-')}"


def _attempt_dirs(root: Path, key: str) -> list[Path]:
    base = root / "runs" / "subagents"
    if not base.exists():
        return []
    return sorted(base.glob(f"*/context-review/{key}/*/attempt-*"))


def _review_docs(root: Path) -> list[dict]:
    reviews = root / "desk" / "reviews"
    if not reviews.exists():
        return []
    docs: list[dict] = []
    for path in sorted(reviews.rglob("*.md")):
        docs.append(extract_model_data(ReviewDoc, path.read_text(encoding="utf-8")))
    return docs


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_preflight_writes_attempt_evidence_and_receipt(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 1
    attempt = attempts[0]
    assert attempt.name == "attempt-1"
    for name in ("input.md", "manifest.json", "output.md", "stderr.log", "receipt.json"):
        assert (attempt / name).is_file(), name

    input_bytes = (attempt / "input.md").read_bytes()
    assert input_bytes.decode().startswith("FILE:desk/tasks/task-x.md\n")

    manifest = _json(attempt / "manifest.json")
    assert manifest["input_sha256"] == __import__("hashlib").sha256(input_bytes).hexdigest()
    assert manifest["sources"][0]["path"] == "desk/tasks/task-x.md"
    assert manifest["argv"][0] == "pi"
    assert manifest["argv"][-1].startswith("@")

    receipt = _json(attempt / "receipt.json")
    assert receipt["technical_ok"] is True
    assert receipt["returncode"] == 0
    assert receipt["input_sha256"] == manifest["input_sha256"]

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    doc = docs[0]
    assert doc["verdict"] == "pending"
    assert doc["subject"] == "doc:TaskCodeDoc:task-x"
    assert doc["run_dir"] == attempt.relative_to(root).as_posix()
    assert doc["input_sha256"] == manifest["input_sha256"]
    assert doc["output_sha256"] == receipt["output_sha256"]


def test_unchanged_second_run_is_reviewed_and_does_not_call_the_model(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _log = fake_pi[1]
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    calls_after_first = _pi_calls(_log)
    assert calls_after_first == 1

    second = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert second.returncode == 0, second.stdout + second.stderr
    assert "unchanged" in second.stdout
    assert _pi_calls(_log) == calls_after_first
    assert len(_attempt_dirs(root, "task-x/preflight")) == 1

    status = _deskops(root, "review", "status", "task-x", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    payload = json.loads(status.stdout)
    preflight = next(item for item in payload if item["key"] == "task-x/preflight")
    assert preflight["state"] == "reviewed"


def test_edited_goal_is_stale_and_next_run_uses_a_new_sha(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    first_sha = _attempt_dirs(root, "task-x/preflight")[0].parent.name

    edit = _deskops(root, "edit", "task", "task-x", "goal", "goal changed")
    assert edit.returncode == 0, edit.stdout + edit.stderr

    status = _deskops(root, "review", "status", "task-x", "--format", "json")
    payload = json.loads(status.stdout)
    preflight = next(item for item in payload if item["key"] == "task-x/preflight")
    assert preflight["state"] == "stale"

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 2
    new_shas = {attempt.parent.name for attempt in attempts}
    assert first_sha in new_shas
    assert len(new_shas) == 2


def test_bundle_includes_rituals_pills_and_files_in_order(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    pill = _deskops(
        root,
        "add",
        "pill",
        "--title",
        "Guardrail",
        "--what",
        "keep layers clean",
        "--why",
        "safety",
        "--when",
        "always",
        "--where",
        "desk",
        "--how",
        "read first",
        "--how-not",
        "skip it",
    )
    assert pill.returncode == 0, pill.stdout + pill.stderr
    assert _deskops(root, "bind", "pill", "task-x", "pill-guardrail").returncode == 0

    doc = root / "docs" / "foo.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("# Foo\nsmall file\n", encoding="utf-8")
    edit = _deskops(root, "edit", "task", "task-x", "files", '["docs/foo.md"]')
    assert edit.returncode == 0, edit.stdout + edit.stderr

    assert _deskops(root, "review", "bundle", "task-x", "--run", "test-run").returncode == 0

    attempt = _attempt_dirs(root, "task-x/bundle")[0]
    input_text = (attempt / "input.md").read_text(encoding="utf-8")
    file_headers = [line for line in input_text.splitlines() if line.startswith("FILE:")]
    assert file_headers[0] == "FILE:desk/tasks/task-x.md"
    assert "FILE:desk/rituals/phase.md" in file_headers
    assert "FILE:desk/rituals/execution.md" in file_headers
    assert "FILE:desk/rituals/testing.md" in file_headers
    assert "FILE:desk/rituals/closeout.md" in file_headers
    assert "FILE:desk/contexts/pill-guardrail.md" in file_headers
    assert "FILE:docs/foo.md" in file_headers
    assert file_headers[-1] == "FILE:instruccion"

    # Order: task, rituals, pill, file, instruction.
    ordered = [
        "FILE:desk/tasks/task-x.md",
        "FILE:desk/rituals/phase.md",
        "FILE:desk/rituals/execution.md",
        "FILE:desk/rituals/testing.md",
        "FILE:desk/rituals/closeout.md",
        "FILE:desk/contexts/pill-guardrail.md",
        "FILE:docs/foo.md",
        "FILE:instruccion",
    ]
    assert file_headers == ordered


def test_node_writes_one_review_doc_per_node(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "gates-por-tipo"
    shutil.copytree(PLAN_SRC, plan_dir)

    result = _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    node_docs = [doc for doc in _review_docs(root) if doc["kind"] == "node"]
    node_ids = [doc["id"] for doc in node_docs]
    assert "review-deskops-gates-por-tipo-gc01-node-1" in node_ids
    assert "review-deskops-gates-por-tipo-pc01-node-1" in node_ids
    assert "review-deskops-gates-por-tipo-root-node-1" in node_ids
    for doc in node_docs:
        assert doc["subject"] == ""
        assert doc["subject_ref"].startswith("desk/drawer/plans/gates-por-tipo/dag.yaml#node:")
        assert doc["verdict"] == "pending"


def test_dispose_writes_the_verdict_and_a_second_dispose_fails(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0

    disposed = _deskops(
        root,
        "review",
        "dispose",
        "review-task-x-preflight-1",
        "--verdict",
        "accepted",
        "--reason",
        "looks right",
    )
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    doc = docs[0]
    assert doc["verdict"] == "accepted"
    assert doc["reason"] == "looks right"
    assert doc["disposed_at"]
    assert doc["disposed_by"]

    again = _deskops(
        root,
        "review",
        "dispose",
        "review-task-x-preflight-1",
        "--verdict",
        "rejected",
        "--reason",
        "changed my mind",
    )
    assert again.returncode == 1
    assert "already has verdict" in again.stdout


def test_third_good_attempt_on_the_same_key_fails_without_force(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "gates-por-tipo"
    shutil.copytree(PLAN_SRC, plan_dir)
    brief = plan_dir / "brief.md"
    log = fake_pi[1]

    assert _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r").returncode == 0
    brief.write_text(brief.read_text(encoding="utf-8") + "\n# change one\n", encoding="utf-8")
    assert _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r").returncode == 0
    assert _pi_calls(log) == 2

    brief.write_text(brief.read_text(encoding="utf-8") + "\n# change two\n", encoding="utf-8")
    third = _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r")
    assert third.returncode == 1
    assert "tope --max-attempts" in third.stdout
    assert _pi_calls(log) == 2


def test_transport_failure_leaves_technical_failure_and_incomplete(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    monkeypatch.setenv("FAKE_PI_MODE", "fail")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    receipt = _json(attempt / "receipt.json")
    assert receipt["technical_ok"] is False
    assert receipt["returncode"] == 1

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    assert docs[0]["verdict"] == "incomplete"
    assert docs[0]["reason"] == "technical"


def test_output_without_reformulacion_is_a_transport_failure(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    monkeypatch.setenv("FAKE_PI_MODE", "no-reformulacion")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    assert _json(attempt / "receipt.json")["technical_ok"] is False
    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert docs[0]["verdict"] == "incomplete"
    assert docs[0]["reason"] == "technical"


def test_force_requires_reason(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    result = _deskops(root, "review", "preflight", "task-x", "--force", "--run", "test-run")
    assert result.returncode == 2
    assert "--force requires --reason" in result.stdout


def test_force_with_reason_retries_the_same_input(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    log = fake_pi[1]
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    assert _pi_calls(log) == 1

    result = _deskops(root, "review", "preflight", "task-x", "--force", "--reason", "again", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr
    assert _pi_calls(log) == 2

    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 2
    manifest = _json(attempts[1] / "manifest.json")
    assert manifest["retry_reason"] == "again"
    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-2"]
    assert len(docs) == 1
    assert docs[0]["reason"] == "again"


def test_init_and_desk_update_seed_the_deepseek_flash_profile_idempotently(
    tmp_path: Path,
) -> None:
    from deskops.cli.main import main

    root = tmp_path / "repo"
    root.mkdir()
    assert main(["init", str(root)]) == 0

    profile = root / "desk" / "runtimes" / "runtime-pi-deepseek-flash.md"
    assert profile.is_file()
    first = profile.read_text(encoding="utf-8")

    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert profile.read_text(encoding="utf-8") == first

    # An existing profile is never overwritten.
    profile.write_text("# my own profile\n", encoding="utf-8")
    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert profile.read_text(encoding="utf-8") == "# my own profile\n"


@pytest.mark.parametrize(
    ("receipts", "expected"),
    [
        ([], "missing"),
        ([("old", "accepted"), ("old", "rejected"), ("old", "incomplete")], "stale"),
        ([("current", "incomplete")], "technical_failure"),
        ([("current", "incomplete"), ("current", "pending")], "reviewed"),
        ([("current", "pending"), ("current", "rejected")], "rejected"),
        ([("current", "accepted"), ("current", "rejected"), ("current", "pending"),
          ("current", "incomplete"), ("old", "rejected")], "accepted"),
        ([("old", "accepted"), ("current", "rejected")], "rejected"),
    ],
)
def test_status_classifies_only_current_receipts_without_mutating_evidence(
    lifecycle_desk: Path, receipts: list[tuple[str, str]], expected: str
) -> None:
    from deskops.cli.main import main
    from deskops.services.review import ReviewService, _sha

    root = lifecycle_desk
    assert main([
        "add", "task", "--title", "Status", "--goal", "review goal",
        "--scope", "review scope", "--validation", "pytest", "--task-type", "task.code",
        "--root", str(root),
    ]) == 0
    service = ReviewService(root)
    task_path, task_id = service._resolve_task("task-status")
    input_data, _, _ = service._preflight_input(task_path, task_id)
    for index, (identity, verdict) in enumerate(receipts):
        evidence = root / "runs" / "subagents" / f"receipt-{index}"
        evidence.mkdir(parents=True)
        (evidence / "input.md").write_bytes(input_data if identity == "current" else b"old input\n")
        (evidence / "manifest.json").write_text(json.dumps({"profile": "test", "attempt": index}))
        review_id, _ = service._write_review(
            kind="preflight", subject=f"doc:TaskCodeDoc:{task_id}", subject_ref="",
            engine="test", run_dir=evidence.relative_to(root).as_posix(),
            input_sha256=_sha(input_data) if identity == "current" else _sha(b"old input\n"),
            output_sha256=_sha(b"review output"),
            verdict="pending" if verdict in {"accepted", "rejected"} else verdict, reason="test evidence",
            node_id=None,
        )
        if verdict in {"accepted", "rejected"}:
            service.dispose(review_id, verdict, "test disposition")
    preserved = {
        path: path.read_bytes()
        for directory in (root / "desk" / "reviews", root / "runs")
        if directory.exists() for path in directory.rglob("*") if path.is_file()
    }
    reports = {item["key"]: item for item in service.status("task-status")}
    assert reports["task-status/preflight"] == {
        "key": "task-status/preflight", "state": expected, "input_sha256": _sha(input_data),
    }
    assert reports["task-status/bundle"]["state"] == "missing"
    assert all(path.read_bytes() == content for path, content in preserved.items())


@pytest.mark.parametrize("tracked", [False, True], ids=["plain", "pinned"])
def test_disposed_review_status_uses_task_identity(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], tracked: bool
) -> None:
    root = lifecycle_desk
    if not tracked:
        shutil.rmtree(root / ".sldb")
    _add_task(root, title="Identity")
    result = _deskops(root, "review", "preflight", "task-identity", "--run", "identity")
    assert result.returncode == 0, result.stdout + result.stderr
    doc = _review_docs(root)[0]
    assert doc["subject"].startswith("doc:TaskCodeDoc:task-identity" if tracked else "doc:TaskDoc:task-identity")
    disposed = _deskops(root, "review", "dispose", doc["id"], "--verdict", "accepted", "--reason", "correct")
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr
    subject = _review_docs(root)[0]["subject"]
    if tracked:
        # GO07 pins the actual stored subject on disposition, not a parser fixture.
        assert "@sha256:" in subject
    else:
        assert "@" not in subject
    for target in [("task-identity",), ()]:
        status = _deskops(root, "review", "status", *target, "--format", "json")
        assert status.returncode == 0, status.stdout + status.stderr
        report = next(item for item in json.loads(status.stdout) if item["key"] == "task-identity/preflight")
        assert report["state"] == "accepted"
    edit = _deskops(root, "edit", "task", "task-identity", "goal", "changed input")
    assert edit.returncode == 0, edit.stdout + edit.stderr
    status = _deskops(root, "review", "status", "task-identity", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    assert next(item for item in json.loads(status.stdout) if item["key"] == "task-identity/preflight")["state"] == "stale"

FILE:instruccion
Cold-bundle de la tarea task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_record.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && git diff --stat (solo los dos archivos de test)


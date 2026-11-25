FILE:desk/tasks/task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo.md
---
sldb:
  by: agent
  at: '2026-11-17T02:08:10Z'
  authority: generated
  via: create_document
id: task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo
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
- deskops/models/review.py
- tests/test_review_doc.py
- tests/test_review_command.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops review node acepta ids de nodo con punto como WS13.1 en el subject_ref del recibo

## Rationale

_Explain why this task exists or the business driver behind it._

deskops review node desk/drawer/plans/workspace-documental (triaje del 2026-11-16) aborta con 'Validation error: 1 validation error for ReviewDoc subject_ref String should match pattern' para el nodo WS13.1: SUBJECT_REF_PATTERN en deskops/models/review.py (r'^([^\s#]+#node:[A-Za-z0-9_-]+)?$') no admite el punto, y ese plan tiene 19 nodos con punto (WS13.1, WS15.2, WS32.1, ...). La corrida entera se corta en el primero y no escribe ningun recibo.

## Goal

_Describe the concrete result this task must produce._

SUBJECT_REF_PATTERN acepta el punto en el id de nodo (por ejemplo dag.yaml#node:WS13.1) y deskops review node escribe el recibo de un nodo con punto; un id con espacio o con '#' sigue rechazado.

## Scope

_State what is in scope and what is out of scope._

Entra: SUBJECT_REF_PATTERN en deskops/models/review.py, el modelo ReviewDoc del store si declara el mismo patron, y tests en tests/test_review_doc.py y tests/test_review_command.py. Sale: el formato de los ids de nodo de los planes y los review_id que se derivan del nodo (si el punto choca en el review_id, se informa en el resultado sin cambiar su formato).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Agregar el punto a la clase de caracteres del id de nodo en SUBJECT_REF_PATTERN (y donde el store declare el mismo patron). 2) Test de modelo: subject_ref con #node:WS13.1 valida; con espacio o '#' extra no. 3) Test de review node en desk sandbox con un dag.yaml de prueba que tenga un nodo con punto, con el pi falso que ya usan los tests, que escribe su recibo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py

## Done When

_Name the observable condition that makes the task complete._

Un subject_ref con id de nodo con punto valida, review node escribe su recibo en el sandbox, los ids con espacio o '#' siguen rechazados y los dos archivos de la Validation pasan.

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

FILE:deskops/models/review.py
"""A review receipt anchored to the contract of the document it reviewed (``ReviewDoc``).

A review is a document, not a fact computed in Python (plan gates-por-tipo, D2): the
``ReviewDoc`` records what was reviewed (``subject``), who ran it and with which engine, the
run evidence under ``runs/``, the input/output hashes, and the verdict written by whoever
operates the desk. ``deskops review`` (GC03) writes the receipt with ``verdict: pending``;
``deskops review dispose`` writes the verdict; ``deskops edit review`` refuses to touch it
because a new review is a new document (DC3).

The subject is a document anchor: ``doc:<Model>:<id>``, pinned by sldb (GO07) with
``@sha256:<contract hash>`` when the receipt is saved through ``save_document_payload``. The
field is declared in ``__doc_anchors__``, not ``__references__``: sldb reads every
``__doc_anchors__`` field as a reference too (the ``^subject`` edge the activation rules walk)
and computes its ``anchor_state`` (``intact``, ``changed``, ``lost``) when it composes the
index. Nothing here fabricates that edge or that state.
"""

from __future__ import annotations

import re
from typing import Any
from typing import Literal

from pydantic import Field, model_validator

from sldb import StructuredNLDoc


REVIEW_ID_PATTERN = (
    r"^review-.+-(preflight|bundle|reproduction|goldens|owner|node"
    r"|evidence-(tests|commit|atom|materialization|document|external))-[0-9]+$"
)
SUBJECT_PATTERN = r"^(doc:[A-Z][A-Za-z0-9_]*:[^\s:@]+(@sha256:[0-9a-f]{64})?)?$"
SUBJECT_REF_PATTERN = r"^([^\s#]+#node:[A-Za-z0-9_-]+)?$"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

ReviewKind = Literal["preflight", "bundle", "reproduction", "goldens", "owner", "node", "evidence"]
#: Closeout evidence a kind ``evidence`` receipt records (CC33a): one receipt per verified kind.
EvidenceFact = Literal["", "tests", "commit", "atom", "materialization", "document", "external"]
ReviewVerdict = Literal["pending", "accepted", "rejected", "incomplete"]


class ReviewDoc(StructuredNLDoc):
    """Receipt of one cold review (or another external check) bound to a document contract."""

    #: sldb treats every ``__doc_anchors__`` field as a reference too (GO07) and pins it on
    #: save; no Python here fakes the anchor edge or its state.
    __doc_anchors__ = ["subject"]
    __references__ = []
    __semantics__ = {"type": ["workflow", "review"], "workspace": ["desk", "runs"]}
    __template__ = """---
# review-<task>-<kind>-<n>
id: ⸢rev•id⸥
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: ⸢rev•kind⸥
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ⸢rev•fact⸥
# kind evidence only: what the producer verified, one item per line
value: ⸢rev•value⸥
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: ⸢rev•subject⸥
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ⸢rev•subject_ref⸥
# RuntimeProfileDoc name or "human"
engine: ⸢rev•engine⸥
actor: ⸢rev•actor⸥
# Run evidence directory under runs/, relative to the project root
run_dir: ⸢rev•run_dir⸥
input_sha256: ⸢rev•input_sha256⸥
output_sha256: ⸢rev•output_sha256⸥
# pending | accepted | rejected | incomplete
verdict: ⸢rev•verdict⸥
reason: ⸢rev•reason⸥
# ISO 8601 timestamp
created_at: ⸢rev•created_at⸥
# ISO 8601 timestamp, empty while pending
disposed_at: ⸢rev•disposed_at⸥
disposed_by: ⸢rev•disposed_by⸥
# e.g. workspace:desk
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what was reviewed and the evidence this receipt records._

⸢rev•summary⸥

## Disposition

_Record the verdict rationale and who disposed of the review._

⸢rev•disposition⸥
""".strip()

    @model_validator(mode="before")
    @classmethod
    def _absent_evidence_fields_are_empty(cls, data: Any) -> Any:
        """Receipts written before kind ``evidence`` have no ``fact``/``value`` keys: empty."""
        if isinstance(data, dict):
            return {key: value for key, value in data.items() if not (value is None and key in ("fact", "value"))}
        return data

    id: str = Field(
        description="Stable review identifier: 'review-<task-id>-<kind>-<n>'.",
        pattern=REVIEW_ID_PATTERN,
    )
    title: str = Field(description="Short human-readable label for the review.")
    kind: ReviewKind = Field(
        description="Review kind: preflight, bundle, reproduction, goldens, owner, node, or evidence."
    )
    fact: EvidenceFact = Field(
        default="",
        description="Closeout evidence kind a kind 'evidence' receipt records; empty for every other kind.",
    )
    value: str = Field(
        default="",
        description="What the closeout producer verified (kind 'evidence'): sorted items joined by newlines.",
    )
    subject: str = Field(
        default="",
        description="Document anchor 'doc:<Model>:<id>' (optionally pinned with @sha256:<hash>); "
        "empty for reviews of plan nodes.",
        pattern=SUBJECT_PATTERN,
    )
    subject_ref: str = Field(
        default="",
        description="Plan-node reference '<plan>/dag.yaml#node:<ID>'; empty when subject names a document.",
        pattern=SUBJECT_REF_PATTERN,
    )
    engine: str = Field(default="", description="RuntimeProfileDoc name that produced the review, or 'human'.")
    actor: str = Field(default="", description="Identity that ran or disposed of the review (deskops/identity.py).")
    run_dir: str = Field(
        default="", description="Run evidence directory under runs/, relative to the project root."
    )
    input_sha256: str = Field(default="", description="SHA-256 of the review input, 64 lowercase hex digits or empty.")
    output_sha256: str = Field(default="", description="SHA-256 of the review output, 64 lowercase hex digits or empty.")
    verdict: ReviewVerdict = Field(
        default="pending", description="Review verdict: pending, accepted, rejected, or incomplete."
    )
    reason: str = Field(default="", description="Why the verdict was reached; required when accepted or rejected.")
    created_at: str = Field(description="ISO 8601 timestamp when the review receipt was created.")
    disposed_at: str = Field(default="", description="ISO 8601 timestamp of the disposition; empty while pending.")
    disposed_by: str = Field(default="", description="Identity that disposed of the review; empty while pending.")
    summary: str = Field(default="", description="What was reviewed and what evidence the receipt records.")
    disposition: str = Field(default="", description="Verdict rationale and who disposed of the review.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'workspace:desk'.",
    )

    @model_validator(mode="after")
    def _validate_review(self) -> "ReviewDoc":
        subject = self.subject.strip()
        subject_ref = self.subject_ref.strip()
        if bool(subject) == bool(subject_ref):
            raise ValueError("exactly one of subject or subject_ref must be non-empty")
        if self.kind == "evidence" and not self.fact:
            raise ValueError("kind 'evidence' requires fact")
        if self.kind != "evidence" and (self.fact or self.value):
            raise ValueError("fact and value are only for kind 'evidence'")
        if self.verdict in {"accepted", "rejected"}:
            if not self.reason.strip():
                raise ValueError(f"verdict {self.verdict!r} requires a non-empty reason")
            if not self.disposed_by.strip():
                raise ValueError(f"verdict {self.verdict!r} requires disposed_by")
        if self.verdict == "pending" and (self.disposed_at.strip() or self.disposed_by.strip()):
            raise ValueError("disposed_at and disposed_by must be empty while verdict is pending")
        for field_name in ("input_sha256", "output_sha256"):
            value = getattr(self, field_name).strip()
            if value and not SHA256_PATTERN.fullmatch(value):
                raise ValueError(f"{field_name} must be 64 lowercase hex digits or empty")
        if self.run_dir and self.run_dir != "runs" and not self.run_dir.startswith("runs/"):
            raise ValueError("run_dir must be relative to the project root and under runs/")
        return self

FILE:tests/test_review_doc.py
"""GC02: ``ReviewDoc`` as a review receipt anchored to the reviewed document's contract.

Covers each Done When line of task-gc02: the model roundtrip, the closed ``kind`` and
``verdict`` vocabularies, the subject form and its exclusivity with ``subject_ref``, the
review subject registered for ``deskops edit review`` (where the verdict is refused and
written by ``deskops review dispose`` instead), the receipt tracked as
``ReviewDoc:<id>`` in a temporary desk, ``desk/reviews/`` created by ``init`` and
``desk update``, and the ``sldb edges show`` anchor link that stays an ``xfail`` until
sldb GO07 treats ``__doc_anchors__`` as references (``G_SLDB_ANCHORS``).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from pydantic import ValidationError
from sldb.api import doc_status
from sldb.api import track_document_file
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops.cli.main import main
from deskops.models import ReviewDoc


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
SLDB = [sys.executable, "-m", "sldb"]


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    return env


def _run(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*argv], cwd=root, env=_env(), capture_output=True, text=True
    )


def _deskops(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return _run(root, *CLI, *argv, "--root", str(root))


def _sldb(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return _run(root, *SLDB, *argv)


def _init(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    result = _run(root, *CLI, "init", str(root))
    assert result.returncode == 0, result.stdout + result.stderr


def _payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": "review-task-x-preflight-1",
        "title": "Preflight of task-x",
        "kind": "preflight",
        "subject": "doc:TaskCodeDoc:task-x",
        "subject_ref": "",
        "engine": "pi",
        "actor": "robocop2",
        "run_dir": "runs/subagents/20260101-preflight/context-review/task-x/abc/attempt-1",
        "input_sha256": "a" * 64,
        "output_sha256": "b" * 64,
        "verdict": "pending",
        "reason": "",
        "created_at": "2026-01-01T00:00:00Z",
        "disposed_at": "",
        "disposed_by": "",
        "summary": "Reviewed only the task document.",
        "disposition": "No disposition yet.",
        "tags": ["workspace:desk"],
    }
    payload.update(overrides)
    return payload


def _write_review(root: Path, **overrides: object) -> Path:
    payload = _payload(**overrides)
    review_id = str(payload["id"])
    kind = str(payload["kind"])
    task_id = "task-x"
    path = root / "desk" / "reviews" / task_id / f"{kind}-1.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_model_markdown(ReviewDoc, payload) + "\n", encoding="utf-8")
    track_document_file(root / ".sldb", "ReviewDoc", path, name=review_id, pythonpath=str(ROOT), force=True)
    return path


# ------------------------------------------------------------------ model
def test_review_doc_roundtrips_a_payload() -> None:
    payload = _payload()
    expected = ReviewDoc(**payload).model_dump()
    rendered = render_model_markdown(ReviewDoc, payload)
    extracted = extract_model_data(ReviewDoc, rendered)

    assert ReviewDoc(**extracted).model_dump() == expected
    assert getattr(ReviewDoc, "__doc_anchors__") == ["subject"]
    assert "subject" not in getattr(ReviewDoc, "__references__")


def test_review_kind_outside_the_closed_vocabulary_fails() -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_payload(kind="cold-bundle"))
    assert "kind" in str(excinfo.value)


def test_review_accepted_without_reason_fails() -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_payload(verdict="accepted", reason="", disposed_by="robocop2"))
    assert "reason" in str(excinfo.value)


def test_review_subject_without_the_doc_prefix_fails() -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_payload(subject="task-x", subject_ref=""))
    assert "subject" in str(excinfo.value)


def test_review_subject_with_doc_prefix_validates() -> None:
    review = ReviewDoc(**_payload(subject="doc:TaskCodeDoc:task-x", subject_ref=""))
    assert review.subject == "doc:TaskCodeDoc:task-x"

    pinned = ReviewDoc(**_payload(subject=f"doc:TaskCodeDoc:task-x@sha256:{'c' * 64}"))
    assert pinned.subject.endswith("@" + "sha256:" + "c" * 64)


def test_review_plan_node_subject_ref_is_the_alternative_to_subject() -> None:
    review = ReviewDoc(
        **_payload(subject="", subject_ref="desk/drawer/plans/gates-por-tipo/dag.yaml#node:GC02")
    )
    assert review.subject == ""
    assert review.subject_ref.endswith("#node:GC02")

    with pytest.raises(ValidationError):
        ReviewDoc(**_payload(subject="doc:TaskCodeDoc:task-x", subject_ref="plan/dag.yaml#node:GC02"))


# ------------------------------------------------------------------ desk
def test_review_doc_is_tracked_as_review_doc_in_a_temporary_desk(lifecycle_desk: Path) -> None:
    root = lifecycle_desk

    path = _write_review(root)

    status = doc_status(root / ".sldb", "ReviewDoc/review-task-x-preflight-1")
    assert status.exists
    assert status.model == "ReviewDoc"
    assert status.path and path.resolve() == (root / status.path).resolve()

    shown = _sldb(root, "find", "review-task-x-preflight-1", "--in", "physical", "--type", "doc", "--store", ".sldb", "--format", "json")
    assert shown.returncode == 0, shown.stdout + shown.stderr
    results = json.loads(shown.stdout)["results"]
    assert [(item["name"], item["model"]) for item in results] == [
        ("review-task-x-preflight-1", "ReviewDoc")
    ]


def test_init_creates_the_reviews_directory(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _init(root)
    assert (root / "desk" / "reviews").is_dir()


def test_desk_update_does_not_require_the_reviews_directory(lifecycle_desk: Path) -> None:
    # git does not keep an empty desk/reviews/; the review service creates it with the first receipt.
    root = lifecycle_desk
    assert (root / "desk" / "reviews").is_dir()

    (root / "desk" / "reviews").rmdir()
    assert not (root / "desk" / "reviews").exists()

    updated = _deskops(root, "desk", "update", "--apply")
    assert updated.returncode == 0, updated.stdout + updated.stderr
    assert "desk/reviews/" not in updated.stdout


@pytest.mark.xfail(strict=True, reason="G_SLDB_ANCHORS: sldb GO07")
def test_sldb_edges_show_links_the_review_to_the_task_by_subject(lifecycle_desk: Path) -> None:
    root = lifecycle_desk

    created = _deskops(
        root,
        "add",
        "task",
        "--title",
        "Task x",
        "--goal",
        "g",
        "--scope",
        "s",
        "--task-type",
        "task.code",
    )
    assert created.returncode == 0, created.stdout + created.stderr
    _write_review(root)

    shown = _sldb(root, "edges", "show", "ReviewDoc:review-task-x-preflight-1", "--store", ".sldb")
    assert shown.returncode == 0, shown.stdout + shown.stderr
    edges = json.loads(shown.stdout)
    assert any(
        edge["relation"] == "references"
        and edge.get("field") == "subject"
        and edge["target"] == "sldb://document/TaskCodeDoc:task-x"
        for edge in edges
    ), edges


# ------------------------------------------------------------------ edit surface
@pytest.mark.parametrize("field", ["verdict", "reason", "disposed_at", "disposed_by"])
def test_edit_review_refuses_the_disposition_fields(
    lifecycle_desk: Path, capsys: pytest.CaptureFixture[str], field: str
) -> None:
    root = lifecycle_desk
    _write_review(root)
    capsys.readouterr()

    result = main(["edit", "review", "review-task-x-preflight-1", field, "accepted", "--root", str(root)])
    captured = capsys.readouterr()

    assert result == 1
    assert "verdict is written by deskops review dispose (GC03); a new review is a new document" in captured.out


# ------------------------------------------------------------------ kind evidence (CC33a)
def _evidence(**overrides: object) -> dict[str, object]:
    fields: dict[str, object] = dict(
        id="review-task-x-evidence-tests-1",
        kind="evidence",
        fact="tests",
        value="tests/test_a.py\ntests/test_b.py",
        engine="deskops-closeout",
        run_dir="",
        output_sha256="",
        verdict="accepted",
        reason="verified: tests tests/test_a.py\ntests/test_b.py",
        disposed_at="2026-01-01T00:00:00Z",
        disposed_by="robocop2",
    )
    fields.update(overrides)
    return _payload(**fields)


def test_evidence_receipt_roundtrips_fact_and_a_multiline_value() -> None:
    payload = _evidence()
    rendered = render_model_markdown(ReviewDoc, payload)
    extracted = extract_model_data(ReviewDoc, rendered)
    assert extracted["fact"] == "tests"
    assert extracted["value"] == "tests/test_a.py\ntests/test_b.py"
    assert ReviewDoc(**extracted).model_dump() == ReviewDoc(**payload).model_dump()


def test_evidence_receipt_requires_fact() -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_evidence(fact=""))
    assert "requires fact" in str(excinfo.value)


def test_fact_outside_the_evidence_vocabulary_fails() -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_evidence(fact="goldens"))
    assert "fact" in str(excinfo.value)


@pytest.mark.parametrize("field", ["fact", "value"])
def test_fact_and_value_are_refused_outside_kind_evidence(field: str) -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_payload(**{field: "tests"}))
    assert "only for kind 'evidence'" in str(excinfo.value)


def test_a_receipt_written_before_kind_evidence_still_reads_with_empty_fact_and_value() -> None:
    rendered = render_model_markdown(ReviewDoc, _payload())
    legacy = "\n".join(
        line for line in rendered.splitlines() if not line.startswith(("fact:", "value:", "# kind evidence only"))
    )
    extracted = extract_model_data(ReviewDoc, legacy)
    assert extracted["fact"] == "" and extracted["value"] == ""
    assert ReviewDoc(**extracted).kind == "preflight"

FILE:tests/test_review_command.py
"""GC03: ``deskops review`` — cold context reviews and their disposition.

Each test runs in a temporary desk with a fake ``pi`` executable placed first on
``PATH``. The fake prints a ``REFORMULACION`` section (or fails) and counts its
invocations, so no test ever calls the real model or touches the network.
"""
from __future__ import annotations

import json
import os
import re
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
    assert re.fullmatch(r"doc:TaskCodeDoc:task-x@sha256:[0-9a-f]{64}", doc["subject"]), doc["subject"]
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


# --------------------------------------------------------------- claude engine
# A RuntimeProfileDoc whose binary is claude (pi missing, e.g. the scion-claude image) builds a
# `claude -p` argv: profile model, reviewer system prompt, no tools/session/MCP/skills/settings,
# and the input on stdin instead of `@<path>`. The fake claude echoes what it received.

FAKE_CLAUDE = """#!/usr/bin/env python3
import os
import sys

data = sys.stdin.read()
log = os.environ.get("FAKE_CLAUDE_LOG")
if log:
    with open(log, "a", encoding="utf-8") as handle:
        handle.write(repr(sys.argv[1:]) + "\\n")
        handle.write("STDIN:" + data.splitlines()[0] + "\\n")
print("REFORMULACION\\nPropósito: revisar.\\nAMBIGUEDADES: ninguna.\\nDRY-RUN: leer.\\nFUTURO: nada.")
"""

CLAUDE_ENGINE = {
    "id": "runtime-claude",
    "kind": "claude",
    "binary": "claude",
    "model_flag": "--model",
    "system_prompt_flag": "--append-system-prompt",
    "extra_args": ["--print", "--model", "haiku"],
}


def test_claude_profile_argv_is_isolated_print_mode_without_input_path(tmp_path: Path) -> None:
    from deskops.services.review import SYSTEM
    from deskops.services.review import ReviewService

    service = ReviewService(tmp_path)
    input_path = tmp_path / "input.md"
    command = service._command(CLAUDE_ENGINE, input_path, b"FILE:desk/tasks/task-x.md\nhola\n")
    argv = command["argv"]

    assert argv[0] == "claude"
    assert "-p" in argv and "--print" not in argv
    assert argv[argv.index("--model") + 1] == "haiku"
    assert argv[argv.index("--system-prompt") + 1] == SYSTEM
    assert "--append-system-prompt" not in argv
    assert argv[argv.index("--tools") + 1] == ""
    for flag in ("--no-session-persistence", "--strict-mcp-config", "--disable-slash-commands"):
        assert flag in argv, flag
    assert argv[argv.index("--setting-sources") + 1] == ""
    assert not any(item.startswith("@") for item in argv)
    assert str(input_path) not in argv
    assert command["stdin"].startswith("FILE:desk/tasks/task-x.md")
    assert command["binary"] == "claude" and command["model"] == "haiku"
    assert command["input_delivery"] == "stdin"
    assert "--no-session-persistence" in command["isolation_flags"]


def test_claude_profile_without_model_is_refused(tmp_path: Path) -> None:
    from deskops.errors import DomainError
    from deskops.services.review import ReviewService

    engine = {**CLAUDE_ENGINE, "extra_args": ["--print"]}
    with pytest.raises(DomainError, match="names no model"):
        ReviewService(tmp_path)._command(engine, tmp_path / "input.md", b"x")


def test_pi_profile_argv_is_unchanged(tmp_path: Path) -> None:
    from deskops.services.review import ReviewService

    engine = {"id": "runtime-pi", "kind": "pi", "binary": "pi", "extra_args": ["--no-tools", "--print"]}
    command = ReviewService(tmp_path)._command(engine, tmp_path / "input.md", b"x")
    assert command["argv"] == ["pi", "--no-tools", "--print", f"@{tmp_path / 'input.md'}"]
    assert command["stdin"] is None and command["input_delivery"] == "file"


def test_preflight_with_claude_engine_sends_input_on_stdin_and_records_it(
    lifecycle_desk: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    bin_dir = tmp_path / "claude-bin"
    bin_dir.mkdir()
    claude = bin_dir / "claude"
    claude.write_text(FAKE_CLAUDE, encoding="utf-8")
    claude.chmod(0o755)
    log = tmp_path / "claude.log"
    monkeypatch.setenv("FAKE_CLAUDE_LOG", str(log))
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    _add_task(root, title="X")
    payload = tmp_path / "runtime-claude.yaml"
    payload.write_text(
        "title: claude haiku reviewer\nkind: claude\nbinary: claude\nmodel_flag: --model\n"
        "extra_args: [--print, --model, haiku]\n",
        encoding="utf-8",
    )
    added = _deskops(root, "add", "runtime-profile", "--from-yaml", str(payload))
    assert added.returncode == 0, added.stdout + added.stderr

    result = _deskops(
        root, "review", "preflight", "task-x", "--run", "claude-run", "--engine", "runtime-claude-haiku-reviewer"
    )
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    manifest = _json(attempt / "manifest.json")
    assert manifest["binary"] == "claude"
    assert manifest["model"] == "haiku"
    assert manifest["profile"] == "runtime-claude-haiku-reviewer"
    assert manifest["input_delivery"] == "stdin"
    assert "--strict-mcp-config" in manifest["isolation_flags"]
    assert not any(item.startswith("@") for item in manifest["argv"])
    assert _json(attempt / "receipt.json")["technical_ok"] is True
    assert "STDIN:FILE:desk/tasks/task-x.md" in log.read_text(encoding="utf-8")
    doc = next(doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1")
    assert doc["engine"] == "runtime-claude-haiku-reviewer"

FILE:instruccion
Cold-bundle de la tarea task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py


FILE:desk/tasks/task-se-retiran-del-drawer-los-planes-workspace-documental-gates-por-tipo-deskops-ui-y-deskops-como-confi.md
---
sldb:
  by: agent
  at: '2026-11-17T02:54:58Z'
  authority: generated
  via: create_document
id: task-se-retiran-del-drawer-los-planes-workspace-documental-gates-por-tipo-deskops-ui-y-deskops-como-confi
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/tasks/task-jp-decide-si-el-plan-workspace-documental-se-retira-con-sus-67-fichas-o-se-rescatan-nodos.md
depends_on:
- task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo
pills: []
files:
- tests/test_review_command.py
- tests/test_review_doc.py
- deskops/cli/registry.py
- docs/operator-manual.md
- docs/deskops-ui.md
- desk/drawer/plans/gates-por-tipo/dag.yaml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# se retiran del drawer los planes workspace-documental, gates-por-tipo, deskops-ui y deskops-como-config y el test de review node usa un plan fixture propio

## Rationale

_Explain why this task exists or the business driver behind it._

Triaje del drawer del 2026-11-16 pedido por el supervisor: cada nodo de los cuatro planes de desk/drawer/plans/ paso por deskops review node y se decidio botarlo o pasarlo a tarea. De 105 nodos solo dos siguen vigentes y ya tienen destino (GC08 es la tarea task-los-rituales-context-review-y-phase-nombran-deskops-review-y-la-regla-de-activacion-como-gate-de-la; WS47 se pidio a sldb). El resto esta resuelto, duplicado por tareas activas u obsoleto, con su motivo en el recibo de review node de cada nodo (desk/reviews/deskops-<plan>-<nodo>/). Los planes no se pueden borrar sin mas: tests/test_review_command.py copia el plan real gates-por-tipo como fixture (PLAN_SRC) y tests/test_review_doc.py, deskops/cli/registry.py (ejemplos de ayuda), docs/operator-manual.md y docs/deskops-ui.md lo citan.

## Goal

_Describe the concrete result this task must produce._

desk/drawer/plans/ queda sin esos cuatro planes y desk/drawer/tasks/ sin la carpeta workspace-documental (git rm); los tests de review node usan un plan de prueba propio bajo tests/fixtures/plans/ (copia minima de gates-por-tipo con los nodos que los tests necesitan); los ejemplos de ayuda y las docs dejan de citar los planes borrados; los tests pasan.

## Scope

_State what is in scope and what is out of scope._

Entra: git rm de desk/drawer/plans/workspace-documental, desk/drawer/plans/gates-por-tipo, desk/drawer/plans/deskops-ui, desk/drawer/plans/deskops-como-config y desk/drawer/tasks/workspace-documental; el fixture nuevo en tests/fixtures/plans/; PLAN_SRC y las rutas de tests/test_review_command.py y tests/test_review_doc.py; los ejemplos de deskops/cli/registry.py que nombran gates-por-tipo (pasan a una ruta de ejemplo generica de plan) y sus goldens de ayuda; la linea de docs/operator-manual.md y la cita de docs/deskops-ui.md (queda como texto historico sin ruta viva). Sale: los recibos de review node ya escritos en desk/reviews/ (quedan como registro), la tarea de GC08 y tests/test_graph_missing_existing_files.py (usa rutas inventadas de un plan p, no los planes reales).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Copiar a tests/fixtures/plans/gates-por-tipo/ solo lo que los tests de review node leen (dag.yaml recortado a los nodos que usan, por ejemplo ROOT, GC01, GC02 y GC03) y apuntar PLAN_SRC ahi. 2) Correr los tests de review con el plan real todavia presente para comprobar el fixture. 3) git rm de los cuatro planes y de la carpeta de fichas. 4) Ajustar ejemplos de registry.py, regenerar solo sus goldens de ayuda, y las dos docs. 5) deskops graph missing --root . no debe sumar entradas nuevas por los planes borrados.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (sin entradas nuevas por los planes borrados)

## Done When

_Name the observable condition that makes the task complete._

Los cuatro planes y la carpeta de fichas ya no estan en el arbol, los tests de review usan el fixture, ninguna ruta viva del repo cita los planes borrados, los cuatro archivos de test de la Validation pasan y graph missing no crece.

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


def test_node_writes_the_review_doc_of_a_dotted_node_id(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "con-punto"
    plan_dir.mkdir(parents=True)
    (plan_dir / "dag.yaml").write_text(
        "id: deskops-con-punto\n"
        "hierarchy:\n"
        "  root:\n"
        "    id: ROOT\n"
        "    title: Plan con ids de nodo con punto\n"
        "    children: [WS13.1]\n"
        "tasks:\n"
        "- id: WS13.1\n"
        "  title: Nodo con punto\n"
        "  depends_on: []\n",
        encoding="utf-8",
    )

    result = _deskops(root, "review", "node", "desk/drawer/plans/con-punto", "WS13.1", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    node_docs = [doc for doc in _review_docs(root) if doc["kind"] == "node"]
    assert [doc["id"] for doc in node_docs] == ["review-deskops-con-punto-ws13.1-node-1"]
    assert node_docs[0]["subject_ref"] == "desk/drawer/plans/con-punto/dag.yaml#node:WS13.1"
    assert node_docs[0]["verdict"] == "pending"


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


def _accept_task_reviews(root: Path, task_id: str) -> None:
    for mode in ("preflight", "bundle"):
        result = _deskops(root, "review", mode, task_id, "--run", "contract")
        assert result.returncode == 0, result.stdout + result.stderr
    for doc in _review_docs(root):
        disposed = _deskops(root, "review", "dispose", doc["id"], "--verdict", "accepted", "--reason", "ok")
        assert disposed.returncode == 0, disposed.stdout + disposed.stderr


def _task_states(root: Path, task_id: str) -> dict[str, str]:
    status = _deskops(root, "review", "status", task_id, "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    return {item["key"].rsplit("/", 1)[-1]: item["state"] for item in json.loads(status.stdout)}


def test_receipts_record_the_task_contract_digest(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="Contract")
    _accept_task_reviews(root, "task-contract")
    docs = {doc["kind"]: doc for doc in _review_docs(root)}
    assert set(docs) == {"preflight", "bundle"}
    for doc in docs.values():
        assert re.fullmatch(r"[0-9a-f]{64}", doc["contract_sha256"]), doc
        assert doc["contract_sha256"] != doc["input_sha256"]
    assert docs["preflight"]["contract_sha256"] != docs["bundle"]["contract_sha256"]


def test_edited_tags_and_status_keep_accepted_receipts_and_goal_stales_them(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="Contract")
    _accept_task_reviews(root, "task-contract")
    assert _task_states(root, "task-contract") == {"preflight": "accepted", "bundle": "accepted"}

    tags = _deskops(root, "edit", "task", "task-contract", "tags", "['host:otro', 'workspace:desk']")
    assert tags.returncode == 0, tags.stdout + tags.stderr
    # status (with current_node and history) changes through deskops advance, which the two
    # accepted receipts unlock (rule-activation-task-code reads them as anchor_state intact).
    advanced = _deskops(root, "advance", "task", "task-contract")
    assert advanced.returncode == 0, advanced.stdout + advanced.stderr
    text = (root / "desk" / "tasks" / "task-contract.md").read_text(encoding="utf-8")
    assert "host:otro" in text and "\nstatus: draft\n" not in text
    assert _task_states(root, "task-contract") == {"preflight": "accepted", "bundle": "accepted"}

    goal = _deskops(root, "edit", "task", "task-contract", "goal", "goal changed")
    assert goal.returncode == 0, goal.stdout + goal.stderr
    assert _task_states(root, "task-contract") == {"preflight": "stale", "bundle": "stale"}


def test_bundle_state_still_follows_the_linked_files(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="Contract")
    linked = root / "linked.txt"
    linked.write_text("one\n", encoding="utf-8")
    files = _deskops(root, "edit", "task", "task-contract", "files", "['linked.txt']")
    assert files.returncode == 0, files.stdout + files.stderr
    _accept_task_reviews(root, "task-contract")
    linked.write_text("two\n", encoding="utf-8")
    assert _task_states(root, "task-contract") == {"preflight": "accepted", "bundle": "stale"}


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


def test_review_plan_node_subject_ref_accepts_a_dotted_node_id() -> None:
    review = ReviewDoc(
        **_payload(subject="", subject_ref="desk/drawer/plans/workspace-documental/dag.yaml#node:WS13.1")
    )
    assert review.subject_ref.endswith("#node:WS13.1")


@pytest.mark.parametrize("node_id", ["WS 13", "WS13#x"])
def test_review_plan_node_subject_ref_rejects_a_space_or_a_second_hash(node_id: str) -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_payload(subject="", subject_ref=f"plan/dag.yaml#node:{node_id}"))
    assert "subject_ref" in str(excinfo.value)


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

FILE:docs/operator-manual.md
# deskops Operator Manual

This manual is the end-to-end operational playbook for `deskops`.

It is written for two audiences:

- people who operate a desk by hand
- agents that follow documented commands instead of reconstructing behavior from source

The examples are executable. Every fenced block marked `bash runnable` is
extracted, in document order, by `tests/test_operator_manual.py`. The test runs
the blocks in a throwaway git repository under `pytest`'s `tmp_path`, with an
isolated `HOME`, so the manual cannot drift from the real CLI.

Blocks marked `bash` are illustrative only. They show expected failures,
destructive alternatives, cross-repo targeting, or commands that need an
external runtime such as Herdr.

For the first, shortest walkthrough, read `docs/quickstart.md`. For the CLI's
first-use question index, run `deskops faq`. This manual does not re-document
SLDB; it only covers the deskops workflow surface built on top of SLDB.

## Runnables convention

The runnable walkthrough assumes:

- the current directory is an empty git repository with at least one commit
- `deskops` resolves to this checkout (`tests/test_operator_manual.py` supplies
  a shim so the examples stay spelled `deskops ...`)
- no real `~/.sldb` or user desk is touched

Run one block at a time, or let the test run all blocks in order. State created
by one block is visible to later blocks.

## Machine and repository setup

### Help and bootstrap

`deskops bootstrap` is the machine-level repair path. It verifies that SLDB is
importable, installs it from the sibling checkout only when needed, creates the
global `~/.sldb` store, and registers the deskops model set there.

```bash runnable
deskops --help
deskops bootstrap
```

### Initialize the repository

`deskops init` runs the bootstrap preflight, creates a local `.sldb/` store,
scaffolds `desk/`, and writes the lifecycle graph under `desk/lifecycle/`.

```bash runnable
deskops init .
```

### Orient yourself

```bash runnable
deskops about
deskops faq
deskops faq 1
```

`deskops faq` with no argument lists the available questions. Pass a question
index, slug, or text fragment to print one answer.

### Check desk health

`deskops doctor` reports desk shape, store registration, tracking, and model
validity. `deskops status` is a deprecated alias for the same command.

```bash runnable
deskops doctor --root .
deskops status --root .
```

The report has two parts. **Errors** mean the desk is broken: missing structure,
a tracked document that is gone, a document its model cannot read, an unregistered
model, a store that cannot be read. They make `doctor` exit 1. **Alerts** mean the
store moved under an expected change: a document edited, moved or added by hand, a
model contract that changed. Nothing is broken; register them with
`deskops desk update --apply`. Alerts alone exit 0, and they are always printed.

A task its model rejects (its `status`, `current_node` and `history` are not a state
the lifecycle can produce) is an error of its own, one line per task with the file and
the validator's text, read from the task's frontmatter, while doctor still runs the other
checks (structure, store, models). `sldb stores check` names such a document as
`store/doc-invalid` and goes on; doctor reads that finding too, for a tracked document
under another model, and does not repeat a task its frontmatter listing already named.
A task the legacy migration decides says
`Migrate it with deskops desk update --apply`; any other one says what its owner can
do (`decide its state: deskops closeout supersede --task <id> --reason ... --ref ...`).

`doctor` also compares the desk's managed seeds (the lifecycle graph and its rules
under `desk/lifecycle/`) with the ones the installed deskops ships, by the same
comparison `deskops desk update --apply` makes before rewriting them. Each copy
that differs is one finding, naming the top-level frontmatter fields that differ
(`body` when only the text below the frontmatter does; the `sldb:` write
provenance is named only when nothing else differs):

```text
lifecycle seed out of date: desk/lifecycle/execution-task_activates.md differs from the deskops package (attributes). Fix: deskops desk update --apply
```

It is an **error** when a lifecycle edge's transition fields differ (`source_id`,
`target_id`, `relation_type`, `condition`, `attributes`): `deskops advance` refuses
that edge. Any other difference (a rule, the body or notes of a seed) is an
**alert**. A desk seeded before CC31 has `attributes: {}` on its edges and shows
up here; `deskops desk update --apply` restores the managed seeds.

`doctor` raises one **alert** per absolute path (`/home/...`, `/mnt/...`) in the
frontmatter of a desk document: a path written on one machine does not exist on
another. It never changes the exit code. The store already knows where the
neighbouring repositories are (`.sldb/store.yaml` `links`, read through sldb, plus the
registry entries whose path is relative; the root of a neighbour is the parent of its
linked `.sldb`), so the alert says what the path becomes:

```text
Absolute path: desk/registry/repo-sldb.md path: /home/jp/proyectos/SLDB_1/sldb (becomes ../sldb; fix: deskops doctor --repair)
```

`--repair` rewrites those that resolve, through the desk's sldb transaction: the
`path` of a registry entry becomes a path relative to the repository root, and each
absolute entry of a task's `files` and `references` becomes `<repo-id>:<path>`, the
form `closeout resolved-by` accepts (a path of this repository becomes relative to its
root, without prefix). A path that exists here is placed by the root it falls under; a
path that does not exist (another machine) is placed only when what follows the
ecosystem folder (`SLDB_1`) names one neighbour without ambiguity. Anything else stays
an alert with its reason (no ecosystem folder, no neighbour, ambiguous, no registry
entry for that root, a field other than registry `path`, `files` and `references`).

`--repair` otherwise acts on errors only (it scaffolds structure and registers models). Use it
when you understand the reported errors:

```bash
deskops doctor --root . --repair
```

### Inspect the lifecycle graph

On a fresh desk, `next --diagram` renders the state machine as Mermaid from the
source spec. The states are ritual docs and the transitions are sldb relation
docs.

```bash runnable
deskops next --diagram --root .
```

The rendered edges include their conditions:

- `task_activates` moves a draft task into execution.
- `task_hands_to_closeout` requires a non-empty `validation` field.
- `task_completes` requires `status = 'ready_for_testing'` and verified
  closeout evidence.

## Repository identity and the ecosystem registry

`deskops repo whoami` prints the repository's configured project identity.
`deskops repo register` writes a canonical `RepositoryDoc` into the registry and
tracks it in SLDB.

Register the current repository before sending messages. Message delivery
requires the current repository to resolve through the registry when any
registry entries exist.

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo register "$identity" . --store .sldb --pythonpath .
deskops repo whoami --root .
```

`deskops repo remove <id>` takes a registration out of the registry so the
repository can be registered again, for example after a rename:

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo remove "$identity" --root . --store .sldb
deskops repo register "$identity" . --store .sldb --pythonpath .
```

`deskops add repository` is different: it creates a local repository artifact
under `desk/registry/` for discovery or routing. It is not the canonical
ecosystem registration path. The runnable walkthrough creates one later for a
sibling desk.

Cross-repo targeting uses the registered repository id:

```bash
deskops message send "Need a follow-up" --to sibling-desk --title "Follow-up"
deskops list tasks --include-repos
```

## Desk scaffold, migration, and repair

`deskops desk install` scaffolds only the desk folders and starter docs. It does
not create a store, register a repository, or write the lifecycle graph.

```bash runnable
mkdir -p ../sibling
deskops desk install ../sibling
deskops desk migrate --root ../sibling
deskops desk update --root ../sibling --apply
```

- `desk install <path>` creates `tasks/`, `contexts/`, `rituals/`, `atoms/`,
  `roles/`, `inbox/`, `drawer/`, the starter boards/pills/rituals, and
  `desk/config.json`.
- `desk migrate` adopts a legacy or partial desk non-destructively. It reports
  what it adopted, preserved, or left for manual conversion.
- `desk update` is a dry run by default. Add `--apply` to create a missing
  store, register missing models, and write the lifecycle graph.
- `desk update` also migrates the tasks a desk migrated before CC31 left in a
  state no transition produces: an empty history with a terminal or drawer
  status at a node. The dry run lists them as `Legacy task states to migrate`;
  `--apply` writes them first, one line per changed field
  (`desk/tasks/<task>.md: history [] -> [superseded]`). The table:
  `superseded` gets `history [superseded]` (its node stays); `closed`,
  `resolved`, `done`, `complete` and `cancelled` (pre-lifecycle resolved), and
  `deferred` and `candidate` (drawer), get `current_node ''`, outside the
  lifecycle. A non-terminal status with an empty history (any status that is
  not `draft` nor one of those above, nor a closeout status: `active`,
  `ready_for_testing`, `blocked`...) is backed by no transition, so it gets
  `status draft` at the entry node `ritual-execution` (an empty
  `current_node` stays empty), reported as
  `desk/tasks/<task>.md: status active -> draft` plus
  `current_node <node> -> ritual-execution` when the node moves, and its
  `summary` gets one line in front, `Migrada a draft por deskops desk update:
  estado heredado '<status>' sin history (<YYYY-MM-DD UTC>).`, followed by the
  previous summary. A non-empty history with an incoherent status is not
  migrated. Any other task the model rejects is listed under
  `Invalid task documents (not written)` with the validator's text and what its
  owner can do; it is never written. The migration writes the frontmatter
  directly because the model rejects the state, and validates the new text with
  `TaskDoc`; a task it still rejects is restored. A document sldb names with
  `store/doc-invalid` that the task listing does not cover is reported under
  `Invalid documents (not written)` with the model's rejection. `sldb stores
  check` names invalid documents and goes on, so `--apply` keeps every other
  repair (structure, lifecycle graph, models, tracking, task types, indexes); a
  store check with no JSON and a failing exit code is still an environment
  error. `--apply` exits 0
  when nothing is left and 1 while a task or another invalid document waits
  for its owner (as the dry-run does); a second run migrates nothing.

A dry run exits `1` when it finds divergence:

```bash
deskops desk update --root ../sibling
# Desk divergence report:
# - Missing store: .sldb
# - Unregistered models: ...
# Run with --apply to repair these issues.
```

## Artifact commands

The `add`, `edit`, `list`, and `show` families are generated from the artifact
registry. The same grammar applies to every artifact subject.

### Add artifacts

```bash runnable
deskops add atom --root . \
  --title "Operator manual evidence" \
  --five-wh-one-plus what \
  --answer "The operator manual examples run against the real CLI." \
  --tags system:manual topic:docs

deskops add pill --root . \
  --title "Pattern: Manual examples stay runnable" \
  --summary "Executable documentation." \
  --what "What." --why "Why." --when "When." --where "Where." \
  --how "How." --how-not "How not." \
  --tags topic:docs

deskops add ritual --root . \
  --title "Manual ritual" \
  --purpose "Purpose." --trigger "Trigger." --completion "Completion."

deskops add board --root . \
  --title "Manual board" --scope "Scope." --purpose "Purpose."

deskops add materialization --root . \
  --title "Manual materialization" \
  --source-atoms atom-operator-manual-evidence \
  --target-kind board \
  --target-identity desk/tasks/Board.md \
  --intent "Document the CLI." \
  --validation pytest

deskops add repository --root . \
  --name "Sibling desk" --path ../sibling --description "Sibling sandbox."

deskops add faq-doc --root . --title "Manual FAQ" --body "FAQ body."

deskops add step --root . \
  --title "Manual step" --action "Action." --outcome "Outcome."

deskops add inbox-note --root . \
  --kind suggestion \
  --created-at "2026-01-01T00:00:00" \
  --status open \
  --title "Manual inbox note" \
  --body "Promote this note."
```

Required and commonly used flags per subject:

| Subject | Required flags | Common extras |
|---|---|---|
| `task` | `--title` | `--why`, `--goal`, `--scope`, `--task-type` (default `task.code`), `--implementation-path`, `--done-when`, `--validation`, `--from-drawer`, `--depends-on`, `--evidence` (adds kinds only), `--inherits-from`, `--atom`, `--inherit-acceptance-context` |
| `pill` | `--what`, `--why`, `--when`, `--where`, `--how`, `--how-not` | `--summary`, `--tags` |
| `ritual` | `--purpose`, `--trigger`, `--completion` | `--preconditions`, `--steps`, `--validation`, `--failure-modes`, `--tags` |
| `board` | `--scope`, `--purpose` | `--tasks`, `--pills`, `--rituals`, `--notes`, `--tags` |
| `atom` | `--five-wh-one-plus`, `--answer` | `--title`, `--tags`, `--provenance` |
| `materialization` | `--target-kind`, `--target-identity`, `--intent` | `--source-atoms`, `--validation`, `--tags`, `--provenance` |
| `repository` | `--name`, `--description` | `--path`, `--status`, `--tags` |
| `inbox-note` | `--kind`, `--created-at`, `--status`, `--body` | `--sender-project`, `--target-project`, `--title`, `--acknowledged-by`, `--acknowledged-at` |
| `faq-doc` | `--body` | `--title` |
| `step` | `--action`, `--outcome` | `--title`, `--tags` |

`--validation`, `--depends-on`, `--atom`, and similar list flags accept repeated
or space-separated values. Put them last in a command when mixing with another
multi-value flag, because argparse consumes following tokens until the next
flag.

`--from-yaml <file>` loads the payload from YAML for every `add` subject.

`--evidence <kind>...` adds closeout evidence kinds to the type's (`tests`,
`commit`, `atom`, `materialization`, `document`, `external`); it cannot remove
one the type requires. Without `--task-type` the type is `task.code`. See Closeout.

### List artifacts

Plural subjects list all documents of a type. `--format json` is available on
every list command. `list tasks --include-repos` also follows task boards
registered as sibling repositories.

```bash runnable
deskops list atoms --root .
deskops list pills --root .
deskops list rituals --root .
deskops list boards --root .
deskops list materializations --root .
deskops list repositories --root .
deskops list faq-docs --root .
deskops list steps --root .
deskops list inbox-notes --root .
```

### Show artifacts

Singular subjects show one document by exact id, filename, stem, or a unique
slug fragment. `--format json` is available.

```bash runnable
deskops show atom atom-operator-manual-evidence --root .
deskops show pill pill-pattern-manual-examples-stay-runnable --root .
deskops show ritual ritual-manual-ritual --root .
deskops show board board-manual-board --root .
deskops show materialization materialization-manual-materialization --root .
deskops show repository repo-sibling-desk --root .
deskops show faq-doc faq-manual-faq --root .
deskops show step step-manual-step --root .
deskops show inbox-note inbox-note-manual-inbox-note --root .
```

### Edit artifacts

The edit grammar is:

```text
deskops edit <subject> <selector> <field> <value> [--root .]
```

Field names accept hyphens in place of underscores. Values are parsed like SLDB
field values, so JSON lists and quoted strings work. The document is re-rendered
through its model.

A section field of text whose template carries an italic placeholder paragraph
(`_Outline the expected implementation route or affected surface._` in a task,
`_Describe the incoming message with enough evidence to triage._` in an inbox
note) gets it from the template on every render, so `edit` drops from the value
any paragraph that is exactly that field's placeholder. Passing the raw section
text back with a new paragraph leaves one placeholder, the same value twice leaves
the same file, and a value that is only the placeholder empties the field. The
phrase inside a longer paragraph, a quote, a list or a code block is content and
stays. The placeholders are read from the model's template, never from a list.

```bash runnable
deskops edit atom atom-operator-manual-evidence title "Operator manual evidence (edited)" --root .
deskops edit pill pill-pattern-manual-examples-stay-runnable summary "Edited summary." --root .
deskops edit ritual ritual-manual-ritual summary "Edited summary." --root .
deskops edit board board-manual-board notes "Edited notes." --root .
deskops edit materialization materialization-manual-materialization intent "Edited intent." --root .
deskops edit repository repo-sibling-desk status maintenance --root .
deskops edit faq-doc faq-manual-faq body "Edited FAQ body." --root .
deskops edit step step-manual-step outcome "Edited outcome." --root .
deskops edit inbox-note inbox-note-manual-inbox-note body "Edited inbox body." --root .
```

The same subjects exist for `add`, `edit`, `list`, and `show`; `list` uses
plural names and `show` uses singular names.

## Inbox, messages, and drawer

### Send, list, read, and acknowledge messages

`deskops message` is the canonical cross-desk surface. Files are written to the
target desk's `desk/inbox/` as timestamped Markdown notes. Acknowledging closes
the note but keeps the file as the trace.

```bash runnable
deskops message send "Please clarify the manual example." \
  --kind unclear --title "Manual message" --root .
deskops message list --root .
deskops message read manual-message --root .
deskops message ack manual-message --root .
```

`--to <repo>` targets another registered repository. `--from <project>` overrides
the resolved sender identity.
`--desk-root` targets an explicit desk directory. `--format json|yaml` prints
the result for machines.

### Promote an inbox note to a drawer candidate

Inbox notes are intake. Promotion turns one note into a loose deferred candidate
under `desk/drawer/tasks/`, removes the inbox file, and records the new
candidate on the drawer board. The candidate is not yet an active task.

```bash runnable
deskops promote inbox-to-drawer-task manual-inbox-note --root .
```

`--title <text>` overrides the candidate title.

### Remove a drawer entry

`deskops drawer remove` removes the file, its tracking, and its drawer-board
bullets. It refuses when an active task records the entry in `from_drawer`
unless `--force` is passed. Any other reference to the entry is left as it is.
Each file that holds one is reported on stderr as
`alert: <entry> still referenced by <file>`, and the exit code does not change.
These references are what `sldb.api.referrers` finds over the desk graph: a
drawer-board bullet in another form, such as `` `tasks/<id>.md` ``, or a task
that names the entry. `deskops closeout` reports the files that still name the
closed task in the same way.

```bash runnable
deskops message send "Remove this candidate." \
  --kind suggestion --title "Removable candidate" --root .
deskops promote inbox-to-drawer-task removable-candidate --root .
deskops drawer remove task-removable-candidate --root .
```

### Retire any other desk document

`deskops retire` removes one obsolete file under `desk/` that has no dedicated
verb (pills, inbox notes, steps, roles, runtimes, FAQ docs, materializations,
leftovers), with a reason and a `--ref` that resolves to an ancestor commit or
an existing path. The declared fields that name the document lose that entry
in the transaction that deletes it. For a pill, these are the `pills` of the
Board and of every task. A mention in prose, such as a path in a task body, is
never rewritten, so retire refuses while one remains unless `--force` is passed.
Both kinds of reference are what `sldb.api.referrers` finds: the store's field
index, and the mention patterns of the desk graph. Tasks, drawer entries, atoms, and registry
entries keep their own verbs: `closeout`, `drawer remove`, `atoms delete`,
`repo remove`.

```bash runnable
deskops retire desk/steps/step-manual-step.md --root . \
  --reason "The manual step was only an example" \
  --ref "$(git rev-parse HEAD)"
```

## Tasks

### Author a task from a drawer candidate

There is no direct drawer-to-active promotion. A person or agent authors the
active task explicitly and records the drawer file with `--from-drawer`. The
drawer file is kept for manual cleanup. Like every task, its type declares its
closeout evidence: `--task-type task.docs` declares `commit` and `document`.

When the `files` of a task name another repository of the desk's registry
(`deskops repo register`), `add task` prints one more line after creating it, and
creates it all the same (it never blocks and does not change the type):

```text
Files of <task-id> belong to repository <repo-id>; if the work lives there consider task_type task.external or a mirror task in its desk.
```

A file belongs to another repository when it is `<repo-id>:<path>` with a registered
id, an absolute path under that repository's registered root, or a relative path that
starts at the parent folder (`../<repo>/...`) and resolves under it. Anything else is
local. Only `files` count, not `references`; the line is not printed for `task.external`
or when every file is local. `deskops doctor` lists the same line as an alert for each
open task (not closed, resolved, done, complete, superseded or cancelled) that is not
`task.external` and has such files; it does not change doctor's exit code.

```bash runnable
deskops add task --root . \
  --title "Close a manual task" \
  --task-type task.docs \
  --why "Why." \
  --goal "Goal." \
  --scope "Scope." \
  --implementation-path "Path." \
  --done-when "Done." \
  --from-drawer task-manual-inbox-note \
  --validation "pytest tests/test_manual_smoke.py"
```

### Bind reusable context pills

Pills are reusable atomic context, not one-to-one task artifacts. Bind the ones
whose `when`, `where`, and `how_not` match the task.

```bash runnable
deskops bind pill task-close-a-manual-task \
  pill-pattern-manual-examples-stay-runnable --root .
```

### Inspect, edit, and advance a task

`next <task>` explains the next valid workflow action without mutating the
task; `next <task> --why` adds why this task and these actions were selected. `show task` prints the lifecycle gates and whether each holds.

```bash runnable
deskops list tasks --root .
deskops show task task-close-a-manual-task --root .
deskops next task-close-a-manual-task --root .
deskops edit task task-close-a-manual-task scope "Edited scope." --root .
deskops review record task-close-a-manual-task --kind preflight --operator "Manual operator" \
  --evidence desk/tasks/task-close-a-manual-task.md --reason "Contract read; nothing ambiguous" --root .
deskops review dispose review-task-close-a-manual-task-preflight-1 --verdict accepted --reason "Contract reviewed by the operator" --root .
deskops advance task task-close-a-manual-task --root .
deskops advance task task-close-a-manual-task --root .
```

A task leaves `ritual-execution` only with the review receipts its type asks for
(here `task.docs`: an accepted `preflight` on the task's current contract, so it
is recorded after the last edit). This sandbox has no reviewer model, so the
operator records a human receipt (`engine: human`, `no model available`; see
[Cold context reviews](#cold-context-reviews)); a desk where the model runs uses
`deskops review preflight`. The two advances move the task from `draft` to `active` and then
`ready_for_testing`. `advance` stops at `ritual-closeout`; it never closes a
task. When no outgoing transition condition holds, it exits non-zero and names
the blocked gate.

Before applying an edge, `advance` checks it against the lifecycle the installed
deskops ships: same `relation_type`, same target ritual and same
`attributes.sets.status`. An edge that differs (a desk seeded before CC31 has
`attributes: {}`) would write a state the task model rejects, so `advance` stops
first, exits 1 and leaves the task unchanged:

```text
Error: Cannot advance task-x via task_activates: the edge desk/lifecycle/execution-task_activates.md does not set status active (attributes.sets.status is missing). The desk's lifecycle seeds are out of date: run 'deskops desk update --apply'.
```

`deskops doctor` reports the same seed; `deskops desk update --apply` restores it.

There is no manual override: a transition fires only when its condition
holds, and a blocked task stays where it is while `advance` names the gate.
Closing is `deskops closeout commit` for work that was done, `closeout
resolved-by` for work that already entered the history (for example through a
PR) before the closeout, `closeout supersede` when the task's subject no longer
exists, and `closeout retire` for a task resolved before the ritual lifecycle.

## Closeout

A task's type declares the evidence that closes it (`task.code`: tests + commit + atom|materialization; `task.docs` and `task.decision`: commit + document; `task.external`: external; `task.aggregate`: children + commit; `task.refactor`: task.code's evidence plus goldens). `--evidence` only adds kinds to the type's, never removes one. `deskops closeout verify`
checks exactly that set for a board-routed task, nothing more and nothing less,
and prints `esta tarea declaró X; encontré Y` (declared X; found Y):

| Evidence | What counts |
|---|---|
| `tests` | an existing `.py` file under `tests/`, optionally with `::node`, or a `pytest <path>` reference |
| `atom` / `materialization` | one gate: an atom reference, or graph/materialization coverage or a routed follow-up reference for every path in `files`; exempt in a desk without local atom documents |
| `commit` | a lowercase 7-40 character commit id resolving to `HEAD` or an ancestor |
| `document` | an existing `.md`, `.rst`, `.txt`, `.adoc`, or `.yaml` file in `references` or `files`, outside `tests/` and `desk/tasks/` |
| `external` | an `http(s)` URL in `references`, for work tracked outside the repository |

Changed `.py` files in a task that did not declare `tests` print a visible alert
without blocking. A task created before the field existed is gated as code and
alerted to declare its evidence with
`deskops edit task <id> closeout_evidence '["commit", "document"]'`.

Verify before adding evidence. It exits `1` and prints the missing gates:

```bash
deskops closeout verify --root . --task task-close-a-manual-task
```

The manual task was authored with `--task-type task.docs`, so its type declares
`commit` and `document`: the gate asks for no test file. The example still writes
`tests/test_manual_smoke.py` because the task's `--validation` names it, and
the `pytest ...` reference is extra context the gate does not read. The atom
file is the document evidence. The commit reference must already exist, so use
an earlier commit such as the repository seed or the authoring commit. The
closing commit does not exist yet.

```bash runnable
mkdir -p tests
cat > tests/test_manual_smoke.py <<'EOF'
def test_manual_smoke():
    assert True
EOF

commit="$(git rev-parse HEAD)"
deskops edit task task-close-a-manual-task references \
  "[\"desk/atoms/atom-operator-manual-evidence.md\", \"pytest tests/test_manual_smoke.py::test_manual_smoke\", \"$commit\"]" \
  --root .
deskops edit task task-close-a-manual-task files \
  '["desk/atoms/atom-operator-manual-evidence.md"]' --root .
deskops closeout verify --root . --task task-close-a-manual-task
```

`deskops closeout commit` creates the closing commit itself. It offers two
routes:

- `--run-dir runs/subagents/<dir>` links the commit to subagent run evidence
  and adds `Task-Id`, `Run-Dir`, `Run-Id`, and `Session-Sha256` trailers.
- `--no-run --reason "<why>"` closes manually and adds `Task-Id`,
  `Closeout-Mode: manual`, and `Closeout-Reason` trailers.

Either route removes the task bundle from `desk/tasks/`, removes it from
`desk/tasks/Board.md`, records the commit in `runs/subagents/index.jsonl`, and
commits only the paths it staged. Unrelated staged work stays staged. `--paths`
accepts files and directories.

```bash runnable
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --no-run --reason "Operator manual runnable example" \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

A subagent-run closeout instead looks like:

```bash
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --run-dir runs/subagents/20260101-120000-task-close-a-manual-task \
  --run-id 6046eaef \
  --session ~/.pi/agent/sessions/<dir>/6046eaef/run-0/session.jsonl \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

### Supersede or retire a task

Two closes skip the evidence gates because no work is being proven.
`closeout supersede` closes a task whose subject no longer exists. `closeout
retire` removes a task whose status is already `resolved`, `closed`, `done`,
`complete` or `cancelled`, as pre-lifecycle tasks are, or `superseded`,
`deferred` or `candidate` with an empty history (what a desk migrated before
CC31 left; a `superseded` task with only its `superseded` record, what
`desk update --apply` makes of it, too). Retire reads the task's frontmatter, so it also removes a task its
model rejects. `closeout supersede` also closes a task
its model rejects (a lifecycle no migration decides, such as a `draft` after
`task_hands_to_closeout`): it reads and writes the frontmatter, with the same
commit and trailers. Both close one invalid task while others remain invalid:
sldb names the others with `store/doc-invalid` and goes on. Both need `--reason` and at least one
`--ref` (an ancestor commit; supersede also accepts an existing path), make
exactly one closing commit with `Closeout-Mode: superseded` or
`Closeout-Mode: legacy-resolved` trailers, and take the task off the Board.

```bash runnable
deskops add task --root . \
  --title "Superseded manual task" \
  --task-type task.docs \
  --goal "Goal." --scope "Scope." --validation "pytest"
deskops closeout supersede --root . \
  --task task-superseded-manual-task \
  --reason "The feature this task targeted was removed before any work started" \
  --ref "$(git rev-parse HEAD)"
```

```bash
deskops closeout retire --root . \
  --task task-already-resolved \
  --reason "Resolved before the ritual lifecycle existed" \
  --ref 3900ad4
```

### Close a task whose work already entered the history

`closeout resolved-by` closes a task whose work was already committed, for
example merged through a PR, before anyone ran its closeout. It does not ask for
an atom per changed file. Its evidence is a `--reason`, at least one `--ref`
that is a commit at HEAD or an ancestor (further refs may be ancestor commits or
http(s) URLs, such as the PR), and at least one `--test` that the tests gate
accepts for the task's `files`. A ref or test that does not resolve is refused
and nothing is written. It makes exactly one closing commit with
`Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and
one `Closeout-Test` per test; the task is marked `resolved` (history
`resolved-by`) and leaves the Board. `--paths` adds paths to the closing commit
and `--message` replaces its subject. Like supersede, it also closes a task its
model rejects (a lifecycle no migration decides, such as a `draft` after
`task_hands_to_closeout`): it reads the task's `files` and history from the
frontmatter, applies the same ref and test gates, writes `status: resolved` and
the `resolved-by` record into the frontmatter (validated with `TaskDoc`, restored
if it fails) and makes the same closing commit with the same trailers. With a
store, each of the three closes its invalid task while another one of the same
model remains invalid: sldb names it with `store/doc-invalid` and goes on, so
the tasks can be closed one after the other. Tasks that are not the one being
closed can also be migrated with `deskops desk update --apply` or decided by
hand.

```bash
deskops closeout resolved-by --root . \
  --task task-fix-thing \
  --reason "The fix entered main through PR #42 before the closeout" \
  --ref 9f64f0f --ref https://example.com/org/repo/pull/42 \
  --test tests/test_fix_thing.py
```

When the task's code entered another repository (a task.code of a coordinating
desk whose code lives in a sibling repo), qualify the ref and the test with that
repository's id: `--ref <repo-id>:<sha>` and `--test <repo-id>:<test path>`.
The id is looked up in the desk's own registry, `desk/registry/repo-*.md`,
written by `deskops repo register`. The reference is cut at its first `:`: when
what comes before it is a registered id, the rest is checked in that
repository's registered root, with the same rules as a local reference (a
lowercase commit id that is its HEAD or an ancestor; an existing `.py` file
under one of its `tests/` directories, optionally with a pytest `::node`). The
task's `files` do not widen where another repository's tests live. A prefix
that is not a registered id (or a reference without `:`) is checked locally as
before, and a prefix naming the desk itself (its `project_identity`, or a
registered repository whose root is the desk's root) is local. A registered
repository whose root is missing on this machine refuses the close with
`Registered repository <id> is not at <path> on this machine.` and writes
nothing. The closing commit is the same, made in the desk's repository, and its
`Closeout-Ref` and `Closeout-Test` trailers keep each reference as written
(`Closeout-Ref: infra:87671716`). `closeout verify`, `closeout commit` and
`closeout supersede` still accept only local evidence.

```bash
deskops repo register infra --path /srv/infra --id infra --store .sldb
deskops closeout resolved-by --root . \
  --task task-wire-infra \
  --reason "The code entered infra through PR #7" \
  --ref infra:87671716 --ref https://example.com/org/infra/pull/7 \
  --test infra:tests/test_wire.py
```

## Issues

Issues are plain Markdown files under `desk/issues/` or
`desk/drawer/issues/`. They are intentionally not modeled documents.
`deskops issue list` filters by `open`, `closed`, or `all`. `deskops issue close`
rewrites the status and appends a `## Resolution` section; it never deletes the
file.

```bash runnable
mkdir -p desk/issues
cat > desk/issues/issue-manual-example.md <<'EOF'
# Manual example issue

## Status

open

## Problem

The manual needs an issue example.
EOF

deskops issue list --root .
deskops issue close issue-manual-example --reason "Manual example" --ref . --root .
deskops issue list --status closed --root .
```

### Replace text in an unmodeled desk file

`deskops desk replace` edits a file under `desk/` that no `deskops edit`
subject reaches (issue bodies, drawer notes, role prompts, the tag namespace
file). `--old` must occur exactly `--count` times (default 1); a modeled
document is refused and pointed at its `edit` verb. The write is sldb's
`replace_text` inside the desk transaction: a store-tracked file (a role prompt)
must still validate under its model after the replacement, or nothing is written
and the command exits 1 with `Refusing to replace in <path>: ...`.

```bash runnable
deskops desk replace desk/issues/issue-manual-example.md --root . \
  --old "The manual needs an issue example." \
  --new "The manual has an issue example."
```

## Atoms

Atoms are the durable knowledge layer. The `atoms` commands cover namespaces,
protoatoms, typed atoms, crossroads, domain trees, provenance-preserving
creation, splitting, merging, deletion, and validation.

### Namespaces, crossroads, and the domain tree

A domain tag such as `domain:manual.docs` needs a written crossroad for every
parent path, created top-down. Crossroads describe what hangs below a path.
sldb checks it (and that every atom or protoatom namespace is declared) as its
tag family, from the declaration `deskops init` and `deskops desk update --apply`
write in `.sldb/store.yaml`; a desk without a store checks neither. See
`docs/atoms.md` ("Who checks the namespaces and the domain parents").

```bash runnable
deskops atoms add-namespace manual \
  --meaning "Manual-only tags" \
  --use-when "Operator manual examples" \
  --do-not-use-when "Durable knowledge" \
  --example manual:example --root .

deskops atoms crossroad manual \
  --title "Manual domain" --content "Root of manual examples." --root .
deskops atoms crossroad manual.docs \
  --title "Manual docs" --content "Documentation children." --root .

deskops atoms proto proto-manual \
  --title "Manual proto" --content "Free text." \
  --tag domain:manual.docs --root .

deskops atoms tree --root .
```

### Type a protoatom

`atoms type` converts a protoatom into a tracked model document and keeps the
protoatom as a redirect stub. For `AtomDoc`, pass `--content-field answer`
because `AtomDoc` has no `content` field.

```bash runnable
deskops atoms type proto-manual \
  --model AtomDoc \
  --id atom-typed-manual \
  --content-field answer \
  --data '{"title":"Typed manual atom","five_wh_one_plus":"what"}' \
  --root .
```

### Create an atom from a source

`atoms create` preserves exact provenance from a pill field, a missing graph
finding, or a diagram source.

```bash runnable
deskops atoms create atom-from-manual-pill \
  --five-wh-one-plus what \
  --from-pill pill-pattern-manual-examples-stay-runnable \
  --root .
```

Other source routes:

```bash
deskops atoms create atom-from-graph \
  --five-wh-one-plus what \
  --from-graph source-id->target-id \
  --graph .deskops/graph.json --root .

deskops atoms create atom-from-diagram \
  --five-wh-one-plus what \
  --from-diagram docs/diagrams/example/source.mmd --root .
```

### Merge, delete, and validate

Merge rewrites every reference to the source atom so that it names the target,
in the same transaction as the merge. It covers fields such as a task's
`atoms`, `atom:atom-<source>` anywhere in a task or issue, and a bare
`atom-<source>` under a Related Atoms heading. The source stays as a redirect
stub. `atoms delete` and `atoms split` find the same references. `atoms split` is not shown here: since CC35a sldb
refuses headings inside a field, so a sectioned atom cannot be written through
the CLI (see the drawer entry
task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field).

```bash runnable
deskops add atom --root . \
  --title "Merge source manual atom" \
  --five-wh-one-plus what \
  --answer "One."
deskops add atom --root . \
  --title "Merge target manual atom" \
  --five-wh-one-plus what \
  --answer "Two."
deskops atoms merge atom-merge-source-manual-atom \
  --into atom-merge-target-manual-atom --root .

deskops add atom --root . \
  --title "Delete manual atom" \
  --five-wh-one-plus what \
  --answer "Temporary."
deskops atoms delete atom-delete-manual-atom --root .

deskops atoms validate --all --root .
deskops list atoms --root .
deskops show atom atom-typed-manual --root .
```

`list atoms` and `show atom` are the current spellings; `atoms list` and
`atoms show` are deprecated aliases. `atoms delete` refuses to delete an atom with inbound references
unless `--force` is passed.

### Reorganize atoms by tag namespace

`atoms reorganize` moves atoms into folders derived from the
`atom_folder_axis` configured in `desk/config.json`. Without that config it
exits non-zero:

```bash
deskops atoms reorganize --dry-run --root .
# Error: No 'atom_folder_axis' configured in desk/config.json; nothing to reorganize.
```

Configure one namespace, then run it:

```json
{ "atom_folder_axis": "object" }
```

```bash
deskops atoms reorganize --dry-run --root .
deskops atoms reorganize --root .
```

## Graph

The graph surface builds a KGDB snapshot, shows one node's neighbors, reports
missing declared targets, and writes review-only self-reflection findings.

```bash runnable
deskops graph build --root . --output .deskops/graph.json
deskops graph neighbors atom:atom-from-manual-pill --root . --graph .deskops/graph.json
deskops graph missing --root . --graph .deskops/graph.json
deskops graph reflect --root . --graph .deskops/graph.json
```

`graph missing` exits `1` when a declared target does not resolve. For example,
a materialization whose `--target-identity` names a file that does not exist as
a graph node is reported as `missing_declared_target`.

`graph reflect` writes `.sldb/runtime/self_reflection_findings.json` and only
reports findings; it does not edit desk documents.

## Roles, materialization, and drift

Role docs under `desk/roles/` are materialized into pi-agent files.
`deskops materialize` writes them to `~/.pi/agent/agents/` by default; `--out`
overrides the directory. `deskops drift check` compares rendered output with
the installed files and also checks runtime-profile bindings.

A role with `kind: pi` needs a matching `RuntimeProfileDoc` under
`desk/runtimes/`. Without it, drift reports a missing runtime profile.

```bash runnable
cat > desk/roles/manual-role.md <<'EOF'
---
id: role-manual-example
name: manual-example
description: Example role for the operator manual.
kind: pi
model: example-model
fallback_models: []
tools: []
system_prompt_mode: replace
inherit_project_context: true
inherit_skills: true
default_context: fresh
---

# Manual example role

Act as the example role.
EOF

mkdir -p desk/runtimes
cat > desk/runtimes/runtime-pi.md <<'EOF'
---
id: runtime-pi
status: active
kind: pi
binary: pi
model_flag: --model
fallback_models_flag: ''
fallback_models_join: comma
tools_flag: --tools
tools_join: comma
system_prompt_flag: --append-system-prompt
system_prompt_delivery: file
session_flag: --session
extra_args: []
unsupported_role_fields:
- fallback_models
tags:
- system:manual
---

# Pi runtime

## Summary

Pi agent runtime profile.

## Notes

Example profile.
EOF

deskops materialize --root . --out .pi-agent
deskops drift check --root . --out .pi-agent
```

`drift check` exits `1` on any finding. A mismatch names the installed file and
the role doc it was rendered from.

## Runtime and Herdr

The `runtime` commands manage a live Herdr Space. They need a `herdr`
executable and are not part of the runnable walkthrough.

```bash
# Initialize or reuse this desk's Herdr Space.
deskops runtime init --root .
deskops runtime init --root . --agents

# Inspect, focus, and close the Space.
deskops runtime status --root .
deskops runtime attach --root .
deskops runtime stop --root .

# List live agents machine-wide.
deskops runtime workers
deskops runtime workers --format json

# Block on one agent's lifecycle and report blocked/done settles.
deskops runtime supervise deskops-executor --root .
deskops runtime supervise deskops-executor --max-iterations 1 --timeout-ms 30000

# Materialize a RoleDoc + RuntimeProfileDoc as a Scion agent template
# (.scion/templates/<role-name>/: scion-agent.yaml, system-prompt.md, agents.md).
deskops runtime template deskops-executor --root .
deskops runtime template deskops-executor --root . --harness claude \
  --mode executor --task task-fix-thing --agent deskops-e-0123456789ab

# A tester is its own role and mode, with separate scope and completion rules.
deskops runtime template deskops-tester --root . --harness claude \
  --mode tester --task task-fix-thing --agent deskops-t-0123456789ab \
  --task-root . --run-dir runs/subagents/20261110-120000-task-fix-thing-testing
```

`runtime template` needs no live Herdr Space: it writes the template files from
the role and runtime-profile docs. `--mode executor` writes the agents.md for one
bounded task, `--mode tester` writes the independent verification instructions,
and `--mode coordinator` writes it for an agent that owns a desk. An explicit
mode always wins; otherwise only the selected role's own name/id is inspected
(a name or id ending in `-tester` chooses tester; a selected name or id naming a
supervisor/coordinator chooses coordinator; anything else executor). With
`--task` and `--agent` it also records the in_progress RunDoc launch intent under
`runs/subagents/`; its summary says it is intent, not proof of start.
`--task-root` names the repository whose desk owns the task (default `--root`)
and `--run-dir` points at the evidence directory. An existing RunDoc is reused
for reconciliation but never overwritten: a retry gets a new run_dir, and
attempts and their evidence are immutable.

`--context-file` accepts JSON with exactly `project`, `workspace_root`,
`desk_root`, `source_root` and `sldb_root`. `project` is a non-empty Scion slug
or UUID, never a filesystem path; the other four are absolute directories inside
`workspace_root`, where `desk_root` contains `desk/`, `source_root` contains the
`deskops` package and `sldb_root` is sldb's `src` directory. Missing, unknown,
relative, out-of-workspace or invalid values are refused before any template is
written. A valid context emits `DESKOPS_DESK_ROOT`, `DESKOPS_SOURCE_ROOT`,
`DESKOPS_SLDB_SOURCE_ROOT`, `DESKOPS_WORKSPACE_ROOT`, `DESKOPS_SCION_PROJECT`
and `PYTHONPATH=source_root:sldb_root`, plus a volume whose source and target are
`workspace_root`. It carries no secrets. Omitting the flag preserves CLI, path
and environment compatibility; the corrected prompt text is intentionally not
byte-identical to the faulty earlier wording.

Four optional container keys describe how this machine runs the agent:
`memory_limit` (a size such as `6Gi`) and `cpu_limit` (cores, such as `2`) are
written as `resources.limits`; `shared_paths` is a list of absolute host paths
bound at the same path (for example `/dev/shm`, so tests share the host tmpfs and
`/dev/shm/sldb1-tests.lock`); `env` adds static variables such as
`TMPDIR=/dev/shm` and may not redefine the derived ones. Omitted, nothing changes.

The coordinator derives a stable child identity from the task contract:
`deskops-e-<12hex>` for an executor or `deskops-t-<12hex>` for a tester, where
the hex is SHA-256 of `task_id + NUL + contract_sha256 + NUL + role`.
`contract_sha256` is the SLDB `TaskDoc.__contract__` digest. Attempt 1 uses the
base name, attempt 2 appends `-a2`, and there is no attempt 3; labels are
`deskops.task_id`, `deskops.contract_sha256`, `deskops.role` and
`deskops.attempt`. The runtime helper `scion_child_identity(task_path, role,
attempt)` returns that name and label set, and `scion_start_argv` builds the
explicit native start argv. These helpers only derive identity/argv; native
Scion orchestration remains Scion, not a DeskOps scheduler.

Native labels must be printable ASCII and at most 63 characters. The helper
preserves the full canonical task id and 64-hex contract hash in its returned
identity and name derivation; `deskops.contract_sha256` carries the 63-hex prefix.
A long or non-ASCII task-id label uses a bounded hash descriptor while TaskDoc
and RunDoc retain the full id. Copy the helper label map exactly rather than
pasting a full 64-hex digest into `--label`.

The generated coordinator reconciles its own existing executor/tester lanes and
completed handoffs before selecting new work; a restart or successful child
completion must not skip its own task or duplicate a child. It reads Scion
activity first and phase only as fallback, because the native bridge can report
`activity=completed` while `phase=running`. A dependency-ready task missing its
preflight/bundle receipt is routine work: run the cheap context review and
adjudicate factual findings before dispatch. Implementation and validation run
from the configured `desk_root`, with template artifacts and evidence under the
assigned desk `runs/` path rather than `/tmp`. Closeout runs
`deskops closeout verify`, reviews the diff, and commits only scoped
implementation/evidence/review paths with `closeout commit --paths` (never
`git add -A`). The coordinator signals `task_completed` only after all authorized
work is closed, declared evidence verified and required phase integration/commit
done; an external blocker is recorded and signalled as blocked, and only an
actual owner decision uses `ask_user`.

`runtime supervise` never answers a blocked agent's prompt and never advances a
task on a done settle. A human or supervisor decides what happens next.

## Cold context reviews

`deskops review` runs the cheap isolated reviewer from
`desk/rituals/context-review.md` and writes the receipts (`ReviewDoc`) under
`desk/reviews/`. The default engine is the `runtime-pi-deepseek-flash` profile
seeded under `desk/runtimes/` by `deskops init` and `deskops desk update --apply`;
`--engine` picks any other `RuntimeProfileDoc` under `desk/runtimes/`. Every run
also writes ritual evidence under
`runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/`.

The reviewer is an external model process, so these examples are illustrative
only; they are not part of the runnable walkthrough.

```bash
deskops review preflight task-fix-thing --root .
deskops review bundle task-fix-thing --root .
deskops review node desk/drawer/plans/gates-por-tipo GC03 --root .
deskops review status task-fix-thing --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

An unchanged input is not reviewed again; a second run does not call the model.
`review status` compares the SHA-256 of the exact current builder input bytes
with all receipts for the key. No receipts means `missing`; receipts with no
matching input mean `stale`, regardless of their old verdict. Among matching
receipts, priority is `accepted`, `rejected`, `pending` (reported as `reviewed`),
then `incomplete` (reported as `technical_failure`). A current accepted
receipt therefore survives later rejected or failed attempts. Task subjects
use the same task id whether plain or pinned with a SHA-256 anchor. Status
preserves receipts and run evidence and does not change lifecycle gates.
See [the source atom](../desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md).

`--max-attempts` (default 2) caps the good
attempts per key; `--force --reason` is the only way to re-review a key whose
input already has a good attempt. A transport failure (non-zero exit, timeout,
or output without `REFORMULACION`) is recorded with `technical_ok: false` and a
`verdict: incomplete` / `reason: technical` receipt, kept separate from
comprehension findings.

Reproduction, goldens and owner receipts are not produced by a model: whoever
operates the desk records them with the evidence they checked, and disposes of
them like any other receipt.

```bash
deskops review record task-fix-thing --kind reproduction --evidence runs/repro.log --reason "..." --root .
deskops review record task-fix-thing --kind owner --reason "approved by the owner" --root .
```

`record` writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor`
from the desk identity, and the evidence paths in `summary`. Each `--evidence` is
an existing file inside the root; anything else fails with
`Error: evidence not found: <path>` (exit 1) and writes nothing. `reproduction`
and `goldens` need at least one `--evidence`; `owner` may carry only `--reason`.
`input_sha256` is the SHA-256 of `<path>\n<content>\n` for each evidence file,
paths relative to the root, sorted and without repeats (empty without evidence).
`--kind` accepts `reproduction`, `goldens`, `owner`, `preflight` and `bundle`;
`node` comes from its own command. `deskops review dispose <review-id>` writes
the verdict.

A desk with no model to run the reviewer (the CI scenarios, the quickstart) can
still activate a task: whoever operates it records the `preflight` and `bundle`
receipts by hand. `--operator <name>` is required for those two kinds; without
it the command fails and writes nothing. The receipt keeps `engine: human`,
names the operator as its `actor`, and says `no model available` in its title
and `summary`, so nobody mistakes it for a model review. It is not a stand-in
for `deskops review preflight|bundle` on a desk where the model runs.

```bash
deskops review record task-fix-thing --kind preflight --operator "Ana" --evidence desk/tasks/task-fix-thing.md --reason "read the contract; no ambiguity" --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

## Verb coverage

This table maps every CLI verb to the section that documents it.

| Verb | Section |
|---|---|
| `about` | Orient yourself |
| `doctor`, `status` | Check desk health |
| `faq` | Orient yourself |
| `bootstrap` | Help and bootstrap |
| `init` | Initialize the repository |
| `inbox` | Inbox, messages, and drawer |
| `message send/list/read/ack` | Send, list, read, and acknowledge messages |
| `promote inbox-to-drawer-task` | Promote an inbox note to a drawer candidate |
| `drawer remove` | Remove a drawer entry |
| `retire` | Retire any other desk document |
| `issue close/list` | Issues |
| `add task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Add artifacts |
| `edit ...` | Edit artifacts |
| `bind pill` | Bind reusable context pills |
| `next`, `next --why`, `next --diagram` | Inspect the lifecycle graph; Inspect, edit, and advance a task |
| `list tasks/pills/rituals/boards/atoms/materializations/repositories/inbox-notes/faq-docs/steps` | List artifacts |
| `show task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Show artifacts |
| `advance task` | Inspect, edit, and advance a task |
| `repo register/whoami/remove` | Repository identity and the ecosystem registry |
| `desk install/migrate/update` | Desk scaffold, migration, and repair |
| `desk replace` | Replace text in an unmodeled desk file |
| `atoms add-namespace/list/reorganize/show/validate/create/delete/split/merge/crossroad/proto/type/tree` | Atoms |
| `graph build/neighbors/missing/reflect` | Graph |
| `materialize` | Roles, materialization, and drift |
| `drift check` | Roles, materialization, and drift |
| `closeout verify/commit` | Closeout |
| `closeout supersede/retire` | Supersede or retire a task |
| `closeout resolved-by` | Close a task whose work already entered the history |
| `runtime init/status/attach/stop/workers/supervise/template` | Runtime and Herdr |
| `review node/preflight/bundle/status/dispose/record` | Cold context reviews |

FILE:docs/deskops-ui.md
# deskops view: el contrato de datos de la UI de deskops

`deskops view {board,task <id>,drawer,inbox,agents} --root <repo> --format json|text`
produce las vistas que dibuja la UI de deskops (graph_ui, `frontends/desk/`).

`board` y `task` son `ViewDoc` de sldb: las semillas `deskops/data/views/board.md` y
`task.md` (viven solo en el paquete, sin `desk/views/`), trackeadas como `ViewDoc` en el
store del propio repo deskops. `deskops view` las evalúa con `sldb.api.run_view` sobre el
store del desk y `deskops.cli.commands.view.project(view, resultado, root)` proyecta el
resultado a este contrato. graph_ui lee `GET /views/<vista>` de `sldb serve` (con ETag) y
llama a la misma `project` en proceso, así que sirve exactamente el mismo JSON. `drawer`,
`inbox` y `agents` los arma el CLI (ver «Fuentes de cada campo»).

Mientras sldb no resuelva una `ViewDoc` de un store enlazado (hipótesis H9), `board` y
`task` responden solo en un desk cuyo propio store trackea las `ViewDoc` (el repo deskops);
en los demás salen con el sobre de error `Unknown view: <vista>`.

Reglas comunes:

- **Solo lectura.** Ninguna vista escribe en `desk/`, `.sldb/` ni `runs/`.
- **Una lectura por corrida.** `board` y `task` abren un `read_snapshot`: la ruta y el
  payload de cada tarea, sus transiciones, el grafo de reglas y el contexto del grafo de
  closeout se leen una vez y se comparten entre las tarjetas. El grafo no recorre `runs/`
  salvo que una materialización declare un `target_identity` allí. Es una optimización de
  lectura: el JSON y el texto no cambian (los fijan los goldens de `tests/test_view_goldens.py`).
- **Sin datos inventados.** Una referencia que no resuelve (pill, atom, tarea del Board,
  nota, línea del índice de corridas, runtime de Herdr) no aparece como dato: va a
  `errors` como `{"reference": "<id o ruta>", "cause": "<por qué>"}`; si la referencia la hace
  una tarea (una pill o un atom de la tarea), el error lleva además `"task": "<id de la tarea>"`
  para que la UI marque la tarjeta.
- `--format json` es el contrato estable; `--format text` es un resumen legible.
- Toda vista lleva `view` (nombre), `contract` (versión, hoy `1`), `root` (ruta absoluta
  del repo) y `errors`.
- Un error que impide la vista entera (no hay `desk/tasks/Board.md`, la tarea no resuelve)
  sale como el sobre de error de deskops (`{"ok": false, "error": {...}}`) con código 1.

## board

Una columna por nodo del ciclo de vida, en el orden de
`deskops/spec/workflows/task_lifecycle.yaml` (`ritual-execution`, `ritual-testing`,
`ritual-closeout`). Las tareas salen de `desk/tasks/Board.md` (el Board es la verdad).

```json
{
  "view": "board", "contract": 1, "root": "/abs/repo",
  "board": {"path": "desk/tasks/Board.md", "pills": [{"id": "pill-…", "title": "…", "source": "board"}]},
  "columns": [
    {"node": "ritual-execution", "phase": "execution", "purpose": "…", "in_lifecycle": true,
     "count": 1, "tasks": [CARD]}
  ],
  "counts": {"tasks": 1, "by_node": {"ritual-execution": 1, "ritual-testing": 0, "ritual-closeout": 0},
             "gates_holding": 1, "gates_total": 1},
  "errors": []
}
```

Una tarea cuyo `current_node` no es un nodo del ciclo de vida aparece en una columna
extra con `in_lifecycle: false` y además en `errors`.

`CARD`:

```json
{
  "id": "task-…", "title": "…", "status": "draft", "current_node": "ritual-execution",
  "task_type": "code", "path": "desk/tasks/task-….md",
  "gates": [{"relation_type": "task_activates", "target": "ritual-testing", "condition": "", "holds": true}],
  "gates_holding": 1, "gates_total": 1,
  "closeout": {
    "ok": false, "declared": ["tests", "commit"], "found": [], "summary": "…",
    "implicit_code": false, "alerts": [],
    "evidence": [{"gate": "tests", "state": "pending", "evidence": [], "findings": [{"code": "…", "message": "…"}]}]
  },
  "pills": [{"id": "pill-…", "title": "…", "source": "task|board"}],
  "atoms": [{"id": "atom-…", "title": "…"}]
}
```

- `gates` es exactamente lo que devuelve `DeskopsOperations.show_task` (transiciones que
  salen del nodo actual, con su condición sldb y si se cumple hoy).
- `closeout` resume `verify_task_closeout`: `declared`/`found` tal cual; `evidence` trae
  una entrada por compuerta (`tests`, `atom_or_materialization_link`, `commit`,
  `document`, `external`) con `state`:
  `holds` (la compuerta se cumple), `pending` (falta, y la tarea aún no está en
  `ritual-closeout`) o `failing` (falta y la tarea está en `ritual-closeout`, o el tipo
  declarado no existe en el vocabulario).
- `pills`: `effective_pills` de la tarea (`source: task`) más las pills del Board
  (`source: board`), resueltas a `PillDoc`, igual que las fusiona `deskops next`.
- `atoms`: `effective_atoms` más las referencias `atom-*`, resueltos a `AtomDoc`.

## task

```json
{
  "view": "task", "contract": 1, "root": "/abs/repo",
  "task": {
    CARD…,
    "on_board": true,
    "why": "…", "goal": "…", "scope": "…", "implementation_path": "…",
    "validation": ["…"], "done_when": "…", "references": ["…"], "files": ["…"],
    "depends_on": ["…"], "inherits_from": ["…"], "from_drawer": "", "history": ["task_activates"],
    "pills": [{"id": "…", "title": "…", "source": "task", "what": "…", "when": "…", "how_not": "…"}],
    "atoms": [{"id": "…", "title": "…", "question": "what", "answer": "…"}]
  },
  "next": {"phase": "execution", "ritual": "desk/rituals/execution.md", "next_actions": ["…"], "advance_when": ["…"]},
  "revision": "<sha256 hex>",
  "errors": []
}
```

- `validation`, `done_when` y `references` son los efectivos (con herencia).
- `next` viene de `next_action_report`; si falla, `next` es `null` y la causa va a `errors`.
- `revision` = el ETag de la vista `task` (`run_view(...)["revision"]`, GD25): cambia cuando
  cambia la tarea, el Board o una pill o un atom que la vista leyó. Es la guarda que usa
  `POST /api/desk/advance` de graph_ui: con un `revision` viejo responde 409.

## drawer

```json
{
  "view": "drawer", "contract": 1, "root": "/abs/repo", "count": 1,
  "tasks": [{
    "id": "task-…", "markdown": "<texto completo del archivo>", "title": "…", "status": "deferred",
    "excerpt": ["primeras líneas del cuerpo"], "path": "desk/drawer/tasks/task-….md",
    "command": "deskops add task --root . --from-drawer desk/drawer/tasks/task-….md --title '…'"
  }],
  "errors": []
}
```

- Archivos `desk/drawer/tasks/*.md` salvo `Board.md` y `README.md`.
- `markdown`: el archivo completo, para la vista en crudo (solo lectura).
- `excerpt`: hasta 3 líneas no vacías del cuerpo, sin encabezados ni las pistas en cursiva
  de la plantilla (`_Explain …_`).
- `status` es `null` si el archivo no es un `TaskDoc` válido (la causa va a `errors`).
- `command` es el inicio del comando para autorizar la tarea; el resto de campos
  (`--goal`, `--scope`, `--validation`, `--task-type`…) los decide quien la promueve.

## inbox

```json
{
  "view": "inbox", "contract": 1, "root": "/abs/repo", "count": 2, "open": 1,
  "notes": [{
    "id": "20261104-101500-suggestion-…", "path": "desk/inbox/….md", "kind": "suggestion",
    "title": "…", "sender": "sldb", "target": "deskops", "date": "2026-11-04T10:15:00",
    "status": "open", "acknowledged": false, "acknowledged_by": null, "acknowledged_at": null,
    "body": "…", "revision": "<sha256 de los bytes de la nota>"
  }],
  "errors": []
}
```

- Mismo orden y misma lectura del frontmatter que `deskops message list` (más nuevas
  primero); `acknowledged` es `status == "closed"`, que es lo que escribe `message ack`.
- `date` sale del sello `YYYYMMDD-HHMMSS` del nombre de archivo; sin sello, `null` y aviso.
- `body` es el campo `body` del `InboxNoteDoc`.
- `revision` = `sha256(bytes del archivo de la nota)`: la guarda de las acciones del inbox
  (Reconocer, Pasar al drawer) en la UI.

## agents

```json
{
  "view": "agents", "contract": 1, "root": "/abs/repo",
  "workers": [{"pane": "w1:p1", "kind": "claude", "name": null, "status": "idle", "cwd": "…",
               "title": "…", "workspace": "w1", "seq": 3, "focused": false}],
  "workers_error": null, "live_workers": 1,
  "runs": [{"task_id": "task-…", "run_id": null, "run_dir": null, "commit": null, "mode": "manual", "on_board": false}],
  "runs_total": 122, "runs_limit": 20,
  "errors": []
}
```

- `workers` es la forma pública de `deskops runtime workers` (Herdr, toda la máquina, no
  solo este desk). Si Herdr no responde: `workers: null`, `live_workers: null`,
  `workers_error` con la causa y una entrada en `errors`; nunca una lista vacía muda.
- `runs`: las últimas `--runs` (20 por omisión) líneas de `runs/subagents/index.jsonl`, la
  más nueva primero; `on_board` dice si la tarea sigue en el Board.

## Fuentes de cada campo (CC34)

`run_view` es la vista `ViewDoc` evaluada por sldb. «Agregado CLI, pendiente de sldb Hn»
es un campo que el CLI todavía arma con una operación de lectura que ya existía, porque el
modelo de `ViewDoc` no lo expresa aún; cada uno se retira cuando sldb cierre su hipótesis.

| Campo | Fuente |
|---|---|
| `view`, `contract`, `root` | constantes del CLI |
| `board.path`, `board.pills` (ids) | `run_view`, sección `board` (campos `tasks`, `pills`) |
| tareas del Board, su orden, `errors` de referencias | `run_view`, secciones `board` y `tasks` (el Board manda) |
| columnas (`node`, agrupación) | `run_view`, sección `tasks` (`group_by: current_node`) |
| `phase`, `purpose`, `in_lifecycle` de cada columna | agregado CLI, pendiente de sldb H5 (spec del ciclo de vida) |
| `CARD.id/title/status/current_node/task_type/path` | `run_view`, filas de `tasks` / `task` |
| `CARD.gates`, `gates_holding`, `gates_total` | agregado CLI, pendiente de sldb H1-H3 (`show_task`) |
| `CARD.closeout` | agregado CLI, pendiente de sldb H4 (`verify_task_closeout` sin recibos) |
| `CARD.pills`, `CARD.atoms` (títulos y detalle) | `run_view`, secciones `pills` y `atoms` |
| lista efectiva de pills y atoms; `validation`, `done_when`, `references` | agregado CLI, pendiente de sldb H6 (`resolve_task_payload`) |
| `counts` | suma del CLI sobre las tarjetas |
| `task.on_board` | `run_view`, arista `tasks` del Board |
| `task.why/goal/scope/implementation_path/files/depends_on/inherits_from/from_drawer/history` | `run_view`, fila de `task` |
| `next` | agregado CLI, pendiente de sldb H5 (`next_action_report`) |
| `revision` (task) | `run_view` (ETag de GD25) |
| `drawer.*` (`markdown`, `excerpt`, `command`...) | agregado CLI, lectura del archivo, pendiente de H7 y H10 |
| `inbox.*`, `notes[].revision` | agregado CLI, lectura del archivo, pendiente de H8 y H10 |
| `agents.*` | CLI (`deskops/runtime/desk_agents.py`): no son documentos |

## Mapeo de la pantalla de Stitch a fuentes reales

Copiado de `desk/drawer/plans/deskops-ui/alcance.md` (plan deskops-ui, 2026-11-04).

| Elemento de Stitch | Fuente real | Campo de la vista | Si no hay fuente |
|---|---|---|---|
| Columnas por etapa | `current_node` de cada tarea del Board; orden del spec | `board.columns` | — |
| Checklist de gates de la tarjeta | `show_task` → gates, más evidencia de `verify_task_closeout` | `CARD.gates`, `CARD.closeout.evidence` | — |
| "n de m rituales" | conteo de los mismos gates | `CARD.gates_holding`/`gates_total` | — |
| Pills de la tarjeta | `effective_pills` + pills del Board → `PillDoc` | `CARD.pills` (+ `what/when/how_not` en task) | id en `errors` |
| Atoms | `atoms` y referencias `atom-*` → `AtomDoc` | `CARD.atoms` (+ `answer` en task) | id en `errors` |
| "Promover a Atom" | no hay operación | — | botón deshabilitado: "requiere operación de graduación (no existe)" |
| "Iniciar ejecución" | no hay dispatch | — | deshabilitado: "llega con runtime dispatch (fábrica E3)" |
| Avanzar | `POST /api/desk/advance` de graph_ui | `task.revision` (ETag) | — |
| Diferir a drawer | no hay operación | — | deshabilitado con motivo |
| Drawer: lista y vista raw | `desk/drawer/tasks/*.md` | `drawer.tasks` | — |
| Drawer: "Promover a Desk" | `add task --from-drawer` | `drawer.tasks[].command` | se muestra el comando, no un botón |
| Inbox: lista, lectura, emisor → destino | `InboxNoteDoc` | `inbox.notes` | — |
| Inbox: Reconocer | `deskops message ack` | — (acción de UI05) | — |
| Inbox: Pasar a drawer | `promote inbox-to-drawer-task` | — (acción de UI05) | — |
| Agentes y corridas | `runtime workers`, `runs/subagents/index.jsonl` | `agents.workers`, `agents.runs` | causa en `workers_error` |
| Métricas de cabecera | conteos derivables | `board.counts`, `drawer.count`, `inbox.open`, `agents.live_workers` | ningún porcentaje inventado |
| Hilo del inbox, firmas, prioridad, TTL, autor, versión | no existe | — | no se dibuja |
| Gates por tipo, recibos, `anchor_state` | plan `gates-por-tipo`, sldb GO07 | — | no se dibuja hasta que existan |

FILE:desk/drawer/plans/gates-por-tipo/dag.yaml
id: deskops-gates-por-tipo
revision: 3
revision_note: 'Rev 3 (2026-11-06): plan congelado (frozen) por decisión del dueño (deskops-como-config-arbol.md, T0.2, DK2): GC01, GC02, GC06 y GC03 cerrados en main de deskops; GC04, GC05 y GC07-GC11 no se promueven aquí y se rehacen en el plan deskops-como-config (ver frozen_note). Rev 2 (2026-11-05): gates.G_TYPES.evidence corregida (task.debug no es subtipo de task.code, como fijan brief.md §Tipos y GC01), hallada en el preflight de GC01. Rev 1 (2026-11-04): plan inicial, lado consumidor del plan grafo-operable de sldb (rev 9). Sin revisión en frío todavía. execution_authorized=false.'
status: frozen
frozen_note: 'Congelado tras GC03 (2026-11-06). Cerrados: GC01, GC02, GC06 y GC03 (squash 9df4c82a; closeout commits en main de deskops). GC04, GC05 y GC07-GC11 no se ejecutan en este plan: los toma desk/drawer/plans/deskops-como-config/ (GC04 → CC31; GC05 y G_CONSUMER → CC32; GC07 y GC09-GC11 → CC33 y CC35 donde aplican, el resto queda pendiente del dueño; GC08 → regla 5 de alcance.md en cada nodo). Gate G_GATES_FROZEN de ese plan.'
as_of: '2026-11-04'
source: dag.yaml es canónico; brief.md, alcance.md y decisiones.md son sus fuentes de contexto
execution_authorized: false
estimate_legend:
  S: un entregable acotado, chico; no es promesa de tiempo
  M: una capacidad o contrato acotado; se parte al promover si tiene más de un entregable
  L: toca el núcleo de deskops (modelos o ciclo de vida); se parte al promover
gates:
  G_SLDB_LANG:
    title: Lenguaje de predicados unificado disponible en sldb
    state: pending
    resolver: plan grafo-operable de sldb, nodo GO05 cerrado en main de sldb; deskops pinnea esa versión en pyproject.toml
    evidence: sldb docs find --where acepta any()/all() sobre una relación y --explain nombra la cláusula; versión de sldb con GO05 en pyproject.toml de deskops
  G_SLDB_RULES:
    title: RuleDoc, rules check y rules explain disponibles en sldb
    state: pending
    resolver: plan grafo-operable de sldb, nodo GO06 cerrado; versión pinneada en pyproject.toml
    evidence: sldb rules explain RULE SUBJECT devuelve el finding con node, holds, clause, seen; RuleDoc con subject model <= X, where, condition, severity, moment
  G_SLDB_ANCHORS:
    title: 'Anclas doc: con hash de contrato disponibles en sldb'
    state: pending
    resolver: plan grafo-operable de sldb, nodo GO07 cerrado; versión pinneada en pyproject.toml
    evidence: un campo __doc_anchors__ con doc:Model:name se guarda pinneado a @sha256:<hash>; anchors check reporta intact/changed/lost; anchor_state consultable desde una regla por ^campo
  G_SLDB_EVAL:
    title: Evaluación on_transition con edges_holding findings y edges_blocked
    state: pending
    resolver: plan grafo-operable de sldb, nodo GO08 cerrado; versión pinneada en pyproject.toml
    evidence: edges_holding devuelve effects y findings por arista; edges_blocked(store, node, subject) devuelve las aristas con finding error; el test end-to-end de GO08 (Task + Review + regla any(^subject ...)) pasa en sldb
  G_SLDB_EFFECTS:
    title: Transiciones como datos de la arista (attributes.sets, terminal, apply_effects)
    state: pending
    resolver: plan grafo-operable de sldb, nodo GO09 cerrado; versión pinneada en pyproject.toml
    evidence: edges_holding devuelve effects = {sets resueltos, terminal}; apply_effects(subject, effects, model) valida y devuelve el payload nuevo
  G_TYPES:
    title: Tipos de tarea cerrados y con jerarquía en deskops
    state: pending
    produced_by: GC01
    resolver: cierre de GC01 (revisión en frío aceptada por el desk de deskops, tests verdes, closeout commit)
    evidence: add task --task-type rechaza un tipo no registrado; model <= TaskCodeDoc incluye a task.refactor y no a task.debug; TASK_TYPE_EVIDENCE no existe
  G_RECEIPTS:
    title: deskops review escribe recibos ReviewDoc en el desk
    state: pending
    produced_by: GC03
    resolver: cierre de GC03
    evidence: deskops review preflight <task> deja un ReviewDoc en desk/reviews/ con subject doc:<Modelo>:<id> y evidencia bajo runs/; deskops review dispose escribe el veredicto
  G_CONSUMER:
    title: deskops prueba el gate de activación con RuleDoc (gate externo del plan de sldb)
    state: pending
    produced_by: GC05
    resolver: cierre de GC05 y nota a sldb por deskops message send --to sldb con el hash del commit
    evidence: en un desk temporal, una tarea sin recibo de revisión no se activa y la explicación nombra la cláusula; con recibo atado al hash de contrato vigente, se activa; con el contrato editado, el recibo queda changed y vuelve a bloquear
external_references:
  sldb_producer_plan:
    repo: sldb
    path: desk/drawer/plans/grafo-operable/
    status: reviewed_pending_promotion (rev 9; GO01 cerrado)
    note: 'produce GO02 __contract__, GO05 lenguaje, GO06 RuleDoc, GO07 anclas doc:, GO08 evaluación y edges_blocked, GO09 effects. Este plan no inventa API más allá de lo que rev 9 fija; lo que no fija va como hipótesis en el scope del nodo.'
  governed_review_driver:
    repo: sldb
    path: desk/drawer/plans/grafo-operable/context_review.py
    status: reference
    note: modos node, preflight, bundle, status; SYSTEM, ARGV y SELECTION del revisor; tope --max-attempts 2; GC03 lo reemplaza por deskops review
  earlier_review_driver:
    repo: deskops
    path: desk/drawer/plans/workspace-documental/context_review.py
    status: reference
    note: modos run y status; tests/test_context_review_helper.py lo importa por ruta; GC03 lo retira junto con ese test
  sldb_inbox_note:
    repo: deskops
    path: desk/inbox/20261104-213901-suggestion-sldb-eval-a-reglas-declaradas-plan-grafo-operable-en-sldb-desk-drawer-plans-grafo-operable.md
    status: open
    note: nota de sldb (GO01) que nombra lo que queda para deskops; se cierra (ack) al autorizar este plan
hierarchy:
  root:
    id: ROOT
    title: Gates por tipo de tarea en deskops
    owner_repo: deskops
    scope: 'deskops escribe sus gates de workflow como documentos (tipos de tarea con jerarquía, RuleDoc de activación por tipo, ReviewDoc como recibo, efectos en las aristas) y sldb los evalúa; se cierran las dos vías que saltan gates; un comando deskops review reemplaza los scripts de revisión en frío; la composición (parent_id, children, depends_on) pasa al grafo. Tres paquetes: tipos y recibos (sin dependencia de sldb), gates en el grafo (depende de los nodos GO05 a GO09 de sldb), composición y grafo. El orden entre paquetes lo imponen las aristas depends_on de sus hijos.'
    acceptance: 'Todos los hijos cerrados; G_TYPES, G_RECEIPTS y G_CONSUMER satisfechos y G_CONSUMER informado a sldb. CHANGELOG y docs al día significa que cada hijo cumplió su propia aceptación de CHANGELOG y docs; ROOT no agrega criterio.'
    children: [PC01, PC02, PC03]
  packages:
    - id: PC01
      title: Tipos, recibos y revisor
      node_role: aggregate
      owner_repo: deskops
      children: [GC01, GC02, GC03]
      scope: 'Lo que deskops puede hacer sin esperar a sldb: tipos de tarea como modelos con jerarquía y evidencia de cierre declarada en el tipo (GC01); el modelo ReviewDoc como recibo con subject en __doc_anchors__ (GC02); el comando deskops review que produce esos recibos y retira los dos scripts (GC03). Antes de G_SLDB_ANCHORS el subject se guarda sin hash (sldb lo pinnea cuando GO07 exista; deskops no calcula hashes).'
      acceptance: 'G_TYPES y G_RECEIPTS satisfechos; add task --task-type solo acepta tipos registrados; deskops review preflight y bundle dejan ReviewDoc y evidencia en runs/; ningún script context_review.py queda en los drawers de deskops.'
    - id: PC02
      title: Gates por tipo en el grafo
      node_role: aggregate
      owner_repo: deskops
      children: [GC04, GC05, GC06, GC07, GC08]
      scope: 'Que el ciclo de vida sea entero grafo y que los gates sean reglas: efectos en las aristas y advance por edges_holding (GC04); RuleDoc de activación por tipo y explicación por edges_blocked, que produce G_CONSUMER (GC05); cierre de advance --to y de edit task sobre campos del ciclo de vida (GC06, sin dependencia de sldb); herencia de tareas leída del grafo y cierre sobre effective_* (GC07); rituales y manual al día (GC08). GC06 puede correr apenas cierre GC01; GC04 y GC05 esperan a sldb.'
      acceptance: 'Una tarea task.code sin recibos no se activa y deskops advance muestra el finding con la cláusula; con recibos intactos y aceptados se activa y su status lo escribe el efecto de la arista; advance --to no existe; edit task status falla; task_lifecycle.yaml no tiene sets_status ni terminal; los rituales nombran deskops review y ReviewDoc.'
    - id: PC03
      title: Composición y grafo
      node_role: aggregate
      owner_repo: deskops
      children: [GC09, GC10, GC11]
      scope: 'Que un plan como este se promueva nodo a nodo y el DAG quede en el grafo: parent_id, children y task.aggregate con su regla (GC09); promoción de un nodo de dag.yaml a TaskDoc con tipo, padre y dependencias, y revisión de nodos desde el mismo archivo (GC10); deskops graph leyendo las aristas de sldb en lugar del snapshot por regex (GC11).'
      acceptance: 'Un nodo de dag.yaml se promueve con add task --from-drawer <plan>/dag.yaml --node <id> y la tarea resultante tiene tipo, parent_id y depends_on como aristas del store; un agregado no se activa hasta que sus hijos cierran; deskops graph neighbors de una tarea lista parent_id, children y depends_on tomados del índice de sldb.'
tasks:
  - id: GC01
    title: Tipos de tarea como modelos con jerarquía y evidencia de cierre declarada en el tipo
    kind: code
    node_role: delivery
    parent_id: PC01
    owner_repo: deskops
    estimate: L
    depends_on: []
    requires: []
    scope: 'Módulo deskops/models/task_types.py con las subclases de TaskDoc de la tabla de brief.md §Tipos: TaskCodeDoc (task.code), TaskDocsDoc (task.docs), TaskDebugDoc (task.debug, hereda de TaskDoc: exige reproduction en lugar de bundle y por eso no puede ser subtipo de task.code, donde los gates solo se suman), TaskRefactorDoc (task.refactor, hereda de TaskCodeDoc y suma goldens), TaskDecisionDoc (task.decision), TaskAggregateDoc (task.aggregate; sus campos parent_id/children los agrega GC09), TaskExternalDoc (task.external). Cada subclase fija task_type a su nombre (Literal con default) y declara dos atributos de clase: __closeout_evidence__ (tupla del vocabulario de closeout_gates.py:23, más children para el agregado y goldens para refactor, que este nodo solo declara: su verificación es de GC09 y de un nodo posterior) y __activation_receipts__ (tupla de kinds de ReviewDoc que la regla de GC05 exigirá: preflight, bundle, reproduction, goldens, owner). TaskDoc base conserva el campo task_type: str para leer documentos viejos y declara __contract__ = [title, goal, scope, implementation_path, files, validation, done_when] (sintaxis de sldb GO02 (e); si la versión de sldb instalada no la lee, el atributo es inerte hasta que la lea). Registro: las subclases entran en MODEL_REFS (bootstrap.py:26) y se heredan en cada desk como los demás modelos (bootstrap.py:118-160); un desk agrega tipos propios en desk/models/*.py (DC7) y deskops desk update --apply los registra con sldb add_model y pythonpath = raíz del desk; hipótesis a verificar en el TaskDoc: sldb registra una subclase cuya base es un modelo heredado (federado) y base_models la resuelve. add task --task-type <nombre> rechaza un nombre que no sea un tipo registrado (familia model <= TaskDoc) con el mensaje que lista los tipos; sin --task-type, el default es task.code y se avisa en el envelope. closeout_evidence deja de escribirse en la tarea nueva: se lee del tipo (TASK_TYPE_EVIDENCE y evidence_for_task_type se borran); --evidence solo puede agregar kinds a los del tipo (piso; pendiente del dueño en decisiones.md) y un kind que quite falla. Las tareas existentes conservan su campo closeout_evidence, que el cierre sigue leyendo como override por encima del tipo. El documento de una tarea se guarda bajo el modelo de su tipo (TaskCodeDoc:task-x), de modo que model <= TaskCodeDoc lo encuentra; migración: deskops desk update --apply re-trackea cada tarea de desk/tasks bajo el modelo que su task_type legado indica (code|implementation|test → task.code; docs|spec|design → task.docs; external → task.external; vacío → task.code) y reescribe task_type; la migración es idempotente y reporta cada tarea movida. Produce G_TYPES.'
    acceptance: 'add task --task-type task.code crea una tarea tracked como TaskCodeDoc:<id> con task_type task.code; --task-type foo falla nombrando los tipos registrados; sin --task-type se crea task.code con aviso; en un desk temporal con un desk/models/local_types.py que define TaskCliDoc(TaskCodeDoc) (task.code.cli), desk update --apply lo registra y add task --task-type task.code.cli funciona; sldb docs find --where "model <= TaskCodeDoc" devuelve tareas task.code y task.refactor y no task.docs ni task.debug; closeout verify de una tarea task.docs exige commit y document sin que la tarea tenga closeout_evidence; --evidence que quite un kind del tipo falla y uno que agregue se guarda; una tarea legada con task_type implementation queda task.code tras desk update --apply y una segunda corrida no cambia nada; grep de TASK_TYPE_EVIDENCE en deskops/ no devuelve nada; tests/fixtures/model_contract_hashes.json actualizado; CHANGELOG y docs/workflow-policy-reference.md con la tabla de tipos.'
    output_scope: deskops/models/task.py, deskops/models/task_types.py, deskops/models/__init__.py, deskops/bootstrap.py, deskops/services/closeout_gates.py, deskops/services/tasks.py, deskops/operations.py (creación y verify_task_closeout), deskops/cli/registry.py (add task, desk update), deskops/workspace.py (desk/models), tests/, tests/fixtures/model_contract_hashes.json, docs/workflow-policy-reference.md, CHANGELOG.md
  - id: GC02
    title: ReviewDoc como recibo anclado al contrato de la tarea
    kind: code
    node_role: delivery
    parent_id: PC01
    owner_repo: deskops
    estimate: S
    depends_on: []
    requires: []
    scope: 'Modelo deskops/models/review.py ReviewDoc (StructuredNLDoc, como RunDoc) con campos: id (review-<task>-<kind>-<n>), title, kind (preflight | bundle | reproduction | goldens | owner; vocabulario cerrado validado), subject (str; valor doc:<Modelo>:<id> o vacío para revisiones de nodos de plan), subject_ref (str libre: ruta#node:ID cuando subject está vacío), engine (nombre del RuntimeProfileDoc o "human"), actor (identidad que corrió o dispuso; deskops/identity.py), run_dir (ruta relativa bajo runs/), input_sha256, output_sha256, verdict (pending | accepted | rejected | incomplete), reason (str), created_at, disposed_at, disposed_by, tags; cuerpo: sección Summary y sección Disposition. __doc_anchors__ = ["subject"] y __references__ = ["subject"] (GO07 trata __doc_anchors__ también como references; antes de GO07 el campo es una referencia normal que resuelve doc:Model:name sin sufijo, hipótesis: la versión actual de sldb acepta en un campo __references__ un valor con prefijo doc: o GC02 lo declara solo en __doc_anchors__ y espera a GO07; el TaskDoc fija cuál). Un ReviewDoc vive en desk/reviews/<task-id>/<kind>-<n>.md y se trackea; deskops init/desk update crean desk/reviews/. Validación al escribir: kind y verdict en su vocabulario; verdict accepted o rejected exige reason no vacía y disposed_by; subject con forma doc:<Modelo>:<id> o vacío. Un ReviewDoc no se edita con edit review verdict: edit lo rechaza (el veredicto se escribe con deskops review dispose, GC03). Registro en MODEL_REFS. Este nodo no escribe ReviewDocs desde ningún comando; GC03 lo hace.'
    acceptance: 'ReviewDoc renderiza y extrae ida y vuelta con un payload de ejemplo; un kind fuera del vocabulario falla al validar; verdict accepted sin reason falla; subject "task-x" (sin prefijo doc:) falla; subject "doc:TaskCodeDoc:task-x" valida; en un desk temporal un ReviewDoc guardado con deskops (doc_io) queda tracked como ReviewDoc:<id> y sldb edges show lo enlaza a la tarea por subject; edit review verdict falla con el mensaje que remite a review dispose; tests/fixtures/model_contract_hashes.json actualizado; CHANGELOG.'
    output_scope: deskops/models/review.py, deskops/models/__init__.py, deskops/bootstrap.py (MODEL_REFS), deskops/workspace.py (desk/reviews), deskops/operations.py (edit refuses verdict), tests/, tests/fixtures/model_contract_hashes.json, CHANGELOG.md
  - id: GC03
    title: Comando deskops review que reemplaza a los dos scripts de revisión en frío
    kind: code
    node_role: delivery
    parent_id: PC01
    owner_repo: deskops
    estimate: M
    depends_on: [GC02]
    requires: []
    scope: 'Comando deskops review con subcomandos: node <plan-dir> [IDS...] (revisa nodos de un dag.yaml del drawer: contrato del nodo con las claves KEEP del script gobernado, vecinos como edge, gates, y los cuatro archivos base del plan si existen: context-review-guide.md, brief.md, alcance.md, decisiones.md), preflight <task> (input = solo el TaskDoc), bundle <task> (TaskDoc + rituales enrutados por el Board + pills ligadas + átomos ligados + archivos que files nombra, menores de 60 KB + validación), status [<task> | <plan-dir>] (compara el hash del input vigente con los ReviewDoc existentes; sin llamar al modelo), dispose <review-id> --verdict accepted|rejected|incomplete --reason <texto> (escribe verdict, reason, disposed_at, disposed_by; falla si el ReviewDoc ya tiene veredicto distinto de pending). Cada corrida escribe la evidencia que el ritual pide bajo runs/subagents/<run>/context-review/<clave>/<sha256 del input>/attempt-N/ (input.md con FILE:<ruta> en orden documentado, manifest.json con argv, modelo, perfil, selection_reason, fuentes con sha256; output.md; stderr.log; receipt.json) y además un ReviewDoc (GC02) con verdict pending, subject = doc:<Modelo>:<id> de la tarea (sin hash: lo pinnea sldb cuando exista GO07; para node, subject vacío y subject_ref = <plan>/dag.yaml#node:<ID>), engine, run_dir, input_sha256, output_sha256. Motor: --engine <RuntimeProfileDoc> con default el perfil pi deepseek-flash del ritual (context-review.md paso 3), escrito por init como desk/runtimes/runtime-pi-deepseek-flash.md con los flags de aislamiento (--offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools) y el system prompt SYSTEM del script gobernado como texto del perfil; el perfil Scion queda como opción futura detrás de --engine y este nodo no lo implementa. Topes (D9): un input sin cambios no se vuelve a revisar (status lo dice); --max-attempts 2 por clave a nivel de plan; para preflight y bundle una por hash de contrato de la tarea, y una repetición exige --force con --reason, que queda en manifest.json y en el ReviewDoc. Falla de transporte (exit distinto de 0 o salida sin la sección REFORMULACION) deja receipt.json con technical_ok false y ReviewDoc con verdict incomplete y reason "technical", separado de los hallazgos de comprensión (ritual, paso 5). Retiro: se borran desk/drawer/plans/workspace-documental/context_review.py y tests/test_context_review_helper.py (los sustituyen los tests de este nodo); sldb/desk/drawer/plans/grafo-operable/context_review.py es de sldb y no se toca: se le manda nota por deskops message send --to sldb de que deskops review lo cubre. Produce G_RECEIPTS.'
    acceptance: 'En un desk temporal con un ejecutable pi falso (fixture que devuelve una salida con REFORMULACION), deskops review preflight task-x escribe attempt-1 con los cinco archivos y un ReviewDoc review-task-x-preflight-1 con verdict pending, subject doc:TaskCodeDoc:task-x, run_dir e input_sha256 iguales a los del manifest; una segunda corrida sin cambios no llama al ejecutable y status lo reporta como reviewed; editar goal de la tarea hace que status la reporte stale y la siguiente corrida cree attempt bajo otro sha; bundle incluye en input.md los rituales del Board, las pills ligadas y los archivos de files, en ese orden, con FILE: por archivo; node sobre este mismo plan (gates-por-tipo) escribe un ReviewDoc por nodo con subject vacío y subject_ref; review dispose review-task-x-preflight-1 --verdict accepted --reason "..." escribe verdict, reason, disposed_at y disposed_by y una segunda dispose falla; un tercer intento sobre la misma clave a nivel de plan falla sin --force; un pi falso que sale con exit 1 deja technical_ok false y verdict incomplete; grep de context_review.py en desk/drawer de deskops no devuelve nada; CHANGELOG; docs/operator-manual.md con la sección deskops review.'
    output_scope: deskops/cli/registry.py, deskops/cli/commands/review.py, deskops/services/review.py, deskops/workspace.py (runtime-pi-deepseek-flash), desk/runtimes/, desk/drawer/plans/workspace-documental/context_review.py (borrado), tests/, docs/operator-manual.md, CHANGELOG.md
  - id: GC04
    title: Efectos de transición en las aristas y advance por edges_holding
    kind: code
    node_role: delivery
    parent_id: PC02
    owner_repo: deskops
    estimate: M
    depends_on: []
    requires: [G_SLDB_EFFECTS]
    scope: 'ensure_lifecycle_graph escribe cada RelationDoc de desk/lifecycle/ con attributes: {sets: {status: <sets_status>}, terminal: <bool>} según la convención de sldb GO09, y deja de dejar los documentos existentes como están (lifecycle.py:280, :328, :354): desk update --apply reescribe un RelationDoc cuyo condition o attributes difieran del spec y lo reporta. task_lifecycle.yaml conserva transitions como plantilla para escribir el grafo (relation_type, source, target, condition, sets, terminal, bajo la clave attributes) y states para next_actions; las claves sets_status y terminal al nivel de la transición desaparecen del YAML y de Transition/LifecycleSpec.effect (lifecycle.py:48-49, :62-66). advance: edges_holding(store, ritual_export_id(current_node), payload) devuelve las aristas que se cumplen con effects; se toma la primera en el orden del spec, se aplica apply_effects(payload, effects, modelo del tipo de la tarea) y, si terminal, current_node = complete; history se sigue escribiendo en deskops (sldb no la conoce). Sin arista que se cumpla, el mensaje de bloqueo lista las condiciones como hoy; mostrar findings es de GC05 (edges_blocked). _add_closeout_facts y el borrado posterior de las claves (operations.py:441-450, tasks.py:196-199) quedan como están hasta GC05, que decide el destino de closeout_evidence_verified. La transición terminal sigue sin persistirse desde advance: la única puerta de cierre es closeout commit (tasks.py:200-205).'
    acceptance: 'En un desk temporal, los tres RelationDoc tienen attributes.sets.status (active, ready_for_testing, closed) y task_completes tiene terminal true; advance de una tarea en ritual-execution deja status active y current_node ritual-testing con el status leído de effects (test que cambia el sets del RelationDoc a otro valor y comprueba que advance escribe ese valor, sin tocar el YAML); grep de sets_status en deskops/ y en task_lifecycle.yaml no devuelve nada; un desk con RelationDocs de la versión anterior (sin attributes) queda reescrito por desk update --apply y una segunda corrida no cambia nada; los tests de tests/test_lifecycle_graph.py y tests/test_lifecycle_end_to_end.py pasan (adaptados a effects); CHANGELOG.'
    output_scope: deskops/lifecycle.py, deskops/spec/workflows/task_lifecycle.yaml, deskops/services/tasks.py, deskops/workflow/next_actions.py, deskops/lifecycle_migration.py, tests/, docs/workflow-policy-reference.md, CHANGELOG.md
  - id: GC05
    title: Reglas de activación por tipo y explicación por edges_blocked (produce G_CONSUMER)
    kind: code
    node_role: delivery
    parent_id: PC02
    owner_repo: deskops
    estimate: L
    depends_on: [GC01, GC02, GC04]
    requires: [G_SLDB_LANG, G_SLDB_RULES, G_SLDB_ANCHORS, G_SLDB_EVAL]
    scope: 'Reglas escritas por init y desk update --apply en desk/rules/ (idempotentes, reescritas si difieren), todas con severity error, moment on_transition y where "current_node = "ritual-execution"" (hipótesis: rev 9 no filtra las reglas on_transition por tipo de relación, así que la transición se distingue por el nodo de partida en where; si sldb agrega un filtro por relación, se usa ese). Una regla común activation-depends-on.md con subject "model <= TaskDoc" y condition all(depends_on: status = "closed") (DC6: una dependencia cerrada fue borrada y sldb la omite; una abierta falla nombrándola). Una regla por tipo de fábrica que declare __activation_receipts__ no vacío, activation-<tipo>.md, con subject "model <= <ModeloDelTipo>", message "activación de <tipo>" y condition = conjunción de any(^subject: kind = "<kind>" and anchor_state = "intact" and verdict = "accepted") por cada kind de __activation_receipts__ del tipo. Herencia por familia: un documento cumple las reglas de su tipo y de todos sus ancestros (sldb evalúa cada regla cuyo sujeto lo incluye), así que un subtipo suma gates y nunca quita (brief.md §Tipos): task.refactor pasa por la regla de task.code (preflight + bundle) y por la suya (goldens); task.debug no hereda de task.code justamente porque reemplaza bundle por reproduction. Un tipo propio de un desk sin regla propia queda cubierto por las de sus ancestros; si suma kinds, el desk escribe su regla con deskops add rule --type <tipo>, que genera el archivo desde __activation_receipts__ del tipo menos los kinds que ya exigen sus ancestros. advance: si edges_holding no devuelve task_activates, deskops llama a edges_blocked(store, nodo, payload) y muestra cada finding (what: message + explicación de GO02 con cláusula, nodo y valor visto) en el envelope como la explicación del bloqueo; show y next muestran lo mismo bajo gates. El hecho closeout_evidence_verified (operations.py:441-450) se mantiene en este nodo: la evidencia de cierre son hechos externos que deskops verifica (DC2); se documenta como la única condición que no es regla. Test de integración que es la evidencia de G_CONSUMER (sldb dag.yaml gates.G_CONSUMER): en un desk temporal, una tarea task.code sin ReviewDoc no se activa y la explicación nombra any(^subject ...); con dos ReviewDoc (preflight y bundle) accepted y pinneados se activa; editar goal deja los recibos changed y advance vuelve a bloquear nombrando anchor_state; editar references no cambia nada. Al cerrar: deskops message send --to sldb --kind suggestion con título "G_CONSUMER producido por deskops: gates-por-tipo GC05" y cuerpo con el hash del commit y la ruta del test. Produce G_CONSUMER.'
    acceptance: 'desk/rules/ tiene la regla común y una RuleDoc por tipo de fábrica con recibos, y sldb rules check sin --subject no reporta errores de parseo; el test de integración de G_CONSUMER pasa en sus tres pasos; una tarea task.docs se activa con solo preflight y una task.code no; una task.refactor con preflight y bundle no se activa hasta tener goldens y una task.debug se activa con preflight y reproduction sin bundle; una tarea con depends_on a una tarea abierta no se activa y el finding nombra la dependencia; tras cerrar esa dependencia (closeout commit la borra) se activa; deskops advance de una tarea bloqueada imprime los findings con cláusula y valor visto y deskops show los lista bajo gates; add rule --type task.code.cli en un desk con ese tipo genera una RuleDoc válida; desk update --apply sobre un desk sin desk/rules/ las escribe y una segunda corrida no cambia nada; la nota a sldb existe en sldb/desk/inbox; CHANGELOG; docs/workflow-policy-reference.md con la regla de cada tipo.'
    output_scope: deskops/lifecycle.py, deskops/services/tasks.py, deskops/services/rules.py, deskops/workspace.py (desk/rules), deskops/cli/registry.py (add rule), deskops/cli/commands/operations.py (show, next), deskops/operations.py, desk/rules/, tests/, docs/workflow-policy-reference.md, CHANGELOG.md, sldb/desk/inbox (vía message send)
  - id: GC06
    title: 'Cierre de las vías de escape: advance --to y edit task sobre campos del ciclo de vida'
    kind: code
    node_role: delivery
    parent_id: PC02
    owner_repo: deskops
    estimate: S
    depends_on: [GC01]
    requires: []
    scope: 'Se retira la opción --to de deskops advance (registry y tasks.py:179-192); cada uso documentado se reemplaza: cerrar → closeout commit; superseded → closeout supersede; blocked → nada que escribir (DC4: blocked es la regla que no se cumple; mientras GC05 no exista, el mensaje de bloqueo de advance ya lo dice). edit task rechaza status, current_node, task_type, closeout_evidence e history con un error que dice quién escribe cada campo (advance y closeout; add task para task_type) y con exit 1 (error de dominio); el resto de campos sigue editable. El inbox 20261029-213633 (advance --to superseded no cambia status) se cierra con ack porque la opción desaparece. Sin dependencia de sldb: con task_activates aún sin condición (hasta GC05) retirar --to no bloquea a nadie.'
    acceptance: 'deskops advance task-x --to ritual-testing falla con error de uso (exit 2) y el help de advance no menciona --to; deskops edit task task-x status closed falla con exit 1 y el mensaje nombra closeout commit; lo mismo para current_node, task_type, closeout_evidence e history; deskops edit task task-x goal "..." sigue funcionando; el golden del help se actualiza; tests/test_cli.py y test_cli_help_examples.py pasan; CHANGELOG con entrada breaking; docs/operator-manual.md sin --to.'
    output_scope: deskops/cli/registry.py, deskops/services/tasks.py, deskops/operations.py (edit_artifact_field), deskops/cli/commands/operations.py, tests/, tests/fixtures (goldens de help), docs/operator-manual.md, desk/inbox/20261029-213633-unclear-advance-to-superseded-no-cambia-status.md (ack), CHANGELOG.md
  - id: GC07
    title: Herencia de tareas leída del grafo y cierre sobre effective_*
    kind: code
    node_role: delivery
    parent_id: PC02
    owner_repo: deskops
    estimate: S
    depends_on: [GC01]
    requires: [G_SLDB_LANG]
    scope: '_resolve_task_payload (operations.py:1028-1071) deja de recorrer inherits_from en Python: la cadena de ancestros se obtiene de sldb siguiendo inherits_from+ (clausura de GO02 (b), conjunto sin duplicados, origen excluido, termina ante ciclos; un ciclo deja de ser error y se documenta) y los effective_* se calculan sobre esa lista en el orden que sldb devuelve (hipótesis: el orden de un conjunto alcanzado por camino lo fija GO05; si no, deskops ordena por id y lo documenta). El gate de cierre lee effective_references y effective_atoms en lugar de references y atoms crudos (closeout_gates.py:129, :146): la evidencia heredada cuenta. inherit_acceptance_context conserva su semántica. Sin GO04 el payload de los ancestros se sigue leyendo del Markdown por doc_io (sin cambio); lo que cambia es quién resuelve la cadena.'
    acceptance: 'Una tarea C con inherits_from B y B con inherits_from A tiene effective_pills = pills de A ∪ B ∪ C en ese orden; un ciclo A→B→A no levanta ValueError y effective_* contiene a ambos una vez; closeout verify de una tarea cuyo commit está solo en references de su padre pasa el gate commit; grep de "Task inheritance cycle" en deskops/ no devuelve nada; tests existentes de herencia (tests/test_composition.py o el que corresponda) adaptados y verdes; CHANGELOG.'
    output_scope: deskops/operations.py (_resolve_task_payload, _closeout_reference_evidence), deskops/services/closeout_gates.py, tests/, CHANGELOG.md
  - id: GC08
    title: Rituales, manual y guía de workflow al día con tipos, recibos y deskops review
    kind: docs
    node_role: delivery
    parent_id: PC02
    owner_repo: deskops
    estimate: S
    depends_on: [GC03, GC05, GC06]
    requires: []
    scope: 'desk/rituals/execution.md: los pasos 5 a 9 nombran deskops review preflight y deskops review bundle, el ReviewDoc como evidencia y review dispose como la disposición del coordinador; se retira la ruta runs/subagents/<run-dir>/preflight.md como lugar único. desk/rituals/context-review.md: paso 2 y 3 remiten al perfil runtime-pi-deepseek-flash y a runs/ que el comando escribe; paso 8 nombra los dos kinds; se agrega el tope D9. desk/rituals/phase.md: el gate de la fase es la regla de activación de cada tipo, no un paso manual. docs/workflow-policy-reference.md: tabla de tipos (de GC01), reglas por tipo (de GC05), campos del contrato, qué campos no se editan (GC06). docs/operator-manual.md y docs/quickstart.md: flujo add task --task-type → review preflight → review bundle → review dispose → advance. Las ediciones de rituales se hacen con deskops edit ritual (son documentos tracked), no a mano.'
    acceptance: 'Los tres rituales extraen ida y vuelta por RitualDoc tras la edición (deskops doctor sin alertas nuevas); grep de "preflight.md" en desk/rituals y docs no devuelve nada; grep de "deskops review" aparece en execution.md, context-review.md, operator-manual.md y quickstart.md; la tabla de tipos de workflow-policy-reference.md coincide con la de brief.md; los tests de ejemplos del help (test_cli_help_examples.py) pasan; CHANGELOG.'
    output_scope: desk/rituals/execution.md, desk/rituals/context-review.md, desk/rituals/phase.md, docs/workflow-policy-reference.md, docs/operator-manual.md, docs/quickstart.md, CHANGELOG.md
  - id: GC09
    title: 'Composición: parent_id, children y el tipo task.aggregate'
    kind: code
    node_role: delivery
    parent_id: PC03
    owner_repo: deskops
    estimate: M
    depends_on: [GC01, GC05]
    requires: [G_SLDB_LANG]
    scope: 'TaskDoc agrega parent_id: str (referencia a TaskDoc, vacío por defecto) y children: list[str] (referencia a TaskDoc), los dos en __references__ y __reference_models__. add task --parent <id> escribe parent_id en la nueva y agrega el id a children del padre (transacción de doc_io); el padre debe ser task.aggregate, si no falla. deskops doctor alerta cuando parent_id y children no se corresponden. Regla de activación de task.aggregate (molde de GC05): nonempty(children) and count(children: status != "closed") = 0 (DC6: los hijos cerrados fueron borrados y no cuentan; uno abierto cuenta). Evidencia de cierre children (declarada en GC01): closeout verify comprueba que cada id de children tiene un commit "closeout: <id>" alcanzable desde HEAD (closure.py:570 fija ese mensaje) o está en desk/tasks con status closed; falla nombrando el hijo que falta. show y next listan children y parent_id. Los agregados no se promueven ni se despachan: deskops advance de un agregado cuyo gate se cumple lo lleva a ritual-testing y de ahí a closeout como cualquier tarea; el ritual de testing para un agregado es la validación conjunta de la fase (phase.md).'
    acceptance: 'add task --parent P falla si P no es task.aggregate; con P agregado, la nueva tarea tiene parent_id P y P tiene a la nueva en children; sldb edges show P lista la arista children; con dos hijos abiertos advance P se bloquea y el finding nombra count(children ...); tras cerrar los dos con closeout commit, advance P activa; closeout verify de P con un hijo sin commit de closeout falla nombrándolo; doctor alerta ante un hijo con parent_id P ausente de children de P; tests/fixtures/model_contract_hashes.json actualizado; CHANGELOG; docs/workflow-policy-reference.md con la sección de composición.'
    output_scope: deskops/models/task.py, deskops/models/task_types.py, deskops/services/tasks.py, deskops/services/closeout_gates.py, deskops/services/rules.py (molde del agregado), deskops/doctor_findings.py, deskops/cli/registry.py (add task --parent), deskops/cli/commands/operations.py, tests/, tests/fixtures/model_contract_hashes.json, docs/workflow-policy-reference.md, CHANGELOG.md
  - id: GC10
    title: Promoción nodo a nodo desde dag.yaml y revisión de nodos sobre el mismo archivo
    kind: code
    node_role: delivery
    parent_id: PC03
    owner_repo: deskops
    estimate: M
    depends_on: [GC03, GC09]
    requires: []
    scope: 'deskops add task --from-drawer <plan-dir>/dag.yaml --node <ID> crea el TaskDoc del nodo: title, goal (= scope del nodo), scope (= output_scope), validation (= acceptance partida por ";" como lista), done_when (= acceptance), files (= output_scope partido por ","), task_type según kind (code → task.code; design | docs → task.docs; decision → task.decision; otro → error), from_drawer = <plan-dir>/dag.yaml#node:<ID>; depends_on = los ids de tarea de los nodos depends_on del DAG ya promovidos (un nodo prerrequisito no promovido es error que lo nombra: se promueve en orden); parent_id = la tarea task.aggregate del paquete (parent_id del nodo), creada por este mismo comando la primera vez con title del paquete y children vacío; un nodo con requires a un gate pending del DAG es error que nombra el gate (un gate pending no se promueve, como hoy: "un archivo presente no satisface un gate"). El mapa nodo → tarea se guarda en el dag.yaml bajo promoted: {ID: <task-id>} (única escritura al drawer; idempotente) para que review node y status crucen nodos con tareas. Tras promover, deskops review preflight y bundle trabajan sobre el TaskDoc como con cualquier tarea; review node sigue leyendo el dag.yaml. Las revisiones de nodo ya hechas (ReviewDoc con subject_ref) no se transfieren a la tarea: el preflight y el bundle son suyos. build_plan.py y validate_plan.py de workspace-documental quedan como están (plan cerrado); los planes nuevos no necesitan scripts.'
    acceptance: 'Sobre este plan (gates-por-tipo) en un desk temporal, add task --from-drawer desk/drawer/plans/gates-por-tipo/dag.yaml --node GC02 crea una TaskCodeDoc (kind code) con parent_id = la tarea de PC01 (creada al vuelo, task.aggregate) y depends_on vacío; --node GC03 después tiene depends_on = [tarea de GC02]; --node GC03 antes que GC02 falla nombrando GC02; --node GC04 falla nombrando G_SLDB_EFFECTS pending; dag.yaml queda con promoted y una segunda promoción del mismo nodo falla como duplicado; review status <plan-dir> muestra por nodo la tarea promovida y el estado de sus revisiones; CHANGELOG; docs/operator-manual.md con la sección de promoción por nodo.'
    output_scope: deskops/services/drawer.py, deskops/services/tasks.py, deskops/services/review.py (status por plan), deskops/cli/registry.py (add task --node), tests/, docs/operator-manual.md, CHANGELOG.md
  - id: GC11
    title: deskops graph sobre las aristas de sldb
    kind: code
    node_role: delivery
    parent_id: PC03
    owner_repo: deskops
    estimate: S
    depends_on: [GC09]
    requires: []
    scope: 'El snapshot de deskops graph toma nodos y aristas del índice de aristas de sldb (lo que extract_edges.py:245-310 ya lee) y retira los extractores por regex de ids en prosa (extract_edges.py:22-34, :631): una mención en prosa deja de ser arista. Las aristas de referencia de TaskDoc (depends_on, inherits_from, parent_id, children, pills, atoms, current_node) y de ReviewDoc (subject) aparecen con su nombre de campo como role. Los nodos de archivos fuente (extract_sources.py) y las materializaciones se conservan si el índice de sldb no los cubre; el TaskDoc fija la lista tras el grep. graph missing reporta las unresolved_references del índice de sldb. El esquema del snapshot sube de versión; graph neighbors y reflect leen el nuevo.'
    acceptance: 'graph build de un desk temporal con una tarea task.code con depends_on, parent_id y un ReviewDoc produce aristas con role depends_on, parent_id, children y subject; una mención "task-otra" en la prosa de un documento no produce arista; graph missing reporta un depends_on a una tarea inexistente; goldens de graph (tests/fixtures) regenerados y el diff revisado en el TaskDoc; grep de TASK_OR_ISSUE_RE en deskops/ no devuelve nada; tests/test_graph_*.py verdes; CHANGELOG.'
    output_scope: deskops/graph/extract_edges.py, deskops/graph/snapshot.py, deskops/graph/checks.py, deskops/graph/self_reflection.py, deskops/cli/commands/graph.py, tests/, tests/fixtures (goldens de graph), docs/knowledge-graph/, CHANGELOG.md

FILE:instruccion
Cold-bundle de la tarea task-se-retiran-del-drawer-los-planes-workspace-documental-gates-por-tipo-deskops-ui-y-deskops-como-confi: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (sin entradas nuevas por los planes borrados)


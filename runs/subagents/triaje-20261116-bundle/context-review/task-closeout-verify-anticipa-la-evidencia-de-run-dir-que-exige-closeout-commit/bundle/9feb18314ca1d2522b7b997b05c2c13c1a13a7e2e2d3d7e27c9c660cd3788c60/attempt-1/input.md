FILE:desk/tasks/task-closeout-verify-anticipa-la-evidencia-de-run-dir-que-exige-closeout-commit.md
---
sldb:
  by: agent
  at: '2026-11-16T05:00:10Z'
  authority: generated
  via: save_document_payload
id: task-closeout-verify-anticipa-la-evidencia-de-run-dir-que-exige-closeout-commit
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261031-195117-unclear-closeout-verify-no-anticipa-la-evidencia-que-exige-closeout-commit.md
depends_on: []
pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
files:
- deskops/cli/commands/closeout.py
- deskops/services/closure.py
- tests/test_closeout_declared_evidence.py
- tests/fixtures/golden (el golden de ayuda de closeout verify)
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# closeout verify anticipa la evidencia de run-dir que exige closeout commit

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del inbox (2026-10-31, cierres de WS02 y WS04): `deskops closeout verify` da ok:true y despues `deskops closeout commit --run-dir` falla con 'Missing required evidence ... task.txt'. verify no revisa los archivos de evidencia del run-dir, asi que su ok no anticipa el cierre.

## Goal

_Describe the concrete result this task must produce._

`deskops closeout verify --task <id> --run-dir <dir>` acepta --run-dir opcional; cuando se da, reporta como falla (ok:false) cada archivo de REQUIRED_EVIDENCE que falte en el run-dir, con el mismo texto que usa commit. Sin --run-dir, verify se comporta igual que hoy.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/closeout.py (parser de verify, alrededor de las lineas 83-86), deskops/services/closure.py (REQUIRED_EVIDENCE alrededor de la linea 104, el chequeo de commit alrededor de 539-543, verify_task_closeout alrededor de 843), el golden de ayuda de `closeout verify` que lee tests/test_output_goldens.py, y tests/test_closeout_declared_evidence.py. No entra: cambiar que evidencia exige commit ni el formato del reporte JSON fuera del nuevo hallazgo. Precisiones del preflight 1: el golden es tests/fixtures/golden/help/deskops_closeout_verify.txt; el texto de falla es el que hoy arma commit en closure.py: 'Missing required evidence in <run_dir>: <archivos separados por coma>'. Los numeros de linea son orientativos: se ubican por nombre de funcion. El atomo de sandbox implica que los tests usan un desk temporal, como los tests existentes del archivo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Extraer de commit un helper `missing_run_evidence(run_dir) -> list[str]`. 2) Usarlo en commit (sin cambio de comportamiento) y en verify cuando llega run_dir. 3) Agregar --run-dir al parser de verify y actualizar su golden de ayuda. 4) Tests: run-dir sin task.txt -> verify ok:false nombrando task.txt; run-dir completo -> ok:true; sin --run-dir -> igual que antes.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

verify con un run-dir incompleto da ok:false y nombra el archivo faltante; commit y verify usan el mismo helper; los tests listados pasan.

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

FILE:deskops/cli/commands/closeout.py
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from deskops.operations import DeskopsOperations
from deskops.services.closure import ClosureService


class CloseoutCLI:
    """Tool-made closing commits, linked to run evidence or marked manual.

    The closing commit is created by ``ClosureService``, not by agent
    discretion. With --run-dir the commit message carries immutable trailers
    linking it to the run evidence directory; with --no-run it carries
    Closeout-Mode: manual and the stated reason instead. ``supersede`` closes a
    task whose subject no longer exists, with a reason and a resolvable ref
    instead of run evidence; ``retire`` removes a task that was already resolved
    before the ritual lifecycle, keeping its status; ``resolved-by`` closes a task
whose work already entered the history, with an ancestor commit and an accepted
test instead of an atom per file. Either way an append-only
    index records the task
    and run, committed together with the closing commit; the commit hash is
    resolved from its Task-Id trailer.
    """

    def run(self, args: Any) -> int:
        command = getattr(args, "closeout_command", None)
        if command == "commit":
            return self._commit(args)
        if command == "supersede":
            return self._supersede(args)
        if command == "retire":
            return self._retire(args)
        if command == "resolved-by":
            return self._resolved_by(args)
        if command == "verify":
            return self._verify(args)
        print("Usage: deskops closeout {commit|supersede|retire|resolved-by|verify} ...")
        return 1

    def _retire(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_retired(
            args.task,
            reason=getattr(args, "reason", "") or "",
            refs=getattr(args, "ref", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _resolved_by(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_resolved_by(
            args.task,
            reason=getattr(args, "reason", "") or "",
            refs=getattr(args, "ref", None),
            tests=getattr(args, "test", None),
            paths=getattr(args, "paths", None),
            message=getattr(args, "message", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _supersede(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_superseded(
            args.task,
            reason=getattr(args, "reason", "") or "",
            refs=getattr(args, "ref", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _verify(self, args: Any) -> int:
        root = Path(args.root).resolve()
        # verify also writes the evidence receipts (CC33a); the envelope is unchanged.
        report = DeskopsOperations(root).closure.verify_task_closeout(args.task, write_receipts=True)
        print(json.dumps(report, indent=2, sort_keys=True))
        # The JSON stays machine-readable on stdout; the declared/found line and the
        # alerts are always said aloud on stderr, never silently folded into the report.
        print(f"Closeout gate: {report['summary']}", file=sys.stderr)
        for alert in report.get("alerts") or []:
            print(f"ALERTA {alert['code']}: {alert['message']}", file=sys.stderr)
        return 0 if report["ok"] else 1

    def _commit(self, args: Any) -> int:
        run_dir_arg = getattr(args, "run_dir", None)
        no_run = bool(getattr(args, "no_run", False))
        reason = getattr(args, "reason", None)
        if run_dir_arg and no_run:
            print("Pass either --run-dir or --no-run, not both.")
            return 1
        if not run_dir_arg and not no_run:
            print(
                "Closing a task needs one of two routes: --run-dir <runs/subagents/dir> to link the "
                "commit to a subagent run, or --no-run --reason \"<why>\" to close it manually."
            )
            return 1
        if no_run:
            return self._commit_manual(args, reason)
        if reason is not None:
            print("--reason applies only to --no-run; a --run-dir closeout takes its evidence from the run.")
            return 1
        return self._commit_with_run(args)

    def _commit_manual(self, args: Any, reason: str | None) -> int:
        root = Path(args.root).resolve()
        run_only = [flag for flag, attr in (("--run-id", "run_id"), ("--session", "session")) if getattr(args, attr, None)]
        if run_only:
            print(f"{', '.join(run_only)} applies only to --run-dir; a --no-run closeout has no run to record.")
            return 1
        if not " ".join((reason or "").split()):
            print("--no-run needs a non-empty --reason saying why the task closes without a subagent run.")
            return 1

        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_manual(
            args.task,
            reason=reason or "",
            paths=getattr(args, "paths", None),
            message=getattr(args, "message", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _commit_with_run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_with_run(
            args.task,
            run_dir=args.run_dir,
            paths=getattr(args, "paths", None),
            run_id=getattr(args, "run_id", None),
            session=getattr(args, "session", None),
            message=getattr(args, "message", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

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

FILE:instruccion
Cold-bundle de la tarea task-closeout-verify-anticipa-la-evidencia-de-run-dir-que-exige-closeout-commit: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea


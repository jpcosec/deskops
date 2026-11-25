FILE:desk/tasks/task-el-test-de-llaves-de-message-send-deja-de-ser-xfail-porque-sldb-ya-renderiza-los-valores-literales.md
---
sldb:
  by: agent
  at: '2026-11-17T13:34:04Z'
  authority: generated
  via: create_document
id: task-el-test-de-llaves-de-message-send-deja-de-ser-xfail-porque-sldb-ya-renderiza-los-valores-literales
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- runs/subagents/test-deskops-t-bfb4a8401ae2/verdict.md
depends_on: []
pills: []
files:
- tests/test_message_cli.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
---

# el test de llaves de message send deja de ser xfail porque sldb ya renderiza los valores literales

## Rationale

_Explain why this task exists or the business driver behind it._

La tarea de llaves (63b519b2) dejo en tests/test_message_cli.py un test xfail(strict=True) con reason SLDB_JINJA_VALUE_NOTE (lineas 359-365), a la espera de que sldb dejara de compilar como Jinja los valores de los campos. sldb lo arreglo en d49f6ddc ('El valor de un campo se renderiza literal: render_model_markdown deja de compilar los valores del usuario como Jinja'), ya instalado en /mnt/ssd/herramientas/sldb. Con eso las 4 variantes dan XPASS estricto y tests/test_message_cli.py falla, lo que deja roja la suite de deskops (lo encontro el tester de ack --reason).

## Goal

_Describe the concrete result this task must produce._

tests/test_message_cli.py::test_message_send_keeps_braces_in_the_body_literal es un test normal (sin xfail) y sus 4 variantes pasan contra el sldb instalado; la constante SLDB_JINJA_VALUE_NOTE se borra si ya no se usa.

## Scope

_State what is in scope and what is out of scope._

Entra: el decorador xfail y la constante SLDB_JINJA_VALUE_NOTE en tests/test_message_cli.py. Sale: codigo de deskops y de sldb, y el resto de los tests.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Confirmar que el sldb que importa el venv incluye d49f6ddc (git -C /mnt/ssd/herramientas/sldb merge-base --is-ancestor d49f6ddc HEAD). 2) Quitar el xfail y la constante. 3) Correr la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_message_cli.py pasa entero sin xfail ni XPASS y git diff solo toca ese archivo.

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

FILE:desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---
sldb:
  by: agent
  at: '2026-11-17T01:11:30Z'
  authority: generated
  via: create_document
id: atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
title: deskops message es el unico comando de mensajeria del desk
five_wh_one_plus: what
tags:
- system:deskops
- topic:inbox
provenance: tests/test_message_cli.py
---

# deskops message es el unico comando de mensajeria del desk

## Answer

Las notas del inbox de un desk se envian, listan, leen y confirman con deskops message send|list|read|ack (send con --to <repo> para otro desk del ecosistema). El alias deskops inbox se retiro el 2026-11-16: deskops inbox ya no es un comando (invalid choice). Docs, la skill deskops-workflow y los tests usan solo deskops message.

FILE:tests/test_message_cli.py
"""Canonical `deskops message` transport surface.

`deskops message {send|list|read|ack}` is the cross-desk coordination CLI.
It routes to `deskops.cli.commands.message.MessageCLI`; the retired `inbox`
alias is no longer a command.
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
TESTS = Path(__file__).resolve().parent
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))

from deskops.cli.main import main
from test_cli import _setup_inbox_identity_env


def _cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv], cwd=root, capture_output=True, text=True
    )


def _sldb_stores_check(store_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_path)],
        capture_output=True,
        text=True,
    )


def _init_repos(tmp_path: Path) -> tuple[Path, Path]:
    repos = []
    for name in ("repo-a", "repo-b"):
        repo = tmp_path / name
        repo.mkdir()
        result = _cli(repo, "init", str(repo))
        assert result.returncode == 0, result.stderr or result.stdout
        repos.append(repo)
    return repos[0], repos[1]


def _deliver(repo_a: Path, repo_b: Path, title: str) -> tuple[Path, dict]:
    result = _cli(
        repo_a,
        "message",
        "send",
        "A note for repo B.",
        "--title",
        title,
        "--kind",
        "suggestion",
        "--root",
        str(repo_b),
        "--format",
        "json",
    )
    assert result.returncode == 0, result.stderr or result.stdout
    notes = list((repo_b / "desk" / "inbox").glob("*.md"))
    assert len(notes) == 1
    return notes[0], json.loads(result.stdout)


def test_message_help_documents_transport_verbs(capsys) -> None:
    assert main(["message", "--help"]) == 0
    output = " ".join(capsys.readouterr().out.split())
    assert "{send,list,read,ack}" in output
    assert "deskops message send" in output


def test_retired_inbox_alias_is_an_unknown_command(capsys) -> None:
    assert main(["inbox", "--list"]) == 2
    assert "invalid choice: 'inbox'" in capsys.readouterr().err


def test_message_send_list_read_ack_roundtrip(tmp_path: Path, monkeypatch, capsys) -> None:
    sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    monkeypatch.chdir(sender_repo)

    assert main(
        [
            "message",
            "send",
            "Please acknowledge this message.",
            "--title",
            "Transport verbs",
            "--kind",
            "suggestion",
            "--to",
            "target-repo",
            "--store",
            str(store_path),
            "--format",
            "json",
        ]
    ) == 0
    delivered = json.loads(capsys.readouterr().out)
    assert delivered["sender_project"] == "sender-repo"
    assert delivered["target_project"] == "target-repo"

    note = next((target_repo / "desk" / "inbox").glob("*.md"))
    monkeypatch.chdir(target_repo)

    assert main(
        ["message", "list", "--root", str(target_repo), "--store", str(target_repo / ".sldb"), "--format", "json"]
    ) == 0
    listed = json.loads(capsys.readouterr().out)
    assert [item["id"] for item in listed["notes"]] == [note.stem]

    assert main(
        ["message", "read", note.stem, "--root", str(target_repo), "--store", str(target_repo / ".sldb"), "--format", "json"]
    ) == 0
    read = json.loads(capsys.readouterr().out)
    assert read["status"] == "open"
    assert "Please acknowledge this message." in read["body"]

    assert main(
        ["message", "ack", note.stem, "--root", str(target_repo), "--store", str(target_repo / ".sldb"), "--format", "json"]
    ) == 0
    acked = json.loads(capsys.readouterr().out)
    assert acked["status"] == "closed"
    assert acked["acknowledged_by"] == "target-repo"


def test_message_list_reports_empty_inbox(tmp_path: Path, monkeypatch, capsys) -> None:
    _sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    monkeypatch.chdir(target_repo)

    assert main(["message", "list", "--root", str(target_repo), "--store", str(target_repo / ".sldb")]) == 0
    assert "No messages." in capsys.readouterr().out


def test_message_delivery_tracks_note_in_target_repo_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    repo_a, repo_b = _init_repos(tmp_path)
    note, payload = _deliver(repo_a, repo_b, "Tracked in the target store")

    assert payload["target_project"] == "repo-b"
    assert payload["verified"] is True
    assert doc_status(repo_a / ".sldb", note.stem).status == "missing"
    tracked = doc_status(repo_b / ".sldb", note.stem)
    assert tracked.status == "ok"
    assert tracked.path == f"desk/inbox/{note.name}"
    assert not Path(tracked.path).is_absolute()
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout
    assert "PASS" in check.stdout


def test_message_ack_refreshes_note_tracked_in_target_repo_store(tmp_path: Path) -> None:
    from sldb.api import doc_status

    repo_a, repo_b = _init_repos(tmp_path)
    note, _ = _deliver(repo_a, repo_b, "Acknowledged in the target store")

    result = _cli(
        repo_b,
        "message",
        "ack",
        note.stem,
        "--root",
        str(repo_b),
        "--format",
        "json",
    )
    assert result.returncode == 0, result.stderr or result.stdout
    acked = json.loads(result.stdout)
    assert acked["status"] == "closed"
    assert acked["acknowledged_by"] == "repo-b"
    assert doc_status(repo_b / ".sldb", note.stem).status == "ok"
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout
    assert "PASS" in check.stdout
    assert doc_status(repo_a / ".sldb", note.stem).status == "missing"


def test_message_ack_restores_note_when_tracking_fails(tmp_path: Path, monkeypatch) -> None:
    from sldb.api import doc_status
    from sldb.core.exceptions import SLDBStoreError

    repo_a, repo_b = _init_repos(tmp_path)
    note, _ = _deliver(repo_a, repo_b, "Restored when tracking fails")
    original = note.read_bytes()

    def failing_save(*_args, **_kwargs):
        raise SLDBStoreError("simulated refresh failure")

    # The ack is `Transaction.update` of the tracked note: the store's save step fails.
    monkeypatch.setattr("sldb.api.documents.transaction_ops.save_document_payload", failing_save)
    monkeypatch.chdir(repo_b)

    assert main(["message", "ack", note.stem, "--root", str(repo_b)]) == 1
    assert note.read_bytes() == original
    assert doc_status(repo_b / ".sldb", note.stem).status == "ok"
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout
    assert "PASS" in check.stdout


def test_message_ack_reason_is_stored_and_shown_by_read(tmp_path: Path) -> None:
    from sldb.api import doc_status

    repo_a, repo_b = _init_repos(tmp_path)
    note, _ = _deliver(repo_a, repo_b, "Acknowledged with a reason")
    reason = "Ya resuelto: la tarea X cubre esto"

    result = _cli(
        repo_b, "message", "ack", note.stem, "--root", str(repo_b), "--reason", reason, "--format", "json"
    )
    assert result.returncode == 0, result.stderr or result.stdout
    acked = json.loads(result.stdout)
    assert acked["status"] == "closed"
    assert acked["ack_reason"] == reason
    assert "ack_reason: 'Ya resuelto: la tarea X cubre esto'" in note.read_text(encoding="utf-8")
    assert doc_status(repo_b / ".sldb", note.stem).status == "ok"
    check = _sldb_stores_check(repo_b / ".sldb")
    assert check.returncode == 0, check.stderr or check.stdout

    read_json = _cli(repo_b, "message", "read", note.stem, "--root", str(repo_b), "--format", "json")
    assert read_json.returncode == 0, read_json.stderr or read_json.stdout
    assert json.loads(read_json.stdout)["ack_reason"] == reason

    read_text = _cli(repo_b, "message", "read", note.stem, "--root", str(repo_b))
    assert read_text.returncode == 0, read_text.stderr or read_text.stdout
    lines = read_text.stdout.splitlines()
    ack_at = next(i for i, line in enumerate(lines) if line.startswith("acknowledged_at: "))
    assert lines[ack_at + 1] == f"Ack reason: {reason}"


def test_message_ack_without_reason_leaves_ack_reason_empty(tmp_path: Path) -> None:
    repo_a, repo_b = _init_repos(tmp_path)
    note, _ = _deliver(repo_a, repo_b, "Acknowledged without a reason")

    result = _cli(repo_b, "message", "ack", note.stem, "--root", str(repo_b), "--format", "json")
    assert result.returncode == 0, result.stderr or result.stdout
    acked = json.loads(result.stdout)
    assert acked["status"] == "closed"
    assert acked["acknowledged_by"] == "repo-b"
    assert acked["ack_reason"] == ""

    read_json = _cli(repo_b, "message", "read", note.stem, "--root", str(repo_b), "--format", "json")
    assert json.loads(read_json.stdout)["ack_reason"] == ""
    read_text = _cli(repo_b, "message", "read", note.stem, "--root", str(repo_b))
    assert read_text.returncode == 0, read_text.stderr or read_text.stdout
    assert "Ack reason" not in read_text.stdout


OLD_NOTE = """---
kind: suggestion
sender_project: repo-a
target_project: repo-b
created_at: '2026-01-01T00:00:00'
status: open
---

# Old note

_Describe the incoming message with enough evidence to triage._

Written before ack_reason existed.
"""


def test_message_old_note_without_ack_reason_still_reads_and_acks(tmp_path: Path) -> None:
    repo = tmp_path / "repo-old"
    inbox = repo / "desk" / "inbox"
    inbox.mkdir(parents=True)
    note = inbox / "20260101-000000-suggestion-old-note.md"
    note.write_text(OLD_NOTE, encoding="utf-8")

    read_json = _cli(repo, "message", "read", note.stem, "--root", str(repo), "--format", "json")
    assert read_json.returncode == 0, read_json.stderr or read_json.stdout
    read = json.loads(read_json.stdout)
    assert read["status"] == "open"
    assert read["ack_reason"] == ""

    acked = _cli(repo, "message", "ack", note.stem, "--root", str(repo), "--reason", "Aviso leido", "--format", "json")
    assert acked.returncode == 0, acked.stderr or acked.stdout
    assert json.loads(acked.stdout)["ack_reason"] == "Aviso leido"
    reread = _cli(repo, "message", "read", note.stem, "--root", str(repo), "--format", "json")
    assert json.loads(reread.stdout)["ack_reason"] == "Aviso leido"

    # An old note acked without --reason, as before ack_reason existed.
    plain = inbox / "20260101-000001-suggestion-old-plain.md"
    plain.write_text(OLD_NOTE, encoding="utf-8")
    acked_plain = _cli(repo, "message", "ack", plain.stem, "--root", str(repo), "--format", "json")
    assert acked_plain.returncode == 0, acked_plain.stderr or acked_plain.stdout
    assert json.loads(acked_plain.stdout)["ack_reason"] == ""


def test_message_list_uses_store_when_no_root_is_given(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    """`--store` alone anchors the desk, so the old root default cannot mask it."""
    repo = tmp_path / "store-repo"
    inbox = repo / "desk" / "inbox"
    inbox.mkdir(parents=True)
    note = inbox / "20260101-000000-suggestion-stored.md"
    note.write_text(
        "---\nkind: suggestion\nsender_project: sender\ntarget_project: store-repo\n"
        "created_at: 2026-01-01T00:00:00\nstatus: open\ntitle: Stored note\n---\n\n"
        "# Stored note\n\nBody.\n",
        encoding="utf-8",
    )
    store = repo / ".sldb"
    (store / "core").mkdir(parents=True)
    (store / "core" / "store_index.yaml").write_text("{}\n", encoding="utf-8")

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)

    assert main(["message", "list", "--store", str(store), "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert [item["id"] for item in payload["notes"]] == [note.stem]


def test_message_ack_rejects_a_fragment_that_matches_two_notes(tmp_path: Path) -> None:
    """2026-10-19: `message ack 20261019-120241` acked 20261019-120253, whose title quoted it."""
    repo_a, repo_b = _init_repos(tmp_path)
    first, _ = _deliver(repo_a, repo_b, "sldb ci en verde")
    prefix = first.stem.split("-suggestion-")[0]
    result = _cli(
        repo_a, "message", "send", "Corrected hashes.", "--title", f"correccion de mi nota {prefix}",
        "--kind", "suggestion", "--root", str(repo_b),
    )
    assert result.returncode == 0, result.stderr or result.stdout
    (second,) = [path for path in (repo_b / "desk" / "inbox").glob("*.md") if path != first]
    assert prefix in second.stem

    ambiguous = _cli(repo_b, "message", "ack", prefix, "--root", str(repo_b))

    assert ambiguous.returncode == 2, ambiguous.stdout + ambiguous.stderr
    output = ambiguous.stdout + ambiguous.stderr
    assert first.stem in output and second.stem in output
    for note in (first, second):
        assert "status: open" in note.read_text(encoding="utf-8")

    exact = _cli(repo_b, "message", "ack", first.stem, "--root", str(repo_b))

    assert exact.returncode == 0, exact.stdout + exact.stderr
    assert "status: closed" in first.read_text(encoding="utf-8")
    assert "status: open" in second.read_text(encoding="utf-8")


# sldb renders a field value as Jinja source (sldb/core/renderer_engine/base.py replace_markers):
# two or three opening braces raise TemplateSyntaxError and a valid expression is evaluated and
# stored altered with rc 0. Reported to sldb; this pins the literal contract until sldb fixes it.
SLDB_JINJA_VALUE_NOTE = (
    "20261117-015212-suggestion-render-model-markdown-interpreta-como-jinja-el-valor-de-los-campos"
    "-llaves-dobles-rompen-expresiones-se-evaluan.md"
)


@pytest.mark.xfail(strict=True, reason=SLDB_JINJA_VALUE_NOTE)
@pytest.mark.parametrize(
    "body",
    [
        "docker inspect --format {{.State.Health.Status}} web",
        "texto {{a fin",
        "this is not valid json {{{",
        "valor {{ 7*7 }} y {# oculto #} fin",
    ],
)
def test_message_send_keeps_braces_in_the_body_literal(tmp_path: Path, monkeypatch, capsys, body: str) -> None:
    sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    monkeypatch.chdir(sender_repo)

    rc = main(
        ["message", "send", body, "--title", "Llaves", "--kind", "unclear",
         "--to", "target-repo", "--store", str(store_path), "--format", "json"]
    )

    assert rc == 0, capsys.readouterr()
    note = next((target_repo / "desk" / "inbox").glob("*.md"))
    assert body in note.read_text(encoding="utf-8")

FILE:instruccion
Cold-bundle de la tarea task-el-test-de-llaves-de-message-send-deja-de-ser-xfail-porque-sldb-ya-renderiza-los-valores-literales: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py


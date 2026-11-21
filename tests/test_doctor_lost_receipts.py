"""`deskops doctor` and the receipts of a closed task: a lost subject anchor is audit, not an alert."""

from __future__ import annotations

from pathlib import Path
import subprocess

from test_doctor_alerts import _desk, _doctor, _store_check_says as _fake_store_check

_real_run = subprocess.run


def _store_check_says(monkeypatch, docs, **store) -> None:
    """The store check is faked; git is real (the fake patches ``subprocess.run`` globally)."""
    _fake_store_check(monkeypatch, docs, **store)
    fake = subprocess.run
    monkeypatch.setattr(
        "subprocess.run", lambda argv, *a, **k: _real_run(argv, *a, **k) if argv and argv[0] == "git" else fake(argv, *a, **k)
    )


def _git(root: Path, *argv: str) -> None:
    _real_run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *argv], cwd=root, check=True, capture_output=True)


def _lost(task_id: str, n: int = 1) -> dict:
    review = f"review-{task_id}-preflight-{n}"
    return {
        "code": "anchors/doc_lost",
        "subject": f"ReviewDoc:{review}",
        "what": f"subject -> TaskCodeDoc:{task_id}: lost (doc:TaskCodeDoc:{task_id}@sha256:{'0' * 64})",
        "fix": "",
    }


def _commit(root: Path, *trailers: str) -> None:
    if not (root / ".git").exists():
        _git(root, "init", "-q")
    _git(root, "commit", "-q", "--allow-empty", "-m", "x\n\n" + "\n".join(trailers) + "\n")


def test_receipts_of_a_closed_task_do_not_alert(tmp_path: Path, monkeypatch, capsys) -> None:
    root, docs = _desk(tmp_path, capsys)
    _commit(root, "Task-Id: task-done", "Run-Dir: runs/subagents/x", "Run-Id: x")
    _commit(root, "Task-Id: task-old", "Closeout-Mode: resolved-by")
    _store_check_says(monkeypatch, docs, alerts=[_lost("task-done"), _lost("task-old", 2)])
    code, out = _doctor(root, capsys)
    assert code == 0 and "lost" not in out
    assert "Desk is healthy" in out


def test_receipts_of_a_task_gone_without_closeout_still_alert_without_desk_update(tmp_path: Path, monkeypatch, capsys) -> None:
    root, docs = _desk(tmp_path, capsys)
    # A code commit with only Task-Id is not a closeout.
    _commit(root, "Task-Id: task-vanished")
    _store_check_says(monkeypatch, docs, alerts=[_lost("task-vanished")])
    code, out = _doctor(root, capsys)
    assert code == 0
    assert "task-vanished: lost" in out and "1 alert(s)" in out
    assert "register edits" not in out
    assert "does not repair these" in out

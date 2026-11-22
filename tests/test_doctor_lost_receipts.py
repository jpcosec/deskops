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
    assert "the task was deleted without closeout: restore it from git or close it with" in out
    assert "deskops closeout resolved-by" in out
    assert "desk update --apply" not in out


def test_closeout_known_only_by_its_subject_does_not_alert(tmp_path: Path, monkeypatch, capsys) -> None:
    root, docs = _desk(tmp_path, capsys)
    _git(root, "init", "-q")
    _git(root, "commit", "-q", "--allow-empty", "-m", "closeout: task-subj [skip ci]")
    # A longer id sharing the prefix is not closed by that subject.
    _store_check_says(monkeypatch, docs, alerts=[_lost("task-subj"), _lost("task-subj-other")])
    code, out = _doctor(root, capsys)
    assert code == 0
    assert "task-subj-other: lost" in out and "1 alert(s)" in out
    assert "TaskCodeDoc:task-subj: lost" not in out


def test_a_task_closed_with_a_real_closeout_commit_leaves_no_lost_alert(lifecycle_desk: Path, capsys) -> None:
    from deskops.cli.main import main
    from test_closeout_rules import _desk as _closeable_task
    from test_closeout_rules import _route
    from test_closeout_rules import _run

    root = lifecycle_desk
    task_id = _closeable_task(root)
    _route(root, task_id)
    code, out = _run(["closeout", "verify", "--task", task_id, "--root", str(root)])
    assert code == 0, out
    args = ["closeout", "commit", "--task", task_id, "--no-run", "--reason", "doctor test", "--paths", "desk", "--root", str(root)]
    code, out = _run(args)
    assert code == 0, out
    assert not (root / "desk" / "tasks" / f"{task_id}.md").exists()
    capsys.readouterr()
    main(["doctor", "--root", str(root)])
    out = capsys.readouterr().out
    assert "lost" not in out and "does not repair" not in out

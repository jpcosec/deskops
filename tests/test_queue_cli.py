"""`deskops queue job set` edits desk/config.json; the init seed retries dispatch-reap on exit 3."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from deskops.config import DeskConfig
from tests.test_queue import _cli, _configure, _sh

ROOT = Path(__file__).resolve().parents[1]


def _read(root: Path) -> dict:
    return json.loads((root / "desk" / "config.json").read_text(encoding="utf-8"))


def test_job_set_changes_only_that_job(lifecycle_desk: Path) -> None:
    desk = lifecycle_desk
    _configure(desk, {"dispatch-reap": _sh("true", 600), "other": _sh("echo hi")}, integrate=None)
    before = _read(desk)
    result = _cli(desk, "queue", "job", "set", "dispatch-reap", "retry_exit_codes", "[3]", "--root", ".")
    assert result.returncode == 0, result.stderr or result.stdout
    after = _read(desk)
    assert after["queue_jobs"]["dispatch-reap"]["retry_exit_codes"] == [3]
    before["queue_jobs"]["dispatch-reap"]["retry_exit_codes"] = [3]
    assert after == before
    assert DeskConfig.load(desk / "desk").queue_jobs["dispatch-reap"].retry_exit_codes == [3]


def test_job_set_rejects_bad_input_and_leaves_file(lifecycle_desk: Path) -> None:
    desk = lifecycle_desk
    _configure(desk, {"a": _sh("true")})
    raw = (desk / "desk" / "config.json").read_text(encoding="utf-8")
    for argv in (
        ("nope", "timeout", "5"),
        ("a", "bogus", "1"),
        ("a", "retry_exit_codes", "[\"x\"]"),
        ("a", "timeout", "0"),
    ):
        result = _cli(desk, "queue", "job", "set", *argv, "--root", ".")
        assert result.returncode == 2, (argv, result.stdout, result.stderr)
        assert (desk / "desk" / "config.json").read_text(encoding="utf-8") == raw


def test_init_seed_retries_dispatch_reap() -> None:
    seed = json.loads((ROOT / "deskops" / "data" / "templates" / "config.json").read_text(encoding="utf-8"))
    assert seed["queue_jobs"]["dispatch-reap"]["retry_exit_codes"] == [3]
    DeskConfig.model_validate(seed)

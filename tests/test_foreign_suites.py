"""The pytest bridge that runs a suite written in another language (deskops.testing.foreign_suites)."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

from deskops.operations import DeskopsOperations
from deskops.testing.foreign_suites import GO_TEST, VITEST, run_foreign_suite
from tests.test_closeout_gates import ATOM, _task, _write, bare_desk, store_desk  # noqa: F401  (fixtures)


def _python(code: str) -> list[str]:
    return [sys.executable, "-c", code]


def test_canonical_commands() -> None:
    assert VITEST == ["npx", "vitest", "run"]
    assert GO_TEST == ["go", "test", "./..."]


def test_exit_code_zero_passes(tmp_path: Path) -> None:
    assert run_foreign_suite(_python("print('ok')"), cwd=tmp_path) is None


def test_nonzero_exit_fails_naming_command_rc_and_output(tmp_path: Path) -> None:
    code = "import sys; print('out-line'); print('err-line', file=sys.stderr); sys.exit(3)"
    with pytest.raises(pytest.fail.Exception) as raised:
        run_foreign_suite(_python(code), cwd=tmp_path)
    message = str(raised.value)
    assert sys.executable in message
    assert "exit code 3" in message
    assert f"cwd: {tmp_path}" in message
    stdout_at = message.index("--- stdout")
    stderr_at = message.index("--- stderr")
    assert message[stdout_at:stderr_at].splitlines()[1:] == ["out-line"]
    assert message[stderr_at:].splitlines()[1:] == ["err-line"]


def test_only_the_last_200_lines_of_each_stream_are_kept(tmp_path: Path) -> None:
    code = (
        "import sys\n"
        "for i in range(300): print(f'out{i:03d}')\n"
        "for i in range(300): print(f'err{i:03d}', file=sys.stderr)\n"
        "sys.exit(1)\n"
    )
    with pytest.raises(pytest.fail.Exception) as raised:
        run_foreign_suite(_python(code), cwd=tmp_path)
    message = str(raised.value)
    assert "out099" not in message and "out100" in message and "out299" in message
    assert "err099" not in message and "err100" in message and "err299" in message


def test_missing_executable_fails_with_a_clear_message(tmp_path: Path) -> None:
    with pytest.raises(pytest.fail.Exception) as raised:
        run_foreign_suite(["deskops-no-such-executable-xyz", "run"], cwd=tmp_path)
    message = str(raised.value)
    assert "not found" in message
    assert "deskops-no-such-executable-xyz" in message


def test_timeout_fails(tmp_path: Path) -> None:
    with pytest.raises(pytest.fail.Exception) as raised:
        run_foreign_suite(_python("import time; print('started', flush=True); time.sleep(30)"), cwd=tmp_path, timeout=0.5)
    message = str(raised.value)
    assert "timed out after 0.5 seconds" in message


def test_cwd_is_respected_as_str_and_path(tmp_path: Path) -> None:
    (tmp_path / "marker.txt").write_text("here\n", encoding="utf-8")
    check = _python("import os, sys; sys.exit(0 if os.path.exists('marker.txt') else 5)")
    run_foreign_suite(check, cwd=tmp_path)
    run_foreign_suite(check, cwd=str(tmp_path))
    other = tmp_path / "other"
    other.mkdir()
    with pytest.raises(pytest.fail.Exception, match="exit code 5"):
        run_foreign_suite(check, cwd=other)


def test_env_replaces_the_environment(tmp_path: Path) -> None:
    check = _python("import os, sys; sys.exit(0 if os.environ.get('BRIDGE_MARK') == 'yes' and 'HOME' not in os.environ else 4)")
    run_foreign_suite(check, cwd=tmp_path, env={"BRIDGE_MARK": "yes"})


SUITE_FILE = "tests/test_vitest_suite.py"
SUITE_TEXT = (
    "from pathlib import Path\n\n"
    "from deskops.testing.foreign_suites import VITEST, run_foreign_suite\n\n\n"
    "def test_vitest_suite() -> None:\n"
    "    run_foreign_suite(VITEST, cwd=Path(__file__).resolve().parents[1])\n"
)


@pytest.mark.parametrize("desk", ["bare_desk", "store_desk"])
def test_closeout_verify_takes_the_bridge_file_as_tests_evidence(desk: str, request: pytest.FixtureRequest) -> None:
    root: Path = request.getfixturevalue(desk)
    _write(root / SUITE_FILE, SUITE_TEXT)
    task_id = "task-foreign-suite"
    text = _task(task_id, [], [ATOM]).replace("- tests/test_skill_cli_drift.py\n", f"- {SUITE_FILE}\n", 1)
    _write(root / "desk" / "tasks" / f"{task_id}.md", text)
    if desk == "store_desk":
        from sldb.api import track_document_file

        pythonpath = str(Path(__file__).resolve().parents[1])
        path = root / "desk" / "tasks" / f"{task_id}.md"
        track_document_file(root / ".sldb", "TaskDoc", path, name=task_id, pythonpath=pythonpath, force=True)

    tests_gate = DeskopsOperations(root).verify_task_closeout(task_id)["gates"]["tests"]

    assert tests_gate["ok"] is True
    assert tests_gate["evidence"] == [SUITE_FILE]

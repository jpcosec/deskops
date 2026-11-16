"""Run a test suite written in another language from a pytest test.

The closeout tests gate of deskops only takes a ``.py`` file under ``tests/`` as test
evidence. A repository whose suite is vitest, go test or anything else declares it with
a short ``tests/test_<suite>_suite.py`` that calls :func:`run_foreign_suite` with the
repository root as ``cwd``; pytest then fails when the foreign suite fails, and that
``.py`` file is what the closeout cites.

This module is meant to be imported only under pytest; the deskops CLI never imports it.
"""

from __future__ import annotations

import os
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

VITEST: list[str] = ["npx", "vitest", "run"]
GO_TEST: list[str] = ["go", "test", "./..."]

TAIL_LINES = 200


def _tail(text: str | bytes | None, lines: int = TAIL_LINES) -> str:
    if text is None:
        return ""
    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="replace")
    return "\n".join(text.splitlines()[-lines:])


def _failure_message(command: list[str], cwd: str, cause: str, stdout: str | bytes | None, stderr: str | bytes | None) -> str:
    return (
        f"foreign suite failed: {cause}\n"
        f"command: {' '.join(command)}\n"
        f"cwd: {cwd}\n"
        f"--- stdout (last {TAIL_LINES} lines) ---\n{_tail(stdout)}\n"
        f"--- stderr (last {TAIL_LINES} lines) ---\n{_tail(stderr)}"
    )


def run_foreign_suite(
    command: Sequence[str],
    *,
    cwd: str | os.PathLike[str],
    timeout: float | None = None,
    env: Mapping[str, str] | None = None,
) -> None:
    """Run ``command`` (an argument list, no shell) in ``cwd``; ``pytest.fail`` unless it exits 0.

    It fails when the exit code is not 0, when the executable is not found and when
    ``timeout`` seconds pass (``None``: no limit). The message names the command, the
    cwd, the exit code or the cause, and the last 200 lines of stdout and then of
    stderr. ``env`` replaces the whole environment, as in :mod:`subprocess`; ``None``
    inherits it.
    """
    import pytest

    argv = [str(part) for part in command]
    workdir = str(Path(cwd))
    try:
        result = subprocess.run(
            argv,
            cwd=workdir,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
            env=dict(env) if env is not None else None,
        )
    except FileNotFoundError as error:
        missing = error.filename or argv[0]
        cause = f"executable or cwd not found: {missing}"
        pytest.fail(_failure_message(argv, workdir, cause, None, None), pytrace=False)
    except OSError as error:
        cause = f"could not start the command: {error}"
        pytest.fail(_failure_message(argv, workdir, cause, None, None), pytrace=False)
    except subprocess.TimeoutExpired as error:
        cause = f"timed out after {timeout} seconds"
        pytest.fail(_failure_message(argv, workdir, cause, error.stdout, error.stderr), pytrace=False)
    if result.returncode != 0:
        cause = f"exit code {result.returncode}"
        pytest.fail(_failure_message(argv, workdir, cause, result.stdout, result.stderr), pytrace=False)

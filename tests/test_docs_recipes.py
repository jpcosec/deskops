"""Execute the recipes of ``docs/configuration.md`` in a temporary desk.

The doc marks what the test runs with the fence's info string:

- ``<lang> recipe:<path>``: a file the recipe writes at ``<path>`` in the desk;
- ``bash recipe``: commands that must exit 0;
- ``bash recipe-fails``: a command that must exit non-zero (the blocked step).

The blocks run in document order in one desk made by ``deskops init``. The test then
checks the outcome the doc promises: the new task is blocked by its own rule, activated
once the rule holds, and the new view answers with the task.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "configuration.md"
FENCE = re.compile(r"^```(\S+)[ \t]+(recipe\S*)[ \t]*\n(.*?)^```[ \t]*$", re.DOTALL | re.MULTILINE)


def _steps() -> list[tuple[str, str, str]]:
    """``(kind, target, body)`` in document order; kind is ``file``, ``run`` or ``fails``."""
    text = DOC.read_text(encoding="utf-8")
    steps: list[tuple[str, str, str]] = []
    for match in FENCE.finditer(text):
        _lang, tag, body = match.groups()
        if tag.startswith("recipe:"):
            steps.append(("file", tag.split(":", 1)[1], body))
        elif tag == "recipe":
            steps.append(("run", "", body))
        elif tag == "recipe-fails":
            steps.append(("fails", "", body))
        else:  # pragma: no cover - a typo in the doc must not pass silently
            raise AssertionError(f"unknown recipe fence: {tag}")
    return steps


def _sandbox(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    root = tmp_path / "repo"
    home = tmp_path / "home"
    bin_dir = tmp_path / "bin"
    for folder in (root, home, bin_dir):
        folder.mkdir(exist_ok=True)
    for name in ("deskops", "sldb"):
        shim = bin_dir / name
        shim.write_text(f"#!/bin/sh\nexec {shlex.quote(sys.executable)} -m {name} \"$@\"\n", encoding="utf-8")
        shim.chmod(0o755)
    (home / ".gitconfig").write_text("[user]\n\tname = Recipes Test\n\temail = recipes@example.invalid\n", encoding="utf-8")
    env = dict(os.environ)
    env.update(
        {
            "HOME": str(home),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "PYTHONPATH": str(REPO_ROOT),
            "PATH": f"{bin_dir}{os.pathsep}{env.get('PATH', '')}",
        }
    )
    return root, env


def _sh(root: Path, env: dict[str, str], command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", command],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=900,
    )


def test_configuration_doc_declares_both_recipes() -> None:
    steps = _steps()
    files = [target for kind, target, _ in steps if kind == "file"]
    assert files == [
        "desk/models/runbook_types.py",
        "desk/lifecycle/rule-activation-task-runbook.md",
        "desk/views/runbooks.md",
    ]
    assert any(kind == "fails" for kind, _, _ in steps)


def test_new_task_type_is_blocked_then_activated_and_new_view_answers(tmp_path: Path) -> None:
    root, env = _sandbox(tmp_path)
    assert _sh(root, env, "git init -q && git commit --allow-empty -q -m seed && deskops init .").returncode == 0

    blocked_seen = False
    activated_seen = False
    view_output = ""
    for index, (kind, target, body) in enumerate(_steps(), start=1):
        if kind == "file":
            path = root / target
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            continue
        for command in [line for line in body.splitlines() if line.strip()]:
            result = _sh(root, env, command)
            report = f"step {index}: {command}\n--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
            if kind == "fails":
                assert result.returncode != 0, report
                if command.startswith("deskops advance"):
                    assert "is blocked by its rules" in result.stdout, report
                    assert "rule-activation-task-runbook" in result.stdout, report
                    blocked_seen = True
                continue
            assert result.returncode == 0, report
            if command.startswith("deskops advance"):
                assert "Advanced to ritual-testing via task_activates" in result.stdout, report
                activated_seen = True
            if command.startswith("sldb views run"):
                view_output = result.stdout

    assert blocked_seen, "the recipe never showed the task blocked by its rule"
    assert activated_seen, "the recipe never activated the task"
    assert "TaskRunbookDoc:task-runbook-uno" in view_output
    assert view_output.index("ritual-testing") < view_output.index("TaskRunbookDoc:task-runbook-uno") < view_output.index("ritual-closeout")

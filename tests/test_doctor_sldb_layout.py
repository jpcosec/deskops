from __future__ import annotations

from pathlib import Path

import pytest

from deskops.cli.main import main

from test_doctor_unmodeled_surfaces import _init_repo


def _doctor(root: Path, capsys) -> tuple[int, str]:
    code = main(["doctor", "--root", str(root)])
    return code, capsys.readouterr().out


def _signal_runtime(root: Path) -> None:
    (root / ".sldb" / "runtime").mkdir(parents=True)


def _signal_journal(root: Path) -> None:
    (root / ".sldb" / "journal").write_text("x\n", encoding="utf-8")


def _signal_ignore_core(root: Path) -> None:
    gitignore = root / ".gitignore"
    gitignore.write_text(gitignore.read_text(encoding="utf-8") + "/.sldb/core/\n", encoding="utf-8")


def _signal_ignore_runtime(root: Path) -> None:
    gitignore = root / ".gitignore"
    gitignore.write_text(gitignore.read_text(encoding="utf-8") + ".sldb/runtime\n", encoding="utf-8")


@pytest.mark.parametrize("signal", [_signal_runtime, _signal_journal, _signal_ignore_core, _signal_ignore_runtime])
def test_each_old_layout_signal_is_an_error_with_the_remedy(tmp_path: Path, capsys, signal) -> None:
    root = tmp_path / "project"
    _init_repo(root, capsys)
    signal(root)
    code, out = _doctor(root, capsys)
    assert code == 1
    assert f"sldb stores migrate-layout --store {root / '.sldb'}" in out
    assert "Desk is healthy" not in out


def test_a_migrated_repo_has_no_layout_issue(tmp_path: Path, capsys) -> None:
    root = tmp_path / "project"
    _init_repo(root, capsys)
    _, out = _doctor(root, capsys)
    assert "migrate-layout" not in out


def test_init_refuses_an_old_layout_and_names_the_remedy(tmp_path: Path, capsys) -> None:
    root = tmp_path / "project"
    _init_repo(root, capsys)
    _signal_runtime(root)
    capsys.readouterr()
    assert main(["init", str(root)]) != 0
    assert f"sldb stores migrate-layout --store {root / '.sldb'}" in capsys.readouterr().out

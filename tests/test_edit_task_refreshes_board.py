from __future__ import annotations

from pathlib import Path

from deskops.cli.main import main


def _board(root: Path) -> str:
    return (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")


def test_edit_task_goal_and_title_refresh_board_line(tmp_path: Path, capsys) -> None:
    assert main(["init", str(tmp_path)]) == 0
    assert main([
        "add", "task", "--root", str(tmp_path), "--title", "Prueba board",
        "--task-type", "task.code", "--goal", "objetivo viejo",
        "--why", "w", "--scope", "s", "--implementation-path", "i",
        "--done-when", "d", "--validation", "pytest",
    ]) == 0
    assert "objetivo viejo" in _board(tmp_path)

    assert main(["edit", "task", "task-prueba-board", "goal", "objetivo nuevo", "--root", str(tmp_path)]) == 0
    board = _board(tmp_path)
    assert "objetivo nuevo" in board
    assert "objetivo viejo" not in board

    assert main(["edit", "task", "task-prueba-board", "title", "Titulo nuevo", "--root", str(tmp_path)]) == 0
    board = _board(tmp_path)
    assert "- Titulo nuevo [draft] - objetivo nuevo" in board
    assert "Prueba board [" not in board

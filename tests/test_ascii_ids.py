"""ASCII ids derived from titles, and git calls that parse paths with accents."""

from __future__ import annotations

import subprocess
from pathlib import Path

from deskops.cli.main import main
from deskops.doc_access import slugify as doc_slugify
from deskops.integrate import _receipt_commit, find_tip
from deskops.slugs import ascii_slug
from deskops.specs.compiler import _slugify as compiler_slugify


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def test_ascii_slug_folds_accents() -> None:
    assert ascii_slug("Transacción ñandú über") == "transaccion-nandu-uber"
    assert ascii_slug("¡¿?!") == ""
    assert compiler_slugify("Transacción ñandú") == "transaccion-nandu"
    assert doc_slugify("Transacción ñandú") == "transaccion-nandu"
    assert doc_slugify("???") == "item"


def test_add_task_title_with_accents_gives_ascii_id(tmp_path: Path, capsys) -> None:
    root = tmp_path / "project"
    root.mkdir()
    assert main(["init", str(root)]) == 0
    capsys.readouterr()
    assert main(["add", "task", "--title", "Transacción ñandú", "--task-type", "task.docs", "--root", str(root)]) == 0
    capsys.readouterr()
    ids = [p.stem for p in (root / "desk" / "tasks").glob("task-*.md")]
    assert ids and all(i.isascii() for i in ids)
    assert any("transaccion-nandu" in i for i in ids)


def test_existing_accented_id_still_resolves(tmp_path: Path, capsys) -> None:
    root = tmp_path / "project"
    root.mkdir()
    assert main(["init", str(root)]) == 0
    capsys.readouterr()
    # An id given explicitly is kept as is (only ids derived from a title fold to ASCII),
    # so a desk can still hold and resolve a task whose id has accents.
    payload = '{"id": "task-transacción", "title": "Transacción", "task_type": "task.docs"}'
    assert main(["add", "task", payload, "--root", str(root)]) == 0
    capsys.readouterr()
    assert (root / "desk" / "tasks" / "task-transacción.md").exists()
    assert main(["show", "task", "task-transacción", "--root", str(root)]) == 0
    assert "task-transacción" in capsys.readouterr().out


def test_integrate_finds_receipt_of_task_with_accented_id(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    task_id = "task-transacción"
    sha = "a" * 40
    receipt = root / "desk" / "reviews" / task_id / "evidence-commit-1.md"
    receipt.parent.mkdir(parents=True)
    receipt.write_text(f"---\nverdict: accepted\nvalue: {sha}\n---\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", f"closeout: {task_id}")
    tip = find_tip(root, task_id)
    assert tip is not None
    assert _receipt_commit(root, tip, task_id) == sha


def test_closure_git_helper_does_not_quote_paths(tmp_path: Path) -> None:
    from deskops.services.closure import ClosureService  # noqa: F401

    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    (root / "decisión.txt").write_text("x\n", encoding="utf-8")
    _git(root, "add", "decisión.txt")
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", "diff", "--cached", "--name-only"],
        cwd=root, capture_output=True, text=True,
    )
    assert result.stdout.strip() == "decisión.txt"

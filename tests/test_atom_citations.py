"""``deskops atoms citations``: code -> atom citations, checked and recorded in the graph.

Every case runs in a sandbox repository under ``tmp_path`` (the ``lifecycle_desk`` fixture: a git
repo with a desk and its sldb store as ``deskops init`` leaves it): a valid citation, a broken one (``--check`` exits 1) and an
orphan atom (a warning, exit 0), and ``--write`` makes ``deskops show atom`` list the citers.
"""

from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from deskops import doc_access
from deskops.cli.main import main
from deskops.models import AtomDoc
from deskops.services.atoms import comment_citations
from deskops.services.atoms import docstring_citations


ATOM = """---
id: {atom_id}
title: {atom_id}
five_wh_one_plus: how
tags:
- system:deskops
provenance: docs/source.md
---

# {atom_id}

## Answer

Sandbox atom.
"""

MODULE = '''"""Sandbox module.

Atoms:
atom-cited
'''

PY_VALID = MODULE + '"""\n\nVALUE = 1\n'
PY_BROKEN = '"""Broken module.\n\nAtoms:\natom-missing\n"""\n'
CONFIG_VALID = "key: value\n# Atom: atom-cited\n"


def _git(root: Path, *argv: str) -> None:
    subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True, text=True)


def _sandbox(root: Path, files: dict[str, str], atoms: tuple[str, ...] = ("atom-cited",)) -> Path:
    """``root`` is the ``lifecycle_desk`` fixture: a git repo with a desk as `deskops init` leaves it."""
    for atom_id in atoms:
        path = root / "desk" / "atoms" / f"{atom_id}.md"
        path.write_text(ATOM.format(atom_id=atom_id), encoding="utf-8")
        doc_access.track_created_document(root, AtomDoc, path, atom_id)
    for relative, text in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    _git(root, "add", "--", *files)
    return root


def _run(capsys: pytest.CaptureFixture[str], *argv: str) -> tuple[int, str]:
    capsys.readouterr()
    code = main(list(argv))
    return code, capsys.readouterr().out


# ---------------------------------------------------------------- grammar
def test_docstring_block_ends_at_empty_line_or_non_id_line() -> None:
    source = '"""Title.\n\nAtoms:\natom-one\natom-two\n\natom-not-in-block\n"""\n'
    assert docstring_citations(source) == [(4, "atom-one"), (5, "atom-two")]
    stopped = '"""Title.\n\nAtoms:\natom-one\n  atom-indented\natom-after\n"""\n'
    assert docstring_citations(stopped) == [(4, "atom-one")]
    assert docstring_citations('VALUE = """\nAtoms:\natom-one\n"""\n') == []
    assert docstring_citations("def broken(:\n") == []


def test_comment_citations_need_an_atom_id() -> None:
    text = "# Atom: atom-one\nx  # Atom: atom-two\n# Atom: <id>\n# Atom: Atom-Upper\n"
    assert comment_citations(text) == [(1, "atom-one"), (2, "atom-two")]


# ---------------------------------------------------------------- the verb
def test_valid_citation_checks_clean_and_write_lists_citers_in_show_atom(
    lifecycle_desk: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _sandbox(
        lifecycle_desk,
        {"pkg/module.py": PY_VALID, "config.yaml": CONFIG_VALID, "latin1.txt": "x"},
    )
    (root / "latin1.txt").write_bytes(b"# Atom: atom-cited \xe9\xff\n")  # not UTF-8: skipped

    code, out = _run(capsys, "atoms", "citations", "--check", "--root", str(root))
    assert code == 0, out
    assert "- config.yaml:2 -> atom-cited" in out
    assert "- pkg/module.py:4 -> atom-cited" in out
    assert "latin1.txt" not in out
    assert "Broken citations" not in out

    code, out = _run(capsys, "atoms", "citations", "--write", "--root", str(root))
    assert code == 0, out
    assert "Graph: 2 cited_by relation(s) created, 0 removed." in out
    assert (root / "desk" / "citations" / "type-cited_by.md").exists()

    code, out = _run(capsys, "show", "atom", "atom-cited", "--root", str(root))
    assert code == 0, out
    assert "Cited by:\n- config.yaml\n- pkg/module.py" in out

    # Idempotent; a citation that disappears from the code leaves the graph on the next write.
    code, out = _run(capsys, "atoms", "citations", "--write", "--root", str(root))
    assert "Graph: 0 cited_by relation(s) created, 0 removed." in out
    (root / "config.yaml").write_text("key: value\n", encoding="utf-8")
    code, out = _run(capsys, "atoms", "citations", "--write", "--root", str(root))
    assert "Graph: 0 cited_by relation(s) created, 1 removed." in out
    code, out = _run(capsys, "show", "atom", "atom-cited", "--root", str(root))
    assert "Cited by:\n- pkg/module.py" in out
    assert "config.yaml" not in out


def test_broken_citation_fails_check_even_with_orphans(
    lifecycle_desk: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _sandbox(
        lifecycle_desk,
        {"pkg/module.py": PY_VALID, "pkg/broken.py": PY_BROKEN},
        atoms=("atom-cited", "atom-lonely"),
    )
    code, out = _run(capsys, "atoms", "citations", "--check", "--root", str(root))
    assert code == 1, out
    assert "Broken citations: 1" in out
    assert "- pkg/broken.py:4 -> atom-missing (no such atom)" in out
    assert "Warning: atoms without a citation: 1" in out

    # Without --check the scan only reports.
    code, _out = _run(capsys, "atoms", "citations", "--root", str(root))
    assert code == 0


def test_orphan_atom_is_a_warning_with_exit_zero(lifecycle_desk: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _sandbox(lifecycle_desk, {"pkg/module.py": PY_VALID}, atoms=("atom-cited", "atom-lonely"))
    code, out = _run(capsys, "atoms", "citations", "--check", "--root", str(root))
    assert code == 0, out
    assert "Warning: atoms without a citation: 1\n- atom-lonely" in out
    assert "Broken citations" not in out

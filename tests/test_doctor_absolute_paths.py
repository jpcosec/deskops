"""`deskops doctor` finds absolute paths in the desk; `--repair` writes them as addresses any machine resolves.

The fixtures live under tmp_path: ``<tmp>/eco/`` is the ecosystem folder, ``eco/project`` the desk
under test and ``eco/sldb``, ``eco/spec2viz`` its neighbours, linked in ``.sldb/store.yaml``.
Paths of "another machine" are ``/home/jp/proyectos/eco/<repo>``, whose ecosystem folder is
named like the fixture's.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops import absolute_paths
from deskops.cli.main import main
from deskops.identity import load_repository_registry
from deskops.doc_access import read_doc
from deskops.models import RepositoryDoc, TaskDoc

OTHER = "/home/jp/proyectos/eco"


def _out(capsys) -> str:
    return capsys.readouterr().out


def _eco(tmp_path: Path, capsys, *, neighbours=("sldb", "spec2viz")) -> Path:
    eco = tmp_path / "eco"
    root = eco / "project"
    root.mkdir(parents=True)
    for name in neighbours:
        (eco / name / ".sldb").mkdir(parents=True)
    assert main(["init", str(root)]) == 0
    capsys.readouterr()
    store = root / ".sldb" / "store.yaml"
    text = store.read_text(encoding="utf-8")
    links = "".join(f"- name: {n}\n  path: ../{n}/.sldb\n" for n in neighbours)
    store.write_text(text.replace("links:\n", "links:\n" + links, 1), encoding="utf-8")
    return root


def _register(root: Path, capsys, name: str, path: str) -> Path:
    assert main(["repo", "register", name, path, "--store", str(root / ".sldb")]) == 0
    capsys.readouterr()
    return root / "desk" / "registry" / f"repo-{name}.md"


def _set_path(doc: Path, value: str) -> None:
    lines = doc.read_text(encoding="utf-8").splitlines()
    doc.write_text("\n".join(f"path: {value}" if ln.startswith("path:") else ln for ln in lines) + "\n", encoding="utf-8")


def _task(root: Path, capsys, title: str, files: list[str], references: list[str] | None = None) -> Path:
    assert main(["add", "task", "--root", str(root), "--title", title, "--why", "w", "--goal", "g",
                 "--scope", "s", "--implementation-path", "i", "--done-when", "d"]) == 0
    capsys.readouterr()
    (path,) = [p for p in (root / "desk" / "tasks").glob("task-*.md") if p.name.startswith("task-" + title.split()[0])]
    text = path.read_text(encoding="utf-8")
    block = lambda key, vals: f"{key}:\n" + "".join(f"- {v}\n" for v in vals) if vals else f"{key}: []\n"
    text = text.replace("files: []\n", block("files", files), 1)
    text = text.replace("references: []\n", block("references", references or []), 1)
    path.write_text(text, encoding="utf-8")
    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0  # the store indexes the hand-made fixture
    capsys.readouterr()
    return path


def _doctor(root: Path, capsys, *extra: str) -> tuple[int, str]:
    code = main(["doctor", "--root", str(root), *extra])
    return code, _out(capsys)


def _abs_lines(out: str) -> list[str]:
    return [ln for ln in out.splitlines() if "Absolute path:" in ln]


def test_a_path_that_exists_under_a_neighbour_becomes_a_relative_registry_path(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    doc = _register(root, capsys, "sldb", "../sldb")
    _set_path(doc, str((tmp_path / "eco" / "sldb")))
    code, out = _doctor(root, capsys)
    assert code == 0 and "becomes ../sldb" in "\n".join(_abs_lines(out))
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0 and "-> ../sldb" in out
    assert read_doc(doc, RepositoryDoc)["path"] == "../sldb"
    assert _abs_lines(_doctor(root, capsys)[1]) == []


def test_a_path_from_another_machine_is_placed_by_the_ecosystem_folder(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    doc = _register(root, capsys, "spec2viz", "../spec2viz")
    _set_path(doc, f"{OTHER}/spec2viz")
    task = _task(root, capsys, "alpha", [f"{OTHER}/spec2viz/src/a.py"])
    _register(root, capsys, "sldb", "../sldb")
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0, out
    assert read_doc(doc, RepositoryDoc)["path"] == "../spec2viz"
    assert read_doc(task, TaskDoc)["files"] == ["spec2viz:src/a.py"]
    assert _abs_lines(out) == []


def test_an_ambiguous_path_stays_an_alert_with_its_reason(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    _register(root, capsys, "sldb", "../sldb")
    value = f"{OTHER}/sldb/x/eco/project/a.py"  # the folder appears twice: sldb, and the desk's own repo
    task = _task(root, capsys, "beta", [value])
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0
    assert read_doc(task, TaskDoc)["files"] == [value]
    lines = _abs_lines(out)
    assert len(lines) == 1 and value in lines[0] and "not rewritten: ambiguous" in lines[0]
    assert "Desk is healthy, with" in out


def test_a_path_that_names_no_neighbour_is_left_with_its_reason(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    task = _task(root, capsys, "gamma", ["/home/jp/AntonIA/repos/other/a.py", f"{OTHER}/unknown/a.py"])
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0 and len(_abs_lines(out)) == 2
    assert "no '" in out and "names no repository" in out
    assert len(read_doc(task, TaskDoc)["files"]) == 2


def test_a_path_of_the_own_repo_is_relative_to_its_root_without_prefix(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    task = _task(root, capsys, "delta", [str(root / "src" / "a.py"), f"{OTHER}/project/b.py"],
                 references=[f"{OTHER}/project/docs/c.md"])
    code, _out_ = _doctor(root, capsys, "--repair")
    assert code == 0
    payload = read_doc(task, TaskDoc)
    assert payload["files"] == ["src/a.py", "b.py"]
    assert payload["references"] == ["docs/c.md"]


def test_a_neighbour_without_registry_entry_is_an_alert(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    task = _task(root, capsys, "eps", [f"{OTHER}/sldb/a.py"])
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0 and "register it with deskops repo register" in out
    assert read_doc(task, TaskDoc)["files"] == [f"{OTHER}/sldb/a.py"]


def test_a_registry_with_two_repos_resolves_after_repair(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    docs = {n: _register(root, capsys, n, f"../{n}") for n in ("sldb", "spec2viz")}
    _set_path(docs["sldb"], f"{OTHER}/sldb")
    _set_path(docs["spec2viz"], str(tmp_path / "eco" / "spec2viz"))
    task = _task(root, capsys, "zeta", [f"{OTHER}/sldb/a.py", str(tmp_path / "eco" / "spec2viz" / "b.py")])
    before = {e.id: e.repo_root for e in load_repository_registry(root / "desk", root)}
    assert before["sldb"] != (tmp_path / "eco" / "sldb").resolve()  # another machine: not there
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0 and _abs_lines(out) == []
    after = {e.id: e.repo_root for e in load_repository_registry(root / "desk", root)}
    assert after == {"sldb": (tmp_path / "eco" / "sldb").resolve(), "spec2viz": (tmp_path / "eco" / "spec2viz").resolve()}
    assert read_doc(task, TaskDoc)["files"] == ["sldb:a.py", "spec2viz:b.py"]


def test_the_exit_code_does_not_change_and_repair_is_idempotent(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    doc = _register(root, capsys, "sldb", "../sldb")
    _set_path(doc, f"{OTHER}/sldb")
    assert _doctor(root, capsys)[0] == 0
    assert _doctor(root, capsys, "--repair")[0] == 0
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0 and "Absolute path" not in out


@pytest.mark.parametrize("value, absolute", [("/loop", False), ("//host/x", False), ("a/b", False),
                                              ("/home/jp/x/y", True), ("two words /a/b", False)])
def test_what_counts_as_an_absolute_path(value: str, absolute: bool) -> None:
    assert absolute_paths.looks_absolute(value) is absolute

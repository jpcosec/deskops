from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.cli.main import main
from sldb.cli.main import main as sldb_main
from sldb.store.io import load_documents_index
from sldb.store.io import load_models_index
from sldb.store.io import load_store_index


ATOM_ARGS = [
    "--title",
    "Trackable atom",
    "--five-wh-one-plus",
    "what",
    "--answer",
    "Created atoms should be visible through deskops and sldb.",
]


def _install_sandbox(root: Path) -> None:
    assert main(["desk", "install", str(root)]) == 0


def test_atoms_validate_accepts_valid_atom(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_ARGS]) == 0
    capsys.readouterr()

    result = main(["atoms", "validate", "atom-trackable-atom", "--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 0
    assert "Atom: atom-trackable-atom" in captured.out
    assert "- valid" in captured.out


def test_atoms_validate_all_reports_slug_and_provenance_errors(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    atoms_dir = tmp_path / "desk" / "atoms"
    bad_atom = atoms_dir / "atom-bad.md"
    bad_atom.write_text(
        "---\n"
        "id: bad-atom\n"
        "title: Bad Atom\n"
        "five_wh_one_plus: what\n"
        "tags:\n"
        "- unknown:value\n"
        "provenance: docs/missing-source.md\n"
        "---\n\n"
        "# Bad Atom\n\n"
        "## Answer\n\n"
        "Broken atom.\n",
        encoding="utf-8",
    )

    result = main(["atoms", "validate", "--all", "--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 1
    assert "Atom: bad-atom" in captured.out
    assert "filename must match atom id 'bad-atom'" in captured.out
    assert "atom id must follow slug convention atom-<slug>" in captured.out
    # Without a store sldb checks no namespace (test_domain_tree covers the declared desk).
    assert "Unknown atom tag namespace" not in captured.out
    assert "provenance is not resolvable: docs/missing-source.md" in captured.out


def test_atoms_delete_blocks_when_inbound_references_exist(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_ARGS]) == 0
    capsys.readouterr()

    task_path = tmp_path / "desk" / "tasks" / "task-ref.md"
    task_path.write_text(
        "# Ref\n\nReferences atom:atom-trackable-atom from a task.\n",
        encoding="utf-8",
    )

    result = main(["atoms", "delete", "atom-trackable-atom", "--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 1
    assert "Refusing to delete atom-trackable-atom" in captured.out
    assert "desk/tasks/task-ref.md:3" in captured.out
    assert (tmp_path / "desk" / "atoms" / "atom-trackable-atom.md").exists()
    assert "atom:atom-trackable-atom" in task_path.read_text(encoding="utf-8")


def test_atoms_delete_force_removes_file_and_untracks_store(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    store = tmp_path / ".sldb"
    assert sldb_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert sldb_main(
        [
            "models",
            "add",
            "deskops.models:AtomDoc",
            "--store",
            str(store),
            "--pythonpath",
            str(ROOT),
        ]
    ) == 0
    capsys.readouterr()

    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_ARGS]) == 0
    capsys.readouterr()

    task_path = tmp_path / "desk" / "tasks" / "task-ref.md"
    task_path.write_text(
        "# Ref\n\nReferences atom:atom-trackable-atom from a task.\n",
        encoding="utf-8",
    )

    result = main(["atoms", "delete", "atom-trackable-atom", "--force", "--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 0
    assert "Deleted atom atom-trackable-atom" in captured.out
    assert "Store untracked: yes" in captured.out
    assert not (tmp_path / "desk" / "atoms" / "atom-trackable-atom.md").exists()
    assert "atom:atom-trackable-atom" in task_path.read_text(encoding="utf-8")

    store_index = load_store_index(store)
    model_entry = next(entry for entry in store_index.models if entry.name == "AtomDoc")
    models_index = load_models_index(tmp_path / model_entry.models_index)
    documents_index = load_documents_index(tmp_path / models_index.documents_index)
    assert all(entry.name != "atom-trackable-atom" for entry in documents_index.documents)


def _add_conv_atom(root: Path, title: str, conv: str) -> int:
    args = ["--title", title, "--five-wh-one-plus", "what", "--answer", "Acuerdo."]
    return main(["add", "atom", "--root", str(root), *args, "--conv", conv])


def test_add_atom_with_conv_writes_conversation_ref(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    assert _add_conv_atom(tmp_path, "Acuerdo uno", "#acuerdos-sldb1/1234") == 0
    capsys.readouterr()
    text = (tmp_path / "desk" / "atoms" / "atom-acuerdo-uno.md").read_text(encoding="utf-8")
    assert "conversation_ref: '#acuerdos-sldb1/1234'" in text or "conversation_ref: #acuerdos-sldb1/1234" in text
    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_ARGS]) == 0
    assert "conversation_ref" not in (tmp_path / "desk" / "atoms" / "atom-trackable-atom.md").read_text(encoding="utf-8")


def test_list_atoms_filters_by_conv(tmp_path: Path, capsys) -> None:
    import json

    _install_sandbox(tmp_path)
    assert _add_conv_atom(tmp_path, "Uno", "#acuerdos-sldb1/1") == 0
    assert _add_conv_atom(tmp_path, "Dos", "#acuerdos-sldb1") == 0
    assert _add_conv_atom(tmp_path, "Tres", "#otro/9") == 0
    assert _add_conv_atom(tmp_path, "Cuatro", "#acuerdos-sldb10/1") == 0
    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_ARGS]) == 0
    capsys.readouterr()

    assert main(["list", "atoms", "--root", str(tmp_path), "--conv", "#acuerdos-sldb1", "--format", "json"]) == 0
    atoms = json.loads(capsys.readouterr().out)["atoms"]
    assert sorted(a["id"] for a in atoms) == ["atom-dos", "atom-uno"]
    assert {a["conversation_ref"] for a in atoms} == {"#acuerdos-sldb1/1", "#acuerdos-sldb1"}


def test_add_atom_refuses_duplicate_conv(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    assert _add_conv_atom(tmp_path, "Primero", "#h/5") == 0
    capsys.readouterr()
    assert _add_conv_atom(tmp_path, "Segundo", "#h/5") == 1
    captured = capsys.readouterr()
    assert "ya existe atom-primero con conversation_ref #h/5" in captured.err
    assert not (tmp_path / "desk" / "atoms" / "atom-segundo.md").exists()

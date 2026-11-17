from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import re

import pytest
from sldb.core.exceptions import SLDBStoreError
from sldb.runtime.validation import render_model_markdown

from deskops.bootstrap import SLDBBootstrap
from sldb.api import doc_exists

from deskops.cli.main import main
from deskops.identity import load_repository_registry
from deskops.identity import EcosystemIdentity
from deskops.models import RepositoryDoc


def _write_repo_doc(
    registry_dir: Path,
    *,
    repo_id: str,
    repo_path: str,
    name: str | None = None,
    filename: str | None = None,
) -> Path:
    payload = {
        "id": repo_id,
        "name": name or repo_id,
        "path": repo_path,
        "status": "active",
        "description": f"Repository for {repo_id}.",
        "tags": [],
    }
    path = registry_dir / (filename or f"repo-{repo_id}.md")
    path.write_text(render_model_markdown(RepositoryDoc, payload) + "\n", encoding="utf-8")
    return path


def _write_config(repo_root: Path, project_identity: str) -> None:
    desk_root = repo_root / "desk"
    desk_root.mkdir(parents=True, exist_ok=True)
    (desk_root / "config.json").write_text(
        json.dumps({"project_identity": project_identity}, indent=2) + "\n",
        encoding="utf-8",
    )


def _init_ecosystem(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    with contextlib.redirect_stdout(io.StringIO()):
        assert SLDBBootstrap().init_local_store(root) == 0
    desk_root = root / "desk"
    desk_root.mkdir(parents=True, exist_ok=True)
    (desk_root / "config.json").write_text(
        json.dumps({"project_identity": "graph_ui"}, indent=2) + "\n",
        encoding="utf-8",
    )
    return root / ".sldb"


def test_repo_remove_then_register_same_path_under_correct_id(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A mis-registered id is removable so the same root can be registered again."""
    root = tmp_path / "ecosystem"
    store_path = _init_ecosystem(root)
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)

    register_wrong = main([
        "repo", "register", "graph-ui", str(root), "--store", str(store_path),
    ])
    capsys.readouterr()
    assert register_wrong == 0

    registry_file = root / "desk" / "registry" / "repo-graph-ui.md"
    assert registry_file.exists()
    assert doc_exists(root / ".sldb", registry_file.relative_to(root).as_posix())

    removed = main(["repo", "remove", "graph-ui", "--store", str(store_path)])
    remove_out = capsys.readouterr().out
    assert removed == 0
    assert str(registry_file) in remove_out
    assert not registry_file.exists()
    assert not doc_exists(root / ".sldb", registry_file.relative_to(root).as_posix())

    missing = main(["repo", "remove", "not-registered", "--store", str(store_path)])
    missing_out = capsys.readouterr().out
    assert missing == 1
    assert "not-registered" in missing_out
    assert "(none)" in missing_out

    register_right = main([
        "repo",
        "register",
        "graph_ui",
        str(root),
        "--id",
        "graph_ui",
        "--store",
        str(store_path),
    ])
    capsys.readouterr()
    assert register_right == 0
    assert (root / "desk" / "registry" / "repo-graph_ui.md").exists()

    whoami = main(["repo", "whoami", "--root", str(root), "--store", str(store_path)])
    whoami_out = capsys.readouterr().out
    assert whoami == 0
    assert whoami_out.strip() == "graph_ui"


def test_repo_remove_missing_id_lists_existing_ids(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="graph-ui", repo_path="graph-ui")
    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    result = main(["repo", "remove", "ghost", "--store", str(store_path)])
    captured = capsys.readouterr()

    assert result == 1
    assert "Repository 'ghost' is not registered" in captured.out
    assert "graph-ui" in captured.out
    assert (registry_dir / "repo-graph-ui.md").exists()


def test_resolve_registered_desk_reports_actionable_missing_registry_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (tmp_path / "desk" / "registry").mkdir(parents=True)
    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    with pytest.raises(SLDBStoreError, match="Supported path: run 'deskops repo register <name> --path <abs>'"):
        EcosystemIdentity(str(store_path)).how_do_i_find_another("deskops")



def test_resolve_canonical_project_identity_reports_actionable_unregistered_root_message(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    repo_root = tmp_path / "sender-repo"
    _write_config(repo_root, "sender-repo")
    _write_repo_doc(registry_dir, repo_id="sender-repo", repo_path="other-root")

    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    expected = f"Supported path: run 'deskops repo register <name> --path {repo_root.resolve()}'"
    with pytest.raises(SLDBStoreError, match=re.escape(expected)):
        EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root, require_registry_match=True)



def test_repo_register_accepts_optional_path_flag_and_does_not_crash_on_registry_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "ecosystem"
    desk_root = root / "desk"
    registry_dir = desk_root / "registry"
    registry_dir.mkdir(parents=True)
    # A real store that registers RepositoryDoc: the registration is written and tracked in
    # its transaction (the old fake tracking seam is gone with doc_io).
    from sldb.api import add_model, init_store

    init_store(path=root)
    store_path = root / ".sldb"
    add_model(store_path, "deskops.models:RepositoryDoc", pythonpath=str(Path(__file__).resolve().parents[1]))

    _write_repo_doc(registry_dir, repo_id="existing-repo", repo_path="tools/existing-repo")

    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    monkeypatch.setattr("deskops.cli.commands.repo.get_store_context", lambda _arg: (store_path, root))
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, root))
    monkeypatch.setattr("deskops.cli.commands.repo.find_local_store", lambda: store_path)

    repo_root = (tmp_path / "external" / "deskops").resolve()
    result = main([
        "repo",
        "register",
        "deskops",
        "--path",
        str(repo_root),
        "--store",
        str(store_path),
    ])

    captured = capsys.readouterr()
    output_path = registry_dir / "repo-deskops.md"

    assert result == 0
    assert output_path.exists()
    assert doc_exists(store_path, "repo-deskops")
    assert "Unexpected:" not in captured.out
    assert f"Wrote {output_path}" in captured.out

    entries = load_repository_registry(desk_root, root)
    deskops_entry = next(entry for entry in entries if entry.id == "deskops")
    assert deskops_entry.repo_root == repo_root
    # The stored path is relative to the repo holding desk/registry, not this machine's absolute path.
    assert deskops_entry.relative_path == "../external/deskops"


def _register_cli(root: Path, store_path: Path, name: str, path: str, capsys: pytest.CaptureFixture[str]) -> Path:
    assert main(["repo", "register", name, "--path", path, "--store", str(store_path)]) == 0
    capsys.readouterr()
    return root / "desk" / "registry" / f"repo-{name}.md"


def test_repo_register_stores_the_path_relative_to_the_registry_repo_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An absolute path, the repo itself and a ~ path are all written relative to the repo
    that holds desk/registry (here the ecosystem root), and resolve back to the same root."""
    root = tmp_path / "ecosystem"
    store_path = _init_ecosystem(root)
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    sibling = (tmp_path / "sibling").resolve()
    nested = (root / "tools" / "nested").resolve()
    homed = (tmp_path / "home" / "proyectos" / "homed").resolve()

    expected = {
        "sibling": (str(sibling), "../sibling", sibling),
        "self": (str(root), ".", root.resolve()),
        "nested": (str(nested), "tools/nested", nested),
        "homed": ("~/proyectos/homed", "../home/proyectos/homed", homed),
    }
    for name, (given, _stored, _resolved) in expected.items():
        _register_cli(root, store_path, name, given, capsys)

    entries = {entry.id: entry for entry in load_repository_registry(root / "desk", root)}
    for name, (_given, stored, resolved) in expected.items():
        assert entries[name].relative_path == stored
        assert entries[name].repo_root == resolved
        doc = (root / "desk" / "registry" / f"repo-{name}.md").read_text(encoding="utf-8")
        assert str(tmp_path) not in doc


def test_old_registry_entries_with_absolute_or_home_paths_still_resolve(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Entries written before relative paths (absolute, or with ~) resolve for every reader:
    the identity registry and doc_access.repository_root share resolve_registered_root."""
    from deskops import doc_access

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    root = tmp_path / "ecosystem"
    registry_dir = root / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    absolute = (tmp_path / "old-absolute").resolve()
    absolute.mkdir()
    homed = (tmp_path / "home" / "proyectos" / "homed").resolve()
    homed.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="old-absolute", repo_path=str(absolute))
    _write_repo_doc(registry_dir, repo_id="old-home", repo_path="~/proyectos/homed")

    entries = {entry.id: entry for entry in load_repository_registry(root / "desk", root)}
    assert entries["old-absolute"].repo_root == absolute
    assert entries["old-home"].repo_root == homed
    assert doc_access.repository_root(root, {"path": str(absolute)}) == absolute
    assert doc_access.repository_root(root, {"path": "~/proyectos/homed"}) == homed
    assert doc_access.repository_root(root, {"path": "../old-absolute"}) == absolute


def test_doctor_names_registry_entries_that_do_not_resolve_on_this_machine(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """One alert per desk/registry entry whose path does not resolve: id, stored path and
    absolute path tried. Alerts never change doctor's exit code; resolving entries are silent."""
    root = tmp_path / "project"
    root.mkdir()
    assert main(["init", str(root)]) == 0
    capsys.readouterr()
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    store_path = root / ".sldb"
    baseline_code = main(["doctor", "--root", str(root)])
    capsys.readouterr()

    present = (tmp_path / "present").resolve()
    present.mkdir()
    _register_cli(root, store_path, "present", str(present), capsys)
    gone = _register_cli(root, store_path, "gone", str(tmp_path / "gone"), capsys)
    other_machine = _register_cli(root, store_path, "other-machine", str(tmp_path / "x"), capsys)
    lines = other_machine.read_text(encoding="utf-8").splitlines()
    other_machine.write_text(
        "\n".join("path: /home/jp/proyectos/nowhere" if ln.startswith("path:") else ln for ln in lines) + "\n",
        encoding="utf-8",
    )
    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    capsys.readouterr()

    code = main(["doctor", "--root", str(root)])
    out = capsys.readouterr().out
    assert code == baseline_code
    alerts = [ln for ln in out.splitlines() if "does not resolve on this machine" in ln]
    assert len(alerts) == 2, out
    assert any(
        "'gone'" in ln and "path '../gone'" in ln and str((tmp_path / "gone").resolve()) in ln for ln in alerts
    ), alerts
    assert any(
        "'other-machine'" in ln and "path '/home/jp/proyectos/nowhere'" in ln and "/home/jp/proyectos/nowhere" in ln
        for ln in alerts
    ), alerts
    assert not any("'present'" in ln for ln in alerts)
    assert gone.exists()

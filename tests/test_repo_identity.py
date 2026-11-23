from __future__ import annotations

import json
from pathlib import Path

import pytest
from sldb.core.exceptions import SLDBStoreError
from sldb.runtime.validation import render_model_markdown

from deskops.cli.main import main
from deskops.identity import EcosystemIdentity
from deskops.identity import load_repository_registry
from deskops.identity import resolve_store_context
from deskops.models import RepositoryDoc


def _write_repo_doc(registry_dir: Path, *, repo_id: str, repo_path: str, name: str | None = None, filename: str | None = None) -> Path:
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


def test_repo_identity_resolver_returns_single_registered_match(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    repo_root = tmp_path / "sender-repo"
    (repo_root / "desk").mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="sender-repo", repo_path="sender-repo", name="Sender Repo")

    store_path = tmp_path / ".sldb"
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    assert EcosystemIdentity(str(store_path)).how_do_i_find_another("sender-repo") == (repo_root / "desk").resolve()
    assert EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root / "subdir", require_registry_match=False) == "sender-repo"


def test_repo_identity_resolver_fails_on_duplicate_id(tmp_path: Path) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="shared-id", repo_path="repo-one", filename="repo-one.md")
    _write_repo_doc(registry_dir, repo_id="shared-id", repo_path="repo-two", filename="repo-two.md")

    with pytest.raises(SLDBStoreError, match="Duplicate repository id 'shared-id'"):
        load_repository_registry(tmp_path / "desk", tmp_path)


def test_repo_identity_resolver_fails_on_duplicate_root(tmp_path: Path) -> None:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="repo-one", repo_path="shared-root", filename="repo-one.md")
    _write_repo_doc(registry_dir, repo_id="repo-two", repo_path="shared-root", filename="repo-two.md")

    with pytest.raises(SLDBStoreError, match="Duplicate repository root"):
        load_repository_registry(tmp_path / "desk", tmp_path)


def test_repo_whoami_prints_canonical_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    repo_root = tmp_path / "deskops-child"
    _write_config(repo_root, "deskops-child")
    registry_dir = repo_root / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="deskops-child", repo_path=".")

    store_path = repo_root / ".sldb"
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self, **kw: 0)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, repo_root))

    result = main(["repo", "whoami", "--root", str(repo_root), "--store", str(store_path)])

    captured = capsys.readouterr()
    assert result == 0
    assert captured.out.strip() == "deskops-child"


def test_repo_local_desk_without_a_registry_is_its_own_authority(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A desk that keeps no registry must still resolve its own identity.

    Without this, `deskops message ack` and `deskops next` inside such a repo
    fail with "Repository id '<name>' not found in registry", which makes inbox
    triage impossible from the repository the note is addressed to.
    """
    repo_root = tmp_path / "repo-local"
    _write_config(repo_root, "repo-local")

    store_path = repo_root / ".sldb"
    store_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, repo_root))

    assert EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root, require_registry_match=True) == "repo-local"
    assert EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root, require_registry_match=False) == "repo-local"


def test_a_registry_that_lacks_the_repo_still_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The fallback is only for a missing registry, not for a disagreement."""
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    _write_repo_doc(registry_dir, repo_id="someone-else", repo_path="someone-else")

    repo_root = tmp_path / "repo-local"
    _write_config(repo_root, "repo-local")
    store_path = repo_root / ".sldb"
    store_path.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))

    with pytest.raises(SLDBStoreError, match="not found in registry"):
        EcosystemIdentity(str(store_path)).what_repository_am_i_in(repo_root, require_registry_match=True)


def _make_store(root: Path) -> Path:
    store = root / ".sldb"
    (store / "core").mkdir(parents=True)
    (store / "core" / "store_index.yaml").write_text("{}\n", encoding="utf-8")
    return store


def test_nested_sandbox_never_reads_the_outer_repository_store(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A sandbox with its own desk/ is the boundary; the repo store above it is invisible."""
    outer = tmp_path / "outer"
    (outer / ".git").mkdir(parents=True)
    (outer / "desk").mkdir()
    outer_store = _make_store(outer)

    sandbox = outer / ".tmp" / "deskops-cli-test"
    (sandbox / "desk").mkdir(parents=True)
    monkeypatch.chdir(sandbox)

    assert outer_store.exists()
    with pytest.raises(SLDBStoreError, match="No local store found"):
        resolve_store_context(None)


def test_nested_sandbox_uses_its_own_store_when_it_has_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    outer = tmp_path / "outer"
    (outer / ".git").mkdir(parents=True)
    (outer / "desk").mkdir()
    _make_store(outer)

    sandbox = outer / ".tmp" / "deskops-cli-test"
    (sandbox / "desk").mkdir(parents=True)
    sandbox_store = _make_store(sandbox)
    monkeypatch.chdir(sandbox)

    store, root = resolve_store_context(None)

    assert store == sandbox_store.resolve()
    assert root == sandbox.resolve()


def _init_desk(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str, *extra: str) -> Path:
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self, **kw: 0)
    root = tmp_path / name
    root.mkdir()
    assert main(["init", str(root), *extra]) == 0
    return root


def test_init_with_id_sets_project_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    root = _init_desk(tmp_path, monkeypatch, "wf-desks", "--id", "workflow")
    capsys.readouterr()
    assert json.loads((root / "desk" / "config.json").read_text())["project_identity"] == "workflow"

    assert main(["init", str(root), "--id", "other"]) == 0
    out = capsys.readouterr().out
    assert "repo whoami --set other" in out
    assert json.loads((root / "desk" / "config.json").read_text())["project_identity"] == "workflow"

    plain = _init_desk(tmp_path, monkeypatch, "plain-desk")
    assert json.loads((plain / "desk" / "config.json").read_text())["project_identity"] == "plain-desk"


def test_whoami_set_rewrites_only_project_identity(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config = tmp_path / "desk" / "config.json"
    config.parent.mkdir()
    config.write_text(json.dumps({"project_identity": "old", "versions": {"desk_format": 1}, "x": [1, 2]}, indent=2) + "\n", encoding="utf-8")
    before = config.read_text()

    assert main(["repo", "whoami", "--set", "new-id", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.strip() == "project_identity: old -> new-id"
    assert config.read_text() == before.replace('"old"', '"new-id"')


def test_whoami_set_rejects_non_slug(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_config(tmp_path, "old")
    before = (tmp_path / "desk" / "config.json").read_text()
    assert main(["repo", "whoami", "--set", "Bad_Id", "--root", str(tmp_path)]) == 1
    assert "slug" in capsys.readouterr().out
    assert (tmp_path / "desk" / "config.json").read_text() == before


def test_register_warns_when_id_differs_from_desk_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    root = _init_desk(tmp_path, monkeypatch, "wf-desks")
    capsys.readouterr()
    assert main(["repo", "register", "workflow", str(root), "--id", "workflow", "--store", str(root / ".sldb")]) == 0
    err = capsys.readouterr().err
    assert "project_identity wf-desks" in err
    assert f"deskops repo whoami --set workflow --root {root}" in err

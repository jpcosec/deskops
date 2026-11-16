"""`message send --to <repo>` resolves the target from the ecosystem registry.

MEPU (2026-11-15): `deskops message send --to deskops` did not resolve from another repo,
because only the sender's own ``desk/registry`` was read and MEPU's lists nobody. The
target is looked up first in the sender's registry and then in the ecosystem registry
(``~/setup/desk/registry``, or ``$DESKOPS_ECOSYSTEM_REGISTRY``). A registered root that does
not exist on this machine is an error and nothing is written.

The tests run the real CLI in subprocesses; ``HOME`` is the throwaway home of conftest, so
``~/setup`` is built inside it.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

from deskops.models import RepositoryDoc
from sldb.runtime.validation import render_model_markdown

ROOT = Path(__file__).resolve().parents[1]
# The CLI subprocess imports this checkout (and the sldb conftest put on sys.path), not
# whatever deskops the interpreter has installed.
_PYTHONPATH = os.pathsep.join([str(ROOT), *(p for p in sys.path if p)])


def _cli(cwd: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv],
        cwd=cwd,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": _PYTHONPATH, **(env or {})},
    )


def _init_repo(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    result = _cli(path, "init", str(path))
    assert result.returncode == 0, result.stderr or result.stdout
    return path


def _register(registry_dir: Path, repo_id: str, repo_path: str) -> None:
    registry_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": repo_id,
        "name": repo_id,
        "path": repo_path,
        "status": "active",
        "description": f"Repository for {repo_id}.",
        "tags": [],
    }
    (registry_dir / f"repo-{repo_id}.md").write_text(
        render_model_markdown(RepositoryDoc, payload) + "\n", encoding="utf-8"
    )


def _home() -> Path:
    return Path(os.environ["HOME"])


def _inbox(repo: Path) -> list[Path]:
    return sorted((repo / "desk" / "inbox").glob("*.md"))


def _send(sender: Path, to: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return _cli(
        sender, "message", "send", "Hola desde otro repo.", "--title", "Hola", "--to", to,
        "--format", "json", env=env,
    )


def test_send_to_repo_missing_from_sender_registry_uses_ecosystem_registry(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "mepu")
    target = _init_repo(_home() / "proyectos" / "SLDB_1" / "deskops")
    # The ecosystem registry names the target with a '~' path, valid on every machine.
    _register(_home() / "setup" / "desk" / "registry", "deskops", "~/proyectos/SLDB_1/deskops")
    assert not (sender / "desk" / "registry").exists() or not list((sender / "desk" / "registry").glob("repo-*.md"))

    result = _send(sender, "deskops")

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert Path(payload["path"]).parent == (target / "desk" / "inbox").resolve()
    assert len(_inbox(target)) == 1
    assert _inbox(sender) == []


def test_send_from_repo_without_store_uses_ecosystem_registry(tmp_path: Path) -> None:
    sender = tmp_path / "plain-repo"
    (sender / ".git").mkdir(parents=True)
    target = _init_repo(tmp_path / "sldb")
    registry = _home() / "setup" / "desk" / "registry"
    _register(registry, "sldb", str(target))
    # Neither store nor desk config: the ecosystem registry names the sender too.
    _register(registry, "plain-repo", str(sender))

    result = _send(sender, "sldb")

    assert result.returncode == 0, result.stderr or result.stdout
    assert json.loads(result.stdout)["sender_project"] == "plain-repo"
    assert len(_inbox(target)) == 1


def test_sender_registry_wins_over_ecosystem_registry(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender")
    local_target = _init_repo(tmp_path / "local-spec2viz")
    other_target = _init_repo(tmp_path / "other-spec2viz")
    _register(sender / "desk" / "registry", "spec2viz", str(local_target))
    _register(_home() / "setup" / "desk" / "registry", "spec2viz", str(other_target))

    result = _send(sender, "spec2viz")

    assert result.returncode == 0, result.stderr or result.stdout
    assert len(_inbox(local_target)) == 1
    assert _inbox(other_target) == []


def test_registry_dir_comes_from_environment(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender")
    target = _init_repo(tmp_path / "target")
    registry = tmp_path / "eco" / "desk" / "registry"
    # Relative paths resolve against the root of the repo that holds the registry.
    _register(registry, "target", "../target")

    result = _send(sender, "target", env={"DESKOPS_ECOSYSTEM_REGISTRY": str(registry)})

    assert result.returncode == 0, result.stderr or result.stdout
    assert len(_inbox(target)) == 1


def test_root_missing_on_this_machine_is_an_error_and_writes_nothing(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender")
    elsewhere = tmp_path / "other-machine" / "mepu"
    _register(_home() / "setup" / "desk" / "registry", "mepu", str(elsewhere))

    result = _send(sender, "mepu")

    assert result.returncode != 0
    assert "does not exist on this machine" in (result.stdout + result.stderr)
    assert not elsewhere.exists()
    assert _inbox(sender) == []


def test_unknown_repo_names_both_registries(tmp_path: Path) -> None:
    sender = _init_repo(tmp_path / "sender")
    _register(_home() / "setup" / "desk" / "registry", "sldb", str(tmp_path / "sldb"))

    result = _send(sender, "ghost")

    assert result.returncode != 0
    output = result.stdout + result.stderr
    assert "Repository id 'ghost' not found" in output
    assert "ecosystem registry" in output
    assert "sldb" in output

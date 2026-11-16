"""`deskops add|edit|list|show role` and `... runtime-profile`: RoleDoc and
RuntimeProfileDoc are written through the CLI, never by hand, and the documents
they produce are the ones `deskops runtime template` reads."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.cli.main import main
from deskops.materializers.runtime_profiles import load_runtime_profiles
from deskops.runtime.scion import find_role_doc, scion_template_files
from sldb.cli.main import main as sldb_main


def _desk(root: Path, *, store: bool) -> Path:
    root.mkdir(parents=True)
    assert main(["desk", "install", str(root)]) == 0
    if store:
        assert sldb_main(["stores", "init", "--path", str(root)]) == 0
        for model in ("RoleDoc", "RuntimeProfileDoc"):
            assert sldb_main(
                ["models", "add", f"deskops.models:{model}", "--store", str(root / ".sldb"), "--pythonpath", str(ROOT)]
            ) == 0
    return root


def _add_role_and_profile(root: Path) -> None:
    assert main(
        [
            "add", "role", "--root", str(root), "--name", "ir-executor", "--kind", "claude",
            "--description", "Executor for one IR task.", "--body", "# IR executor\n\n- Never use git add -A.",
        ]
    ) == 0
    assert main(
        [
            "add", "runtime-profile", "--root", str(root), "--title", "Claude on Scion", "--kind", "claude",
            "--binary", "claude", "--status", "active", "--tools-flag=--allowedTools",
        ]
    ) == 0


@pytest.mark.parametrize("store", [False, True], ids=["files", "store"])
def test_add_role_and_runtime_profile_feed_the_scion_template(tmp_path: Path, store: bool, capsys) -> None:
    root = _desk(tmp_path / "repo", store=store)
    _add_role_and_profile(root)

    role_path = root / "desk" / "roles" / "role-ir-executor.md"
    profile_path = root / "desk" / "runtimes" / "runtime-claude-on-scion.md"
    assert role_path.is_file() and profile_path.is_file()

    _, role_doc = find_role_doc(root, "ir-executor")
    assert role_doc["id"] == "role-ir-executor" and role_doc["kind"] == "claude"
    assert "Never use git add -A." in role_doc["body"]
    profile = load_runtime_profiles(root)["claude"]
    assert profile["id"] == "runtime-claude-on-scion" and profile["status"] == "active"

    files = scion_template_files(role_doc, profile, harness="claude", mode="executor")
    assert "Never use git add -A." in files["system-prompt.md"]

    capsys.readouterr()
    assert main(["edit", "role", "role-ir-executor", "description", "Executor for IR.", "--root", str(root)]) == 0
    assert main(["edit", "runtime-profile", "runtime-claude-on-scion", "notes", "OAuth.", "--root", str(root)]) == 0
    _, role_doc = find_role_doc(root, "ir-executor")
    assert role_doc["description"] == "Executor for IR."
    assert load_runtime_profiles(root)["claude"]["notes"] == "OAuth."

    capsys.readouterr()
    assert main(["list", "roles", "--root", str(root)]) == 0
    assert main(["list", "runtime-profiles", "--root", str(root)]) == 0
    listed = capsys.readouterr().out
    assert "role-ir-executor" in listed and "runtime-claude-on-scion" in listed


def test_free_named_role_files_stay_selectable(tmp_path: Path) -> None:
    """Roles seeded before `add role` existed are named after the role (deskops-executor.md)."""
    root = _desk(tmp_path / "repo", store=False)
    _add_role_and_profile(root)
    legacy = root / "desk" / "roles" / "ir-tester.md"
    legacy.write_text(
        (root / "desk" / "roles" / "role-ir-executor.md")
        .read_text(encoding="utf-8")
        .replace("id: role-ir-executor", "id: role-ir-tester")
        .replace("name: ir-executor", "name: ir-tester"),
        encoding="utf-8",
    )
    assert main(["edit", "role", "ir-tester", "description", "Tester for IR.", "--root", str(root)]) == 0
    _, role_doc = find_role_doc(root, "role-ir-tester")
    assert role_doc["description"] == "Tester for IR."

from pathlib import Path

import pytest

from deskops.config import DeskConfig
from deskops.constants import CURRENT_DESK_FORMAT

def test_load_desk_config_defaults(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    config = DeskConfig.load(desk)
    assert config.project_identity == "unknown-project"
    assert config.versions.desk_format == CURRENT_DESK_FORMAT
    assert not config.sandbox.enabled

def test_load_desk_config_from_json(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('''
    {
        "project_identity": "test-repo",
        "sandbox": {
            "enabled": true,
            "sandbox_root": "/tmp/test"
        }
    }
    ''')
    config = DeskConfig.load(desk)
    assert config.project_identity == "test-repo"
    assert config.sandbox.enabled is True
    assert config.sandbox.sandbox_root == "/tmp/test"

def test_load_desk_config_local_override(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('''
    {
        "project_identity": "test-repo",
        "sandbox": {
            "enabled": false,
            "sandbox_root": "/tmp/test"
        }
    }
    ''')
    (desk / "config.local.json").write_text('''
    {
        "sandbox": {
            "enabled": true
        }
    }
    ''')
    config = DeskConfig.load(desk)
    assert config.project_identity == "test-repo"
    assert config.sandbox.enabled is True
    assert config.sandbox.sandbox_root == "/tmp/test"


def test_load_desk_config_deep_merges_nested_versions(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('''
    {
        "versions": {
            "desk_format": "1.0.0",
            "model_version": "1.0.0"
        }
    }
    ''')
    (desk / "config.local.json").write_text('''
    {
        "versions": {
            "model_version": "2.0.0"
        }
    }
    ''')

    config = DeskConfig.load(desk)

    assert config.versions.desk_format == CURRENT_DESK_FORMAT
    assert config.versions.model_version == "2.0.0"


def test_load_desk_config_surfaces_malformed_json_warning(tmp_path: Path):
    desk = tmp_path / "desk"
    desk.mkdir()
    (desk / "config.json").write_text('{"sandbox": {"enabled": true}')

    with pytest.warns(UserWarning, match="Failed to parse desk config"):
        config = DeskConfig.load(desk)

    assert config.has_load_warnings is True
    assert config.load_warnings
    assert config.sandbox.enabled is False


def test_load_takes_identity_from_config_local_json(tmp_path: Path) -> None:
    (tmp_path / "config.json").write_text('{"project_identity": "x"}', encoding="utf-8")
    (tmp_path / "config.local.json").write_text(
        '{"identity": {"scion_project": "p", "agent": "a", "wake": true}}', encoding="utf-8"
    )

    config = DeskConfig.load(tmp_path)

    assert config.identity is not None
    assert (config.identity.scion_project, config.identity.agent, config.identity.wake) == ("p", "a", True)
    assert config.identity.command[:3] == ["scion", "message", "--wake"]


def test_unowned_target_comes_from_config_local_json(tmp_path: Path) -> None:
    assert DeskConfig.load(tmp_path).unowned_target is None
    (tmp_path / "config.local.json").write_text('{"unowned_target": "governance"}', encoding="utf-8")

    assert DeskConfig.load(tmp_path).unowned_target == "governance"

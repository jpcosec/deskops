import subprocess
from pathlib import Path

from deskops.cli.main import CLI

LINES = [
    ".sldb/core/store_index.yaml merge=sldb",
    ".sldb/core/models/*.yaml merge=sldb",
    ".sldb/store.yaml merge=sldb",
]


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)


def _config(root: Path) -> str:
    return _git(root, "config", "--local", "--get", "merge.sldb.driver").stdout.strip()


def test_init_installs_the_merge_driver_in_a_git_desk(tmp_path: Path) -> None:
    assert _git(tmp_path, "init", "-q").returncode == 0
    assert CLI().run(["init", str(tmp_path)]) == 0
    attrs = (tmp_path / ".gitattributes").read_text().splitlines()
    assert all(line in attrs for line in LINES)
    assert _config(tmp_path)


def test_init_outside_git_writes_nothing(tmp_path: Path) -> None:
    assert CLI().run(["init", str(tmp_path)]) == 0
    assert not (tmp_path / ".gitattributes").exists()


def test_desk_update_apply_installs_a_missing_driver_and_is_idempotent(tmp_path: Path, capsys) -> None:
    assert _git(tmp_path, "init", "-q").returncode == 0
    assert CLI().run(["init", str(tmp_path)]) == 0
    (tmp_path / ".gitattributes").unlink()
    _git(tmp_path, "config", "--local", "--unset", "merge.sldb.driver")
    assert not _config(tmp_path)
    capsys.readouterr()
    CLI().run(["desk", "update", "--root", str(tmp_path), "--apply"])
    attrs = (tmp_path / ".gitattributes").read_text().splitlines()
    assert all(line in attrs for line in LINES)
    assert _config(tmp_path)
    before = (tmp_path / ".gitattributes").read_text()
    CLI().run(["desk", "update", "--root", str(tmp_path), "--apply"])
    assert (tmp_path / ".gitattributes").read_text() == before

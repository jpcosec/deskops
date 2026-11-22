"""Detect the pre-c420809c `.sldb` layout (runtime/ and journal inside `.sldb/`) and name its remedy."""

from __future__ import annotations

from pathlib import Path

_IGNORED_OLD = {".sldb/core", ".sldb/runtime"}


def _ignore_pattern(line: str) -> str:
    return line.strip().lstrip("/").rstrip("/")


def old_layout_signals(repo_root: Path) -> list[str]:
    """The old-layout signals present in `repo_root`; empty when there is no `.sldb/` or it is migrated."""
    store = repo_root / ".sldb"
    signals: list[str] = []
    if store.is_dir():
        if (store / "runtime").exists():
            signals.append(".sldb/runtime/ exists")
        if (store / "journal").exists():
            signals.append(".sldb/journal exists")
    gitignore = repo_root / ".gitignore"
    if gitignore.is_file():
        try:
            lines = gitignore.read_text(encoding="utf-8").splitlines()
        except OSError:
            lines = []
        for line in lines:
            if line.strip().startswith("#") or line.strip().startswith("!"):
                continue
            if _ignore_pattern(line) in _IGNORED_OLD:
                signals.append(f".gitignore ignores {_ignore_pattern(line)}")
    return signals


def remedy(repo_root: Path) -> str:
    return f"sldb stores migrate-layout --store {repo_root / '.sldb'}"


def old_layout_message(repo_root: Path) -> str | None:
    signals = old_layout_signals(repo_root)
    if not signals:
        return None
    return f"Old .sldb layout ({'; '.join(signals)}). Migrate with: {remedy(repo_root)}"

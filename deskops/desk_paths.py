"""Selector resolution on disk, for the desk surfaces the store does not track.

Tracked documents resolve through ``sldb.api.select_documents``
(``deskops.doc_access.resolve_document``). What the store does not track (the drawer,
``desk/issues``, a desk without a store) keeps this rule: exact name or stem first, then a
unique prefix; anything else is an error. Both paths word their errors with
``relative_candidates`` and ``not_found_message`` so the messages are the same.

A selector that is a path (it contains ``/``), relative to the repository root or
absolute, names the file whose stem it ends in when it lands inside ``desk/``
(``selector_stem``); one that lands outside is an error.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path


ACCEPTED_SELECTOR_FORMS = "an exact id, a file name, a stem, a unique fragment, or a desk/... path"


def not_found_message(what: str, selector: str) -> str:
    """The error for a selector that names nothing, listing the forms a selector may take."""
    return f"No {what} file found for selector '{selector}'. Accepted forms: {ACCEPTED_SELECTOR_FORMS}."


def selector_stem(desk_root: Path, selector: str) -> str:
    """The selector a path selector stands for: its file stem, when it lands inside ``desk/``.

    A selector without ``/`` is returned as is. A path is resolved against the
    repository root (the parent of ``desk_root``) unless it is absolute; ``..`` is
    resolved too. A path outside ``desk/`` raises ``ValueError``.
    """
    if "/" not in selector:
        return selector
    candidate = Path(selector)
    if not candidate.is_absolute():
        candidate = desk_root.parent / candidate
    resolved = candidate.resolve()
    desk = desk_root.resolve()
    if resolved == desk or not resolved.is_relative_to(desk):
        raise ValueError(f"el selector apunta fuera de desk/: '{selector}'")
    return resolved.stem


def relative_candidates(desk_root: Path, paths: list[Path]) -> str:
    relative = []
    for path in paths:
        try:
            relative.append(str(path.relative_to(desk_root)))
        except ValueError:
            relative.append(str(path))
    return ", ".join(sorted(relative))


# CC35b-a3: untracked surface, resolved on disk
def resolve_selector(
    desk_root: Path,
    directories: list[Path],
    selector: str,
    pattern: str,
    what: str,
    recursive: bool,
    keep: Callable[[Path], bool] | None = None,
) -> Path:
    """Resolve `selector` against `pattern` inside `directories`.

    Tier 1 accepts a file whose name or stem equals the selector. Tier 2
    accepts a unique file whose name or stem starts with it. Zero matches raise
    FileNotFoundError; more than one raise ValueError. `keep`, when given,
    drops candidates before either tier runs. A path selector resolves as its stem
    (``selector_stem``); messages quote the selector as given.
    """
    if not selector or not str(selector).strip():
        raise ValueError(f"Empty or whitespace-only selector provided for {what}")
    given, selector = selector, selector_stem(desk_root, selector)

    candidates: list[Path] = []
    for directory in directories:
        if not directory.exists():
            continue
        matches = directory.rglob(pattern) if recursive else directory.glob(pattern)
        candidates.extend(sorted(matches))
    candidates = sorted(dict.fromkeys(candidates))
    if keep is not None:
        candidates = [path for path in candidates if keep(path)]

    exact = [path for path in candidates if selector in {path.name, path.stem}]
    if len(exact) == 1:
        return exact[0]
    if exact:
        raise ValueError(f"Ambiguous {what} selector '{given}': {relative_candidates(desk_root, exact)}")

    prefix = [path for path in candidates if path.name.startswith(selector) or path.stem.startswith(selector)]
    if not prefix:
        raise FileNotFoundError(not_found_message(what, given))
    if len(prefix) > 1:
        raise ValueError(f"Ambiguous {what} selector '{given}': {relative_candidates(desk_root, prefix)}")
    return prefix[0]

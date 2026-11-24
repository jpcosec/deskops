"""Rewrite the ``tags`` of the desk's documents to the one vocabulary (deskops.tag_vocabulary).

``deskops tags migrate`` lists, per document, the tags the model already says (flat copies of its
``__semantics__``), repeats and class names; ``--apply`` writes the documents again through their
models in one desk transaction. Nothing here decides a hierarchy: that is sldb's semantic store.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import re

import yaml
from sldb.api import select_documents

from deskops import doc_access
from deskops.tag_vocabulary import canonical_tags


_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---", re.S)


@dataclass(frozen=True)
class TagChange:
    model: str
    path: str
    before: tuple[str, ...]
    after: tuple[str, ...]

    @property
    def dropped(self) -> list[str]:
        remaining = list(self.after)
        dropped = []
        for tag in self.before:
            if tag in remaining:
                remaining.remove(tag)
            else:
                dropped.append(tag)
        return dropped


def _written_tags(path: Path) -> list[str]:
    """The ``tags`` the file's frontmatter carries, as written (reading through the model already
    drops what the vocabulary refuses)."""
    match = _FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if match is None:
        return []
    data = yaml.safe_load(match.group(1)) or {}
    tags = data.get("tags") if isinstance(data, dict) else None
    return [tag for tag in tags if isinstance(tag, str)] if isinstance(tags, list) else []


def plan_tag_migration(root: Path) -> list[TagChange]:
    """The documents whose tags change under the one vocabulary, in store order."""
    import deskops.models as models

    store = doc_access.store_path(root)
    changes: list[TagChange] = []
    for row in select_documents(store, {}):
        model = getattr(models, row["model"], None)
        path = root / row["path"]
        if model is None or path.suffix != ".md" or "tags" not in getattr(model, "model_fields", {}):
            continue
        before = tuple(_written_tags(path))
        after = tuple(canonical_tags(before, model))
        if after != before:
            changes.append(TagChange(row["model"], row["path"], before, after))
    return changes


def apply_tag_migration(root: Path, changes: list[TagChange]) -> int:
    import deskops.models as models

    with doc_access.desk_transaction(root):
        for change in changes:
            model = getattr(models, change.model)
            path = root / change.path
            payload: dict[str, Any] = doc_access.read_doc(path, model)
            payload["tags"] = list(change.after)
            doc_access.write_doc(root, path, model, payload)
    return len(changes)


def summarize(changes: list[TagChange]) -> Counter:
    counts: Counter = Counter()
    for change in changes:
        counts.update(change.dropped)
    return counts

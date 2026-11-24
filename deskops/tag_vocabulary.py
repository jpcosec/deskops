"""One vocabulary of semantic tags for the documents deskops writes.

The semantic store of sldb already knows what a model is: ``__semantics__`` gives every
document of a model its dotted tags (``type.workflow.task``, ``workspace.desk``,
``board.tareas``), and the DAG derives the parents from the dots. Writing the same fact again
in the frontmatter as a flat ``namespace:value`` tag (``workspace:desk``, ``artifact:task``)
only makes a second, parentless vocabulary. This module is the only place deskops decides
what a document's ``tags`` field must not carry:

* a repeat of a tag already in the list;
* the name of a model class (``TaskDoc``, ``PrimitiveDoc``): the class is the model, not a tag;
* a flat tag that restates one of the model's own tags (``workspace:desk`` on a document whose
  model says ``workspace.desk``; ``artifact:task`` on one that says ``type.workflow.task``).

It resolves nothing about hierarchy: parents, children and queries by a tag with its
descendants are sldb's (``sldb semantic show``, ``sldb find <tag> --in semantic``).
"""

from __future__ import annotations

import re
from typing import Iterable

from sldb.store.semantic_tags import flatten_model_semantics

_CLASS_NAME = re.compile(r"^[A-Z][A-Za-z0-9]*Doc$")


def is_class_name(tag: str) -> bool:
    """Whether the tag is the name of a model class (``TaskDoc``)."""
    return bool(_CLASS_NAME.match(tag))


def _norm(value: str) -> str:
    return value.replace("-", "_")


def restates_model_tag(tag: str, model_tags: Iterable[str]) -> bool:
    """Whether the flat ``ns:value`` tag says what one of the model's dotted tags already says."""
    namespace, colon, value = tag.partition(":")
    if not colon or not namespace or not value:
        return False
    model_tags = list(model_tags)
    if namespace == "artifact":
        return any(t.startswith("type.") and _norm(t.rsplit(".", 1)[-1]) == _norm(value) for t in model_tags)
    if namespace in ("workspace", "layer", "type"):
        dotted = f"{namespace}.{value}"
        return any(t == dotted or t.startswith(dotted + ".") for t in model_tags)
    return False


def canonical_tags(tags: Iterable[str], model: type | None) -> list[str]:
    """``tags`` without repeats, class names or restatements of the model's own tags, in order."""
    model_tags = flatten_model_semantics(model) if model is not None else []
    kept: list[str] = []
    for tag in tags:
        if not isinstance(tag, str):
            kept.append(tag)
            continue
        if tag in kept or is_class_name(tag) or restates_model_tag(tag, model_tags):
            continue
        kept.append(tag)
    return kept

"""``pointers``: where something applies, as addresses sldb already resolves.

One field, the same in AtomDoc, PillDoc and TaskDoc: a list of strings with a class prefix.
deskops only keeps and checks the shape; resolving a pointer is sldb's job.

- ``doc:<Model>:<id>``: a store document, sldb's export id ``Model:name`` (selectors.md).
- ``tag:<namespace>:<value>``: a category, a complete namespaced tag (tags.md).
- ``code:<path>::<qualified_name>``: a code anchor, sldb's ``code:…::…`` reference
  (code-anchoring.md); the whole module is ``code:<path>::`` (empty name). sldb refuses a
  code reference without ``::``, so this one does too.
"""
from __future__ import annotations

import re

POINTER_CLASSES = ("doc", "tag", "code")

_DOC = re.compile(r"^[A-Za-z][A-Za-z0-9_]*:[^\s:][^\s]*$")
_TAG = re.compile(r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$")
_CODE = re.compile(r"^[^\s:][^\s:]*(?::[^\s:]+)*::([A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*)?$")

_EXPECTED = {
    "doc": "doc:<Model>:<id>",
    "tag": "tag:<namespace>:<value>",
    "code": "code:<path>::<qualified_name> (or code:<path>:: for the whole module)",
}
_SHAPE = {"doc": _DOC, "tag": _TAG, "code": _CODE}


def check_pointer(pointer: str) -> str:
    cls, sep, rest = pointer.partition(":")
    if not sep or cls not in _SHAPE:
        raise ValueError(
            f"Invalid pointer '{pointer}': expected a class prefix, one of "
            + ", ".join(_EXPECTED.values())
            + "."
        )
    if _SHAPE[cls].fullmatch(rest) is None:
        raise ValueError(f"Invalid {cls} pointer '{pointer}': expected {_EXPECTED[cls]}.")
    return pointer


def check_pointers(value: object) -> object:
    """``None`` is an absent key (a document written before the field); anything that is not a
    list of strings is left to pydantic."""
    if value is None:
        return []
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                check_pointer(item)
    return value

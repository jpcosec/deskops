"""Create an ``atom.adr`` and keep what it replaces consistent (``deskops/models/adr.py``).

One ``desk_transaction`` writes the ADR, flips each fully replaced ADR to ``superseded`` and
records the ``supersedes`` ``RelationDoc`` (a partial replacement carries the replaced
``section`` as its attribute and leaves the earlier ADR ``accepted``). The consistency itself
is checked by the ``rule-adr-supersedes`` RuleDoc, not here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops import doc_access
from deskops.doc_access import DocumentRecord
from deskops.models.adr import AtomAdrDoc

SUPERSEDES = "supersedes"
SUPERSESSIONS_DIR = Path("desk") / "supersessions"
SUPERSEDES_TYPE_NAME = "type-supersedes"


def _adr_path(root: Path, adr_id: str) -> Path:
    path = doc_access.resolve_artifact_selector(root, "artifact.atom", doc_access.desk_root(root) / "atoms", adr_id)
    if doc_access.read_doc(path, AtomAdrDoc).get("atom_type") != "atom.adr":
        raise ValueError(f"{adr_id} is not an atom.adr and cannot be superseded.")
    return path


def create_adr(root: Path, raw_payload: dict[str, Any]) -> DocumentRecord:
    """Create the ADR; with ``supersedes`` / ``partial_supersedes`` also update the earlier ones."""
    full = [str(item) for item in raw_payload.get("supersedes") or []]
    partial = [str(item) for item in raw_payload.get("partial_supersedes") or []]
    if partial and not str(raw_payload.get("superseded_section") or "").strip():
        raise ValueError("partial_supersedes needs superseded_section: the section of the earlier ADR it replaces.")
    if raw_payload.get("superseded_section") and not partial:
        raise ValueError("superseded_section only goes with partial_supersedes.")
    previous = {adr_id: _adr_path(root, adr_id) for adr_id in [*full, *partial]}
    with doc_access.desk_transaction(root):
        record = doc_access.create_artifact(root, "artifact.atom", raw_payload)
        for adr_id in full:
            path = previous[adr_id]
            payload = doc_access.read_doc(path, AtomAdrDoc)
            payload["status"] = "superseded"
            doc_access.write_doc(root, path, AtomAdrDoc, payload)
        for adr_id in [*full, *partial]:
            _record_relation(root, record.doc_id, adr_id, None if adr_id in full else str(raw_payload["superseded_section"]))
    return record


def _record_relation(root: Path, new_id: str, old_id: str, section: str | None) -> None:
    if not doc_access.has_store(root):
        return
    from sldb.api import edge_node
    from sldb.api import relation_type_node_id
    from sldb.models.relation_doc import RelationDoc
    from sldb.models.relation_type_doc import RelationTypeDoc

    directory = root / SUPERSESSIONS_DIR
    directory.mkdir(parents=True, exist_ok=True)
    if edge_node(doc_access.store_path(root), relation_type_node_id(SUPERSEDES), include_linked=False) is None:
        doc_access.create_doc(
            root,
            directory / f"{SUPERSEDES_TYPE_NAME}.md",
            RelationTypeDoc,
            {
                "title": "Supersedes",
                "name": SUPERSEDES,
                "direction": "directed",
                "cardinality": "many_to_many",
                "axis": "PROVENANCE",
                "source_types": ["AtomAdrDoc"],
                "target_types": ["AtomAdrDoc"],
                "condition": "",
                "description": (
                    "An accepted ADR replaces an earlier one. Attribute 'section' (optional): the earlier ADR "
                    "is replaced only in that section and stays accepted. Written by `deskops add atom --atom-type atom.adr`."
                ),
            },
            SUPERSEDES_TYPE_NAME,
        )
    name = f"supersedes-{new_id}-{old_id}"
    doc_access.create_doc(
        root,
        directory / f"{name}.md",
        RelationDoc,
        {
            "title": f"{new_id} supersedes {old_id}",
            "source_id": f"AtomAdrDoc:{new_id}",
            "target_id": f"AtomAdrDoc:{old_id}",
            "relation_type": SUPERSEDES,
            "condition": "",
            "attributes": {"section": section} if section else {},
            "notes": "",
        },
        name,
    )

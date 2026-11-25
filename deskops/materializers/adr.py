"""Materialize an ``atom.adr`` as a Markdown document: the atom is the source, the Markdown a projection."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops import doc_access
from deskops.models.adr import AtomAdrDoc


def render_adr_markdown(payload: dict[str, Any]) -> str:
    """Status, Date, Decision Maker, Supersedes, Context, Decision, Consequences (and Alternatives / Applies to when present)."""
    supersedes = [f"`{item}`" for item in payload.get("supersedes") or []]
    section = str(payload.get("superseded_section") or "").strip()
    supersedes += [f"`{item}` (section: {section})" for item in payload.get("partial_supersedes") or []]
    lines = [
        f"# {payload['title']}",
        "",
        f"- Status: {payload.get('status', 'accepted')}",
        f"- Date: {payload['decided_on']}",
        f"- Decision Maker: {payload['decided_by']}",
        f"- Supersedes: {', '.join(supersedes) if supersedes else 'none'}",
        f"- Atom: `{payload['id']}`",
        "",
        "## Context",
        "",
        str(payload["context"]).strip(),
        "",
        "## Decision",
        "",
        str(payload["answer"]).strip(),
        "",
        "## Consequences",
        "",
        str(payload["consequences"]).strip(),
    ]
    if str(payload.get("alternatives") or "").strip():
        lines += ["", "## Alternatives", "", str(payload["alternatives"]).strip()]
    if payload.get("references"):
        lines += ["", "## Applies to", ""] + [f"- {item}" for item in payload["references"]]
    return "\n".join(lines) + "\n"


def materialize_adr(root: Path, selector: str, out: Path | None = None) -> tuple[Path, Path]:
    """Write the ADR ``selector`` names to ``out`` (default ``docs/decisions/<id>.md``); returns (source, output)."""
    path = doc_access.resolve_artifact_selector(root, "artifact.atom", doc_access.desk_root(root) / "atoms", selector)
    payload = doc_access.read_doc(path, AtomAdrDoc)
    if payload.get("atom_type") != "atom.adr":
        raise ValueError(f"{payload['id']} is not an atom.adr.")
    target = out or root / "docs" / "decisions" / f"{payload['id'].removeprefix('atom-')}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_adr_markdown(payload), encoding="utf-8")
    return path, target

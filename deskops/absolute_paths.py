"""Absolute paths in the documents of a desk, and how to say them so any machine resolves them.

A desk written on one machine keeps ``/home/jp/proyectos/SLDB_1/sldb`` in the ``path`` of its
registry and in the ``files`` and ``references`` of its tasks. On another machine that path does
not exist. The store already knows where the neighbouring repositories are: ``.sldb/store.yaml``
declares ``links`` (``name: sldb``, ``path: ../sldb/.sldb``), read here through sldb's own
``load_declaration`` (and ``store_links`` when the declaration cannot be read). The root of a
neighbour is the parent of its linked ``.sldb``.

Rules (task-doctor-detecta-rutas-absolutas):

* a path under this repository's root becomes relative to it, with no prefix;
* a path that exists here and falls under the root of a neighbour (a link, or a registry entry
  whose path is relative) becomes ``../sldb`` in the registry and ``<repo-id>:<path>`` in
  ``files`` and ``references`` (the form ``closeout resolved-by`` accepts);
* a path that does not exist (another machine) is rewritten only when what follows the folder of
  the ecosystem (``SLDB_1``) names one neighbour without ambiguity;
* anything else stays an alert with its reason.

``doctor`` reports; ``doctor --repair`` writes through the desk's sldb transaction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path, PurePosixPath
import re
from typing import Any

import yaml

from deskops.doc_access import desk_transaction, read_doc, write_doc

#: Frontmatter keys that are not content of the document.
_SKIPPED_KEYS = frozenset({"sldb"})
_PREFILTER = re.compile(r"""(?m)[:\-]\s+['"]?/[^\s/'"]""")
_REPAIRABLE = ("files", "references")


@dataclass(frozen=True)
class AbsoluteRef:
    """One absolute path found in the frontmatter of a desk document."""

    doc: str  # path relative to the repository root
    field: str  # dotted key path, with ``[i]`` for list items
    value: str
    key: str  # top-level frontmatter key
    index: int | None  # position in a top-level list, else None


@dataclass(frozen=True)
class Resolution:
    new_value: str | None
    reason: str = ""


@dataclass
class Neighbours:
    """Where the repositories next to this one are, by root."""

    root: Path
    roots: dict[Path, str] = field(default_factory=dict)  # neighbour root -> link name
    ids: dict[Path, list[str]] = field(default_factory=dict)  # root -> registry ids
    own_ids: set[str] = field(default_factory=set)

    @property
    def ecosystem(self) -> str:
        return self.root.parent.name

    def relative_parts(self, root: Path) -> tuple[str, ...]:
        try:
            return root.relative_to(self.root.parent).parts
        except ValueError:
            return ()


def looks_absolute(value: str) -> bool:
    text = value.strip()
    if not text.startswith("/") or text.startswith("//") or re.search(r"\s", text) or len(text) < 2:
        return False
    return "/" in text[1:] or Path(text).exists()


def _walk(value: Any, key_path: str, top: str, index: int | None, out: list[tuple[str, str, str, int | None]]) -> None:
    if isinstance(value, str):
        if looks_absolute(value):
            out.append((key_path, value.strip(), top, index))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            _walk(item, f"{key_path}[{i}]", top, i if key_path == top else None, out)
    elif isinstance(value, dict):
        for k, item in value.items():
            _walk(item, f"{key_path}.{k}", top, None, out)


def scan_document(rel: str, text: str) -> list[AbsoluteRef]:
    """The absolute paths in the frontmatter of one document."""
    if not text.startswith("---"):
        return []
    parts = text.split("---", 2)
    if len(parts) < 3 or not _PREFILTER.search(parts[1]):
        return []
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return []
    if not isinstance(data, dict):
        return []
    found: list[tuple[str, str, str, int | None]] = []
    for key, value in data.items():
        if key not in _SKIPPED_KEYS:
            _walk(value, str(key), str(key), None, found)
    return [AbsoluteRef(rel, fld, value, top, idx) for fld, value, top, idx in found]


def scan_desk(root: Path) -> list[AbsoluteRef]:
    desk = root / "desk"
    refs: list[AbsoluteRef] = []
    if not desk.is_dir():
        return refs
    for path in sorted(desk.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        refs += scan_document(path.relative_to(root).as_posix(), text)
    return refs


def _linked_roots(root: Path) -> dict[Path, str]:
    """Neighbour roots by the links the store declares (``sldb.api``, not the YAML by hand)."""
    store = root / ".sldb"
    found: dict[Path, str] = {}
    if not store.is_dir():
        return found
    try:
        from sldb.api.stores.store_declaration import load_declaration

        entries = [(link["name"], (root / link["path"]).resolve()) for link in load_declaration(store).links]
    except Exception:
        try:
            from sldb.api import store_links

            entries = [(link["name"], Path(link["resolved"])) for link in store_links(store)]
        except Exception:
            return found
    for name, linked in entries:
        found.setdefault(linked.parent if linked.name == ".sldb" else linked, name)
    return found


def _registry(root: Path) -> list[tuple[str, Path, str | None]]:
    """(id, path of the registry document, its ``path`` field) per registered repository."""
    out = []
    for doc in sorted((root / "desk" / "registry").glob("repo-*.md")):
        try:
            from deskops.models import RepositoryDoc

            payload = read_doc(doc, RepositoryDoc)
        except Exception:
            continue
        out.append((str(payload.get("id") or doc.stem.removeprefix("repo-")), doc, payload.get("path")))
    return out


def build_neighbours(root: Path, planned: dict[str, str] | None = None) -> Neighbours:
    """Neighbours from the store links and the registry; ``planned`` maps a registry document
    (relative path) to the value its ``path`` will have, so ids resolve against the rewrite."""
    root = root.resolve()
    near = Neighbours(root=root, roots=_linked_roots(root))
    for repo_id, doc, repo_path in _registry(root):
        rel = doc.relative_to(root).as_posix()
        value = (planned or {}).get(rel, repo_path)
        if not value or value == ".":
            near.own_ids.add(repo_id)
            continue
        if Path(value).is_absolute():
            target = Path(value).resolve()
        else:
            target = (root / value).resolve()
        if target == root:
            near.own_ids.add(repo_id)
            continue
        if not Path(value).is_absolute():
            near.roots.setdefault(target, repo_id)
        near.ids.setdefault(target, []).append(repo_id)
    return near


def _under(path: Path, base: Path) -> PurePosixPath | None:
    try:
        return PurePosixPath(path.relative_to(base).as_posix())
    except ValueError:
        return None


def _locate(near: Neighbours, value: str) -> tuple[Path | None, PurePosixPath, str]:
    """(repository root, path inside it, reason when it cannot be decided)."""
    path = Path(value)
    candidates = [near.root, *near.roots]
    if path.exists() or any(_under(path.resolve(), c) is not None for c in candidates):
        resolved = path.resolve()
        hits = [(c, rest) for c in candidates if (rest := _under(resolved, c)) is not None]
        if not hits:
            return None, PurePosixPath("."), "the path exists here but is under no repository of this desk's links or registry"
        base, rest = max(hits, key=lambda hit: len(hit[0].parts))
        return base, rest, ""
    # Another machine: what follows the folder of the ecosystem names a neighbour.
    parts = path.parts[1:]
    marks = [i for i, part in enumerate(parts) if part == near.ecosystem]
    if not marks:
        return None, PurePosixPath("."), f"the path does not exist here and has no '{near.ecosystem}' folder to place it by"
    found: dict[Path, PurePosixPath] = {}
    for i in marks:
        suffix = parts[i + 1 :]
        best: tuple[Path, int] | None = None
        for base in candidates:
            rel = near.relative_parts(base)
            if rel and tuple(suffix[: len(rel)]) == rel and (best is None or len(rel) > best[1]):
                best = (base, len(rel))
        if best is not None:
            found[best[0]] = PurePosixPath(*suffix[best[1] :]) if suffix[best[1] :] else PurePosixPath(".")
    if not found:
        tail = "/".join(parts[marks[-1] + 1 :]) or "(nothing)"
        return None, PurePosixPath("."), f"what follows '{near.ecosystem}' ({tail}) names no repository of this desk's links or registry"
    if len(found) > 1:
        names = ", ".join(sorted(near.roots.get(b, b.name) for b in found))
        return None, PurePosixPath("."), f"ambiguous: '{near.ecosystem}' appears more than once and places the path in {names}"
    ((base, rest),) = found.items()
    return base, rest, ""


def resolve(near: Neighbours, ref: AbsoluteRef) -> Resolution:
    """The value to write for ``ref``, or why it cannot be rewritten."""
    is_registry_path = ref.doc.startswith("desk/registry/repo-") and ref.field == "path"
    if not is_registry_path and ref.key not in _REPAIRABLE:
        return Resolution(None, f"field '{ref.key}' is not one doctor rewrites (only registry path, files and references)")
    base, rest, reason = _locate(near, ref.value)
    if base is None:
        return Resolution(None, reason)
    if is_registry_path:
        target = base / rest.as_posix()
        return Resolution(os.path.relpath(target, near.root).replace(os.sep, "/") or ".")
    if base == near.root:
        return Resolution(rest.as_posix())
    ids = near.ids.get(base, [])
    if not ids:
        return Resolution(None, f"no repository of the registry has its root at {base.name}; register it with deskops repo register")
    if len(ids) > 1:
        return Resolution(None, f"ambiguous: registry ids {', '.join(sorted(ids))} share one root")
    if rest.as_posix() == ".":
        return Resolution(None, "the path is the repository root itself, which a <repo-id>:<path> reference cannot name")
    return Resolution(f"{ids[0]}:{rest.as_posix()}")


@dataclass
class PathReport:
    pending: list[tuple[AbsoluteRef, Resolution]] = field(default_factory=list)
    alerts: list[str] = field(default_factory=list)
    fixed: list[str] = field(default_factory=list)


def _line(ref: AbsoluteRef, resolution: Resolution, *, repair: bool) -> str:
    where = f"{ref.doc} {ref.field}: {ref.value}"
    if resolution.new_value is None:
        return f"Absolute path: {where} (not rewritten: {resolution.reason})"
    return f"Absolute path: {where} (becomes {resolution.new_value}; fix: deskops doctor --repair)"


def check(root: Path, *, repair: bool) -> PathReport:
    """Report every absolute path of the desk; with ``repair`` rewrite those that resolve."""
    root = root.resolve()
    refs = scan_desk(root)
    report = PathReport()
    if not refs:
        return report
    # Registry paths first: the ids of the files and references resolve against their rewrite.
    registry = [r for r in refs if r.doc.startswith("desk/registry/repo-") and r.field == "path"]
    near = build_neighbours(root)
    planned = {r.doc: res.new_value for r in registry if (res := resolve(near, r)).new_value is not None}
    near = build_neighbours(root, planned)
    results = [(ref, resolve(near, ref)) for ref in refs]
    if repair:
        done = _apply(root, [(ref, res) for ref, res in results if res.new_value is not None], report)
    else:
        done = set()
    for ref, res in results:
        if ref in done:
            continue
        report.alerts.append(_line(ref, res, repair=repair))
    return report


def _apply(root: Path, items: list[tuple[AbsoluteRef, Resolution]], report: PathReport) -> set[AbsoluteRef]:
    """Rewrite per document through the desk's sldb transaction; one failure restores all."""
    from deskops.models import RepositoryDoc, TaskDoc

    by_doc: dict[str, list[tuple[AbsoluteRef, Resolution]]] = {}
    for ref, res in items:
        by_doc.setdefault(ref.doc, []).append((ref, res))
    done: set[AbsoluteRef] = set()
    with desk_transaction(root):
        for rel, group in sorted(by_doc.items()):
            path = root / rel
            model = RepositoryDoc if rel.startswith("desk/registry/repo-") else TaskDoc
            try:
                payload = read_doc(path, model)
            except Exception:
                continue
            applied = []
            for ref, res in group:
                if ref.index is None:
                    if payload.get(ref.key) == ref.value:
                        payload[ref.key] = res.new_value
                        applied.append((ref, res))
                else:
                    values = payload.get(ref.key)
                    if isinstance(values, list) and ref.index < len(values) and values[ref.index] == ref.value:
                        values[ref.index] = res.new_value
                        applied.append((ref, res))
            if not applied:
                continue
            write_doc(root, path, model, payload)
            for ref, res in applied:
                done.add(ref)
                report.fixed.append(f"Absolute path rewritten: {ref.doc} {ref.field}: {ref.value} -> {res.new_value}")
    return done

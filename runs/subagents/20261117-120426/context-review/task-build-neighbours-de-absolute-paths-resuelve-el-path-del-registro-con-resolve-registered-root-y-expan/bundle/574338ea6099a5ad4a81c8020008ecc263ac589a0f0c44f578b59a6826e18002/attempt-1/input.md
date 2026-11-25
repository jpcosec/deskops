FILE:desk/tasks/task-build-neighbours-de-absolute-paths-resuelve-el-path-del-registro-con-resolve-registered-root-y-expan.md
---
sldb:
  by: agent
  at: '2026-11-17T11:58:21Z'
  authority: generated
  via: create_document
id: task-build-neighbours-de-absolute-paths-resuelve-el-path-del-registro-con-resolve-registered-root-y-expan
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- runs/subagents/test-deskops-t-a8ebbb84ed77/verdict.md
depends_on: []
pills: []
files:
- deskops/absolute_paths.py
- tests/test_doctor_absolute_paths.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-repo-register-accepts-explicit-path-and-registry-errors-name-the-fix
---

# build_neighbours de absolute_paths resuelve el path del registro con resolve_registered_root y expande la virgulilla

## Rationale

_Explain why this task exists or the business driver behind it._

Seguimiento del cierre de repo register (24a50d44, closeout 38f92120): ahora doc_access.repository_root resuelve las entradas del registro con deskops.identity.resolve_registered_root, que expande la virgulilla y resuelve rutas relativas contra la raiz del repo del registro. build_neighbours en deskops/absolute_paths.py (fuera de los files de esa tarea) todavia resuelve el path a mano sin expandir la virgulilla, asi que una entrada vieja escrita a mano con la virgulilla da un vecino mal resuelto y doctor la reporta dos veces (por absolute_paths y por el chequeo de registro), como pasa con Chatbot_Infra.

## Goal

_Describe the concrete result this task must produce._

build_neighbours resuelve cada entrada del registro con resolve_registered_root, igual que doc_access.repository_root; una entrada con la virgulilla o relativa resuelve al mismo directorio por los dos caminos.

## Scope

_State what is in scope and what is out of scope._

Entra: build_neighbours en deskops/absolute_paths.py y tests en tests/test_doctor_absolute_paths.py. Sale: el formato de RepositoryDoc, repo register y el chequeo de registro de doctor (ya cerrados).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer build_neighbours y como arma la ruta de cada vecino. 2) Reemplazar la resolucion a mano por resolve_registered_root. 3) Test en desk sandbox (tmp_path) con una entrada de registro con la virgulilla (HOME apuntado al sandbox) y otra relativa: build_neighbours y doc_access.repository_root dan el mismo directorio.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_doctor_absolute_paths.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_registry_robustness.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa (mismo directorio por los dos caminos para una entrada con la virgulilla y una relativa) y los dos archivos de la Validation pasan.

FILE:desk/atoms/workflow-model/atom-code-changes-close-with-tests-and-commit.md
---
id: atom-code-changes-close-with-tests-and-commit
title: Code changes close with tests and commit
five_wh_one_plus: when
tags:
- system:deskops
- topic:testing
- topic:git
- topic:closeout
---

# Code changes close with tests and commit

## Answer

A task that modifies code is not closed until relevant tests pass and the completed change is recorded in a descriptive git commit.

FILE:desk/atoms/atom-repo-register-accepts-explicit-path-and-registry-errors-name-the-fix.md
---
id: atom-repo-register-accepts-explicit-path-and-registry-errors-name-the-fix
title: Repo register accepts explicit --path and registry errors name the fix
five_wh_one_plus: what
tags: []
provenance: null
---

# Repo register accepts explicit --path and registry errors name the fix

## Answer

deskops repo register <name> --path <abs> registers a sibling repository explicitly; registry resolution failures produce an actionable message naming the supported path instead of a bare not-found error, and register never crashes on model-entry shadowing.

FILE:deskops/absolute_paths.py
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

FILE:tests/test_doctor_absolute_paths.py
"""`deskops doctor` finds absolute paths in the desk; `--repair` writes them as addresses any machine resolves.

The fixtures live under tmp_path: ``<tmp>/eco/`` is the ecosystem folder, ``eco/project`` the desk
under test and ``eco/sldb``, ``eco/spec2viz`` its neighbours, linked in ``.sldb/store.yaml``.
Paths of "another machine" are ``/home/jp/proyectos/eco/<repo>``, whose ecosystem folder is
named like the fixture's.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops import absolute_paths
from deskops.cli.main import main
from deskops.identity import load_repository_registry
from deskops.doc_access import read_doc
from deskops.models import RepositoryDoc, TaskDoc

OTHER = "/home/jp/proyectos/eco"


def _out(capsys) -> str:
    return capsys.readouterr().out


def _eco(tmp_path: Path, capsys, *, neighbours=("sldb", "spec2viz")) -> Path:
    eco = tmp_path / "eco"
    root = eco / "project"
    root.mkdir(parents=True)
    for name in neighbours:
        (eco / name / ".sldb").mkdir(parents=True)
    assert main(["init", str(root)]) == 0
    capsys.readouterr()
    store = root / ".sldb" / "store.yaml"
    text = store.read_text(encoding="utf-8")
    links = "".join(f"- name: {n}\n  path: ../{n}/.sldb\n" for n in neighbours)
    store.write_text(text.replace("links:\n", "links:\n" + links, 1), encoding="utf-8")
    return root


def _register(root: Path, capsys, name: str, path: str) -> Path:
    assert main(["repo", "register", name, path, "--store", str(root / ".sldb")]) == 0
    capsys.readouterr()
    return root / "desk" / "registry" / f"repo-{name}.md"


def _set_path(doc: Path, value: str) -> None:
    lines = doc.read_text(encoding="utf-8").splitlines()
    doc.write_text("\n".join(f"path: {value}" if ln.startswith("path:") else ln for ln in lines) + "\n", encoding="utf-8")


def _task(root: Path, capsys, title: str, files: list[str], references: list[str] | None = None) -> Path:
    assert main(["add", "task", "--root", str(root), "--title", title, "--why", "w", "--goal", "g",
                 "--scope", "s", "--implementation-path", "i", "--done-when", "d"]) == 0
    capsys.readouterr()
    (path,) = [p for p in (root / "desk" / "tasks").glob("task-*.md") if p.name.startswith("task-" + title.split()[0])]
    text = path.read_text(encoding="utf-8")
    block = lambda key, vals: f"{key}:\n" + "".join(f"- {v}\n" for v in vals) if vals else f"{key}: []\n"
    text = text.replace("files: []\n", block("files", files), 1)
    text = text.replace("references: []\n", block("references", references or []), 1)
    path.write_text(text, encoding="utf-8")
    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0  # the store indexes the hand-made fixture
    capsys.readouterr()
    return path


def _doctor(root: Path, capsys, *extra: str) -> tuple[int, str]:
    code = main(["doctor", "--root", str(root), *extra])
    return code, _out(capsys)


def _abs_lines(out: str) -> list[str]:
    return [ln for ln in out.splitlines() if "Absolute path:" in ln]


def test_a_path_that_exists_under_a_neighbour_becomes_a_relative_registry_path(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    doc = _register(root, capsys, "sldb", "../sldb")
    _set_path(doc, str((tmp_path / "eco" / "sldb")))
    code, out = _doctor(root, capsys)
    assert code == 0 and "becomes ../sldb" in "\n".join(_abs_lines(out))
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0 and "-> ../sldb" in out
    assert read_doc(doc, RepositoryDoc)["path"] == "../sldb"
    assert _abs_lines(_doctor(root, capsys)[1]) == []


def test_a_path_from_another_machine_is_placed_by_the_ecosystem_folder(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    doc = _register(root, capsys, "spec2viz", "../spec2viz")
    _set_path(doc, f"{OTHER}/spec2viz")
    task = _task(root, capsys, "alpha", [f"{OTHER}/spec2viz/src/a.py"])
    _register(root, capsys, "sldb", "../sldb")
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0, out
    assert read_doc(doc, RepositoryDoc)["path"] == "../spec2viz"
    assert read_doc(task, TaskDoc)["files"] == ["spec2viz:src/a.py"]
    assert _abs_lines(out) == []


def test_an_ambiguous_path_stays_an_alert_with_its_reason(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    _register(root, capsys, "sldb", "../sldb")
    value = f"{OTHER}/sldb/x/eco/project/a.py"  # the folder appears twice: sldb, and the desk's own repo
    task = _task(root, capsys, "beta", [value])
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0
    assert read_doc(task, TaskDoc)["files"] == [value]
    lines = _abs_lines(out)
    assert len(lines) == 1 and value in lines[0] and "not rewritten: ambiguous" in lines[0]
    assert "Desk is healthy, with" in out


def test_a_path_that_names_no_neighbour_is_left_with_its_reason(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    task = _task(root, capsys, "gamma", ["/home/jp/AntonIA/repos/other/a.py", f"{OTHER}/unknown/a.py"])
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0 and len(_abs_lines(out)) == 2
    assert "no '" in out and "names no repository" in out
    assert len(read_doc(task, TaskDoc)["files"]) == 2


def test_a_path_of_the_own_repo_is_relative_to_its_root_without_prefix(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    task = _task(root, capsys, "delta", [str(root / "src" / "a.py"), f"{OTHER}/project/b.py"],
                 references=[f"{OTHER}/project/docs/c.md"])
    code, _out_ = _doctor(root, capsys, "--repair")
    assert code == 0
    payload = read_doc(task, TaskDoc)
    assert payload["files"] == ["src/a.py", "b.py"]
    assert payload["references"] == ["docs/c.md"]


def test_a_neighbour_without_registry_entry_is_an_alert(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    task = _task(root, capsys, "eps", [f"{OTHER}/sldb/a.py"])
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0 and "register it with deskops repo register" in out
    assert read_doc(task, TaskDoc)["files"] == [f"{OTHER}/sldb/a.py"]


def test_a_registry_with_two_repos_resolves_after_repair(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    docs = {n: _register(root, capsys, n, f"../{n}") for n in ("sldb", "spec2viz")}
    _set_path(docs["sldb"], f"{OTHER}/sldb")
    _set_path(docs["spec2viz"], str(tmp_path / "eco" / "spec2viz"))
    task = _task(root, capsys, "zeta", [f"{OTHER}/sldb/a.py", str(tmp_path / "eco" / "spec2viz" / "b.py")])
    before = {e.id: e.repo_root for e in load_repository_registry(root / "desk", root)}
    assert before["sldb"] != (tmp_path / "eco" / "sldb").resolve()  # another machine: not there
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0 and _abs_lines(out) == []
    after = {e.id: e.repo_root for e in load_repository_registry(root / "desk", root)}
    assert after == {"sldb": (tmp_path / "eco" / "sldb").resolve(), "spec2viz": (tmp_path / "eco" / "spec2viz").resolve()}
    assert read_doc(task, TaskDoc)["files"] == ["sldb:a.py", "spec2viz:b.py"]


def test_the_exit_code_does_not_change_and_repair_is_idempotent(tmp_path: Path, capsys) -> None:
    root = _eco(tmp_path, capsys)
    doc = _register(root, capsys, "sldb", "../sldb")
    _set_path(doc, f"{OTHER}/sldb")
    assert _doctor(root, capsys)[0] == 0
    assert _doctor(root, capsys, "--repair")[0] == 0
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0 and "Absolute path" not in out


@pytest.mark.parametrize("value, absolute", [("/loop", False), ("//host/x", False), ("a/b", False),
                                              ("/home/jp/x/y", True), ("two words /a/b", False)])
def test_what_counts_as_an_absolute_path(value: str, absolute: bool) -> None:
    assert absolute_paths.looks_absolute(value) is absolute

FILE:instruccion
Cold-bundle de la tarea task-build-neighbours-de-absolute-paths-resuelve-el-path-del-registro-con-resolve-registered-root-y-expan: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_doctor_absolute_paths.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_registry_robustness.py


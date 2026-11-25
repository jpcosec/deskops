"""The closeout link gate accepts an atom the task declares when the atom cites the changed file.

Piloto UI-122 de MEPU: a UI task changes .ts/.tsx/.css files and a build directory, which the
declared-edge graph has no nodes for; an atom declared in ``atoms`` (or cited in ``references``)
whose provenance or answer names those paths is the link.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil

import pytest
import yaml

from test_closeout import _git, _make_repo, _write, _write_atom, _write_task as _write_existing_task
from test_closeout_atomless import _cli

UI_FILES = [
    "frontend/src/screens/ocs/OcsPanel.tsx",
    "frontend/src/screens/ocs/ocs.css",
    "frontend/src/screens/ocs/vistas.test.ts",
    "src/frontend/v2/",
]


def _write_ui_atom(root: Path, atom_id: str = "atom-vistas-rapidas", *, cites: str) -> None:
    _write(
        root / "desk" / "atoms" / f"{atom_id}.md",
        f"""---
id: {atom_id}
title: Vistas rapidas
five_wh_one_plus: where
tags: []
provenance: frontend/src/screens/ocs/OcsPanel.tsx
---

# Vistas rapidas

## Answer

{cites}
""",
    )


def _repo(tmp_path: Path, *, atoms: list[str], extra_refs: list[str] = ()) -> Path:
    root = _make_repo(tmp_path)
    (root / "tests").mkdir()
    shutil.copyfile(__file__, root / "tests" / Path(__file__).name)
    for rel in UI_FILES:
        target = root / rel / "index.html" if rel.endswith("/") else root / rel
        _write(target, "x\n")
    _write_atom(root)  # an unrelated local atom: the desk has atoms, so coverage is strict
    refs = [f"tests/{Path(__file__).name}", _git(root, "rev-parse", "HEAD"), *extra_refs]
    _write_existing_task(root, refs, UI_FILES)
    path = root / "desk/tasks/task-x.md"
    _, frontmatter, body = path.read_text().split("---", 2)
    payload = yaml.safe_load(frontmatter)
    payload.pop("checklists", None)
    payload["atoms"] = atoms
    path.write_text("---\n" + yaml.safe_dump(payload, sort_keys=False) + "---" + body)
    return root


def _verify(root: Path) -> dict:
    result = _cli(root, "verify")
    assert result.stdout.strip(), result.stderr
    return json.loads(result.stdout)


ANSWER = (
    "Los botones los arma frontend/src/screens/ocs/OcsPanel.tsx, con estilo en "
    "frontend/src/screens/ocs/ocs.css y pruebas en frontend/src/screens/ocs/vistas.test.ts; "
    "el build sellado vive en src/frontend/v2."
)


def test_declared_atom_citing_non_python_files_links_every_changed_file(tmp_path: Path) -> None:
    root = _repo(tmp_path, atoms=["atom-vistas-rapidas"])
    _write_ui_atom(root, cites=ANSWER)
    report = _verify(root)
    gate = report["gates"]["atom_or_materialization_link"]
    assert gate["ok"], gate["findings"]
    for rel in ["frontend/src/screens/ocs/OcsPanel.tsx", "frontend/src/screens/ocs/ocs.css", "src/frontend/v2"]:
        assert f"atom-cites:atom-vistas-rapidas -> {rel}" in gate["evidence"]


def test_atom_cited_by_path_in_references_counts_too(tmp_path: Path) -> None:
    root = _repo(tmp_path, atoms=[], extra_refs=["desk/atoms/atom-vistas-rapidas.md"])
    _write_ui_atom(root, cites=ANSWER)
    assert _verify(root)["gates"]["atom_or_materialization_link"]["ok"]


def test_an_atom_citing_a_directory_covers_the_files_under_it(tmp_path: Path) -> None:
    root = _repo(tmp_path, atoms=["atom-vistas-rapidas"])
    _write_ui_atom(root, cites="La pantalla vive en frontend/src/screens/ocs/ y el build en src/frontend/v2.")
    assert _verify(root)["gates"]["atom_or_materialization_link"]["ok"]


@pytest.mark.parametrize("declared", [False, True])
def test_an_atom_that_does_not_cite_the_file_or_is_not_declared_is_no_link(tmp_path: Path, declared: bool) -> None:
    root = _repo(tmp_path, atoms=["atom-vistas-rapidas"] if declared else [])
    # Declared: cites only a sibling prefix (OcsPanel.tsx.bak, frontend/src/screensaver), never the files.
    # Not declared: cites everything, but the task does not name it.
    _write_ui_atom(
        root,
        cites="Ver frontend/src/screens/ocs/OcsPanel.tsx.bak y frontend/src/screensaver." if declared else ANSWER,
    )
    path = root / "desk/atoms/atom-vistas-rapidas.md"
    path.write_text(path.read_text().replace("provenance: frontend/src/screens/ocs/OcsPanel.tsx", "provenance: null"))
    report = _verify(root)
    gate = report["gates"]["atom_or_materialization_link"]
    assert not gate["ok"]
    missing = [f for f in gate["findings"] if f["code"] == "missing_changed_file_link"]
    assert {f["path"] for f in missing} == {
        "frontend/src/screens/ocs/OcsPanel.tsx", "frontend/src/screens/ocs/ocs.css",
        "frontend/src/screens/ocs/vistas.test.ts", "src/frontend/v2",
    }
    assert "atoms or references whose provenance or text cites this path" in missing[0]["message"]

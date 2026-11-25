from __future__ import annotations

from pathlib import Path

import pytest

from deskops.cli.main import main
from deskops.models.atom import AtomDoc
from deskops.models.pill import PillDoc
from deskops.models.task import TaskDoc

GOOD = ["doc:TaskDoc:task-x", "tag:area:ui.graph", "code:src/a/b.py::Clase.metodo", "code:src/a/b.py::"]
GOOD_EXTRA = ["tag:area:ui:graph", "code:src/a.py::foo~2", "code:src/a.py::Clase.metodo~2"]
BAD = {
    "doc:nada": "doc:<Model>:<id>",
    "tag:SinNamespace": "tag:<namespace>:<value>",
    "code:src/a.py": "code:<path>::<qualified_name>",
    "ruta/suelta.py": "class prefix",
}

ATOM = dict(id="atom-x", title="T", five_wh_one_plus="where", answer="a")
PILL = dict(id="pill-x", title="T", what="w", why="y", when="n", where="h", how="o", how_not="x")
TASK = dict(id="task-x", title="T", status="draft", goal="g", scope="s", implementation_path="i",
            validation=["v"], done_when="d")
MODELS = [(AtomDoc, ATOM), (PillDoc, PILL), (TaskDoc, TASK)]


@pytest.mark.parametrize("model,base", MODELS)
def test_models_default_and_accept_every_class(model, base) -> None:
    assert model(**base).pointers == []
    assert model(**base, pointers=GOOD).pointers == GOOD
    assert model(**{**base, "pointers": None}).pointers == []


@pytest.mark.parametrize("pointer", GOOD_EXTRA)
def test_tag_value_with_colon_and_code_tilde_suffix(pointer) -> None:
    assert TaskDoc(**TASK, pointers=[pointer]).pointers == [pointer]


@pytest.mark.parametrize("model,base", MODELS)
@pytest.mark.parametrize("bad,expected", BAD.items())
def test_models_reject_malformed_pointer_naming_class(model, base, bad, expected) -> None:
    with pytest.raises(ValueError, match="expected") as err:
        model(**base, pointers=[bad])
    assert expected.split(" ")[0] in str(err.value) or expected in str(err.value)


def _add_task(root: Path) -> None:
    assert main([
        "add", "task", "--root", str(root), "--title", "Punteros", "--task-type", "task.code",
        "--goal", "g", "--why", "w", "--scope", "s", "--implementation-path", "i",
        "--done-when", "d", "--validation", "pytest",
        "--pointers", *GOOD,
    ]) == 0


def test_cli_stores_shows_and_rejects_pointers(tmp_path: Path, capsys) -> None:
    assert main(["init", str(tmp_path)]) == 0
    _add_task(tmp_path)
    assert main(["add", "atom", "--root", str(tmp_path), "--title", "At", "--five-wh-one-plus", "where",
                 "--answer", "a", "--pointers", *GOOD]) == 0
    assert main(["add", "pill", "--root", str(tmp_path), "--title", "Pl", "--what", "w", "--why", "y",
                 "--when", "n", "--where", "h", "--how", "o", "--how-not", "x", "--pointers", *GOOD]) == 0
    capsys.readouterr()
    for kind, name in (("atom", "atom-at"), ("pill", "pill-pl")):
        assert main(["show", kind, name, "--root", str(tmp_path)]) == 0
        out = capsys.readouterr().out
        assert all(p in out for p in GOOD), kind
    assert main(["edit", "task", "task-punteros", "pointers", str(GOOD), "--root", str(tmp_path)]) == 0
    assert main(["show", "task", "task-punteros", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert all(p in out for p in GOOD)
    for kind, name in (("task", "task-punteros"), ("atom", "atom-at"), ("pill", "pill-pl")):
        assert main(["edit", kind, name, "pointers", "['doc:nada']", "--root", str(tmp_path)]) != 0
        captured = capsys.readouterr()
        assert "doc:<Model>:<id>" in captured.out + captured.err

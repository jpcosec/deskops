from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.models import AtomDoc
from deskops.atom_tags import add_namespace
from deskops.atom_tags import axis_folder
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


ATOM_SAMPLE = {
    "title": "Deskops models are sldb documents",
    "id": "atom-deskops-models-are-sldb-documents",
    "five_wh_one_plus": "what",
    "answer": "Deskops persists workflow artifacts as sldb StructuredNLDoc models.",
    "tags": ["system:deskops", "system:sldb", "topic:document-model"],
    "provenance": "",
}


def test_atom_doc_roundtrips_new_single_answer_contract() -> None:
    rendered = render_model_markdown(AtomDoc, ATOM_SAMPLE)
    extracted = extract_model_data(AtomDoc, rendered)

    assert extracted == ATOM_SAMPLE
    assert rendered.startswith("---\nid: atom-deskops-models-are-sldb-documents\ntitle: Deskops models are sldb documents\nfive_wh_one_plus: what\ntags:\n- system:deskops\n- system:sldb\n- topic:document-model\nprovenance: ''")
    assert "# atom-xxx, unique identifier" not in rendered
    assert "_Answer the selected 5WH1+ question" not in rendered
    assert "5WH1+: what" not in rendered
    assert "## Answer" in rendered
    assert "## Tags" not in rendered
    assert "Status:" not in rendered
    assert "Materializes Into" not in rendered


def test_atom_doc_rejects_unknown_5wh1_plus_question() -> None:
    invalid = dict(ATOM_SAMPLE)
    invalid["five_wh_one_plus"] = "pattern"

    with pytest.raises(ValueError):
        AtomDoc(**invalid)


def test_atom_doc_rejects_tags_without_namespace() -> None:
    invalid = dict(ATOM_SAMPLE)
    invalid["tags"] = ["deskops"]

    with pytest.raises(ValueError):
        AtomDoc(**invalid)


@pytest.mark.parametrize("tag", ["topic:a..b", "topic:a.", "system:deskops."])
def test_atom_doc_rejects_a_tag_value_with_an_empty_segment(tag: str) -> None:
    """sldb's tag_folder refuses an empty segment (CC35d H3): the atom model never lets one in."""
    invalid = dict(ATOM_SAMPLE)
    invalid["tags"] = [tag]

    with pytest.raises(ValueError, match="empty segment"):
        AtomDoc(**invalid)


def test_atom_doc_keeps_dotted_tag_values() -> None:
    sample = dict(ATOM_SAMPLE)
    sample["tags"] = ["topic:a.b-c.d_e", "layer:document-model", "system:a.1"]

    assert AtomDoc(**sample).tags == sample["tags"]


def test_axis_folder_is_sldb_tag_folder() -> None:
    assert axis_folder("mepu.licitaciones") == Path("mepu/licitaciones")
    assert axis_folder("pizzeria") == Path("pizzeria")
    with pytest.raises(ValueError):
        axis_folder("a..b")


def test_add_namespace_rejects_duplicate_namespace(tmp_path: Path) -> None:
    registry = tmp_path / "desk" / "atoms" / "tag-namespaces.yaml"
    add_namespace(
        registry,
        "pattern",
        meaning="Reusable solution shape.",
        use_when="The atom describes a repeatable solution.",
        do_not_use_when="The atom only mentions a topic.",
        examples=["pattern:roundtrip-validation"],
    )

    with pytest.raises(ValueError, match="already exists"):
        add_namespace(
            registry,
            "pattern",
            meaning="Duplicate.",
            use_when="Duplicate.",
            do_not_use_when="Duplicate.",
            examples=[],
        )


def test_store_declares_flat_host_namespace_and_task_doc_model(tmp_path: Path) -> None:
    from deskops.atom_tags import DEFAULT_ATOM_TAG_NAMESPACES
    from deskops.atom_tags import wanted_tag_declaration

    host = DEFAULT_ATOM_TAG_NAMESPACES["host"]
    assert host["meaning"] == "maquina donde se ejecuta y valida la tarea"
    assert host["do_not_use_when"] == "atoms y pills"
    registry = tmp_path / "desk" / "atoms" / "tag-namespaces.yaml"
    registry.parent.mkdir(parents=True)
    registry.write_text("namespaces:\n  topic:\n    meaning: m\n", encoding="utf-8")

    namespaces, models = wanted_tag_declaration(tmp_path)

    by_name = {item.name: item for item in namespaces}
    assert "TaskDoc" in models
    for name in ("host", "workspace", "artifact", "source"):
        assert by_name[name].hierarchical is False
    assert by_name["topic"].hierarchical is True


def test_desk_update_reports_no_divergence_after_declaring_host(tmp_path: Path, capsys) -> None:
    from deskops.cli.main import CLI
    import subprocess

    cli = CLI()
    assert cli.run(["init", str(tmp_path)]) == 0
    assert cli.run(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()
    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 0
    assert "Tag namespace declaration" not in capsys.readouterr().out

    declared = (tmp_path / ".sldb" / "store.yaml").read_text(encoding="utf-8")
    assert "name: host" in declared and "- TaskDoc" in declared

    assert cli.run(["add", "task", "--root", str(tmp_path), "--title", "Host sandbox", "--goal", "g",
                    "--scope", "s", "--implementation-path", "i", "--done-when", "d",
                    "--validation", "pytest"]) == 0
    assert cli.run(["edit", "task", "task-host-sandbox", "tags",
                    '["workspace:desk", "artifact:task", "host:robocop2"]', "--root", str(tmp_path)]) == 0
    task = tmp_path / "desk" / "tasks" / "task-host-sandbox.md"
    assert "host:robocop2" in task.read_text(encoding="utf-8")
    capsys.readouterr()
    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 0
    assert "Tag namespace declaration" not in capsys.readouterr().out
    checked = subprocess.run(["sldb", "stores", "check", "--store", str(tmp_path / ".sldb")],
                             capture_output=True, text=True)
    assert "host:robocop2" not in checked.stdout + checked.stderr, checked.stdout
    assert "tag" not in "".join(l for l in checked.stdout.splitlines() if "alert" in l and "doc_" not in l).lower()

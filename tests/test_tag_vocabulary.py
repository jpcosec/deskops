"""One tag vocabulary: the model says its own tags, the frontmatter does not repeat them."""

from __future__ import annotations

from pathlib import Path

from sldb.store.semantic_tags import flatten_model_semantics

from deskops.cli.main import main
from deskops.models import ReviewDoc
from deskops.models import TaskDoc
from deskops.tag_vocabulary import canonical_tags
from deskops.tag_vocabulary import is_class_name


def test_task_model_carries_its_own_hierarchy_tags() -> None:
    tags = flatten_model_semantics(TaskDoc)
    assert {"type.workflow.task", "workspace.desk", "board.tareas"} <= set(tags)


def test_flat_restatements_repeats_and_class_names_are_not_kept() -> None:
    given = ["workspace:desk", "artifact:task", "host:robocop2", "TaskDoc", "host:robocop2", "topic:ui"]
    assert canonical_tags(given, TaskDoc) == ["host:robocop2", "topic:ui"]
    assert is_class_name("OperationalArtifactDoc") and not is_class_name("topic:ui")


def test_workspace_desk_is_implied_by_a_deeper_model_tag() -> None:
    # ReviewDoc says workspace.desk.runs, so workspace:desk (its ancestor) adds nothing
    assert canonical_tags(["workspace:desk", "system:deskops"], ReviewDoc) == ["system:deskops"]


def test_models_validate_tags_through_the_vocabulary() -> None:
    task = TaskDoc.model_validate({
        "title": "t", "id": "task-t", "status": "draft", "goal": "g", "scope": "s", "implementation_path": "i",
        "done_when": "d", "tags": ["workspace:desk", "artifact:task", "host:local", "host:local"],
    })
    assert task.tags == ["host:local"]


def test_add_task_writes_no_duplicate_tags(tmp_path: Path) -> None:
    assert main(["init", str(tmp_path)]) == 0
    assert main([
        "add", "task", "--root", str(tmp_path), "--title", "Una", "--why", "w", "--goal", "g", "--scope", "s",
        "--implementation-path", "i", "--done-when", "d", "--validation", "pytest", "--task-type", "task.code",
    ]) == 0
    text = (tmp_path / "desk" / "tasks" / "task-una.md").read_text(encoding="utf-8")
    assert "workspace:desk" not in text and "artifact:task" not in text


def test_tags_migrate_reports_then_rewrites(tmp_path: Path, capsys) -> None:
    assert main(["init", str(tmp_path)]) == 0
    assert main([
        "add", "task", "--root", str(tmp_path), "--title", "Una", "--why", "w", "--goal", "g", "--scope", "s",
        "--implementation-path", "i", "--done-when", "d", "--validation", "pytest", "--task-type", "task.code",
    ]) == 0
    path = tmp_path / "desk" / "tasks" / "task-una.md"
    old = path.read_text(encoding="utf-8").replace("tags: []", "tags:\n- workspace:desk\n- artifact:task", 1)
    assert "artifact:task" in old
    path.write_text(old, encoding="utf-8")
    capsys.readouterr()

    assert main(["tags", "migrate", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "workspace:desk" in out and "artifact:task" in out and "Dry run" in out
    assert "artifact:task" in path.read_text(encoding="utf-8")

    assert main(["tags", "migrate", "--root", str(tmp_path), "--apply"]) == 0
    assert "artifact:task" not in path.read_text(encoding="utf-8")
    assert main(["tags", "migrate", "--root", str(tmp_path)]) == 0
    assert "No document carries" in capsys.readouterr().out


def test_tags_migrate_apply_reindexes_a_canonical_document_behind_its_model(tmp_path: Path, capsys, monkeypatch) -> None:
    from sldb.api import describe_model

    from deskops import doc_access

    root = tmp_path
    # The model has not yet said board.tareas when the document is written and indexed.
    monkeypatch.setattr(TaskDoc, "__semantics__", {"type": ["workflow", "task"], "workspace": ["desk"]})
    assert main(["init", str(root)]) == 0
    assert main([
        "add", "task", "--root", str(root), "--title", "Una", "--why", "w", "--goal", "g", "--scope", "s",
        "--implementation-path", "i", "--done-when", "d", "--validation", "pytest", "--task-type", "task.code",
    ]) == 0
    monkeypatch.undo()
    monkeypatch.setattr(TaskDoc, "__semantics__", {"type": ["workflow", "task"], "workspace": ["desk"], "board": ["tareas"]})

    # sldb keeps the tags it extracted per (path, hash) for the process; a real migration is a fresh one.
    monkeypatch.setattr("sldb.store.semantic_doc_tags._DOC_TAGS", {})

    def indexed() -> list[str]:
        docs = describe_model(doc_access.store_path(root), "TaskCodeDoc", doc_access.package_pythonpath()).documents
        return docs[0].semantic_tags

    assert "board.tareas" not in indexed()
    capsys.readouterr()
    assert main(["tags", "migrate", "--root", str(root)]) == 0
    assert "semantic index older" in capsys.readouterr().out
    assert "board.tareas" not in indexed()

    assert main(["tags", "migrate", "--root", str(root), "--apply"]) == 0
    assert "board.tareas" in indexed()
    capsys.readouterr()
    assert main(["tags", "migrate", "--root", str(root)]) == 0
    assert "No document carries" in capsys.readouterr().out

"""BoardDoc declares DAG phases: tasks per phase and the phase integration."""
import pytest
from pydantic import ValidationError

from deskops.models import BoardDoc
from deskops.models.board import Phase, PhaseIntegration
from sldb.runtime.validation import Validator, render_model_markdown


def board(**extra):
    return BoardDoc(id="board-x", title="B", scope="s", purpose="p", **extra)


def test_two_phases_round_trip_through_render_and_extract():
    doc = board(phases=[
        Phase(id="p1", tasks=["task-a", "task-b"],
              integration=PhaseIntegration(validation=["pytest -q"], closing_commit="close p1")),
        Phase(id="p2", tasks=["task-c"]),
    ])
    parsed = Validator(BoardDoc).extract(render_model_markdown(BoardDoc, doc.render_payload()))
    assert BoardDoc(**{**parsed, "title": "B", "purpose": "p"}).phases == doc.phases


def test_task_in_two_phases_is_rejected():
    with pytest.raises(ValidationError, match="task-a"):
        board(phases=[Phase(id="p1", tasks=["task-a"]), Phase(id="p2", tasks=["task-a"])])


def test_task_repeated_in_one_phase_is_rejected():
    with pytest.raises(ValidationError, match="task-a"):
        board(phases=[Phase(id="p1", tasks=["task-a", "task-a"])])


def test_board_without_phases_is_valid():
    assert board().phases == []

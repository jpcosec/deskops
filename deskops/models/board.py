from pydantic import BaseModel, Field, field_validator, model_validator

from .base import OperationalArtifactDoc


class PhaseIntegration(BaseModel):
    validation: list[str] = Field(
        default_factory=list,
        description="Combined validation commands run once the phase tasks are done.",
    )
    closing_commit: str | None = Field(
        default=None,
        description="Phase closing commit that integrates the phase.",
    )


class Phase(BaseModel):
    id: str = Field(description="Stable phase identifier.")
    tasks: list[str] = Field(default_factory=list, description="Task references forming this phase.")
    integration: PhaseIntegration = Field(
        default_factory=PhaseIntegration,
        description="Phase integration: combined validation and closing commit.",
    )


class BoardDoc(OperationalArtifactDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "board-{slug}",
        "status_default": "active",
        "tags": [],
    }
    __containment__ = {"tasks": ["TaskDoc"], "pills": ["PillDoc"], "rituals": ["RitualDoc"]}
    __semantics__ = {"type": ["workflow", "board"], "workspace": ["desk"]}
    __compositions__ = {
        "task_summaries": {
            "source_field": "tasks",
            "model": "deskops.models:TaskDoc",
            "template": "- {title} [{status}] - {goal}",
        }
    }
    __template__ = """---
# board-xxx
id: ⸢rev•id⸥
# Affected workspace or domain
scope: ⸢rev•scope⸥
# List of task-xxx paths
tasks: ⸢rev•tasks⸥
# List of pill-xxx paths
pills: ⸢rev•pills⸥
# List of ritual-xxx paths
rituals: ⸢rev•rituals⸥
# DAG phases: id, tasks, integration
phases: ⸢rev•phases⸥
# e.g., system:sldb
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Purpose

_Explain what this board routes and why it exists._

⸢rev•purpose⸥

## Notes

_Add short operational notes about the current routed set._

⸢rev•notes⸥

## Task Details

_Generated from the task references above._

⸢render•task_summaries⸥

""".strip()

    title: str = Field(description="Board title for one active routing surface.")
    id: str = Field(description="Stable board identifier.")
    scope: str = Field(description="What area or workspace this board routes.")
    purpose: str = Field(description="Why this board exists and what it indexes.")
    tasks: list[str] = Field(
        default_factory=list,
        description="Active task document references routed by this board.",
    )
    pills: list[str] = Field(
        default_factory=list,
        description="Active pill document references routed by this board.",
    )
    rituals: list[str] = Field(
        default_factory=list,
        description="Ritual document references relevant to this board.",
    )
    phases: list[Phase] = Field(
        default_factory=list,
        description="DAG phases: id, member tasks and the phase integration.",
    )
    notes: str = Field(
        default="No additional notes.",
        description="Short operational notes about the current routed set.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'system:sldb'.",
    )


    @field_validator("phases", mode="before")
    @classmethod
    def _absent_phases_are_empty(cls, value):
        return [] if value is None else value

    @model_validator(mode="after")
    def _task_in_one_phase(self):
        seen: set[str] = set()
        for phase in self.phases:
            for task in phase.tasks:
                if task in seen:
                    raise ValueError(f"task {task!r} appears more than once in the board phases")
                seen.add(task)
        return self

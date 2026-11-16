---
sldb:
  by: agent
  at: '2026-11-16T06:06:26Z'
  authority: generated
  via: save_document_payload
id: task-board-no-refleja-deskops-edit-task-goal
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-board-no-refleja-edit-task-goal.md
---

# Board no refleja deskops edit task goal

## Rationale

_Explain why this task exists or the business driver behind it._

Nota (12-11, inbox 20261112-132201, caso FTC-26): edit task goal actualiza la tarea pero desk/tasks/Board.md sigue con el goal viejo; edit board no encuentra el artefacto y desk replace rechaza el Board por ser documento modelado.

## Goal

_Describe the concrete result this task must produce._

Reproducir en un desk real y corregir: tras deskops edit task <id> goal, la linea de la tarea en Task Details del Board muestra el goal nuevo, o hay un verbo de deskops que refresca el Board.

## Scope

_State what is in scope and what is out of scope._

deskops/services/tasks.py, deskops/models/board.py (plantilla de Task Details), deskops edit; la vista del tablero es de sldb (CC34), no se reimplementa.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- test nuevo de deskops (nombre a fijar al promover) que edita goal y lee el Board

## Done When

_Name the observable condition that makes the task complete._

recibo de reproduccion y test que edita el goal y lee el Board con el valor nuevo.

---
id: task-board-no-refleja-edit-task-goal
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Board no refleja edit task goal

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261112-132201-unclear-board-no-refleja-edit-task-goal.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261112-132201-unclear-board-no-refleja-edit-task-goal.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

En ftcourier, 'deskops edit task <id> goal ...' actualiza la tarea pero desk/tasks/Board.md sigue mostrando el goal viejo en la línea de la tarea. No hay verbo para refrescarlo: 'deskops edit board <Board|board-001|desk/tasks/Board.md> ...' responde 'No artifact.board file found', y 'deskops desk replace desk/tasks/Board.md' lo rechaza porque es un documento modelado de tareas. Caso: FTC-26, 12-11-2026.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.

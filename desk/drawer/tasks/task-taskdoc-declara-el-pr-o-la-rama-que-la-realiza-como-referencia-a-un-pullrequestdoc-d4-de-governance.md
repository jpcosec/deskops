---
sldb:
  by: agent
  at: '2026-11-25T20:14:23Z'
  authority: generated
  via: create_document
id: task-taskdoc-declara-el-pr-o-la-rama-que-la-realiza-como-referencia-a-un-pullrequestdoc-d4-de-governance
status: deferred
summary: ''
tags: []
current_node: ''
history: []
references:
- desk/tasks/task-governance-documento-de-pr-en-desk-prs-y-deskops-pr-check-en-ci.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# TaskDoc declara el PR o la rama que la realiza como referencia a un PullRequestDoc (D4 de Governance)

## Rationale

_Explain why this task exists or the business driver behind it._

JP adoptó el 25-11 la D4 del spec de Governance (docs/spec/spec-procesos-modelables.md de heyantonia/Governance): una tarea declara el PR o la rama que la realiza. Conversa con las tareas de M2 sobre el documento de PR y el cierre dentro del PR.

## Goal

_Describe the concrete result this task must produce._

TaskDoc tiene un campo que referencia el PullRequestDoc (o la rama) que realiza la tarea, el modelo PullRequestDoc existe y una regla puede leerlo.

## Scope

_State what is in scope and what is out of scope._

Entra: el modelo PullRequestDoc (o reusar el que defina la tarea del documento de PR), el campo en TaskDoc, su migración en los desks y una regla de ejemplo. Sale: el cierre dentro del PR (otra tarea de M2).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ver si la tarea del documento de PR ya define PullRequestDoc. 2) Campo en TaskDoc como referencia. 3) Migración. 4) Escenario: una regla lee el PR de la tarea.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core

## Done When

_Name the observable condition that makes the task complete._

Una tarea declara su PR y una regla lo lee.

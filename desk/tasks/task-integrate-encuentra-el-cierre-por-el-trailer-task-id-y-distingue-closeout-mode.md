---
sldb:
  by: agent
  at: '2026-11-25T19:45:30Z'
  authority: generated
  via: create_document
id: task-integrate-encuentra-el-cierre-por-el-trailer-task-id-y-distingue-closeout-mode
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-suite-de-tests-nueva-por-capa-escenarios-del-nucleo-operacion-con-repos-git-temporales-y-contrato-de
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# integrate encuentra el cierre por el trailer Task-Id y distingue Closeout-Mode

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

integrate busca el commit de cierre por trailers (Task-Id, Closeout-Mode) y no por el asunto exacto, y no integra un cierre superseded como si fuera trabajo.

## Scope

_State what is in scope and what is out of scope._

Entra: integrate.py. Sale: integrate por fase (otra tarea).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Buscar por trailers. 2) Distinguir Closeout-Mode. 3) Escenario con --message.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/ops

## Done When

_Name the observable condition that makes the task complete._

Un cierre con --message se integra y uno superseded no.

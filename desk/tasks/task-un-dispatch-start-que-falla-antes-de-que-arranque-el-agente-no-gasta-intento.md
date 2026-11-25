---
sldb:
  by: agent
  at: '2026-11-25T01:44:28Z'
  authority: generated
  via: create_document
id: task-un-dispatch-start-que-falla-antes-de-que-arranque-el-agente-no-gasta-intento
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Un dispatch start que falla antes de que arranque el agente no gasta intento

## Rationale

_Explain why this task exists or the business driver behind it._

Piloto UI-122 de MEPU (nota PARA DESKOPS 20261124-220541 punto 4): dos fallas de infraestructura de scion dejaron la tarea sin intentos sin haber trabajado; quedaron el run_dir, el worktree, la rama y el commit del RunDoc.

## Goal

_Describe the concrete result this task must produce._

Si scion templates sync o scion start fallan, o el agente queda en fase error, dispatch start borra el run_dir, destrackea el RunDoc, deshace su commit (o commitea el borrado), quita worktree y rama, y avisa fallo tecnico reintentable; el siguiente start usa el mismo intento.

## Scope

_State what is in scope and what is out of scope._

deskops/dispatch.py y tests/test_dispatch.py.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- pytest tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

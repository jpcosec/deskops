---
sldb:
  by: agent
  at: '2026-11-25T22:56:06Z'
  authority: generated
  via: create_document
id: task-advance-y-el-cierre-toman-la-transicion-con-la-primitiva-de-sldb-y-se-borra-lifecycle-advance
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-sldb-ofrece-la-primitiva-tomar-transicion-en-su-cli-y-su-api-pedido-c2
- task-el-cierre-toma-la-arista-task-completes-desde-el-nodo-real-de-la-tarea
- task-supersede-resolved-by-y-retire-son-aristas-declaradas-del-ciclo-de-vida
pills: []
files:
- deskops/lifecycle.py
- deskops/services/tasks.py
- deskops/services/closure.py
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# advance y el cierre toman la transición con la primitiva de sldb y se borra lifecycle.advance

## Rationale

_Explain why this task exists or the business driver behind it._

lifecycle.advance reimplementa en deskops lo que es tomar una arista de un grafo de sldb.

## Goal

_Describe the concrete result this task must produce._

deskops advance y closeout llaman a la primitiva de sldb para tomar una arista y lifecycle.advance no existe.

## Scope

_State what is in scope and what is out of scope._

Entra: lifecycle.py, los llamadores en services/tasks.py y closure.py. Sale: qué aristas existen (es del workflow).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reemplazar los llamadores. 2) Borrar lifecycle.advance. 3) Escenarios en verde.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core
- grep -rn 'def advance' deskops/core/lifecycle.py no da resultados

## Done When

_Name the observable condition that makes the task complete._

lifecycle.advance no existe y los escenarios del workflow pasan.

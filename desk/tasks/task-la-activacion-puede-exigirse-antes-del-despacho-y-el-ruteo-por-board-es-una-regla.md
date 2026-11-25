---
sldb:
  by: agent
  at: '2026-11-25T19:44:33Z'
  authority: generated
  via: create_document
id: task-la-activacion-puede-exigirse-antes-del-despacho-y-el-ruteo-por-board-es-una-regla
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-toda-compuerta-de-cierre-y-de-activacion-es-una-clausula-de-ruledoc-con-severidad-que-declara-el-wor
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La activación puede exigirse antes del despacho y el ruteo por Board es una regla

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

dispatch start comprueba lo que el workflow exige para activar (recibos, nodo) antes de lanzar; estar en el Board es una cláusula de regla en vez de un if en closure.py y tasks.py; una tarea sin tipo exige lo que declare el workflow.

## Scope

_State what is in scope and what is out of scope._

Entra: dispatch start, _close, services/tasks.py advance y next, la regla de tarea sin tipo. Sale: cambiar el orden de los ritos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Gate de activación en dispatch. 2) Regla de ruteo. 3) Regla de tarea sin tipo. 4) Quitar xfail de N4, W4, N10 y N1.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core

## Done When

_Name the observable condition that makes the task complete._

Los escenarios de N4, W4, N10 y N1 pasan.

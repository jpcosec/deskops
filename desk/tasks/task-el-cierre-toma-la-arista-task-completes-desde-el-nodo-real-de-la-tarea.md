---
sldb:
  by: agent
  at: '2026-11-25T19:43:39Z'
  authority: generated
  via: create_document
id: task-el-cierre-toma-la-arista-task-completes-desde-el-nodo-real-de-la-tarea
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-escenarios-del-workflow-escritos-para-fallar-hoy-cerrar-desde-ejecucion-con-tests-rojos-fuera-del-bo
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El cierre toma la arista task_completes desde el nodo real de la tarea

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

closeout commit evalúa la arista task_completes completa (condición y nodo) desde el current_node real, en vez de forzar ritual-closeout; los prompts piden tomar task_hands_to_closeout.

## Scope

_State what is in scope and what is out of scope._

Entra: services/closure.py closeout_rule_findings, los prompts del tester y del coordinador. Sale: los cierres alternativos (otra tarea).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Quitar el forzado de CLOSEOUT_NODE. 2) Evaluar la arista. 3) Prompts. 4) Quitar el xfail de W3 y N6.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core

## Done When

_Name the observable condition that makes the task complete._

El escenario de W3 pasa: una tarea en ejecución no cierra si el workflow lo exige.

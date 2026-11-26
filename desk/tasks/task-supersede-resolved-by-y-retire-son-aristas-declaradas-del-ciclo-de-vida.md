---
sldb:
  by: agent
  at: '2026-11-25T22:56:54Z'
  authority: generated
  via: save_document_payload
id: task-supersede-resolved-by-y-retire-son-aristas-declaradas-del-ciclo-de-vida
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-el-cierre-toma-la-arista-task-completes-desde-el-nodo-real-de-la-tarea
- task-escenarios-del-workflow-escritos-para-fallar-hoy-cerrar-desde-ejecucion-con-tests-rojos-fuera-del-bo
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# supersede, resolved-by y retire son aristas declaradas del ciclo de vida

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Los cierres alternativos son RelationDoc con su condición y efectos y se toman como cualquier arista; ninguno escribe status directo, y resolved-by queda en el rito de cierre.

## Scope

_State what is in scope and what is out of scope._

Entra: data/lifecycle, desk/lifecycle, _record_closing_status, el rito de closeout. Sale: cambiar qué exige cada cierre (es del workflow).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) RelationDoc por cierre. 2) Tomarlas en closure.py. 3) Rito. 4) Escenarios.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core

## Done When

_Name the observable condition that makes the task complete._

Ningún cierre escribe status sin tomar una arista.

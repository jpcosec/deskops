---
sldb:
  by: agent
  at: '2026-11-25T22:51:00Z'
  authority: generated
  via: save_document_payload
id: task-la-suite-vieja-se-retira-a-medida-que-cada-modulo-se-muda-a-su-capa
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
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La suite vieja se retira a medida que cada módulo se muda a su capa

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Cada test de la suite vieja queda reemplazado por uno de la suite nueva que prueba la misma capacidad, o se borra si fijaba implementación; al final tests/ solo tiene la suite nueva.

## Scope

_State what is in scope and what is out of scope._

Entra: inventario de los ~118 archivos (capacidad o implementación) y su retiro coordinado con las mudanzas de E1 (capas) y E3. Sale: mantener tests de implementación.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario. 2) Por cada mudanza de E1 y E3, retirar los tests viejos del módulo. 3) Borrar lo que quede.

## Validation

_List the checks required before this task can close._

- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

tests/ contiene solo la suite nueva y cada capacidad tiene su test.

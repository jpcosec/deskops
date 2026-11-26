---
sldb:
  by: agent
  at: '2026-11-25T22:56:45Z'
  authority: generated
  via: save_document_payload
id: task-la-coherencia-de-status-current-node-e-history-es-una-regla-on-write-que-lee-el-grafo-del-desk
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-el-lenguaje-de-reglas-de-sldb-lee-el-ultimo-elemento-de-una-lista-pedido-c3
- task-escenarios-del-workflow-escritos-para-fallar-hoy-cerrar-desde-ejecucion-con-tests-rojos-fuera-del-bo
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La coherencia de status, current_node e history es una regla on_write que lee el grafo del desk

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

El validador de models/task_lifecycle.py pasa a una RuleDoc on_write y lee el grafo del desk, no el del paquete; _check_against_package deja de rechazar aristas propias del desk.

## Scope

_State what is in scope and what is out of scope._

Entra: la regla y borrar el validador. Sale: nada más.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Regla on_write que compara current_node con el último elemento de history. 2) Borrar el validador y _check_against_package. 3) Escenario de escritura incoherente.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core

## Done When

_Name the observable condition that makes the task complete._

models/task_lifecycle.py no existe y una escritura incoherente falla por la regla.

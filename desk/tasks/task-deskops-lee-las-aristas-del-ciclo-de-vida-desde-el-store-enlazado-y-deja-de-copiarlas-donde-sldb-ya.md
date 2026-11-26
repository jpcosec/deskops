---
sldb:
  by: agent
  at: '2026-11-25T19:45:41Z'
  authority: generated
  via: create_document
id: task-deskops-lee-las-aristas-del-ciclo-de-vida-desde-el-store-enlazado-y-deja-de-copiarlas-donde-sldb-ya
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-deskops-se-ordena-en-paquetes-por-capa-core-ops-runtime-operations-surfaces-con-contratos-de-imports
pills: []
files: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops lee las aristas del ciclo de vida desde el store enlazado y deja de copiarlas donde sldb ya lo permite

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

lifecycle.py deja de pasar include_linked=False y lee las aristas del paquete enlazado; la siembra de copias se reduce a lo que sldb todavía no aplica (las reglas, pedido C1).

## Scope

_State what is in scope and what is out of scope._

Entra: las cuatro consultas de lifecycle.py:318-343, la siembra de aristas en desk update. Sale: las reglas enlazadas (esperan C1).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Probar current_node calificado contra el store enlazado. 2) Quitar include_linked=False. 3) Dejar de sembrar aristas.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core tests/ops

## Done When

_Name the observable condition that makes the task complete._

Un desk sin copias locales de las aristas avanza tareas.

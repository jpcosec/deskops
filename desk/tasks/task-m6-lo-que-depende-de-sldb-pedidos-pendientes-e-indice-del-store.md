---
sldb:
  by: agent
  at: '2026-11-25T19:51:11Z'
  authority: generated
  via: create_document
id: task-m6-lo-que-depende-de-sldb-pedidos-pendientes-e-indice-del-store
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-seguimiento-de-lo-que-deskops-necesita-de-sldb-tomar-transicion-ultimo-elemento-de-una-lista-on-dele
- task-seguimiento-del-indice-del-store-de-sldb-base-embebida-y-git-y-de-la-documentacion-de-los-hashes
pills: []
files: []
task_type: task.aggregate
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# M6 Lo que depende de sldb: pedidos pendientes e índice del store

## Rationale

_Explain why this task exists or the business driver behind it._

Macro del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md); agrupa sus subtareas por capa.

## Goal

_Describe the concrete result this task must produce._

Todas las subtareas de M6 cerradas.

## Scope

_State what is in scope and what is out of scope._

Entra: las subtareas listadas en depends_on. Sale: trabajo de otras macros.

## Implementation Path

_Outline the expected implementation route or affected surface._

Se cierra cuando cierran sus subtareas.

## Validation

_List the checks required before this task can close._

- Todas las tareas de depends_on están cerradas

## Done When

_Name the observable condition that makes the task complete._

Todas las subtareas cerradas.

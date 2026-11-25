---
sldb:
  by: agent
  at: '2026-11-25T19:49:51Z'
  authority: generated
  via: create_document
id: task-revisar-las-tareas-congeladas-contra-las-macros-m0-a-m6
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on: []
pills: []
files: []
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Revisar las tareas congeladas contra las macros M0 a M6

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Cada tarea que estaba en el Board antes del 25-11 se cierra con supersede hacia la tarea nueva que la cubre, se reescribe o se retira; ninguna queda apuntando a código o datos que ya no existen.

## Scope

_State what is in scope and what is out of scope._

Entra: todas las tareas previas al 25-11. Sale: las nuevas.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Mapear cada una. 2) Supersede, reescribir o retirar.

## Validation

_List the checks required before this task can close._

- deskops list tasks --root . no muestra tareas que dupliquen una macro

## Done When

_Name the observable condition that makes the task complete._

Ninguna tarea vieja duplica una nueva.

---
sldb:
  by: agent
  at: '2026-11-25T19:56:36Z'
  authority: generated
  via: save_document_payload
id: task-el-board-es-una-vista-calculada-sobre-las-tareas-y-deja-de-ser-un-documento-que-reescriben-todas-las
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

# El Board es un documento generado desde las tareas y sus operaciones quedan mapeadas

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

El Board se genera desde las tareas (no se edita a mano ni lo reescribe cada sesión al crear o cerrar una tarea) y cada operación que se hace sobre él (rutear una tarea, sacarla, ordenar, declarar fases, cambiar pills de board) está mapeada a una operación de deskops que modifica la fuente y regenera el Board.

## Scope

_State what is in scope and what is out of scope._

Entra: inventario de las operaciones que hoy se hacen sobre el Board (en código y a mano), qué dato de las tareas o del BoardDoc es la fuente de cada una, la generación del Board desde esa fuente y las operaciones que falten. Sale: las fases como concepto (tarea de fases) y la UI.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario de escrituras al Board en deskops/ (add task, closeout, retire, supersede, drawer) y de ediciones a mano en el historial de git. 2) Para cada una, la fuente (campo de la tarea o del BoardDoc). 3) Generar el Board desde la fuente. 4) Operaciones faltantes. 5) Escenario: dos sesiones crean tareas distintas sin conflicto en Board.md.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core
- deskops view board --format json

## Done When

_Name the observable condition that makes the task complete._

Cada operación sobre el Board está mapeada a una operación de deskops y el Board se regenera desde su fuente.

---
sldb:
  by: agent
  at: '2026-11-25T20:14:49Z'
  authority: generated
  via: create_document
id: task-lo-retirado-se-borra-y-la-tarea-guarda-un-puntero-a-git-para-ver-su-genealogia
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- deskops/models/task.py
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Lo retirado se borra y la tarea guarda un puntero a git para ver su genealogía

## Rationale

_Explain why this task exists or the business driver behind it._

JP, 25-11: lo retirado puede persistir en git; que promote y los demás verbos borren lo que tengan que borrar (una nota del inbox, un ítem del drawer, una tarea cerrada) y que desde la tarea se pueda ver su genealogía directa en git.

## Goal

_Describe the concrete result this task must produce._

Cada vez que una tarea nace de otro documento (nota del inbox, ítem del drawer, otra tarea) el documento de origen se borra y la tarea guarda un puntero de git a él (ruta y commit donde existía), y una operación muestra la genealogía de una tarea leyendo esos punteros con git.

## Scope

_State what is in scope and what is out of scope._

Entra: el campo de origen con puntero de git en TaskDoc (generalizando from_drawer), que promote inbox-to-drawer-task, add task --from-drawer y los cierres lo escriban y borren el origen, y una operación que recorre la genealogía con git show. Sale: recuperar documentos borrados (git ya lo permite).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Campo origin con path y commit. 2) promote y add task --from-drawer borran el origen y escriben el puntero. 3) Operación genealogy. 4) Escenario: una nota pasa a tarea, se borra, y la genealogía la muestra desde git.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core tests/ops

## Done When

_Name the observable condition that makes the task complete._

Desde una tarea se ve el texto de su origen borrado, leído de git.

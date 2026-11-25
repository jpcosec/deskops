---
sldb:
  by: agent
  at: '2026-11-24T18:29:40Z'
  authority: generated
  via: save_document_payload
id: task-supertareas-y-alta-en-lote-campo-parent-en-taskdoc-y-add-task-from-yaml-con-varias-tareas
status: deferred
summary: 'Borrador sin preparar: preflight rechazado el 2026-11-21 (ver desk/reviews/task-supertareas-y-alta-en-lote-campo-parent-en-taskdoc-y-add-task-from-yaml-con-varias-tareas/).
  Falta Implementation Path concreto, decisiones de diseno y nombre del test antes
  de revisar de nuevo.'
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-194440-unclear-supertareas-y-alta-en-lote.md
- desk/inbox/20261115-195317-unclear-correcci-n-s-hay-supertareas-task-aggregate.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# supertareas y alta en lote: campo parent en TaskDoc y add task --from-yaml con varias tareas

## Rationale

_Explain why this task exists or the business driver behind it._

Origen: nota de MEPU del 15-11 (no llego al inbox de deskops porque --to deskops no resolvia; transcrita en velocidad-hooks-brief.md, Parte D). MEPU arma supertareas (UI-138..UI-146) y altas en tanda a mano; hoy --from-yaml carga una sola tarea y no hay parent.

## Goal

_Describe the concrete result this task must produce._

TaskDoc tiene un campo parent (id de otra tarea) que doctor y el tablero respetan, y deskops add task --from-yaml acepta una lista de tareas y las crea en una sola transaccion (todas o ninguna).

## Scope

_State what is in scope and what is out of scope._

deskops/models (TaskDoc parent), deskops/services/tasks.py, deskops/cli add task; relacion por la API de aristas de sldb, sin grafo propio.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- test nuevo de deskops (nombre a fijar al promover) con un yaml de supertarea y tres hijas

## Done When

_Name the observable condition that makes the task complete._

un yaml con una supertarea y tres hijas crea las cuatro tareas con parent, y un error en la tercera no deja ninguna.

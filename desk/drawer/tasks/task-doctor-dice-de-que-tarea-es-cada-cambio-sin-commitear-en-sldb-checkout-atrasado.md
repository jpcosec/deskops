---
sldb:
  by: agent
  at: '2026-11-24T18:27:46Z'
  authority: generated
  via: save_document_payload
id: task-doctor-dice-de-que-tarea-es-cada-cambio-sin-commitear-en-sldb-checkout-atrasado
status: deferred
summary: 'Borrador sin preparar: preflight rechazado el 2026-11-21 (ver desk/reviews/task-doctor-dice-de-que-tarea-es-cada-cambio-sin-commitear-en-sldb-checkout-atrasado/).
  Falta Implementation Path concreto, decisiones de diseno y nombre del test antes
  de revisar de nuevo.'
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-194446-unclear-checkout-atrasado-con-sldb-sin-commitear.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# doctor dice de que tarea es cada cambio sin commitear en .sldb (checkout atrasado)

## Rationale

_Explain why this task exists or the business driver behind it._

Origen: nota de MEPU del 15-11 (no llego al inbox de deskops porque --to deskops no resolvia; transcrita en velocidad-hooks-brief.md, Parte D). Con el checkout atrasado y .sldb sin commitear no se sabe que cambio de .sldb pertenece a que tarea; se cruza con H1 (hooks) y H2 (merge driver) de sldb.

## Goal

_Describe the concrete result this task must produce._

deskops doctor lista los cambios sin commitear bajo .sldb/ agrupados por la tarea (o el documento de desk) que los origino, y marca los que no tienen dueno.

## Scope

_State what is in scope and what is out of scope._

deskops doctor; lee el estado de git de .sldb y el sujeto de cada documento por la API de sldb; no reimplementa el diff del store (sldb). Depende de H1/H2 en sldb para el caso de merge.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- test nuevo de deskops (nombre a fijar al promover) con un repo real cuyo .sldb cambiaron dos tareas

## Done When

_Name the observable condition that makes the task complete._

un test con un repo real con .sldb modificado por dos tareas muestra los cambios agrupados por tarea.

---
id: task-doctor-los-recibos-de-una-tarea-cerrada-quedan-como-alerta-lost
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# doctor: los recibos de una tarea cerrada quedan como alerta 'lost'

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261114-022915-suggestion-doctor-los-recibos-de-una-tarea-cerrada-quedan-como-alerta-lost.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261114-022915-suggestion-doctor-los-recibos-de-una-tarea-cerrada-quedan-como-alerta-lost.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Visto en ftcourier el 14-11. Al cerrar una tarea con closeout commit o resolved-by, el archivo de la tarea se borra y sus ReviewDoc (preflight, bundle, evidence-*) quedan con el sujeto 'lost'. deskops doctor muestra una alerta por recibo para siempre: 10 alertas de FTC-25 y FTC-27. Los recibos son auditoría y no hay que borrarlos. Sugerencia: que el closeout re-ancle los recibos al commit de cierre o los marque archivados, o que doctor no alerte por recibos de tareas cerradas. Aparte: en ftcourier el enlace al store de deskops en .sldb/store.yaml tenía un '..' de más (apuntaba a /home/proyectos); se corrigió con 'sldb stores add --replace'.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.

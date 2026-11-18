FILE:desk/tasks/task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada.md
---
sldb:
  by: agent
  at: '2026-11-16T06:06:53Z'
  authority: generated
  via: save_document_payload
id: task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-doctor-los-recibos-de-una-tarea-cerrada-quedan-como-alerta-lost.md
---

# doctor no alerta como lost los recibos de una tarea cerrada

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de ftcourier (14-11, inbox 20261114-022915): al cerrar con closeout commit o resolved-by se borra la tarea y sus ReviewDoc quedan con sujeto 'lost'; doctor muestra una alerta por recibo para siempre (10 en FTC-25 y FTC-27). Los recibos son auditoria y no se borran.

## Goal

_Describe the concrete result this task must produce._

Un recibo cuya tarea se cerro (closeout registrado en git o en el store) no produce alerta lost en doctor: el closeout re-ancla los recibos al commit de cierre o los marca archivados; solo los recibos de tareas que desaparecieron sin cierre siguen alertando.

## Scope

_State what is in scope and what is out of scope._

deskops/services/closure.py (closeout commit y resolved-by), deskops doctor, deskops/models/review.py; el estado del ancla lo da sldb, deskops no recalcula anclas.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- test nuevo de deskops (nombre a fijar al promover) con closeout real y doctor

## Done When

_Name the observable condition that makes the task complete._

test: cerrar una tarea con recibos preflight/bundle y correr doctor no da alertas lost; borrar una tarea sin cierre si las da.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


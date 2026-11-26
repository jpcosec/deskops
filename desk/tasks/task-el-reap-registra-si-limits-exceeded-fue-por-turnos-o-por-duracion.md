---
sldb:
  by: agent
  at: '2026-11-26T02:30:06Z'
  authority: generated
  via: create_document
id: task-el-reap-registra-si-limits-exceeded-fue-por-turnos-o-por-duracion
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- ../sala/2026-11-25-planificacion/scion.md
- ../sala/2026-11-25-planificacion/deskops.md
depends_on: []
pills: []
files:
- deskops/dispatch.py
- deskops/models/run.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El reap registra si limits_exceeded fue por turnos o por duración

## Rationale

_Explain why this task exists or the business driver behind it._

Bug del despacho que hoy rompe trabajo en robocop2 (informe del despacho en la sala de planificación, 2026-11-25). JP decidió el 2026-11-25 que entra antes de E1, como excepción al orden de etapas. Hoy el despacho ve activity:limits_exceeded sin saber la causa; el texto está en el log del agente ([LIMITS_EXCEEDED] …) y scion lo necesita para fijar los topes de sus templates.

## Goal

_Describe the concrete result this task must produce._

Cuando reap encuentra un agente en limits_exceeded, imprime y guarda en el RunDoc el motivo (max_turns o max_duration) leído del log del agente.

## Scope

_State what is in scope and what is out of scope._

Entra: reap en dispatch.py y el RunDoc. Sale: cambiar los topes (los fija scion con este dato).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer la línea [LIMITS_EXCEEDED] del log del agente por scion. 2) Guardar el motivo en el RunDoc. 3) Test con un log de ejemplo de cada motivo.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests -k 'reap'

## Done When

_Name the observable condition that makes the task complete._

El RunDoc de un agente cortado dice si fue por turnos o por duración.

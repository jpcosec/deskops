---
sldb:
  by: agent
  at: '2026-11-25T22:54:34Z'
  authority: generated
  via: save_document_payload
id: task-escenarios-del-workflow-escritos-para-fallar-hoy-cerrar-desde-ejecucion-con-tests-rojos-fuera-del-bo
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-suite-de-tests-nueva-por-capa-escenarios-del-nucleo-operacion-con-repos-git-temporales-y-contrato-de
pills: []
files:
- tests/core/
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Escenarios del workflow escritos para fallar hoy: cerrar desde ejecución, con tests rojos, fuera del Board, sin tipo, con recibo humano o autoaprobado

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Tests de escenario en tests/core que documentan cada hallazgo del núcleo (W3, N3, W4/N10, N1, N9) en sus dos versiones: el workflow exige el gate y bloquea, el workflow lo apaga y deja pasar.

## Scope

_State what is in scope and what is out of scope._

Entra: un escenario por hallazgo, marcados xfail con el id del hallazgo. Sale: arreglarlos (cada tarea de E3 quita su xfail).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Desk mínimo con su lifecycle. 2) Un escenario por hallazgo, con el workflow exigiendo y apagando el gate. 3) xfail con el id.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core

## Done When

_Name the observable condition that makes the task complete._

Cada hallazgo del núcleo tiene su escenario marcado xfail.

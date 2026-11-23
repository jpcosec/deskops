---
sldb:
  by: agent
  at: '2026-11-23T11:27:26Z'
  authority: generated
  via: create_document
id: task-el-reap-del-intento-n-de-un-ejecutor-encola-el-tester-aunque-la-tarea-ya-este-en-ritual-testing
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El reap del intento N de un ejecutor encola el tester aunque la tarea ya este en ritual-testing

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-082659-unclear-reintento-de-ejecutor-no-encola-tester-tras-el-reap: tras un FALLA el intento 2 commitea, hace advance y el reap integra, pero no se encola dispatch-tester porque la tarea ya estaba en ritual-testing; el coordinador lo encola a mano.

## Goal

_Describe the concrete result this task must produce._

Despues de integrar el commit de un ejecutor, dispatch reap encola dispatch-tester de la tarea si no hay un tester vivo ni pendiente, sea el intento que sea.

## Scope

_State what is in scope and what is out of scope._

deskops/dispatch.py (reap) y sus tests; nada de la maquina de estados de rituales.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. En reap, tras integrar commits de un ejecutor, comprobar si la cola ya tiene dispatch-tester pendiente o un tester vivo de la tarea. 2. Si no, encolar dispatch-tester. 3. Test: tarea en ritual-testing, intento 2 reapeado -> queda un dispatch-tester pendiente; con uno ya pendiente no se duplica.

## Validation

_List the checks required before this task can close._

- pytest -q tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_dispatch.py cubre el caso del intento 2 y el de no duplicar; pasan.

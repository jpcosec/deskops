---
sldb:
  by: agent
  at: '2026-11-22T10:49:16Z'
  authority: generated
  via: save_document_payload
id: task-dispatch-start-tester-no-lanza-si-la-rama-del-ejecutor-de-la-tarea-todavia-no-esta-integrada
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- deskops/dispatch.py
- tests/test_dispatch.py
- a8a7c3e8b2fa3d853ca0470e005eebc44f923991
depends_on: []
pills: []
files:
- CHANGELOG.md
- deskops/dispatch.py
- tests/test_dispatch.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-dispatch-start-tester-espera-a-que-la-rama-del-ejecutor-este-integrada
---

# dispatch start tester no lanza si la rama del ejecutor de la tarea todavía no está integrada

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21, sldb (notations validate): el reap del ejecutor falló al traer su rama (conflicto con el store sin commitear del checkout principal), pero el hook ya había encolado el tester, que se lanzó y probó main sin el cambio. Su veredicto no habría valido; el coordinador lo detuvo, trajo el commit y re-encoló el tester.

## Goal

_Describe the concrete result this task must produce._

dispatch start tester sale con EXIT_BUSY (3, así la cola lo reintenta) e imprime 'en espera: la rama deskops/<ejecutor> de la tarea no está integrada' si existe alguna rama deskops/<nombre> de un ejecutor de esa tarea (por scion_child_identity, intentos 1 y 2) con commits que no están en la rama principal. Cuando el reap la integra y la borra, el tester lanza.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/dispatch.py (start, rol tester), tests/test_dispatch.py y CHANGELOG.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: con una rama deskops/<ejecutor> con un commit fuera de main, start tester sale 3 con ese mensaje; sin la rama, lanza. p2: implementar. p3: CHANGELOG; commit con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo y tests/test_dispatch.py pasan.

---
sldb:
  by: agent
  at: '2026-11-21T05:35:34Z'
  authority: generated
  via: save_document_payload
id: task-integrate-no-empuja-el-commit-de-codigo-por-separado-cuando-no-avanza-rapido-sobre-el-remoto-lo-llev
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- deskops/integrate.py
- tests/test_integrate.py
- 238099a6e62efdaaa7bc1d6bb3b50b6fe39eefbd
depends_on: []
pills: []
files:
- CHANGELOG.md
- deskops/integrate.py
- tests/test_integrate.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-integrate-no-empuja-por-separado-un-commit-de-codigo-que-no-avanza-rapido-sobre-el-remoto
---

# integrate no empuja el commit de código por separado cuando no avanza rápido sobre el remoto; lo lleva el tip

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21, sldb: con el tip extendido sobre un merge de origin/main (e727297a), integrate de notations validate falló en el paso push: 'git push origin 5c1740d2:main ! [rejected] (non-fast-forward)'. _steps (deskops/integrate.py, línea 347) empuja primero el commit de código si no está en el remoto y después el tip; pero cuando el desk mergeó el remoto después del closeout, el commit de código no desciende del remoto y su push solo es rechazado, aunque el tip (que lo contiene y sí desciende del remoto) avanzaría bien.

## Goal

_Describe the concrete result this task must produce._

En _steps, la lista de pushes incluye 'git push origin <code>:<branch>' solo si el commit de código no está en remote_ref Y remote_ref es ancestro del commit de código (git merge-base --is-ancestor remote_ref code en la copia da 0). Si el commit de código no está en el remoto y no avanza rápido sobre él, se omite su push e imprime 'código va con el tip: <code corto>'; el push del tip, que ya pasó el chequeo de fast-forward, lo lleva. El caso normal (el código avanza rápido) no cambia.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/integrate.py (_steps, alrededor de code_in_origin, línea 347), tests/test_integrate.py y CHANGELOG. Fuera: el resto.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes, en tests/test_integrate.py, reusando el escenario de test_tip_extends_over_a_merge_of_the_remote_branch (el remoto recibe un commit de código de otro, el desk lo mergea después del closeout): integrate sin --dry-run contra el bare remoto termina en ok, el remoto queda en el tip y contiene el commit de código. p2: implementar la condición. p3: CHANGELOG; commit desde el worktree que dispatch te da, con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo y tests/test_integrate.py pasan.

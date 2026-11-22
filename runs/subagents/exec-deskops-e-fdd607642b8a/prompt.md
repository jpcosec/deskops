Task: task-dispatch-start-tester-no-lanza-si-la-rama-del-ejecutor-de-la-tarea-todavia-no-esta-integrada
Title: dispatch start tester no lanza si la rama del ejecutor de la tarea todavía no está integrada
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-21T02:33:30Z'
  authority: generated
  via: create_document
id: task-dispatch-start-tester-no-lanza-si-la-rama-del-ejecutor-de-la-tarea-todavia-no-esta-integrada
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
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
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

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-dispatch-start-tester-no-lanza-si-la-rama-del-ejecutor-de-la-tarea-todavia-no-esta-integrada"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-fdd607642b8a`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-fdd607642b8a

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

Task: task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej
Title: dispatch deja commiteados los RunDoc que escribe, para que el reap pueda traer al main commits del ejecutor que tocan el store
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
  at: '2026-11-21T02:26:22Z'
  authority: generated
  via: create_document
id: task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej
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

# dispatch deja commiteados los RunDoc que escribe, para que el reap pueda traer al main commits del ejecutor que tocan el store

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21, sldb: el reap de la tarea notations validate falló al hacer cherry-pick de deskops/deskops-e-8eb91b4956b3 sobre main: 'Los cambios locales de los siguientes archivos serán sobrescritos: .sldb/core/store_index.yaml'. dispatch start (record_scion_run) escribe el RunDoc del agente en el store del checkout principal (store.yaml, store_index.yaml, models/RunDoc.yaml y el shard) y no lo commitea. Si el commit del ejecutor también toca el store (por ejemplo, selfdoc sync), el cherry-pick choca. El coordinador tuvo que commitear los RunDoc a mano y re-encolar el reap.

## Goal

_Describe the concrete result this task must produce._

Ningún reap falla porque el checkout principal tenga sin commitear el store que escribió dispatch. dispatch start commitea en la rama principal, con pathspec, solo los archivos del store que record_scion_run tocó ('git commit -- <rutas>', mensaje 'run: <agente>' y [skip ci]). Además, reap, antes del cherry-pick, commitea igual cualquier RunDoc pendiente de sus agentes. Si queda otro cambio local que choca, el mensaje de error nombra los archivos y sugiere commitearlos.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/dispatch.py (start y reap) o deskops/runtime/scion.py (record_scion_run), tests/test_dispatch.py y CHANGELOG. Fuera: el resto.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: un repo temporal con store, start escribe el RunDoc, el ejecutor (simulado) commitea en su rama un cambio a store_index.yaml, y reap trae el commit sin error. p2: implementar el commit con pathspec en start, y en reap antes del cherry-pick. p3: CHANGELOG, y commit con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo y tests/test_dispatch.py pasan.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-e5f89cdffe35`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-e5f89cdffe35

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

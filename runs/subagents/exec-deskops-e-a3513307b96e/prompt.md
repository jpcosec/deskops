Task: task-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-sin-depender-del-idioma-de-git-falla-con-lang-e
Title: reap nombra los archivos que bloquean el cherry-pick sin depender del idioma de git (falla con LANG=es_ES del timer)
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
  at: '2026-11-21T11:47:23Z'
  authority: generated
  via: create_document
id: task-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-sin-depender-del-idioma-de-git-falla-con-lang-e
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

# reap nombra los archivos que bloquean el cherry-pick sin depender del idioma de git (falla con LANG=es_ES del timer)

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: tests/test_dispatch.py::test_reap_names_the_files_when_local_changes_block_the_pick (línea 514, del arreglo de RunDoc d42ee663) falló en las dos suites completas de integrate y pasa a mano. Reproducido: con LANG=es_CL.UTF-8 LC_ALL=es_CL.UTF-8 LANGUAGE=es falla y con en_US pasa. El timer deskops-queue corre con LANG=es_ES.UTF-8 (systemctl --user show-environment), así que git responde 'realiza un commit con tus cambios...' y el reap no encuentra los archivos que espera leer del mensaje en inglés. En producción, el aviso del reap tampoco nombra los archivos.

## Goal

_Describe the concrete result this task must produce._

dispatch reap identifica los archivos locales que bloquean el cherry-pick sin parsear el mensaje localizado de git: o corre los comandos de git cuya salida parsea con LC_ALL=C y LANGUAGE= en el entorno, o calcula los archivos con git status --porcelain y la lista de archivos del commit. El mensaje sigue nombrando los archivos y sugiriendo commitearlos, con el mismo rc 8. El test pasa con cualquier locale, y se agrega un test que lo corre con LANG/LC_ALL/LANGUAGE en español.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/dispatch.py (reap), y deskops/runtime si es donde se corre git; tests/test_dispatch.py y CHANGELOG. Fuera: el resto.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: el mismo escenario con LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es en el entorno del subproceso (hay locales es_*.utf8 instalados). p2: buscar en deskops/ los sitios que parsean stdout o stderr de git por texto (grep -rn 'would be overwritten\|Your local changes' deskops/) y forzar LC_ALL=C en esos subprocess, o reemplazar el parseo por porcelain. p3: correr tests/test_dispatch.py con -n 4 y con el locale español. p4: CHANGELOG; commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_dispatch.py pasa con LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es y con en_US.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-sin-depender-del-idioma-de-git-falla-con-lang-e"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-a3513307b96e`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-a3513307b96e

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

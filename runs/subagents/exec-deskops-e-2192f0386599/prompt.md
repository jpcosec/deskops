Task: task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de
Title: La cola reintenta el reap que espera (exit 3), y hay un comando de deskops para editar los trabajos de la cola en desk/config.json
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
  at: '2026-11-22T19:44:03Z'
  authority: generated
  via: create_document
id: task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de
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

# La cola reintenta el reap que espera (exit 3), y hay un comando de deskops para editar los trabajos de la cola en desk/config.json

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-22: con el arreglo del reap (1bb918d5), dispatch reap sale 3 (EXIT_BUSY) y escribe 'en espera: <agente> sigue vivo' cuando el agente vive o su worktree está sucio. Pero el trabajo dispatch-reap de desk/config.json no tiene retry_exit_codes [3], a diferencia de dispatch-executor y dispatch-tester, así que el reap en espera termina en runs/queue/failed y la tarea queda trabada: le pasó a graph-missing a las 18:35 y el coordinador lo re-encoló a mano. No hay comando de deskops para editar desk/config.json (deskops edit no tiene 'config' ni 'queue-job'); el retry de executor y tester se agregó a mano en ef84b70d, antes de la regla de solo CLI.

## Goal

_Describe the concrete result this task must produce._

1) dispatch-reap queda con retry_exit_codes [3] en el config por defecto de deskops init (deskops/data o donde se genere) y en el desk/config.json de deskops, aplicado con el comando del punto 2, no a mano. 2) Un comando deskops queue job set <trabajo> <campo> <valor> --root . (o el nombre que encaje con el CLI existente) edita un trabajo de la cola en desk/config.json, valida el resultado y no toca nada más del archivo.

## Scope

_State what is in scope and what is out of scope._

Dentro: el CLI de queue (deskops/cli), el config por defecto de init, desk/config.json de deskops vía el comando nuevo, tests y CHANGELOG. Fuera: otros desks (sldb e IR los aplica el coordinador con el comando nuevo).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test del comando nuevo: en un desk temporal, set de retry_exit_codes para dispatch-reap; el JSON queda válido y solo cambia ese trabajo. p2: test de que el config por defecto de init trae retry_exit_codes [3] en dispatch-reap. p3: implementar. p4: aplicar el comando en este desk. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue_cli.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan y desk/config.json de deskops tiene retry_exit_codes [3] en dispatch-reap.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-2192f0386599`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-2192f0386599

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

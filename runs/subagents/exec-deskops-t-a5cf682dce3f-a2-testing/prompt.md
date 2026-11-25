Task: task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de
Title: La cola reintenta el reap que espera (exit 3), y hay un comando de deskops para editar los trabajos de la cola en desk/config.json
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-22T23:37:20Z'
  authority: generated
  via: save_document_payload
id: task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-a5cf682dce3f FALLA sobre e95bdb13.
  Lo funcional está bien: ''deskops queue job set dispatch-reap retry_exit_codes [3]
  --json'' funciona, y tanto el template como desk/config.json tienen el retry. Faltan
  dos registros del subcomando nuevo:


  (1) tests/test_command_registry.py:

  - test_registry_paths_match_help_goldens: sobran (''queue'', ''job'') y (''queue'',
  ''job'', ''set'') frente a los goldens;

  - test_mutating_commands_are_declared_explicitly: MUTATING_COMMANDS no declara (''queue'',
  ''job'', ''set''). El grupo (''queue'', ''job'') no muta: decláralo igual que los
  otros grupos.


  (2) tests/test_output_goldens.py::test_help_goldens: help/deskops_queue.txt no lista
  ''job'', y faltan los goldens de ''queue job'' y ''queue job set''.


  Intento 2:

  - agregar el subcomando a MUTATING_COMMANDS como los demás;

  - regenerar los goldens de ayuda con ''python -m pytest -q tests/test_output_goldens.py
  --update-golden'', y revisar con git status que solo cambien deskops_queue.txt y
  los dos goldens nuevos;

  - correr tests/test_command_registry.py, tests/test_output_goldens.py, tests/test_queue.py
  y tests/test_queue_cli.py, y la suite con -n 4;

  - commitear desde tu worktree con ''git commit -- <rutas>'' y el trailer Task-Id.'
- task_activates
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

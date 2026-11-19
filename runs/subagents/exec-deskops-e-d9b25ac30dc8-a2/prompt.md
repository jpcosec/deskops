Task: task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid
Title: queue run deja en espera un trabajo de dispatch start que responde ocupado, en vez de marcarlo fallido
Status: active
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-19T13:14:18Z'
  authority: generated
  via: save_document_payload
id: task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-8940972f7883 FALLA sobre 00ec6562 (informe
  en runs/subagents/exec-deskops-t-8940972f7883-testing/). El Goal se cumple, pero
  faltan dos requisitos de las resoluciones aceptadas (preflight-1 y bundle-1): 1)
  el JSON del trabajo que vuelve a pending debe sumar un contador ''attempts'' (1
  al primer reintento, 2 al segundo); hoy la clave no aparece; 2) el mensaje debe
  ser exactamente ''en espera: <id> ocupado (exit <n>)'', y hoy falta el sufijo ''(exit
  3)''. Intento 2: agregar los dos y ampliar test_retry_exit_code_leaves_job_pending
  para que compruebe attempts tras dos corridas y el mensaje exacto con ''(exit 3)''.'
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# queue run deja en espera un trabajo de dispatch start que responde ocupado, en vez de marcarlo fallido

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-19, desk de sldb: se encolaron dos dispatch-executor seguidos. queue run --all corrió el segundo con el primer ejecutor vivo; dispatch start salió con 3 ('ocupado: deskops-e-b1aa0bc85d34'), la cola lo movió a failed, dejó una nota unclear y se detuvo. El coordinador tuvo que re-encolarlo a mano.

## Goal

_Describe the concrete result this task must produce._

Cuando el comando de un trabajo sale con el código que dispatch usa para 'ocupado' (3), queue run lo deja en pending para la próxima corrida, imprime 'en espera: <id> ocupado' y sigue con el resto (o se detiene sin fallar), igual que con los gates de memoria. Cualquier otro código distinto de 0 sigue siendo un fallo.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/queue.py (queue run) y su test; un campo opcional por tipo de trabajo en queue_jobs, 'retry_exit_codes' (lista de enteros, default vacío), y en la configuración de los desks dispatch-executor y dispatch-tester con [3]; docs/operator-manual.md (Host queue) y CHANGELOG. Fuera: cambiar los códigos de dispatch.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: un trabajo cuyo comando sale con 3 y retry_exit_codes [3] queda en pending después de queue run, sin nota unclear; con otro código va a failed como hoy. p2: implementar en queue.py. p3: docs y CHANGELOG. p4: commit con rutas nombradas y Task-Id; el integrador agrega retry_exit_codes a los config.json de deskops, sldb e IR después de integrar.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan y la suite completa de deskops pasa (la corre integrate).

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

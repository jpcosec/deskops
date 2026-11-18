FILE:desk/tasks/task-deskops-dispatch-reap-encuentra-los-agentes-sin-el-archivo-de-la-tarea-el-ejecutor-commitea-con-task.md
---
sldb:
  by: agent
  at: '2026-11-18T16:43:44Z'
  authority: generated
  via: save_document_payload
id: task-deskops-dispatch-reap-encuentra-los-agentes-sin-el-archivo-de-la-tarea-el-ejecutor-commitea-con-task
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

# deskops dispatch: reap encuentra los agentes sin el archivo de la tarea, el ejecutor commitea con Task-Id y el tester pi corre solo los tests de lo tocado

## Rationale

_Explain why this task exists or the business driver behind it._

Primera corrida real del despacho automático (2026-11-18, tarea roles_root). (1) dispatch reap falló con 'tarea no encontrada' porque la cola lo corrió después de closeout commit, que borra el TaskDoc (nota 20261118-130333-unclear-queue-20261118t160301z-dispatch-reap-task-deskops-dispatch-toma-los-roles-del-desk-de-deskops-para-tareas-de-otros-desks-sldb-ir-y-deskops-int). (2) El ejecutor deskops-e-19b2ea183813 dejó su código sin commitear: el prompt que arma dispatch start no pide commit con trailer Task-Id, y el integrador tuvo que commitear a mano con rutas nombradas, sorteando trabajo ajeno sin commitear. (3) El tester pi deskops-t-1093bfcd825b corrió la suite completa en un solo proceso, llegó al límite de 2 h al 88 % y no dejó informe; la suite completa ya la corre integrate en el host.

## Goal

_Describe the concrete result this task must produce._

Un reap encolado después del cierre detiene y borra los agentes de la tarea igual. El ejecutor despachado entrega un commit de código con rutas nombradas y Task-Id. El tester pi entrega su informe dentro del límite, corriendo solo los tests de los archivos tocados.

## Scope

_State what is in scope and what is out of scope._

En alcance: (a) dispatch.reap (deskops/dispatch.py, def reap) hoy calcula la etiqueta con scion_child_identity(task_path, ...), que lee el TaskDoc, y por eso falla si la tarea ya se cerró. Debe calcularla con _scion_task_label(task_id) (deskops/runtime/scion.py:224: 't-' + los primeros 61 hex de sha256(task_id)), que no lee archivos. El resto de reap no cambia: mismo criterio de terminado (phase, activity, result-summary.md), stop y después delete por agente, 'vivo' y rc 4 si queda alguno vivo. Si un stop o un delete de scion falla, imprime '<nombre> <rol> error:<código>' y sigue con el siguiente agente; ese caso también da rc distinto de 0. (b) El prompt.md que escribe dispatch start para el rol executor termina con estas instrucciones: commitear solo los archivos que el ejecutor cambió para la tarea, nombrados uno por uno (los mismos que lista en result-summary.md), nunca git add -A, git add -u sobre todo el árbol ni git stash, porque puede haber trabajo ajeno sin commitear; mensaje con el trailer 'Task-Id: <id de la tarea>'; sin push; y recién después deskops advance task. (c) El prompt.md del rol tester le dice cómo ubicar el trabajo: 'git log -1 --format=%H --grep "Task-Id: <id>"' da el commit del ejecutor y 'git show --name-only <commit>' sus archivos. Los tests a correr son los archivos tests/*.py de ese commit, más tests/test_<módulo>.py cuando exista para cada módulo de código tocado; de a uno, con TMPDIR=/tmp. El tester escribe result-summary.md con veredicto PASA o FALLA en la primera línea, y el prompt aclara que la suite completa la corre integrate en el host. Fuera de alcance: cambiar la cola o integrate.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: reap con la tarea ya borrada del desk encuentra y borra el agente (scion simulado). p2: implementar (a). p3: tests de los textos de prompt.md por rol (executor con Task-Id y rutas nombradas; tester con solo los tests tocados) e implementación. p4: docs/operator-manual.md (sección de dispatch) y CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm python -m pytest -q tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan y la suite completa de deskops pasa (la corre integrate).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-dispatch-reap-encuentra-los-agentes-sin-el-archivo-de-la-tarea-el-ejecutor-commitea-con-task: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


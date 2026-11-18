---
sldb:
  by: agent
  at: '2026-11-18T16:04:19Z'
  authority: generated
  via: create_document
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

En alcance: (a) dispatch.reap identifica los agentes por la etiqueta deskops.task_id; si el TaskDoc ya no está, usa el id de la tarea (hash de deskops.task_id calculado del id) y sigue, sin fallar. (b) El prompt.md que escribe dispatch start para el rol executor termina con la instrucción de commitear con rutas nombradas (nunca git add -A ni -u sobre el árbol, porque puede haber trabajo ajeno sin commitear) y el trailer Task-Id: <id>, sin push, antes de deskops advance. (c) El prompt.md del rol tester pide solo los tests de los archivos del diff del commit del ejecutor y escribir result-summary.md con veredicto PASA o FALLA; nombra que la suite completa la corre integrate. Fuera de alcance: cambiar la cola o integrate.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: reap con la tarea ya borrada del desk encuentra y borra el agente (scion simulado). p2: implementar (a). p3: tests de los textos de prompt.md por rol (executor con Task-Id y rutas nombradas; tester con solo los tests tocados) e implementación. p4: docs/operator-manual.md (sección de dispatch) y CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm python -m pytest -q tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan y la suite completa de deskops pasa (la corre integrate).

---
sldb:
  by: agent
  at: '2026-11-25T01:07:09Z'
  authority: generated
  via: create_document
id: task-closeout-encola-un-solo-integrate-cuando-cierra-la-ultima-tarea-de-la-fase
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase
- task-integrate-por-lote-una-sola-integracion-por-desk-con-todo-lo-cerrado-pendiente-un-tip-una-suite-un-g
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# closeout encola un solo integrate cuando cierra la ultima tarea de la fase

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-160333-suggestion-jp-integrar-por-lote-una-suite-y-un-push-por-desk-y-ordenar-los-fallidos-de-la-cola y la precision de JP (el lote es la fase del Board). Hoy cada cierre encola su propio integrate y su suite.

## Goal

_Describe the concrete result this task must produce._

Al cerrar una tarea que pertenece a una fase del Board: si quedan tareas abiertas en la fase no se encola nada; si era la ultima se encola un solo trabajo integrate --phase, sin duplicar uno pendiente. Una tarea sin fase encola su integrate como hoy.

## Scope

_State what is in scope and what is out of scope._

El disparo desde closeout y deskops/queue.py (sin duplicados), el job integrate de desk/config.json si necesita pasar la fase, y sus tests. Fuera: integrate --phase (ya hecho en task-integrate-por-lote-una-sola-integracion-por-desk-con-todo-lo-cerrado-pendiente-un-tip-una-suite-un-g), limpieza de failed, skill.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer donde closeout encola integrate hoy. 2) Si la tarea esta en una fase: contar abiertas; encolar integrate --phase solo al cerrar la ultima, y no si ya hay uno pendiente de esa fase. 3) Tests: fase de tres tareas, los dos primeros cierres no encolan, el tercero encola uno; sin fase, igual que hoy. Correr solo tests/test_queue.py y el test del closeout tocado.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_queue.py

## Done When

_Name the observable condition that makes the task complete._

Con una fase de tres tareas solo el tercer cierre encola un integrate --phase y no se duplica; una tarea sin fase encola como antes; tests tocados verdes.

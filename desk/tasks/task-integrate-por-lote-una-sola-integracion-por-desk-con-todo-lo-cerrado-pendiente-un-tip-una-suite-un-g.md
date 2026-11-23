---
sldb:
  by: agent
  at: '2026-11-23T19:16:24Z'
  authority: generated
  via: save_document_payload
id: task-integrate-por-lote-una-sola-integracion-por-desk-con-todo-lo-cerrado-pendiente-un-tip-una-suite-un-g
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261123-160333-suggestion-jp-integrar-por-lote-una-suite-y-un-push-por-desk-y-ordenar-los-fallidos-de-la-cola.md
- desk/inbox/20261123-161332-suggestion-jp-el-lote-de-integraci-n-es-la-fase-del-dag-declarada-en-el-board-falta-en-la-herramienta-y-en-el-skill.md
depends_on:
- task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# integrate por fase: la unidad de integracion es la fase del Board (una suite, un grafo, un store y un push por fase)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-160333-suggestion-jp-integrar-por-lote-una-suite-y-un-push-por-desk-y-ordenar-los-fallidos-de-la-cola (JP 2026-11-23): los 12 trabajos de runs/queue/failed (10 integrate y 2 dispatch-reap del 21 al 23-nov) son problemas de workflow, no de las tareas; todas llegaron a origin despues con otro integrate. Hoy integrate corre una vez por tarea: cada cierre dispara una suite completa (~30-45 min) y un push, y uno que falla por fast-forward, grafo o una prueba sensible al host deja su trabajo en failed aunque el siguiente lo suba.

## Goal

_Describe the concrete result this task must produce._

deskops integrate toma como unidad la fase declarada en el Board: cada tarea de la fase cierra con su validacion dirigida; cuando cierra la ultima tarea de la fase se encola un solo trabajo integrate de esa fase, que corre una suite completa, una comprobacion de grafo y una de store sobre el tip y hace un push (o un PR en modo pr) y el commit de cierre de fase de ritual-phase; un integrate exitoso da por resueltos los integrate anteriores de ese desk que quedaron en failed y cuyo contenido ya esta en origin. Una tarea sin fase declarada se integra como fase de una sola tarea.

## Scope

_State what is in scope and what is out of scope._

deskops/integrate.py (opcion --phase), deskops/queue.py (encolado del integrate de fase al cerrar la ultima tarea, sin duplicados), el disparo desde closeout, el trabajo integrate de desk/config.json (--task-from-env pasa a la fase de la tarea) y sus tests. Fuera: el modelo del Board (tarea task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase) y el skill.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Encolar integrate por desk: si ya hay uno pendiente, no se agrega otro (o se funden sus tareas en el mismo trabajo). 2) integrate sin --task o con varias tareas: integra el tip local completo. 3) Al terminar bien, recorrer failed de integrate del desk y mover a done los que ya estan en origin, con una nota. 4) Tests de encolado, fusion y limpieza de failed.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp pytest -q tests/test_integrate.py tests/test_queue.py

## Done When

_Name the observable condition that makes the task complete._

Con una fase de tres tareas: los dos primeros cierres no encolan integrate; el tercero encola uno solo, que sube las tres con una suite y un push; un integrate exitoso limpia los integrate fallidos ya presentes en origin; tests nuevos y los de integrate y queue verdes.

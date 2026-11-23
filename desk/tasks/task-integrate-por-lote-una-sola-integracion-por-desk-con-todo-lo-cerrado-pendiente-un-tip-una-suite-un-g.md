---
sldb:
  by: agent
  at: '2026-11-23T19:05:41Z'
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
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# integrate por lote: una sola integracion por desk con todo lo cerrado pendiente (un tip, una suite, un grafo, un store, un push)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-160333-suggestion-jp-integrar-por-lote-una-suite-y-un-push-por-desk-y-ordenar-los-fallidos-de-la-cola (JP 2026-11-23): los 12 trabajos de runs/queue/failed (10 integrate y 2 dispatch-reap del 21 al 23-nov) son problemas de workflow, no de las tareas; todas llegaron a origin despues con otro integrate. Hoy integrate corre una vez por tarea: cada cierre dispara una suite completa (~30-45 min) y un push, y uno que falla por fast-forward, grafo o una prueba sensible al host deja su trabajo en failed aunque el siguiente lo suba.

## Goal

_Describe the concrete result this task must produce._

deskops integrate integra de una vez todo lo cerrado y pendiente de subir del desk: toma el tip local, corre una suite completa, una comprobacion de grafo y una de store, y hace un solo push (o un PR en modo pr); varios cierres seguidos encolan un solo trabajo de integrate por desk (los repetidos se funden); un integrate que termina bien da por resueltos los trabajos de integrate anteriores de ese desk que quedaron en failed y cuyo contenido ya esta en origin.

## Scope

_State what is in scope and what is out of scope._

deskops/integrate.py, deskops/queue.py (encolado y fusion de trabajos integrate por desk), el disparo desde closeout, y sus tests. Fuera: dispatch y reap.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Encolar integrate por desk: si ya hay uno pendiente, no se agrega otro (o se funden sus tareas en el mismo trabajo). 2) integrate sin --task o con varias tareas: integra el tip local completo. 3) Al terminar bien, recorrer failed de integrate del desk y mover a done los que ya estan en origin, con una nota. 4) Tests de encolado, fusion y limpieza de failed.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp pytest -q tests/test_integrate.py tests/test_queue.py

## Done When

_Name the observable condition that makes the task complete._

Tres cierres seguidos dejan un solo trabajo de integrate pendiente; un integrate exitoso sube los tres con una sola suite y un push y limpia los integrate fallidos ya presentes en origin; tests nuevos y la suite de integrate y queue verdes.

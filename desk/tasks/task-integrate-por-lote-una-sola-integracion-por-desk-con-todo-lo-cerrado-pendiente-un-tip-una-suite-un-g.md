---
sldb:
  by: agent
  at: '2026-11-25T01:06:45Z'
  authority: generated
  via: save_document_payload
id: task-integrate-por-lote-una-sola-integracion-por-desk-con-todo-lo-cerrado-pendiente-un-tip-una-suite-un-g
status: draft
summary: ''
tags: []
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

deskops integrate --phase <fase> integra de una vez todas las tareas cerradas de esa fase del Board: un tip, una suite completa, una comprobacion de grafo y de store, un push y el commit de cierre de fase de ritual-phase. Una tarea sin fase se integra como fase de una sola tarea (--task sigue andando).

## Scope

_State what is in scope and what is out of scope._

deskops/integrate.py (opcion --phase y resolucion de las tareas de la fase desde el Board) y tests/test_integrate.py. Fuera: el encolado al cerrar la ultima tarea (task-closeout-encola-un-solo-integrate-cuando-cierra-la-ultima-tarea-de-la-fase), la limpieza de failed (task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin), el modelo del Board y el skill.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer como integrate resuelve hoy la tarea y el tip. 2) --phase lee las tareas de la fase del Board, exige que esten todas cerradas y toma el tip que las contiene. 3) Una suite, grafo, store, push y commit de cierre de fase. 4) Tests: fase de dos tareas cerradas se integra con una suite; fase con una abierta falla con mensaje claro; --task sin fase sigue igual. Correr solo tests/test_integrate.py.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_integrate.py

## Done When

_Name the observable condition that makes the task complete._

integrate --phase con dos tareas cerradas corre una sola suite y un push (dry-run en el test); con una tarea abierta falla claro; tests/test_integrate.py verde.

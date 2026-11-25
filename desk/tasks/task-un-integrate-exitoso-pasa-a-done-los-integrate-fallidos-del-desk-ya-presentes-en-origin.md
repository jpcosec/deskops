---
sldb:
  by: agent
  at: '2026-11-25T01:06:55Z'
  authority: generated
  via: create_document
id: task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin
status: draft
summary: ''
tags: []
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

# Un integrate exitoso pasa a done los integrate fallidos del desk ya presentes en origin

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-160333-suggestion-jp-integrar-por-lote-una-suite-y-un-push-por-desk-y-ordenar-los-fallidos-de-la-cola (JP 2026-11-23): los 12 trabajos de runs/queue/failed eran integrate cuyo contenido llego a origin con un integrate posterior; hubo que ordenarlos a mano.

## Goal

_Describe the concrete result this task must produce._

Al terminar bien, deskops integrate recorre runs/queue/failed del desk y mueve a done cada integrate cuyo tip ya es ancestro de origin, dejando una linea en su log de por que.

## Scope

_State what is in scope and what is out of scope._

deskops/integrate.py (paso final) y su test. Fuera: fases, encolado, otros tipos de trabajo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Tras el push exitoso, listar failed/*-integrate-*. 2) Para cada uno, si su tarea o tip ya esta en origin (merge-base --is-ancestor), moverlo a done con una linea en el log. 3) Test con un failed ya en origin (se mueve) y otro que no (se queda). Correr solo ese test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_integrate.py -k failed

## Done When

_Name the observable condition that makes the task complete._

Tras un integrate exitoso, un failed ya en origin pasa a done con su linea de log y uno ausente queda en failed; el test nuevo pasa.

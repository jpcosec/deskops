FILE:desk/tasks/task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin.md
---
sldb:
  by: agent
  at: '2026-11-25T01:27:50Z'
  authority: generated
  via: save_document_payload
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

Repo: /mnt/ssd/proyectos/SLDB_1/deskops. Solo deskops/integrate.py y tests/test_integrate.py. Activacion: al final de un integrate real (no --dry-run) que termino bien, sea porque hizo push o porque reporto 'ya integrado'. Barrido: los JSON de queue_dir(root)/'failed' (deskops.queue.queue_dir; leer con queue._read_job) con kind == 'integrate'. Criterio por trabajo: tomar su task_id, buscar en la rama local el commit de cierre de esa tarea (git log -1 --format=%H --grep='^Task-Id: <task_id>$' <integrate.branch>); si existe y 'git merge-base --is-ancestor <sha> origin/<integrate.branch>' da 0 (despues del fetch que integrate ya hace), mover el JSON a queue_dir(root)/'done' y agregar al final del archivo de su campo log una linea 'resuelto por integrate <task actual>: <sha> ya en origin/<branch>'. Si no hay commit de cierre o no es ancestro, se deja en failed. Tests nuevos en tests/test_integrate.py con nombres que contengan 'failed' (p. ej. test_integrate_moves_failed_already_in_origin_to_done y test_integrate_keeps_failed_not_in_origin), usando el repo git temporal y el origin bare que ya arman los tests de ese archivo. Correr solo pytest -q tests/test_integrate.py -k failed y luego el archivo entero.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_integrate.py

## Done When

_Name the observable condition that makes the task complete._

Tras un integrate exitoso, un integrate en failed cuyo cierre ya esta en origin pasa a done con su linea de log, y uno cuyo cierre no esta queda en failed; tests/test_integrate.py entero pasa.

FILE:instruccion
Cold-bundle de la tarea task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_integrate.py


FILE:desk/tasks/task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk.md
---
sldb:
  by: agent
  at: '2026-11-21T09:14:31Z'
  authority: generated
  via: create_document
id: task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk
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

# init repara el enlace deskops con la resolución por nombre de sldb (#3): test_init_repairs_a_broken_deskops_link en rojo bloquea todo integrate

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: el integrate de deskops falla en la suite con tests/test_doctor_model_registration.py::test_init_repairs_a_broken_deskops_link ('Replaced broken deskops link' no aparece en la salida de init). Falla igual en origin/main 9d83a152 y en main local, en worktree limpio, así que no lo introdujo ninguna tarea de deskops. Pasaba en el integrate de las 06:09 (a0b2e8fe). Entre medio llegó a /mnt/ssd/herramientas/sldb el PR #3 de sldb (9d8584ad, 'enlaces: un store se enlaza por nombre; la ruta es de cada máquina'): store_links, cuando la ruta de un enlace no existe, lo resuelve por el nombre del store. El test rompe el enlace solo cambiando su path (_point_deskops_link_at, línea 153) hacia un directorio borrado; con la resolución por nombre, el enlace 'deskops' queda ok y apuntando al store dueño, así que bootstrap.py (línea ~265, target == owner) devuelve False sin imprimir el reemplazo. También falló en la suite test_dispatch.py::test_reap_names_the_files_when_local_changes_block_the_pick, que pasa solo (intermitente bajo -n 4, fuera de esta tarea).

## Goal

_Describe the concrete result this task must produce._

La suite de deskops vuelve a verde contra el sldb de herramientas. Decidir con evidencia cuál de las dos cosas es cierta y hacerla: (a) con la resolución por nombre, un enlace cuyo path no existe pero cuyo nombre resuelve al store dueño ya no está roto. Entonces init no tiene nada que reparar y el test se reescribe para lo que sí sigue roto: un enlace 'deskops' cuyo nombre resuelve a otro store o a ninguno, o cuyo status no es ok según store_links. El caso 'path viejo pero resoluble por nombre' pasa a un test propio, donde init no imprime reemplazo y el enlace queda resolviendo al dueño. (b) init tiene que normalizar el path guardado aunque resuelva por nombre; entonces bootstrap.py compara también el path guardado y lo reescribe. Preferir (a) salvo que algo de deskops lea el path guardado sin pasar por store_links (buscar con grep).

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/test_doctor_model_registration.py, deskops/bootstrap.py solo si se elige (b), y CHANGELOG. Fuera: sldb (el PR #3 es correcto) y el test intermitente de dispatch.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: confirmar la causa: con el sldb de herramientas, store_links sobre el store del test después de _point_deskops_link_at da status ok y resolved igual al dueño; anotarlo en el run dir. p2: grep -rn 'store_index\|"path"' deskops/ para ver si algo lee el path guardado sin store_links; decidir (a) o (b). p3: implementar y correr tests/test_doctor_model_registration.py. p4: correr la suite completa con -n 4 una vez y anotar el resultado. p5: CHANGELOG; commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_model_registration.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_doctor_model_registration.py pasa entero contra el sldb de /mnt/ssd/herramientas/sldb y la suite completa no tiene fallas de ese archivo.

FILE:instruccion
Cold-bundle de la tarea task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_model_registration.py


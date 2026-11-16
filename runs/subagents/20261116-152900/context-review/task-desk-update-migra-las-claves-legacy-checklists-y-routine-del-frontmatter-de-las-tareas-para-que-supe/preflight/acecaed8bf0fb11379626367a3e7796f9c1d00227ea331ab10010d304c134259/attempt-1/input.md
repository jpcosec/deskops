FILE:desk/tasks/task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe.md
---
sldb:
  by: agent
  at: '2026-11-16T15:28:46Z'
  authority: generated
  via: save_document_payload
id: task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-103216-unclear-closeout-supersede-rechaza-3-taskdocs-de-marcado-con-claves-checklists-routine.md
depends_on: []
pills: []
files:
- deskops/workspace.py
- deskops/cli/commands/desk.py
- tests/test_legacy_task_states.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# desk update migra las claves legacy checklists y routine del frontmatter de las tareas para que supersede y edit puedan reescribirlas

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de marcado del 2026-11-16 (desk/inbox/20261116-103216-unclear-closeout-supersede-rechaza-3-taskdocs-de-marcado-con-claves-checklists-routine.md). En UIs/marcado, deskops closeout supersede rechaza tres TaskDocs heredados de antes de la migracion (task-close-the-runtime-pipeline-baseline, task-close-the-source-and-marker-model-baseline, task-design-the-runtime-architecture-and-extension-model) con "Refusing to rewrite <id>.md: it has content its model (TaskDoc) does not declare, and rewriting would erase it: frontmatter key 'checklists'; frontmatter key 'routine'". El rechazo sale de write_doc en deskops/doc_access.py (undeclared_frontmatter_keys). desk update dice up to date y no las ve, deskops edit no puede quitarlas y retire exige estado cerrado. Bloquea la tarea de marcado task-cerrar-con-supersede-las-53-tareas-de-spec-y-diseno-de-marcado-b3 (50/53 cerradas). Prioridad 1 del supervisor.

## Goal

_Describe the concrete result this task must produce._

deskops desk update (dry-run) lista cada TaskDoc de desk/tasks cuyo frontmatter tiene la clave checklists o routine, que TaskDoc no declara, con el archivo y la clave, y da rc 1 como cualquier migracion pendiente; deskops desk update --apply quita esas dos claves del frontmatter (sin tocar el resto del documento) e imprime por cada archivo la clave quitada y su valor anterior en una linea, para que quede en la salida y en el commit. Despues de --apply, deskops closeout supersede sobre esa tarea ya no da el error de claves no declaradas. La lista de claves es cerrada (checklists, routine): otras claves no declaradas siguen dando el rechazo actual de write_doc.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/workspace.py (junto a legacy_task_states y migrate_legacy_task_states, que ya migran estados legacy de tareas), deskops/cli/commands/desk.py (el reporte y la condicion de "up to date") y tests en tests/test_legacy_task_states.py. No entra: cambiar write_doc ni su rechazo, agregar un flag a supersede, declarar checklists o routine en TaskDoc, cerrar las tareas de marcado (lo hace su coordinador con el CLI nuevo), ni el fallo de deskops message send sin --root que menciona la misma nota. Precisiones del preflight 1: (a) salida de --apply, una linea por clave quitada con la forma '<ruta relativa a la raiz>: removed <clave> = <valor anterior en JSON compacto de una linea>'. (b) desk update --apply da rc 0 si la migracion termina sin errores, igual que las otras migraciones de --apply; solo el dry-run con claves pendientes da rc 1. (c) Caso mixto: si una tarea tiene checklists o routine y ademas otra clave no declarada, --apply quita igual checklists y routine y deja la otra clave; supersede sigue rechazando la tarea por esa otra clave. (d) La edicion es textual sobre el frontmatter: se borran solo las lineas del bloque de esas claves y las demas claves conservan orden y texto, sin re-serializar el YAML. (e) desk/tasks es el de la raiz del desk (--root), igual que el resto de desk update.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer legacy_task_states y migrate_legacy_task_states en deskops/workspace.py, write_doc y undeclared_frontmatter_keys en deskops/doc_access.py, y el bloque de desk update en deskops/cli/commands/desk.py. 2) Detectar en desk/tasks los TaskDocs con checklists o routine en el frontmatter. 3) Reporte en el dry-run y rc 1. 4) En --apply, reescribir el frontmatter sin esas claves e imprimir clave y valor anterior. 5) Tests en un desk sandbox (tmp_path): una tarea con checklists y routine da el reporte y rc 1 en dry-run; tras --apply el archivo ya no tiene esas claves, conserva el cuerpo y el resto del frontmatter, y closeout supersede sobre ella no da el error de claves no declaradas; una tarea con otra clave no declarada no se toca y supersede sigue rechazandola.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_legacy_task_states.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas, cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los casos del paso 5 pasan y desk update --apply deja una tarea con checklists y routine reescribible por closeout supersede.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


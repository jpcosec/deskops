---
sldb:
  by: agent
  at: '2026-11-16T06:04:57Z'
  authority: generated
  via: save_document_payload
id: task-borrar-la-migracion-de-task-type-viejo-legacy-task-type-keys-y-migrate-task-types-y-sus-tests
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on:
- task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply
pills: []
files:
- deskops/workspace.py
- deskops/cli/commands/desk.py
- tests/test_task_types.py
- tests/test_task_lifecycle_validator.py
- docs/workflow-policy-reference.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-retirar-caminos-legacy-migrar-los-datos-y-borrar-el-c-digo-de-compatibilidad.md
---

# Borrar la migracion de task_type viejo (LEGACY_TASK_TYPE_KEYS y migrate_task_types) y sus tests

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (punto 1). Por DK3 de deskops-como-config, un camino de compatibilidad se borra cuando sus consumidores migraron. Sigue vivo: LEGACY_TASK_TYPE_KEYS en deskops/workspace.py:520, migrate_task_types en :712 y su llamada en deskops/cli/commands/desk.py:452; tests en tests/test_task_types.py:107 y 149.

## Goal

_Describe the concrete result this task must produce._

Se borra el camino de migracion de task_type del desk: en deskops/workspace.py LEGACY_TASK_TYPE_KEYS, _task_type_migration_plan, pending_task_type_migration, _task_type_migration_line y migrate_task_types; en deskops/cli/commands/desk.py el import y el uso de pending_task_type_migration (alrededor de las lineas 25 y 375) y la llamada a la migracion (alrededor de 452); y los tests que ejercitan esas funciones. Se conservan LEGACY_TASK_TYPE_MAP y canonical_task_type_name de deskops/models/task_types.py, porque los usan add task (deskops/services/tasks.py:102) y closeout (deskops/services/closure.py:1222); no son parte de esta tarea. TaskDoc generico sigue aceptando cualquier task_type como hoy (test_generic_task_doc_accepts_empty_legacy_or_any_task_type no cambia); lo unico que deja de existir es que desk update proponga o aplique la migracion. En docs/workflow-policy-reference.md (linea 75) se quita la parte 'and migrates legacy task_type strings (...)' y la oracion termina en 'registers them'.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/workspace.py, deskops/cli/commands/desk.py, tests/test_task_types.py, tests/test_task_lifecycle_validator.py (casos legacy) y docs/workflow-policy-reference.md (la frase de migracion). No entra: otros caminos legacy. Precisiones del preflight 1: la dependencia externa esta cerrada cuando deskops show task task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply --root . da status closed. Casos legacy = los tests que nombran LEGACY_TASK_TYPE_KEYS, migrate_task_types o un task_type viejo sin prefijo (code, implementation, test, docs, spec, design, external, vacio) como valor a migrar, p. ej. test_task_lifecycle_validator.py alrededor de 177 y 290-303. La frase de la doc es la oracion de docs/workflow-policy-reference.md linea 75 que empieza con 'A desk adds its own subtypes' en su parte 'and migrates legacy task_type strings (...)'. Despues del borrado, una tarea con task_type viejo se trata como cualquier task_type desconocido hoy (el validador la reporta); no se agrega comportamiento nuevo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Confirmar que la dependencia externa cerro (deskops show task task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply --root . da status closed). 2) Borrar las funciones y usos listados en el goal. 3) Borrar los tests que llaman a esas funciones (grep -rnE de la validacion sobre tests/). 4) Editar la oracion de la doc. 5) El grep de la validacion queda vacio. 6) Tests.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rnE 'LEGACY_TASK_TYPE_KEYS|migrate_task_types|pending_task_type_migration|_task_type_migration' deskops tests docs
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_task_types.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_task_lifecycle_validator.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El grep queda vacio y la suite no tiene fallas nuevas.

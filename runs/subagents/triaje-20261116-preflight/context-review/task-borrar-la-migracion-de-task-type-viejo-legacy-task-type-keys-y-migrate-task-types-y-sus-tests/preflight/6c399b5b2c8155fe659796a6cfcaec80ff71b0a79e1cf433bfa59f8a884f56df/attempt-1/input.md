FILE:desk/tasks/task-borrar-la-migracion-de-task-type-viejo-legacy-task-type-keys-y-migrate-task-types-y-sus-tests.md
---
sldb:
  by: agent
  at: '2026-11-16T04:04:48Z'
  authority: generated
  via: save_document_payload
id: task-borrar-la-migracion-de-task-type-viejo-legacy-task-type-keys-y-migrate-task-types-y-sus-tests
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
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

El mapa, la funcion, la llamada y los tests legacy desaparecen; desk update ya no migra task_type viejos.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/workspace.py, deskops/cli/commands/desk.py, tests/test_task_types.py, tests/test_task_lifecycle_validator.py (casos legacy) y docs/workflow-policy-reference.md (la frase de migracion). No entra: otros caminos legacy.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Confirmar que la dependencia externa cerro. 2) Borrar. 3) `grep -rn 'LEGACY_TASK_TYPE\|migrate_task_types' deskops tests docs` vacio. 4) Tests.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rn 'LEGACY_TASK_TYPE\|migrate_task_types' deskops tests docs
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_task_types.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_task_lifecycle_validator.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

El grep queda vacio y la suite no tiene fallas nuevas.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-borrar-la-migracion-de-task-type-viejo-legacy-task-type-keys-y-migrate-task-types-y-sus-tests: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


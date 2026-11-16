FILE:desk/tasks/task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0.md
---
sldb:
  by: agent
  at: '2026-11-16T05:02:26Z'
  authority: generated
  via: save_document_payload
id: task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0
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
files:
- deskops/cli/commands/desk.py
- tests/test_cli.py
- tests/fixtures/golden/scaffold/update.json
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-desk-update-crea-desk-reviews-vac-o-y-git-no-lo-guarda-en-un-clon-limpio-el-dry-run-vuelve-a-dar-missing-desk-structure-desk-reviews.md
---

# desk update deja de exigir desk/reviews/ vacio y en un clon limpio el dry-run da rc 0

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (worker de graph_ui, 2026-11-10, commit d98fcea): `deskops desk update --apply` crea desk/reviews/ vacio; git no versiona directorios vacios, y en un clon limpio `deskops desk update` (dry-run) vuelve a reportar 'Missing desk structure: desk/reviews/' con rc 1. Sigue hoy en deskops/cli/commands/desk.py:231-232. doctor no lo exige (deskops/cli/commands/doctor.py:66-70). El servicio de reviews crea su carpeta al escribir (deskops/services/review.py, mkdir con parents=True).

## Goal

_Describe the concrete result this task must produce._

desk update ya no cuenta desk/reviews/ como estructura faltante; la carpeta se crea cuando se escribe el primer recibo. En un repo nuevo: `deskops init .`, commit, clon limpio, `deskops desk update --root <clon>` da rc 0.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/desk.py (quitar el chequeo de desk/reviews/), el golden tests/fixtures/golden/scaffold/update.json si cambia, y tests/test_cli.py. No entra: agregar .gitkeep.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Quitar las lineas 231-232. 2) Verificar que review.py crea desk/reviews al escribir el primer recibo. 3) Test en tests/test_cli.py con git init, init, commit, clone y desk update dry-run rc 0. Precisiones del preflight 1: el codigo a quitar es el if que agrega 'desk/reviews/' a missing_desk_files en deskops/cli/commands/desk.py. El golden scaffold/update.json se actualiza solo si su contenido nombra desk/reviews. El test usa tmp_path, subprocess con git init -b main, deskops init, git add/commit, git clone a otro tmp_path y deskops desk update --root <clon> sin --apply; espera rc 0.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El test del clon limpio pasa con rc 0 y el primer recibo crea desk/reviews/.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


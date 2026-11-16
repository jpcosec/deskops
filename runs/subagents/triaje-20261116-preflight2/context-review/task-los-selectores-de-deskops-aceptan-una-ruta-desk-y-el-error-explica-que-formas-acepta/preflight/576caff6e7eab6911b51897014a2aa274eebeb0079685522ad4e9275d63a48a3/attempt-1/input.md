FILE:desk/tasks/task-los-selectores-de-deskops-aceptan-una-ruta-desk-y-el-error-explica-que-formas-acepta.md
---
sldb:
  by: agent
  at: '2026-11-16T05:02:52Z'
  authority: generated
  via: save_document_payload
id: task-los-selectores-de-deskops-aceptan-una-ruta-desk-y-el-error-explica-que-formas-acepta
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md
files:
- deskops/desk_paths.py
- deskops/doc_access.py
- deskops/cli/registry.py
- tests/test_desk_paths.py
- tests/test_tracked_selector_resolution.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-mepu-selector-por-ruta-en-edit-task-y-diagn-stico-drawer.md
---

# Los selectores de deskops aceptan una ruta desk/... y el error explica que formas acepta

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (MEPU, 2026-10-28): `deskops edit task desk/drawer/tasks/<archivo>.md scope ...` falla con 'No artifact.task file found for selector ...', aunque con el stem funciona. Hoy deskops/desk_paths.py:56-64 y deskops/doc_access.py:671-694 comparan solo nombre, stem o prefijo; editable_artifact (doc_access.py:728-737) ya busca tambien en el drawer.

## Goal

_Describe the concrete result this task must produce._

Un selector que es una ruta relativa al repo (desk/...) o absoluta dentro del desk resuelve al mismo artefacto que su stem; un selector que no resuelve da un error que lista las formas aceptadas (id exacto, nombre de archivo, stem, fragmento unico, ruta desk/...). La ayuda de edit task trae un ejemplo con un item del drawer.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/desk_paths.py, deskops/doc_access.py, el texto de ayuda de edit task en deskops/cli/registry.py y sus goldens. No entra: la legibilidad de promote inbox-to-drawer-task (ese camino no se usa para el inbox). Precisiones del preflight 1: normalizacion: si el selector contiene '/', se resuelve con Path(root, selector).resolve() (o tal cual si es absoluto); si cae dentro de <root>/desk se usa su stem; si cae fuera, error 'el selector apunta fuera de desk/'. '..' se resuelve con resolve(); los symlinks no se tratan aparte. La resolucion por fragmento unico no cambia (sigue dando el error de ambiguedad actual). El golden afectado es tests/fixtures/golden/help/deskops_edit_task.txt; el ejemplo de ayuda usa la ruta literal desk/drawer/tasks/<item>.md.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Normalizar el selector: si contiene '/', resolver contra la raiz del repo y quedarse con el stem si cae dentro de desk/. 2) Mensaje de error comun. 3) Tests en tests/test_desk_paths.py y tests/test_tracked_selector_resolution.py; actualizar goldens de ayuda.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_desk_paths.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_tracked_selector_resolution.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

edit task con la ruta del drawer funciona en un test; el error nombra las formas aceptadas; goldens al dia.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-los-selectores-de-deskops-aceptan-una-ruta-desk-y-el-error-explica-que-formas-acepta: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


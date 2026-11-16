FILE:desk/tasks/task-borrar-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph-que-no.md
---
sldb:
  by: agent
  at: '2026-11-16T05:04:35Z'
  authority: generated
  via: save_document_payload
id: task-borrar-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph-que-no
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
- deskops/atom_references.py
- deskops/graph/checks.py
- deskops/workspace.py
- deskops/lifecycle.py
- tests/test_atom_reference_convention.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-retirar-caminos-legacy-migrar-los-datos-y-borrar-el-c-digo-de-compatibilidad.md
---

# Borrar el detector legacy de related_atoms y los alias scaffold_desk y ensure_lifecycle_graph, que no tienen consumidores

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (puntos 3 y 5, verificados el 2026-11-16). LEGACY_FIELD_VIOLATION vive en deskops/atom_references.py:23 y se usa en deskops/graph/checks.py:13 y 196; ningun desk usa related_atoms. Los alias scaffold_desk (deskops/workspace.py:754) y ensure_lifecycle_graph (deskops/lifecycle.py:431) se agregaron contra DK3 en b11a5282; graph_ui ya usa seed_desk y write_lifecycle_graph fuera de runs/. El punto 2 (snapshot en ruta vieja) ya se resolvio en CC33c (120bb672).

## Goal

_Describe the concrete result this task must produce._

Desaparecen el detector, los dos alias y sus tests legacy; nada fuera de runs/ los nombra.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/atom_references.py, deskops/graph/checks.py, deskops/workspace.py, deskops/lifecycle.py, tests/test_atom_reference_convention.py (casos legacy) y los tests que importen los alias. Verificar antes con `grep -rn 'scaffold_desk\|ensure_lifecycle_graph' /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui --include=*.py | grep -v /runs/` vacio. No entra: scripts viejos en UIs/graph_ui/runs/. Precisiones del preflight 1: hoy solo tests/test_atom_reference_convention.py nombra related_atoms o LEGACY_FIELD_VIOLATION, y ningun test importa scaffold_desk ni ensure_lifecycle_graph (solo los definen deskops/workspace.py y deskops/lifecycle.py); casos legacy = los tests de ese archivo que usan esos nombres. La busqueda de consumidores cubre todo /mnt/ssd/proyectos/SLDB_1 excepto directorios runs/ y .git: grep -rn --include=*.py 'scaffold_desk\|ensure_lifecycle_graph\|LEGACY_FIELD_VIOLATION' /mnt/ssd/proyectos/SLDB_1 | grep -v '/runs/'. test_graph_checks.py y test_cli.py solo se corren.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Greps de consumidores. 2) Borrar. 3) Greps de validacion vacios. 4) Tests.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rn 'LEGACY_FIELD_VIOLATION\|def scaffold_desk\|def ensure_lifecycle_graph' deskops tests
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_reference_convention.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_checks.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los greps quedan vacios y la suite no tiene fallas nuevas.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-borrar-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph-que-no: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


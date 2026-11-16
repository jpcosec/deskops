FILE:desk/tasks/task-inbox-y-drawer-quedan-trackeados-en-el-store-del-desk-y-las-vistas-los-leen-del-store-h10-de-cc34.md
---
sldb:
  by: agent
  at: '2026-11-16T04:01:42Z'
  authority: generated
  via: create_document
id: task-inbox-y-drawer-quedan-trackeados-en-el-store-del-desk-y-las-vistas-los-leen-del-store-h10-de-cc34
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
- deskops/data/desk_declaration.yaml
- deskops/cli/commands/view.py
- deskops/cli/commands/message.py
- deskops/cli/commands/promote.py
- tests/test_view.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-inbox-y-drawer-trackeados-en-el-store-del-desk-includes-en-desk-declaration-yaml-y-message-send-promote-trackean-al-escribir-h10-de-cc34.md
---

# Inbox y drawer quedan trackeados en el store del desk y las vistas los leen del store (H10 de CC34)

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (CC34, 2026-11-11). run_view de sldb solo ve documentos trackeados. desk_declaration.yaml no tiene globs de desk/inbox/*.md ni de desk/drawer/tasks/*.md, y deskops/cli/commands/view.py:16 y 359 leen drawer e inbox del disco. `deskops message send` ya trackea la nota al escribir (salida 'Tracked ...' observada el 2026-11-16); falta el drawer.

## Goal

_Describe the concrete result this task must produce._

deskops/data/desk_declaration.yaml incluye los globs de inbox y drawer; los comandos que escriben en el drawer (promote inbox-to-drawer-task y el alta de items del drawer) trackean al escribir; `deskops view` saca drawer e inbox de run_view como board y task. Al cerrar, se avisa a graph_ui para que verifique en navegador sus vistas de drawer e inbox.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/data/desk_declaration.yaml, deskops/cli/commands/view.py, deskops/cli/commands/message.py, deskops/cli/commands/promote.py y deskops/cli/commands/drawer.py si escriben en el drawer, y sus tests. Backend, robocop2. No entra: la verificacion en navegador (graph_ui, maquina local), migrar desks ajenos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Agregar los globs. 2) Trackear al escribir en el drawer. 3) view lee del store. 4) Tests en tests/test_view.py (una nota y un item nuevos aparecen en la vista sin desk update), tests/test_message_delivery.py y tests/test_inbox_promote_cli_gaps.py. 5) `deskops desk update --apply` en el desk de deskops. 6) `deskops message send --to graph_ui` con el hash.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_view.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_delivery.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_inbox_promote_cli_gaps.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

Los tests pasan; en el desk de deskops `deskops view` muestra un item del drawer recien creado sin desk update; nota a graph_ui enviada.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-inbox-y-drawer-quedan-trackeados-en-el-store-del-desk-y-las-vistas-los-leen-del-store-h10-de-cc34: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


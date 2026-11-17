---
sldb:
  by: agent
  at: '2026-11-17T01:25:26Z'
  authority: generated
  via: create_document
id: task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-095054-suggestion-respuesta-a-20261116-011047-la-ui-del-desk-no-muestra-findings-de-gates-ni-recibos-tarea-abierta-en-graph-ui.md
depends_on: []
pills: []
files:
- deskops/cli/commands/view.py
- docs/deskops-ui.md
- tests/test_view.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops view task entrega los recibos de la tarea en un campo receipts del contrato de la vista

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui (nota 20261116-095054) ya dibuja los findings de los gates, pero no puede mostrar los recibos (ReviewDoc con kind, verdict, anchor_state) porque deskops view task no los entrega: solo aparecen dentro del texto de un finding (seen). Pide un campo en el contrato de deskops view (docs/deskops-ui.md) y lo dibuja cuando exista.

## Goal

_Describe the concrete result this task must produce._

deskops view task <id> --format json trae task.receipts: una lista con un objeto por ReviewDoc cuyo subject es la tarea, con id, kind, verdict, anchor_state y created_at, ordenada por created_at; docs/deskops-ui.md documenta el campo.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/view.py (armado de la tarjeta de view task), docs/deskops-ui.md (contrato) y tests en tests/test_view.py. Sale: view board (no lleva recibos), la UI de graph_ui y cualquier cambio en ReviewDoc. anchor_state se lee como lo calcula hoy deskops review status para la tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ver como deskops review status obtiene los ReviewDoc de una tarea y su anchor_state, y reusarlo. 2) Agregar receipts a la salida de view task (json, yaml y text; en text una linea por recibo). 3) Documentar el campo en docs/deskops-ui.md junto a gates. 4) Test en desk sandbox con un recibo registrado por deskops review record.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_view.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_view_goldens.py

## Done When

_Name the observable condition that makes the task complete._

view task --format json trae receipts con los cinco campos para una tarea con recibos, la lista vacia para una sin recibos, docs/deskops-ui.md lo documenta y los dos archivos de la Validation pasan. Al cerrar se avisa a graph_ui con deskops message send --to graph_ui.

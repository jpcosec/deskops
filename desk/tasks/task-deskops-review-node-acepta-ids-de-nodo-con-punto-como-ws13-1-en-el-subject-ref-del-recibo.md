---
sldb:
  by: agent
  at: '2026-11-17T02:08:10Z'
  authority: generated
  via: create_document
id: task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/models/review.py
- tests/test_review_doc.py
- tests/test_review_command.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops review node acepta ids de nodo con punto como WS13.1 en el subject_ref del recibo

## Rationale

_Explain why this task exists or the business driver behind it._

deskops review node desk/drawer/plans/workspace-documental (triaje del 2026-11-16) aborta con 'Validation error: 1 validation error for ReviewDoc subject_ref String should match pattern' para el nodo WS13.1: SUBJECT_REF_PATTERN en deskops/models/review.py (r'^([^\s#]+#node:[A-Za-z0-9_-]+)?$') no admite el punto, y ese plan tiene 19 nodos con punto (WS13.1, WS15.2, WS32.1, ...). La corrida entera se corta en el primero y no escribe ningun recibo.

## Goal

_Describe the concrete result this task must produce._

SUBJECT_REF_PATTERN acepta el punto en el id de nodo (por ejemplo dag.yaml#node:WS13.1) y deskops review node escribe el recibo de un nodo con punto; un id con espacio o con '#' sigue rechazado.

## Scope

_State what is in scope and what is out of scope._

Entra: SUBJECT_REF_PATTERN en deskops/models/review.py, el modelo ReviewDoc del store si declara el mismo patron, y tests en tests/test_review_doc.py y tests/test_review_command.py. Sale: el formato de los ids de nodo de los planes y los review_id que se derivan del nodo (si el punto choca en el review_id, se informa en el resultado sin cambiar su formato).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Agregar el punto a la clase de caracteres del id de nodo en SUBJECT_REF_PATTERN (y donde el store declare el mismo patron). 2) Test de modelo: subject_ref con #node:WS13.1 valida; con espacio o '#' extra no. 3) Test de review node en desk sandbox con un dag.yaml de prueba que tenga un nodo con punto, con el pi falso que ya usan los tests, que escribe su recibo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py

## Done When

_Name the observable condition that makes the task complete._

Un subject_ref con id de nodo con punto valida, review node escribe su recibo en el sandbox, los ids con espacio o '#' siguen rechazados y los dos archivos de la Validation pasan.

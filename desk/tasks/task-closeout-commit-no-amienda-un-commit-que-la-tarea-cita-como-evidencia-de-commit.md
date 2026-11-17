---
sldb:
  by: agent
  at: '2026-11-17T01:24:29Z'
  authority: generated
  via: create_document
id: task-closeout-commit-no-amienda-un-commit-que-la-tarea-cita-como-evidencia-de-commit
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-141853-suggestion-closeout-commit-amienda-el-head-cuando-trae-el-mismo-task-id-closure-py.md
depends_on: []
pills: []
files:
- deskops/services/closure.py
- tests/test_closeout.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# closeout commit no amienda un commit que la tarea cita como evidencia de commit

## Rationale

_Explain why this task exists or the business driver behind it._

deskops/services/closure.py (_close, rama que arma argv) hace git commit --amend cuando el HEAD trae el trailer Task-Id de la misma tarea y Closeout-Mode distinto de record. Si ese HEAD es el commit de codigo que closeout verify ya grabo como evidencia (recibo evidence-commit y sha en references), el amend lo reescribe y el recibo queda citando un commit inalcanzable. Paso en deskops el 2026-11-16: task-puente-de-pytest, verify cito 9f7d4f13 y el closeout lo amendo a 3f613469 (nota 20261116-141853).

## Goal

_Describe the concrete result this task must produce._

closeout commit crea un commit nuevo, sin amend, cuando el HEAD es un commit que la tarea cita como evidencia de commit (su sha, completo o abreviado, esta en references de la tarea o es el value de un recibo evidence-commit aceptado de la tarea). En los demas casos el comportamiento de amend no cambia.

## Scope

_State what is in scope and what is out of scope._

Entra: la decision amend/commit nuevo en deskops/services/closure.py y tests en tests/test_closeout.py. Sale: el amend del indice de runs (index.jsonl) que hace el cierre sobre su propio commit, el contenido de los trailers y cualquier otro modo de cierre (supersede, resolved-by, manual).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer en closure.py la rama head_task_id == task_id y como se leen references y los recibos evidence-commit de la tarea. 2) Antes de elegir amend, comprobar si el sha del HEAD (rev-parse HEAD) es uno de los commits citados; si lo es, commit nuevo. 3) Test en un desk sandbox (tmp_path): commit de codigo con trailer Task-Id de la tarea, su sha corto en references, verify y closeout commit; el commit de codigo sigue siendo ancestro de HEAD con el mismo sha y el cierre es un commit aparte. Otro test: HEAD con Task-Id que NO esta citado sigue amendandose como hoy.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos pasan (el commit citado sobrevive con su sha; el no citado se amienda como antes) y los dos archivos de la Validation pasan.

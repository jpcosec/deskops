---
sldb:
  by: agent
  at: '2026-11-17T01:24:47Z'
  authority: generated
  via: create_document
id: task-closeout-verify-escribe-un-recibo-nuevo-cuando-el-veredicto-cambia-aunque-el-input-sea-el-mismo
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-151745-unclear-closeout-verify-no-escribe-el-recibo-accepted-si-ya-hay-uno-rejected-con-el-mismo-input.md
depends_on: []
pills: []
files:
- deskops/services/closure.py
- tests/test_closeout_declared_evidence.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# closeout verify escribe un recibo nuevo cuando el veredicto cambia aunque el input sea el mismo

## Rationale

_Explain why this task exists or the business driver behind it._

deskops/services/closure.py (_write_evidence_receipts) salta un recibo de evidencia si ya existe uno intacto con el mismo input_sha256, sin mirar el verdict. En sldb-ui (task-ui-rebase-sldb-actual) el primer verify escribio evidence-atom-1 rejected; ya en verde, el verify calcula el mismo input con verdict accepted, lo salta, y closeout commit queda bloqueado por rule-closeout-task-code (seen vacio). Nota 20261116-151745.

## Goal

_Describe the concrete result this task must produce._

closeout verify escribe un recibo nuevo cuando el unico recibo intacto con el mismo fact e input_sha256 tiene otro verdict; si ya hay uno intacto con el mismo input y el mismo verdict, lo salta como hoy.

## Scope

_State what is in scope and what is out of scope._

Entra: la deduplicacion de _write_evidence_receipts en deskops/services/closure.py y tests en tests/test_closeout_declared_evidence.py. Sale: el calculo de input_sha256, los nombres de los recibos y la regla de closeout.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) En _write_evidence_receipts, filtrar same_input por payload verdict igual al verdict nuevo. 2) Test en desk sandbox: un verify con un gate en rojo escribe un recibo rejected; se arregla la causa sin cambiar el input de ese fact; el segundo verify escribe un recibo accepted nuevo y closeout commit pasa la regla. 3) Test de no regresion: dos verify seguidos en verde no duplican recibos.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py

## Done When

_Name the observable condition that makes the task complete._

El caso rejected seguido de accepted con el mismo input escribe el recibo accepted y desbloquea el cierre; dos verify en verde no duplican; los dos archivos de la Validation pasan.

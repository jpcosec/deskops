FILE:desk/tasks/task-valores-con-llaves-rompen-edit-task-message-send-y-closeout-reason-y-closeout-verify-escribe-recibos.md
---
sldb:
  by: agent
  at: '2026-11-16T04:14:35Z'
  authority: generated
  via: create_document
id: task-valores-con-llaves-rompen-edit-task-message-send-y-closeout-reason-y-closeout-verify-escribe-recibos
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-005144-suggestion-closeout-el-gate-de-tests-solo-acepta-py-y-el-de-commit-solo-el-repo-del-desk-tareas-go-bash-o-con-c-digo-en-otro.md
depends_on: []
pills: []
files:
- deskops/services/closure.py
- deskops/cli/commands/closeout.py
- tests/test_closeout.py
- tests/test_message_cli.py
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# Valores con llaves rompen edit task, message send y closeout --reason, y closeout verify escribe recibos

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de scion del 2026-11-16, detalles menores del triaje: (a) `deskops closeout verify` escribe recibos evidence (ReviewDoc y desk/reviews) aunque su ayuda dice que solo chequea; (b) un --reason con llaves en closeout commit imprime 'Missing required field' despues de hacer el commit (parece str.format; deskops/services/closure.py:788 usa success_line.format) y deja sin commitear la proyeccion desk/reviews/<tarea>/evidence-external-2.md; (c) `deskops edit task` y `deskops message send` fallan con TemplateSyntaxError si el valor trae dos llaves de apertura seguidas (p. ej. un docker inspect --format de Go): el texto pasa por Jinja, que deskops no importa directamente (el render es de sldb).

## Goal

_Describe the concrete result this task must produce._

Reproducir (a), (b) y (c) en un desk sandbox y registrar el recibo de reproduccion. Corregir en deskops lo que sea de deskops: verify no escribe nada o su ayuda dice exactamente que escribe; un --reason con llaves queda literal en el commit y el cierre no deja archivos sin commitear. Si (c) nace en el render de sldb, se manda `deskops message send --to sldb` con la reproduccion minima y en deskops queda un test xfail que cita esa nota.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/closure.py, deskops/cli/commands/closeout.py (ayuda de verify), los caminos de edit task y message send hasta la llamada a sldb, y tests. No entra: modificar sldb directamente.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Sandbox con `deskops init`; para cada caso, el comando minimo y su salida en runs/<run>/repro-<caso>.log; `deskops review record <tarea> --kind reproduction --evidence <logs> --reason ... --root .`. 2) Corregir (a) y (b). 3) Ubicar (c) con el traceback. 4) Tests en tests/test_closeout.py y tests/test_message_cli.py.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

Hay recibo de reproduccion de los tres casos; (a) y (b) tienen test verde; (c) tiene test verde o xfail citando la nota a sldb.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-valores-con-llaves-rompen-edit-task-message-send-y-closeout-reason-y-closeout-verify-escribe-recibos: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


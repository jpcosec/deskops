FILE:desk/tasks/task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error.md
---
sldb:
  by: agent
  at: '2026-11-17T01:25:06Z'
  authority: generated
  via: create_document
id: task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-132801-suggestion-deskops-view-un-gate-con-holds-true-trae-a-la-vez-un-finding-de-nivel-error.md
depends_on: []
pills: []
files:
- deskops/cli/commands/view.py
- tests/test_view.py
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops view task entrega holds true en un gate cuya regla de activacion da un finding de error

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui (nota 20261116-132801) vio en el desk de deskops que deskops view task <tarea> --format json da, en el gate task_activates -> ritual-testing, holds true y a la vez findings con level error de rules/rule-activation-task-code (seen vacio). La UI dibuja cumple y el error juntos. Los gates de view salen de DeskopsOperations.show_task (deskops/cli/commands/view.py, _gates).

## Goal

_Describe the concrete result this task must produce._

Reproducir el caso, encontrar por que holds y el finding de error no coinciden, y dejar que holds sea false cuando la regla de activacion del gate da un finding de nivel error; con un test que falla antes y pasa despues.

## Scope

_State what is in scope and what is out of scope._

Entra: el calculo de holds y findings de los gates que entrega show_task y deskops view task (deskops/cli/commands/view.py y lo que lea de deskops/services o deskops/lifecycle), y tests. Sale: la UI de graph_ui y el texto de los findings. Si la causa esta en sldb (evaluacion de la regla), se manda deskops message send --to sldb con la reproduccion minima y en deskops queda un test xfail strict con esa nota como reason.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reproducir en un desk sandbox (tmp_path) una tarea task.code sin recibos de preflight: deskops view task <id> --format json y deskops show task. 2) Registrar la reproduccion con deskops review record <tarea> --kind reproduction. 3) Seguir de donde sale holds (show_task) y de donde salen los findings, y hacer que coincidan. 4) Test que compara holds con la presencia de findings de nivel error.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_view.py

## Done When

_Name the observable condition that makes the task complete._

En el caso reproducido, el gate con finding de error da holds false (o la causa queda ruteada a sldb con test xfail strict), y tests/test_view.py pasa.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


---
sldb:
  by: agent
  at: '2026-11-16T06:06:16Z'
  authority: generated
  via: save_document_payload
id: task-advance-y-closeout-no-derraman-reglas-de-activacion-ni-runtimes-centrales-sin-trackear-en-el-desk-co
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-deskops-derrama-reglas-de-activacion-y-runtimes-centrales-en-el-desk-del-proyecto-consumidor.md
---

# advance y closeout no derraman reglas de activacion ni runtimes centrales sin trackear en el desk consumidor

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de ftcourier (10-11, inbox 20261110-094518): advance y closeout escriben desk/lifecycle/rule-activation-task-*.md (7) y desk/runtimes/runtime-pi-deepseek-flash.md en el desk del proyecto como archivos sin trackear. Se ve tambien hoy en ~/setup (7 rule-activation-* sin trackear).

## Goal

_Describe the concrete result this task must produce._

Las semillas centrales (deskops/data/rules, runtime por defecto) se leen del paquete en tiempo de ejecucion, o se escriben solo por deskops desk update --apply y quedan trackeadas y declaradas; nunca como archivos sueltos sin trackear tras advance o closeout.

## Scope

_State what is in scope and what is out of scope._

deskops/lifecycle.py, deskops/workspace.py, deskops/cli/commands/desk.py; decision de cual de las dos formas en el preflight.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- test nuevo de deskops (nombre a fijar al promover) con advance y closeout en un desk consumidor

## Done When

_Name the observable condition that makes the task complete._

test: advance y closeout en un desk consumidor real dejan git status limpio fuera de lo que la tarea toca.

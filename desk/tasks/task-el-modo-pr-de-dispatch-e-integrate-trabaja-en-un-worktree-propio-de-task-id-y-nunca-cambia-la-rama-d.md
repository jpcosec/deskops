---
sldb:
  by: agent
  at: '2026-11-25T01:43:11Z'
  authority: generated
  via: create_document
id: task-el-modo-pr-de-dispatch-e-integrate-trabaja-en-un-worktree-propio-de-task-id-y-nunca-cambia-la-rama-d
status: draft
summary: ''
tags: []
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
---

# El modo pr de dispatch e integrate trabaja en un worktree propio de task/<id> y nunca cambia la rama del checkout principal

## Rationale

_Explain why this task exists or the business driver behind it._

Piloto UI-122 de MEPU (notas PARA DESKOPS 20261124-220541 punto 5 y 20261124-222637 punto 10): reap en modo pr hizo checkout de task/<id> en el checkout principal compartido y los commits del desk de otras sesiones habrian caido en la rama del PR.

## Goal

_Describe the concrete result this task must produce._

En modo pr, dispatch reap trae los commits del ejecutor a task/<id> en el worktree <root>/.worktrees/<task-id>; closeout verify/commit e integrate usan ese worktree cuando existe la rama task/<id>; el checkout principal no cambia de rama.

## Scope

_State what is in scope and what is out of scope._

deskops/dispatch.py, deskops/integrate.py, deskops/cli/commands/closeout.py, tests/test_dispatch.py, tests/test_integrate.py, docs/operator-manual.md (Integrate modes). Fuera: el modo push.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- pytest tests/test_dispatch.py tests/test_integrate.py

## Done When

_Name the observable condition that makes the task complete._

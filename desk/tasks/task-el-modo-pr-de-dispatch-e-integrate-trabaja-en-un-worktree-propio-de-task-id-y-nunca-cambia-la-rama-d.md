---
sldb:
  by: agent
  at: '2026-11-25T02:58:41Z'
  authority: generated
  via: save_document_payload
id: task-el-modo-pr-de-dispatch-e-integrate-trabaja-en-un-worktree-propio-de-task-id-y-nunca-cambia-la-rama-d
status: ready_for_testing
summary: ''
tags: []
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- 9abe2d6036c1ed91f63252392366491021446ab0
- tests/test_dispatch.py
- tests/test_integrate.py
- atom-en-modo-pr-la-rama-task-id-vive-en-su-propio-worktree-y-el-checkout-principal-nunca-cambia-de-rama
depends_on: []
pills: []
files:
- deskops/dispatch.py
- deskops/integrate.py
- deskops/cli/commands/closeout.py
- tests/test_dispatch.py
- tests/test_integrate.py
- docs/operator-manual.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-en-modo-pr-la-rama-task-id-vive-en-su-propio-worktree-y-el-checkout-principal-nunca-cambia-de-rama
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

1. <root> es el checkout principal pasado con --root; <task-id> es el id completo de la tarea (con prefijo task-; si no lo tiene, task-<id>): worktree <root>/.worktrees/<task-id> en la rama local task/<task-id> (task_worktree_path). 2. ensure_task_worktree(root, id, base): si el worktree ya existe y esta en task/<id> lo usa; si no, git worktree add (con -b desde la base integrate.branch cuando la rama local no existe); .worktrees/ queda en info/exclude. 3. reap (_integrate_branch) en modo pr: exige como antes que el checkout principal este en la base (ya no acepta estar en task/...), commitea ahi el RunDoc, y hace merge --ff-only o cherry-pick de deskops/<agente> dentro del worktree de la tarea; el mensaje dice 'en task/<id> (worktree <ruta>)'. 4. start en modo pr: el worktree del ejecutor parte de task/<id> si la rama local existe (segundo intento), si no de la base; el tester compara contra esa misma rama. 5. pr_task_root(root, id): en modo pr con la rama local task/<id> existente (deteccion automatica, sin flag; solo ramas locales) devuelve su worktree, creandolo si falta; si el checkout ya esta en esa rama, o en modo push, devuelve root. closeout verify, closeout commit (--run-dir y --no-run) e integrate lo usan y lo dicen ('modo pr: ... worktree <ruta>'); integrate deja logs y events en runs/ del checkout principal y lee la config de ahi. 6. El worktree no se borra solo: el manual dice quitarlo con la rama despues del merge del PR. 7. Tests: reap pr deja HEAD del principal en la base y la rama task/<id> con el commit en su worktree; segundo intento parte de task/<id>; closeout verify corre en el worktree; integrate --dry-run con el principal en otra rama usa el worktree y no cambia la rama del principal. 8. Manual: reescribir el punto pr de Integrate modes.

## Validation

_List the checks required before this task can close._

- pytest tests/test_dispatch.py tests/test_integrate.py

## Done When

_Name the observable condition that makes the task complete._

pytest tests/test_dispatch.py tests/test_integrate.py pasa; en ninguna ruta del modo pr se ejecuta git checkout en el checkout principal (git rev-parse --abbrev-ref HEAD del principal no cambia en los tests).

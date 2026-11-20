Task: task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li
Title: se borra el camino legacy de deskops message y el escenario e2e inbox-to-task usa deskops message list
Status: draft
Current node: ritual-execution
Task type: task.code
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-17T01:26:04Z'
  authority: generated
  via: create_document
id: task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-221318-suggestion-restos-del-retiro-del-alias-deskops-inbox.md
depends_on: []
pills: []
files:
- deskops/cli/commands/message.py
- tests/e2e_agent/scenarios/inbox-to-task.yaml
- tests/test_repo_identity.py
- tests/test_inbox_promote_cli_gaps.py
- tests/test_message_cli.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
---

# se borra el camino legacy de deskops message y el escenario e2e inbox-to-task usa deskops message list

## Rationale

_Explain why this task exists or the business driver behind it._

Seguimiento del retiro del alias deskops inbox (8667e8f1, closeout 49465a27; nota 20261116-221318). Quedaron: _run_legacy y su docstring en deskops/cli/commands/message.py, que solo alcanza deskops message sin subcomando; el escenario tests/e2e_agent/scenarios/inbox-to-task.yaml, cuya rama 'deskops inbox list --root .' ahora falla y cae a su alternativa con ||; y docstrings que nombran deskops inbox como comando en tests/test_repo_identity.py y tests/test_inbox_promote_cli_gaps.py.

## Goal

_Describe the concrete result this task must produce._

deskops message sin subcomando da un error de uso claro (la ayuda de message con sus subcomandos) sin pasar por _run_legacy, que se borra; el escenario e2e usa deskops message list --root .; los dos docstrings dejan de presentar deskops inbox como comando vigente.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/message.py, tests/e2e_agent/scenarios/inbox-to-task.yaml, tests/test_repo_identity.py y tests/test_inbox_promote_cli_gaps.py (solo docstrings), y tests de message. Sale: el registro de comandos (deskops inbox ya no existe) y docs.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer _run_legacy y quien lo llama en message.py. 2) Borrarlo y hacer que message sin subcomando imprima el error de uso de argparse o la ayuda, con rc 2. 3) Cambiar la rama del escenario e2e. 4) Ajustar los dos docstrings. 5) Test: deskops message sin subcomando da rc 2 y nombra send, list, read y ack.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_command_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py

## Done When

_Name the observable condition that makes the task complete._

grep de _run_legacy en deskops/ no da nada, el escenario e2e no usa deskops inbox, el test nuevo pasa y los tres archivos de la Validation pasan.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-44a082df5dbe-a2`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-44a082df5dbe-a2

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

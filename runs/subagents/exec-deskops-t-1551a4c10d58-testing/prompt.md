Task: task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li
Title: se borra el camino legacy de deskops message y el escenario e2e inbox-to-task usa deskops message list
Status: active
Current node: ritual-testing
Task type: task.code
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-20T22:30:18Z'
  authority: generated
  via: save_document_payload
id: task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li
status: active
summary: ''
tags:
- host:robocop2
current_node: ritual-testing
history:
- task_activates
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

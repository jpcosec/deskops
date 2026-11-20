PASA

# Tester — task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li

- Commit del ejecutor verificado: `6ae6ea035fc975fe86f1e4f6077ced5e28f7b9a8`
- Archivos del commit: `deskops/cli/commands/message.py`, `tests/e2e_agent/scenarios/inbox-to-task.yaml`, `tests/test_inbox_promote_cli_gaps.py`, `tests/test_message_cli.py`, `tests/test_repo_identity.py`
- Código: `_run_legacy` eliminado y sin referencias; `deskops message` sin subcomando devuelve rc=2 con usage que nombra `{send,list,read,ack}`; el escenario e2e usa `deskops message list --root .`; los dos docstrings ya no presentan `deskops inbox` como comando vigente.

Validaciones (todas PASS):

- `tests/test_message_cli.py`: 17 passed
- `tests/test_inbox_promote_cli_gaps.py`: 21 passed
- `tests/test_repo_identity.py`: 8 passed
- `tests/test_command_registry.py`: 3 passed
- `tests/test_cli.py`: 102 passed
- `tests/e2e_agent/test_agent_scenarios.py::test_reference_solutions[inbox-to-task]`: 1 passed

Comportamiento manual: `python -m deskops message` -> rc=2, stderr con `usage: deskops message [-h] {send,list,read,ack} ...` y `the following arguments are required: message_command`.

Nota de entorno: el `../.venv/bin/python` sugerido por la tarea no importa pytest en este contenedor (intérprete 3.11 contra site-packages 3.12). Los tests se corrieron con `/dev/shm/t311/bin/python`, que tiene el proyecto y pytest 9.2.0; ver `validation.log`.

Sin hallazgos de bloqueo. Veredicto: PASA.

FALLA

Commit del ejecutor: e95bdb13a4c14e794d82aa8eede66dcb2a788ec5
Task-Id: task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de

## Veredicto

El objetivo funcional está implementado y sus tests nuevos pasan, pero el commit deja la suite con regresiones en los tests del registro de comandos y en los goldens de ayuda: no actualizó `tests/test_command_registry.py` ni los fixtures `tests/fixtures/golden/help/` para los dos comandos nuevos (`queue job` y `queue job set`).

## Pruebas ejecutadas

Entorno: `/tmp/deskops-test-venv` (uv, CPython 3.12.16; el `.venv` del workspace está roto porque apunta a un `/usr/bin/python3.12` inexistente). Instalé `deskops` y el `sldb` local en modo editable para que los imports coincidan con el checkout. Cada archivo se corrió por separado con `TMPDIR=/tmp`:

- `tests/test_queue_cli.py`: 3 passed
- `tests/test_queue.py`: 18 passed
- `tests/test_config.py`: 5 passed
- `tests/test_registry_robustness.py`: 8 passed
- `tests/test_cli_grammar.py tests/test_cli_help_examples.py`: 15 passed
- `tests/test_command_registry.py`: **2 failed, 1 passed**
  - `test_registry_paths_match_help_goldens`: sobran `('queue', 'job')` y `('queue', 'job', 'set')` frente a los goldens.
  - `test_mutating_commands_are_declared_explicitly`: `MUTATING_COMMANDS` no declara `('queue', 'job')` ni `('queue', 'job', 'set')`.
- `tests/test_output_goldens.py -k help`: **1 failed, 6 deselected**
  - `test_help_goldens`: `help/deskops_queue.txt` no incluye `job`; además faltan los goldens de `queue job` y `queue job set`.

## Lo que sí cumple

- `deskops queue job set dispatch-reap retry_exit_codes '[3]' --root .` funciona, valida y cambia solo ese trabajo.
- `deskops/data/templates/config.json` y `desk/config.json` tienen `dispatch-reap.retry_exit_codes == [3]`.
- Los tests nuevos del commit (`tests/test_queue_cli.py`) pasan.

## Acción necesaria

Actualizar los goldens de ayuda y `MUTATING_COMMANDS` para el nuevo subcomando, o justificar explícitamente que esos tests no aplican. Con el estado actual, la integración de e95bdb13 no puede considerarse verde.

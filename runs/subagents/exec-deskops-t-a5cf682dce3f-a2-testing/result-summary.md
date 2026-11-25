PASA

Commits del ejecutor:
- e95bdb13a4c14e794d82aa8eede66dcb2a788ec5 (implementación)
- b37b57cdf5a4f73e8e40931edfad11f306ce7a5c (registro y goldens; intento 2)
- Task-Id: task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de

## Veredicto

PASA. La cola reintenta el reap que espera (exit 3) en el seed de `deskops init` y en el `desk/config.json` de este desk, y `deskops queue job set <job> <field> <value> --root .` edita solo el trabajo indicado, valida el resultado y deja el archivo intacto ante entradas inválidas. Quedaron resueltas las dos regresiones del intento 1 (registro de comandos y goldens de ayuda).

## Comprobaciones funcionales

- `desk/config.json`: `queue_jobs.dispatch-reap.retry_exit_codes == [3]` (junto a `run` y `timeout: 600`).
- `deskops/data/templates/config.json`: el seed de init declara `dispatch-executor`, `dispatch-tester` y `dispatch-reap` con `retry_exit_codes: [3]`.
- `tests/test_queue_cli.py` cubre: cambio solo de ese trabajo (igualdad del JSON completo antes/después salvo el campo), validación como `QueueJob`, rechazo de job/campo/valor inválidos sin modificar el archivo, y el seed de init.
- `tests/test_command_registry.py` incluye `('queue', 'job')` y `('queue', 'job', 'set')`; los goldens nuevos son `deskops_queue_job.txt` y `deskops_queue_job_set.txt`, y `deskops_queue.txt` lista `job`.

## Pruebas ejecutadas

El `.venv` del workspace apunta a un `/usr/bin/python3.12` inexistente. Armé un entorno temporal en `/tmp/testenv` (CPython 3.13 con las dependencias del tool de deskops y pytest) sin tocar el repo. Cada archivo se corrió por separado con `TMPDIR=/tmp`:

- `tests/test_queue_cli.py`: 3 passed
- `tests/test_queue.py`: 18 passed
- `tests/test_command_registry.py`: 3 passed
- `tests/test_output_goldens.py`: 7 passed
- `tests/test_scaffold_golden.py`: 3 passed
- `tests/test_config.py`: 5 passed
- `tests/test_cli_grammar.py`: 2 passed
- `tests/test_cli_help_examples.py`: 13 passed
- `tests/test_cli_contract.py`: 8 passed
- `tests/test_registry_robustness.py`: 8 passed
- `tests/test_cli.py`: 103 passed

No hay cambios sin commitear en `deskops/`, `tests/`, `desk/config.json`, `CHANGELOG.md` ni `docs/operator-manual.md`; el árbol solo tiene los documentos de run/task esperados.

## Acción necesaria

Ninguna para el ejecutor.

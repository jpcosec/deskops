PASA

# Veredicto

El trabajo del ejecutor pasa la validación. Probé el commit de corrección
`c972a252` sobre el commit de código `af79c143` (ambos con el Task-Id de la
tarea) en `/mnt/ssd/proyectos/SLDB_1/deskops`.

## Pruebas ejecutadas

Cada archivo se corrió por separado con `TMPDIR=/tmp python -m pytest -q <archivo>`.
El intérprete del `.venv` del workspace no está disponible en esta máquina
(`python3.12` ausente), así que usé el Python 3.13 del host con el mismo
`deskops` editable, sus dependencias y `sldb/src` en `PYTHONPATH`.

- `tests/test_ascii_ids.py`: 6 passed
- `tests/test_integrate.py`: 19 passed
- `tests/test_specs.py`: 5 passed
- `tests/test_add_task_from_drawer.py`: 3 passed
- `tests/test_closeout.py`: 73 passed
- `tests/test_cli.py`: 102 passed
- `tests/test_model_validators.py`: 14 passed
- `tests/test_atom*.py` (9 archivos): 52 passed
- resto de `tests/test_closeout_*.py` (9 archivos): 142 passed

No hubo fallas. No corrí la suite completa, según la consigna del tester.

## Comprobaciones de aceptación

- `ascii_slug` pliega `Transacción ñandú über` a `transaccion-nandu-uber`;
  `compiler.py`, `doc_access.py` y `drawer.py` usan el helper compartido.
- `deskops add task --title 'Transacción ñandú'` genera un id ASCII.
- Un id explícitamente acentuado (`task-transacción`) se conserva y
  `deskops show task task-transacción` lo resuelve.
- Un átomo existente con tilde (`atom-...-caché-...`) sigue validando y
  `deskops show atom <id>` sale con 0.
- `integrate` encuentra el recibo de una tarea cerrada con id acentuado.
- Las llamadas git parseadas de `closure.py` e `integrate.py` llevan
  `-c core.quotepath=false`; `grep -rn quotepath deskops/` las muestra.

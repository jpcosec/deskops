PASA

# Veredicto del tester

El commit del ejecutor cumple el objetivo y la Validation de la tarea: `queue run --all` deja en `pending` el trabajo que sale con un código de `retry_exit_codes`, lo saltea durante el resto de esa corrida y sigue con los siguientes pendientes; si todos quedan en espera, termina sin bucle. Sin `--all` sigue corriendo un solo trabajo, y un fallo normal sigue deteniendo la cola.

## Commit evaluado

- Commit: `9317d460a755c651423ffec1e8bca128409cc6c4`
- Mensaje: `queue run --all sigue con los siguientes trabajos cuando uno queda en espera por retry_exit_codes`
- Trailer: `Task-Id: task-queue-run-sigue-con-los-trabajos-siguientes-cuando-uno-queda-en-espera-por-retry-exit-codes-en-vez-d`
- Archivos:
  - `deskops/queue.py`
  - `tests/test_queue.py`
  - `docs/operator-manual.md`
  - `CHANGELOG.md`

## Pruebas ejecutadas

Con Python 3.13.18 y pytest 9.1.1 de `/mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin/python`:

- `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py`
  - Resultado: **18 passed**, exit 0.
  - Incluye los tests nuevos `test_retry_job_is_skipped_and_queue_continues` y `test_all_waiting_jobs_end_run_without_loop`.

El commit no toca otros módulos de código, así que `tests/test_queue.py` cubre los `tests/*.py` del commit y el `tests/test_<modulo>.py` del módulo tocado. No se ejecutó la suite completa.

## Comprobaciones contra el Goal

- Trabajo A con `retry_exit_codes: [3]` y exit 3: queda en `pending`, con `attempts == 1`, e imprime `en espera: <A> ocupado (exit 3)`.
- B y C salen con 0: quedan en `done` y la corrida retorna 0.
- Si todos los pendientes quedan en espera, la corrida termina sin reintentarlos en bucle.
- Sin `--all`, el comportamiento de un solo trabajo se mantiene.
- Un fallo que no está en `retry_exit_codes` sigue marcando el trabajo como fallido y deteniendo la cola.

## Entorno

El `.venv` de `/workspace` (y el de `/mnt/ssd/proyectos/SLDB_1`) apunta a un Python 3.12 ausente, por lo que `python`/`pytest` del proyecto no arrancan en este contenedor. La validación se ejecutó con el Python 3.13 del `.venv` de `sldb`, que tiene las dependencias del proyecto. No se modificó el repositorio para la validación.

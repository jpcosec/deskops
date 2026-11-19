PASA

# Resultado del tester

Tarea: task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid
Rol: tester
Run: run-deskops-t-8940972f7883-a2 (runs/subagents/exec-deskops-t-8940972f7883-a2-testing)
Commit probado: e893a6313190df132fe381215e08506c57de3137 ("queue run: attempts y (exit n) al dejar en espera")

## Veredicto

**PASA.** El segundo intento del ejecutor cumple el Goal y los dos requisitos que faltaban
en el intento anterior sobre 00ec6562:

1. El JSON del trabajo que vuelve a `pending` suma `attempts` (1 tras el primer reintento,
   2 tras el segundo).
2. El mensaje es exactamente `en espera: <id> ocupado (exit <n>)`, con el sufijo
   `(exit 3)` para el código de "ocupado" de `dispatch start`.
3. Cualquier otro código distinto de 0 sigue moviendo el trabajo a `failed`.
4. El trabajo no deja nota `unclear` y `queue run` termina con código 0 al dejarlo en espera.

## Pruebas corridas

Sobre un árbol limpio del commit (`git archive e893a631...` extraído en `/tmp/deskops-e893`),
con `PYTHONPATH` apuntando a ese árbol y a `sldb/src`:

- `TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_queue.py`
  -> **16 passed**, exit 0 (47.64 s). Log: `pytest-test_queue.log`.
- `TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_config.py`
  (módulo tocado en el entregable: `deskops/config.py`) -> **5 passed**, exit 0. Log:
  `pytest-test_config.log`.
- Suite completa: no corrida (la corre integrate en el host, como indica el encargo).

## Cobertura del cambio

`tests/test_queue.py::test_retry_exit_code_leaves_job_pending` ahora comprueba el mensaje
exacto con `(exit 3)`, que el job sigue en `pending`, que no hay `failed`/`running` ni nota
en inbox, y `attempts == 1` y luego `attempts == 2` tras dos corridas.
`test_other_exit_code_still_fails_with_retry_codes` conserva la comprobación de que un
código no declarado sigue fallando.

## Otros requisitos

- `docs/operator-manual.md` (Host queue) y `CHANGELOG.md` documentan `retry_exit_codes`,
  `attempts` y el mensaje con `(exit <n>)`.
- El commit nombra las rutas tocadas e incluye el `Task-Id`.
- `deskops/queue.py` implementa el reintento sin nota `unclear` y sin marcar `failed`.

## Entorno

No hay `python` en PATH y los `.venv` de `/workspace` y de la raíz del proyecto enlazan a
un Python 3.11 sin pytest; se usó `/workspace/sldb/.venv/bin/python` (3.13.18, pytest 9.1.1),
el mismo entorno que usó el tester anterior.

Evidencia: `pytest-test_queue.log`, `pytest-test_config.log`, `validation.log`.

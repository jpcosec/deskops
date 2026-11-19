FALLA

# Resultado del tester

Tarea: task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid
Rol: tester
Run: run-deskops-t-8940972f7883 (runs/subagents/exec-deskops-t-8940972f7883-testing)
Session: scion://agent/deskops-t-8940972f7883 (session_sha256 no disponible)

## Pruebas corridas

- `TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_queue.py`
  -> **16 passed**, exit 0 (46.50 s). Log: `pytest-test_queue.log`.
- `TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_config.py`
  (modulo tocado: `deskops/config.py`) -> **5 passed**, exit 0. Log: `pytest-test_config.log`.
- Suite completa: no corrida (la corre integrate, como indica el encargo).
- Nota de entorno: no hay `python` en PATH y `.venv/bin/python` esta roto (venv 3.11 con
  site-packages 3.12); use `/workspace/sldb/.venv/bin/python` (3.13.18, pytest 9.1.1).

## Lo que si cumple el commit 00ec6562

- Un job con `retry_exit_codes: [3]` y comando `exit 3` vuelve a `pending`, `queue run`
  retorna 0 y no deja job en `failed` ni nota `unclear`.
- Otro codigo distinto de 0 sigue yendo a `failed` (test y probe manual).
- Funciona con y sin `--all`; el job conserva id y nombre.
- Docs y CHANGELOG actualizados; commit con rutas nombradas y `Task-Id`.

## Por que FALLA

El contrato aceptado (preflight-1 y bundle-1, ambos `accepted`; ver `review-status.txt`)
agrega dos requisitos observables que el commit no implementa y que los tests nuevos no
cubren, aunque el Goal literal del TaskDoc si se cumpla:

1. El JSON del job en `pending` debe **sumar el contador `attempts`**. Probe manual tras
   dos reintentos: la clave `attempts` esta **AUSENTE** (`manual-contract-probe2.log`).
2. El mensaje debe ser **`en espera: <id> ocupado (exit <n>)`**. El commit imprime
   `en espera: <id> ocupado`, **sin el sufijo `(exit 3)`** (`manual-contract-probe.log`).

`tests/test_queue.py::test_retry_exit_code_leaves_job_pending` solo comprueba
`"en espera:"` y `"ocupado"`, las carpetas y la ausencia de nota; no cubre ninguno de
los dos requisitos aceptados. Es un test incompleto, no un fallo de la suite.

## Handoff

Se devuelve al ejecutor para agregar `attempts` y el sufijo `(exit <n>)`, y ampliar el
test que los pruebe. No modifique codigo, tests ni desk; no cree commit.

Evidencia: `validation.log`, `review-status.txt`, `git-evidence.txt`,
`pytest-test_queue.log`, `pytest-test_config.log`, `manual-contract-probe.log`,
`manual-contract-probe2.log`.

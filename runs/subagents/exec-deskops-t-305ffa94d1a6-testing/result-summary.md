PASA

Task: task-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript-test-ts-test-tsx-spec-ts-declara
Commit del ejecutor: 8c836050d304cef91b70e0482ccdc9470d4d6846 ("Closeout tests gate accepts TypeScript test files")

## Validación

- `TMPDIR=/tmp` + `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-305ffa94d1a6` y
  `python -m pytest -q tests/test_closeout_test_paths.py tests/test_closeout_gates.py`
  -> **49 passed** (1 warning de config, sin fallos). Incluye los 6 tests nuevos de TypeScript.
- `tests/test_closeout_resolved_by.py` -> **26 passed** (cubre el mensaje `Unresolvable --test`).

## Comprobación independiente

- `.test.ts`, `.test.tsx`, `.spec.ts`, `.spec.tsx` declarados en `files` cuentan como evidencia.
- Un `.test.ts` bajo un directorio `tests/` cuenta sin declararse; fuera de `tests/` y no declarado no cuenta.
- `node_modules/`, directorios ocultos (`.hidden/`), `.ts` plano y `.test.js` siguen rechazándose.
- Formas `pytest -q <ruta>::nodo` extraen correctamente el candidato TS.
- El mensaje de rechazo en `deskops/services/closure.py` nombra los sufijos aceptados
  (`.py`, `.test.ts`, `.test.tsx`, `.spec.ts`, `.spec.tsx`).
- Sin cambios posteriores al commit en `closeout_gates.py`, `closure.py` ni el test.

## Notas

- El intérprete del venv del host está roto para este montaje (apunta a `/usr/bin/python3.12`
  inexistente); los tests se corrieron con un CPython 3.12 + pytest ya disponible en el entorno,
  con temporales en `/tmp` según lo indicado.
- No se modificó ni se commiteó código, desk ni `.sldb` desde el rol tester.

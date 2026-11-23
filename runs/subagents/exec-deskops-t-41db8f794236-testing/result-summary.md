PASA

# Resultado del tester

Tarea: `task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n`
Tester: `deskops-t-41db8f794236` (role-deskops-tester)

## Commit del ejecutor

`f7772acdee9f620051ad4551b48fc24c294173cd` — *dispatch reap: ruta de limpieza de pytest-of-scion por DESKOPS_SCION_PYTEST_TMP*.
Trailer verificado: `Task-Id: task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n`.

Archivos del commit (coinciden con el scope):
- `deskops/dispatch.py`
- `tests/test_dispatch.py`

## Verificación contra el Goal

1. **La ruta de limpieza se puede redirigir por entorno.**
   `_scion_pytest_tmp()` devuelve `os.environ.get("DESKOPS_SCION_PYTEST_TMP") or SCION_PYTEST_TMP`;
   `_clean_scion_pytest_tmp()` y el mensaje `limpieza:` usan esa función. El valor por defecto sigue
   siendo `/dev/shm/pytest-of-scion`.

2. **El fixture `Env` aísla los tests del `/dev/shm` real.**
   `tests/test_dispatch.py` fija `DESKOPS_SCION_PYTEST_TMP` a `tmp_path / "pytest-of-scion"` en el
   entorno que heredan los subprocesos del CLI, y `_reap_in_process` lo fija con `monkeypatch.setenv`.
   Los tests de limpieza usan la ruta de `tmp_path`.

3. **`test_reap_scion_error_continues_and_fails` ya no imprime `limpieza:` ni toca `/dev/shm`.**
   El test compara `stdout` exactamente con `["deskops-e-bad executor error:9", "deskops-e-ok executor phase:stopped"]`;
   pasa con un `/dev/shm/pytest-of-scion` real presente.

## Tests ejecutados

Con un `/dev/shm/pytest-of-scion` real creado y un fichero centinela dentro:

```
TMPDIR=/tmp /dev/shm/deskops-test-venv/bin/python -m pytest -q tests/test_dispatch.py
49 passed, 1 warning in 524.87s (exit 0)
test -d /dev/shm/pytest-of-scion            -> exit 0
test -f /dev/shm/pytest-of-scion/.sentinel  -> exit 0
```

El centinela siguió presente: ningún test borró el directorio real del host. Incluye los 4 casos de
limpieza de `pytest-of-scion` (2 parametrizados de prompt + 2 de reap).

También se ejecutó aislado `test_tester_prompt_runs_only_touched_tests` → **1 passed**.

No se corrió la suite completa, según la instrucción del encargo para el tester.

## Notas de entorno (no afectan al veredicto)

El venv del repo (`/workspace/.venv`, bind mount de `/mnt/ssd/proyectos/SLDB_1/.venv`) tiene los
symlinks de Python rotos para este contenedor (venv de 3.12, `python3` resuelve a 3.11 y sin pytest).
Los tests se ejecutaron con el CPython 3.12.16 de `/dev/shm/deskops-test-venv`. No se modificó código,
desk ni `.sldb` durante la revisión.

## Veredicto

Los 49 tests de `tests/test_dispatch.py` pasan con el `/dev/shm/pytest-of-scion` real presente y este
sigue existiendo después. **PASA.**

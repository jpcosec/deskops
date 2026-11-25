## REFORMULACION

**Propósito:** modificar `deskops/integrate.py` para que la suite corra con su basetemp dentro de la carpeta temporal de integrate y para que, al arrancar, se limpien carpetas de corridas muertas. **Resultado:** `_run_suite` añade `--basetemp=<work>/pytest` a `PYTEST_ADDOPTS` del env (conservando lo previo, separado por un espacio), porque la suite es `sh -c "... pytest ..."` y argv no llega a pytest; cada work deja `owner.pid`; al empezar la suite, ya con `_suite_lock(cfg.tests_lock)`, se borran carpetas `deskops-integrate-*` de `tempfile.gettempdir()` de corridas muertas (pid muerto, o sin `owner.pid` y mtime mayor que `cfg.suite_timeout`), imprimiendo `"limpieza: <ruta>"`, nunca la propia ni la de un pid vivo. **Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. **Archivos:** `deskops/integrate.py`, `tests/test_integrate.py`. **Límites:** no tocar `desk/config.json`, `deskops/queue.py` ni la limpieza de `/dev/shm/pytest-of-scion`.

## AMBIGUEDADES

1. "Cada carpeta de trabajo deja un archivo owner.pid con el pid del proceso de integrate" — no fija cuándo ni dónde se escribe; obligaría a inventar el orden respecto de la limpieza.
2. "un pid que no vive (os.kill(pid, 0) da ProcessLookupError)" — no cubre `PermissionError`; obligaría a inventar si cuenta como vivo.
3. "Nunca borra la carpeta propia" — no define cómo se identifica; obligaría a inventar el criterio (comparación por ruta).
4. "una función nueva de limpieza" — sin nombre ni firma; obligaría a inventar API.
5. "se imprime en una línea ("limpieza: <ruta>")" — sin canal ni formato exacto de ruta; obligaría a inventar.
6. "echo \"$PYTEST_ADDOPTS\" > <archivo>" — placeholder sin ruta concreta; obligaría a inventar el archivo del test.

## DRY-RUN

**Lecturas:** `deskops/integrate.py` (`_run_suite` ~195, finally ~283, `_steps` ~303), `tests/test_integrate.py`, `desk/config.json` para `suite`, `tests_lock`, `suite_timeout` (solo lectura). **Cambios previstos:** función de limpieza nueva; `_steps` escribe `owner.pid`; `_run_suite` amplía `PYTEST_ADDOPTS`; limpieza invocada bajo `_suite_lock`. **Dependencias:** `_suite_lock`, `tempfile.gettempdir`, `os.kill`, `cfg`. **Validaciones futuras:** pytest de `tests/test_integrate.py` con `TMPDIR=/dev/shm`; suite `-n 4`; corrida real de integrate. Sin ejecutar nada.

## FUTURO

Un nodo ejecutor implementa p1–p4; dispatch provee el worktree; humano/CI valida y decide el commit con `Task-Id`. No es un agregado: es una tarea de código ejecutable.

PASA

# Resultado del tester

Tarea: `task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas`

Commit del ejecutor: `498d51755c799cb837c156da8ce863890c40629d` ("integrate: suite basetemp inside work dir and stale temp cleanup"), con el trailer `Task-Id` de la tarea. HEAD de verificación: `b3109033` ("run: deskops-t-78553b2e9172"); entre ambos solo hay artefactos de run.

## Archivos revisados del commit

- `deskops/integrate.py`
- `tests/test_integrate.py`

Ambos están dentro de los `files` de la tarea. El commit no toca `desk/config.json`, `deskops/queue.py` ni la limpieza de los testers.

## Comprobaciones contra el Goal

| Punto | Resultado |
|---|---|
| `_run_suite` inyecta `--basetemp=<work>/pytest` en `PYTEST_ADDOPTS` | OK. `work = copy.parent` y `--basetemp={work / 'pytest'}` se agrega al env conservando el valor previo separado por un espacio (`deskops/integrate.py:229-232`). Va por env, no por argv, así que llega al `pytest` invocado dentro de `sh -c`. |
| Cada carpeta de trabajo deja `owner.pid` | OK. `_steps` escribe `owner.pid` con `os.getpid()` inmediatamente después de `mkdtemp` (`deskops/integrate.py:347`). |
| Limpieza al empezar la suite y bajo el lock | OK. `_clean_stale_integrate_dirs` se llama dentro del `with _suite_lock(cfg.tests_lock), ...` y antes del `Popen` (`deskops/integrate.py:234-235`). |
| Criterios de borrado | OK. Borra `deskops-integrate-*` con `owner.pid` de un pid muerto (`os.kill(pid, 0)` -> `ProcessLookupError`) o sin `owner.pid` y `mtime` más viejo que `cfg.suite_timeout`; nunca la carpeta propia ni la de un pid vivo (`deskops/integrate.py:204-227`). |
| Salida de cada carpeta borrada | OK. Imprime `limpieza: <ruta>` (`deskops/integrate.py:226`). |

## Tests ejecutados

El `../.venv` del workspace está roto en este contenedor: su `python3` enlaza a `/usr/bin/python3`, no detecta el venv y no encuentra `pytest`; además su `bin/pytest` apunta a `/home/robocop/proyectos/SLDB_1/.venv/bin/python`, inexistente. Se usó el venv operativo `/mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin/python` (Python 3.13, pytest 9.1.1), que resuelve el `deskops` del worktree. No se corrió la suite completa, según la instrucción del tester.

| Comando | Resultado |
|---|---|
| `TMPDIR=/tmp ... -m pytest -q -p no:cacheprovider tests/test_integrate.py -k 'basetemp or stale_integrate'` | 2 passed, 28 deselected (0,51 s) |
| `TMPDIR=/dev/shm ... -m pytest -q -p no:cacheprovider tests/test_integrate.py -k 'basetemp or stale_integrate'` | 2 passed, 28 deselected (0,41 s) |
| `TMPDIR=/tmp ... -m pytest -q -p no:cacheprovider tests/test_integrate.py` | 30 passed, 1 warning (427,32 s) |
| Los dos tests nuevos contra el commit padre `498d5175^` en un worktree temporal | 2 failed (fallan antes del cambio, como exige el plan) |

## Observaciones

Sin fallas ni riesgos bloqueantes. Detalle menor no bloqueante: `_clean_stale_integrate_dirs` usa `shutil.rmtree(..., ignore_errors=True)` y luego imprime `limpieza:` aunque el borrado hubiera fallado; no afecta los criterios de la tarea.

Veredicto: **PASA**.

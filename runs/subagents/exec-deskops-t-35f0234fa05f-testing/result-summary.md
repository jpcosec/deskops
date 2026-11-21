PASA

# Resultado del tester

Tarea: task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe
Run: run-deskops-t-35f0234fa05f

## Commit del ejecutor

`42b1f6888b150495ee8fe4b753cfd8aa1d7354d2` — "dispatch start: untrack stale RunDoc whose run_dir is missing".
Trailer verificado: `Task-Id: task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe`.

Archivos del commit:
- `deskops/dispatch.py`: antes de `record_scion_run` des-trackea el RunDoc `run-<slug>` de la identidad (si existe en el store) y, si el record falla, borra el `run_dir` solo cuando quedó vacío.
- `tests/test_dispatch.py`: nuevo `test_start_untracks_a_stale_rundoc_whose_run_dir_is_missing`.
- `CHANGELOG.md`: entrada en Fixed.

## Pruebas ejecutadas

- `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`
  -> **38 passed**, 1 warning, exit 0 (369.04 s).

No hay otro módulo de código tocado (`deskops/runtime/scion.py` no se modifica); el archivo de test relevante es `tests/test_dispatch.py`. No se corrió la suite completa (la corre integrate en el host).

## Falla antes / pasa después

Sobre un worktree temporal en `286d9a24` (padre del commit) aplicando solo el test nuevo, el caso objetivo falla con el error reportado:

```text
AssertionError: Store error: Doc 'run-deskops-e-7fc08c3ad3f9' already tracked.
assert 1 == 0
```

Con el commit actual (`42b1f688`), ese mismo test y el resto de `tests/test_dispatch.py` pasan. El worktree temporal se eliminó; no se modificó el repo.

## Cobertura del Done When

- RunDoc trackeado con `run_dir` ausente: `dispatch start` des-trackea y re-registra sin fallar; el test lo verifica y comprueba que no queda la carpeta vacía (`run.md` se escribe y la segunda llamada usa la misma identidad).
- RunDoc trackeado con `run_dir` presente sigue contando como intento: lo cubre `test_attempts_then_no_more` (segundo start usa `-a2` y el tercero devuelve "sin intentos"), también en verde.

## Entorno

El `.venv` del checkout apunta a un Python 3.12 ausente en este contenedor y `python` no está en PATH; se usó `/mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin/python` (3.13.18) con `PYTHONPATH=.` y `TMPDIR=/tmp`. El `sldb` importado resuelve a `/mnt/ssd/proyectos/SLDB_1/sldb/src`, la misma fuente editable que usa el proyecto.

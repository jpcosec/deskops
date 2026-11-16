## REFORMULACION
Encargo de tipo `task.code` sobre el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: evitar el OOM de la suite completa de deskops en un solo proceso bajo `MemoryMax=2G`, causado por caches globales de proceso que `tests/conftest.py` no limpia. Resultado: una fixture `autouse` en `tests/conftest.py` que, tras cada test, invalide los caches de sldb (`invalidate_runtime_cache`, `invalidate_index_cache`, `built_cache.clear`, `alert_sink.forget`) y vacíe los dicts `_READ_HASHES` e `_INDEX_ENTRIES` de `deskops/doc_access.py`, de modo que la suite en un proceso termine sin OOM y con las mismas fallas que `-n 4` sobre `origin/main`. Límites: solo `tests/conftest.py` y, si hiciera falta, `deskops/doc_access.py`; no se modifica sldb ni la regla de `-n 4`.

## AMBIGUEDADES
1. "si alguna no existe con ese nombre en el sldb hermano, se llama a la equivalente y se anota" — no define qué hace "equivalente"; obligaría a inventar el criterio de sustitución.
2. "si hace falta, una funcion publica de limpieza en deskops/doc_access.py" frente a "con .clear() desde la fixture, sin API nueva" — tensión no resuelta; obligaría a inventar si se añade API.
3. "los 3 archivos mas pesados = los 3 primeros de pytest --durations=3" — `--durations` reporta tests/llamadas, no archivos; obligaría a inventar la métrica.
4. "las fallas son las mismas que da -n 4 en un worktree limpio" — no fija criterio de igualdad (IDs, conteo); obligaría a inventar la comparación.

## DRY-RUN
Lecturas: `tests/conftest.py:46` (autouse `_isolated_home`), `deskops/doc_access.py` (~150-154), y las cuatro funciones de sldb citadas. Cambios previstos: añadir `_clear_global_caches` autouse con `yield` y limpieza posterior; eventualmente exponer limpieza en `doc_access.py`. Dependencias: sldb hermano instalado en `../.venv`. Validaciones futuras: corrida `systemd-run --user --scope -p MemoryMax=2G ... pytest -q -p no:xdist tests`; corrida `-n 4`; baseline en worktree de `origin/main` para cada falla; informe con la lista.

## FUTURO
Un nodo ejecutor implementa y commitea; un humano valida la lista de fallas aceptadas y las decisiones sobre equivalencias y API.

REFORMULACION
Propósito: que la suite completa de deskops en un solo proceso no muera por OOM con MemoryMax=2G. Resultado: `tests/conftest.py` incorpora una fixture autouse que, tras cada test, invalida los caches globales de sldb y vacía los caches de módulo de `deskops/doc_access.py`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `tests/conftest.py` y limpieza de `_READ_HASHES` e `_INDEX_ENTRIES`; no se modifica sldb ni se abandona `-n 4`; si falta alguno de los nombres sldb indicados, se detiene y reporta, sin buscar equivalente. No es un agregado: es una tarea `task.code` ejecutable.

AMBIGUEDADES
1. “alrededor de las lineas 150-154”: ubica los caches por rango, no por nombre; obliga a inventar si además de `_READ_HASHES` e `_INDEX_ENTRIES` debe limpiarse `_DOC_PAYLOADS` u otro cache.
2. “las fallas son las mismas que da -n 4 en un worktree limpio”: no define criterio de igualdad; obliga a inventar si compara IDs, número o también skips/xfails.
3. “buscar con tracemalloc el cache que crece y limpiarlo”: no define cómo atribuir crecimiento a un cache ni qué hacer si el crecimiento no es un cache; obliga a inventar el diagnóstico y la acción.

DRY-RUN
Lecturas: TaskDoc, `tests/conftest.py` y `deskops/doc_access.py`; verificar en `../sldb/src` que existan `runtime_cache.invalidate_runtime_cache`, `store.io.invalidate_index_cache`, `store.built_cache.clear` y `cli.alert_sink.forget`. Cambios previstos: en conftest, fixture autouse con `yield` que al final llame a esas cuatro funciones y haga `.clear()` sobre `doc_access._READ_HASHES` y `_INDEX_ENTRIES` (sujeto a ambigüedad 1). Dependencias: nombres exactos de sldb, pytest, `../.venv`, `systemd-run`, `TMPDIR=/dev/shm`. Validaciones futuras: ejecutar los dos comandos de Validation y, si hay fallas, reproducirlas en worktree de `origin/main`. No se ejecuta nada.

FUTURO
Un ejecutor futuro aplicará la fixture y correrá las validaciones; un humano decidirá si las fallas baseline son aceptables y autorizará el commit; el cierre aporta tests y commit.

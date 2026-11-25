## REFORMULACION
Encargo ejecutable de tipo `task.code` en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: evitar el OOM de la suite completa de pytest en un solo proceso bajo `MemoryMax=2G`, limpiando caches globales entre tests. Resultado: una fixture autouse en `tests/conftest.py` que, tras cada test, invoque `sldb.store.runtime_cache.invalidate_runtime_cache()`, `sldb.store.io.invalidate_index_cache()`, `sldb.store.built_cache.clear()` y `sldb.cli.alert_sink.forget()`, y vacíe con `.clear()` los dicts de módulo `_READ_HASHES` e `_INDEX_ENTRIES` de `deskops/doc_access.py`. Límites: no se modifica sldb ni la regla de `-n 4`; si algún nombre de API no existe en `/mnt/ssd/proyectos/SLDB_1/sldb/src`, se detiene y reporta, sin buscar equivalencias.

## AMBIGUEDADES
1. «después de cada test llama a…» y «vacía los caches propios…»: no aclara si la limpieza es solo en teardown o también antes del primer test; obligaría a inventar el orden exacto del `yield`.
2. «alrededor de las líneas 150-154»: los números pueden no coincidir; obligaría a asumir qué dicts exactos son, aunque se nombran `_READ_HASHES` e `_INDEX_ENTRIES`.
3. «si alguna no existe con ese nombre… la tarea se detiene»: no define cómo verificar (import en runtime, inspección) ni si `alert_sink.forget` es atributo de módulo o función; obligaría a inventar el criterio de comprobación.
4. «las fallas son las mismas que da -n 4 en un worktree limpio de origin/main»: no fija el comando base ni si la comparación aplica también a la corrida de un proceso; obligaría a inventar el baseline.
5. «Si no cabe, medir el RSS máximo por archivo… y… buscar con tracemalloc el cache que crece»: «no cabe» no tiene umbral ni criterio de parada; obligaría a inventar cuándo se considera resuelto.

## DRY-RUN
Lecturas: `tests/conftest.py` (fixture `_isolated_home`, línea 46), `deskops/doc_access.py` (zona 150-154), y existencia de los cuatro símbolos en `sldb`. Cambios previstos: una fixture autouse con `yield` y limpieza posterior; sin tocar APIs de deskops. Dependencias: pytest, systemd-run de usuario, `TMPDIR=/dev/shm`, `git worktree`. Validaciones futuras: corrida con `systemd-run --user --scope -p MemoryMax=2G`; corrida `-n 4`; comparación de fallas contra worktree de `origin/main`; si hay OOM, medición por archivo y `tracemalloc`.

## FUTURO
Otro nodo/humano decide: confirmar la existencia y firma de las APIs de sldb; aceptar o rechazar la lista de fallas preexistentes; autorizar la ruta de medición si no cabe; y ejecutar el commit final exigido por el átomo.

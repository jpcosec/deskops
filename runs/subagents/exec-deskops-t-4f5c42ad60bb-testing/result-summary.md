PASA

# Result summary

Commit revisado: `196f3cb912269562b1282745f23e58fc63fef758` ("tests: autouse fixture clears global sldb/deskops caches after each test", con trailer `Task-Id`). Solo toca `tests/conftest.py` (+21 líneas).

## Implementación

- Añade la fixture autouse `_clear_global_caches` con `yield`; tras cada test llama a `runtime_cache.invalidate_runtime_cache()`, `store_io.invalidate_index_cache()`, `built_cache.clear()` y `alert_sink.forget()`.
- Vacía los caches de módulo de `deskops/doc_access.py`: `_DOC_PAYLOADS`, `_READ_HASHES` e `_INDEX_ENTRIES`. `_DOC_PAYLOADS` no estaba nombrado en el Scope pero está dentro del rango indicado (líneas ~151-158) y es necesario para el objetivo de memoria.
- Verificado en el sldb hermano (`/mnt/ssd/proyectos/SLDB_1/sldb/src`) que existen los cuatro nombres exactos: `sldb.store.runtime_cache.invalidate_runtime_cache`, `sldb.store.io.invalidate_index_cache` (paquete `store/io/__init__.py`), `sldb.store.built_cache.clear` y `sldb.cli.alert_sink.forget`. No hizo falta detenerse.

## Verificación de la fixture

Test temporal (creado y borrado, fuera del commit) en dos tests:
1. el primero llena `runtime_cache._DOCS`, `store_io._INDEXES/_SAVED`, `built_cache._MEM`, `alert_sink._KEPT` y los tres dicts de `doc_access`;
2. el segundo comprueba al arrancar que todos están vacíos.

Resultado: `2 passed`. La limpieza autouse funciona para sldb y deskops.

## Tests ejecutados (de a un archivo, `TMPDIR=/tmp`, `-p no:xdist`)

Se usó `../sldb/.venv/bin/python` porque `../.venv/bin/python` (3.11) no tiene `markdown_it` instalado en este host.

- `tests/test_doc_readability.py`: 6 passed
- `tests/test_transaction.py`: 11 passed
- `tests/test_taskdoc_read_without_overlay.py`: 1 passed
- `tests/test_tracked_selector_resolution.py`: 15 passed
- `tests/test_ascii_ids.py`: 6 passed
- `tests/test_lifecycle_graph.py`: 24 passed
- `tests/test_desk_paths.py`: 16 passed

Total: 79 passed, 0 fallas. No hay fallas que comparar contra `origin/main`.

## Pendiente para integración

No se corrió la suite completa ni la medición single-process bajo `systemd-run -p MemoryMax=2G`: la instrucción del tester prohíbe correrla aquí y la integra el host. La evidencia de esta fase cubre la corrección de la fixture, la existencia de los símbolos y que los tests relevantes siguen verdes.

## REFORMULACION
Encargo: mover las salidas derivadas de `deskops graph export` y `self_reflection` de `.sldb/runtime/` a `.sldb_cache/`, conservando la estructura de subcarpetas. Resultado: ninguna ruta de escritura en `deskops/` apunta a `.sldb/runtime/`; si un consumidor externo lee la ruta vieja, se le notifica por inbox. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no migrar ni borrar archivos existentes, no tocar `sldb`, revisar solo `graph_ui` como consumidor.

## AMBIGUEDADES
1. "cuerpo con las rutas viejas y nuevas y el hash": no se define de qué es el hash (¿commit, tarea, nota `c420809c`?). Obligaría a inventar el referente.
2. Goal "nada en deskops/ escribe en .sldb/runtime/" vs validación "! grep -rnF '.sldb/runtime' deskops/ --include=*.py": el grep prohíbe toda mención, incluida `EXCLUDED_SOURCE_PREFIXES = (".sldb/runtime/", ...)` en `self_reflection.py`, que no es una escritura. Habría que decidir si se reescribe a `.sldb_cache/` o se elimina, sin criterio explícito.
3. Pill-010: "prefer `.sldb/runtime/` or another agreed ignored runtime location" y "Add or update ignore rules when a new runtime path is introduced", frente a "tests/test_gitignore_policy.py se toca solo si afirma algo sobre .sldb/runtime" y la afirmación no verificada "lo derivado vive en .sldb_cache/, ignorada". No queda claro si procede añadir `.sldb_cache` a `.gitignore`.
4. Scope limita la búsqueda: "grep -rn '.sldb/runtime' /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui ... (excluyendo runs/)", pero el Goal dice "Si algun consumidor fuera de deskops lee la ruta vieja". Ámbito de búsqueda más estrecho que el criterio de cierre.
5. `tests/test_graph_cli.py` figura en Validation pero no en `files` ni en Scope; se ignora si debe modificarse o solo ejecutarse.

## DRY-RUN
Lecturas: `export.py`, `self_reflection.py`, `test_graph_snapshot.py`, `test_graph_self_reflection.py`, `tests/test_gitignore_policy.py`, `.gitignore`, grep de consumidores en `graph_ui`. Cambios previstos: crear `deskops/graph/paths.py` con `DERIVED_ROOT = Path('.sldb_cache')`; reemplazar constantes en `export.py:22` y `self_reflection.py:17-18,39` (y `EXCLUDED_SOURCE_PREFIXES`); ajustar aserciones de tests; opcionalmente `.gitignore`/`test_gitignore_policy.py`; nota inbox a `graph_ui` si hay lectores. Dependencias: API `sldb.api.graph.snapshot.GraphSnapshot`, venv `../.venv`, worktree de `origin/main`. Validaciones futuras: los seis comandos del TaskDoc, incluida la suite completa y comparación de fallas en worktree limpio; commit descriptivo al cierre.

## FUTURO
Un humano decide el alcance real de la búsqueda de consumidores y el borrado manual de archivos viejos no versionados; el emisor confirma el hash de la nota y su envío; el nodo de closeout ejecuta tests, registra fallas preexistentes y crea el commit.

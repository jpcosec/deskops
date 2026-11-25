REFORMULACION
Propósito: mover las salidas derivadas de graph export y self_reflection de `.sldb/runtime/` a `.sldb_cache/`, porque el store versionado es `.sldb/`. Repo: `SLDB_1/deskops` (consumidores en SLDB_1). Resultado: `deskops/graph/paths.py` con `DERIVED_ROOT = Path('.sldb_cache')`, importado por `export.py` y `self_reflection.py`; cada salida conserva su ruta relativa bajo `.sldb_cache/` (`graphs/deskops.kg.json`, `graphs/deskops.nx.json`, `self_reflection_findings.json`, `self_reflection_decisions.json`). Ningún código de `deskops/` escribe en `.sldb/runtime/`; se conservan menciones de exclusión/lectura. Actualizar pill-010 vía `deskops edit pill` a `.sldb_cache/`; ajustar tests; avisar consumidores con título, rutas viejas/nuevas y hash; cerrar con tests y commit. Límites: no migrar ni borrar archivos existentes, no tocar sldb.

AMBIGUEDADES
1. Goal: "grep -rnF '.sldb/runtime' en /mnt/ssd/proyectos/SLDB_1 excluyendo runs/ y .git"; Scope: "`grep -rn '.sldb/runtime' /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui --include=*.py --include=*.js`". Obliga a inventar si se busca todo SLDB_1 o solo graph_ui, y a quién avisar.
2. "las menciones que solo excluyen o leen esa ruta vieja (p. ej. EXCLUDED_SOURCE_PREFIXES) se conservan". No ordena añadir `.sldb_cache/`; obliga a decidir si las salidas nuevas se excluyen del grafo.
3. Implementation Path: "`grep -rn 'sldb/runtime\|"runtime"' deskops/graph deskops/services`", pero Scope/files solo nombran `deskops/graph/*` y tests. Obliga a decidir si `services/` entra.
4. "tests/test_gitignore_policy.py si hace falta" y "se toca solo si afirma algo sobre .sldb/runtime": obliga a decidir si un test sobre `.sldb_cache` ignorada requiere cambio.

DRY-RUN
Lecturas: TaskDoc, pill-010, export.py, self_reflection.py, tests, `.gitignore`, grep de consumidores. Cambios: crear `paths.py`; reemplazar constantes `DEFAULT_*` por `DERIVED_ROOT / ...`; actualizar `runtime_output_path` y expectativas; actualizar pill; valorar exclusión de `.sldb_cache/`; no borrar. Dependencias: `GraphSnapshot`, `deskops edit pill`, `deskops message send`, commit. Validaciones futuras: pytest de snapshot, self_reflection, gitignore, graph_cli; grep sin escrituras; suite completa y baseline en worktree limpio.

FUTURO
El commit produce el hash; un humano decide borrar archivos viejos no versionados y ejecuta/autoriza el aviso; los consumidores deciden migrar sus lecturas.

REFORMULACION
Nodo ejecutable `task.code`, no agregado. Propósito: sacar las salidas derivadas de deskops de `.sldb/runtime/`, alineándolas con sldb c420809c. Resultado: nuevo `deskops/graph/paths.py` con `DERIVED_ROOT = Path('.sldb_cache')`; `export.py` y `self_reflection.py` escriben bajo `.sldb_cache/` conservando sus subrutas relativas; tests y pill-010 actualizados; consumidores externos avisados. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no migrar ni borrar archivos viejos, no tocar sldb; conservar menciones de exclusión/lectura de `.sldb/runtime/`; cerrar con commit.

AMBIGUEDADES
1. Alcance de consumidores: Goal dice “grep -rnF '.sldb/runtime' en /mnt/ssd/proyectos/SLDB_1 excluyendo runs/ y .git” y “si alguno fuera de deskops lee”; Scope dice “grep -rn '.sldb/runtime' /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui”. Obliga a inventar si buscar todo SLDB_1 o solo graph_ui.
2. “si alguno fuera de deskops lee la ruta vieja”: un hit textual no prueba lectura. Obliga a inventar el criterio para distinguir mención/documentación de lectura real y decidir el aviso.
3. `tests/test_graph_cli.py` aparece en Validation pero no en Scope/files. Si falla por la ruta, obliga a inventar si editarlo pese a no estar en alcance.
4. `EXCLUDED_SOURCE_PREFIXES` conserva `.sldb/runtime/`, pero no se indica añadir `.sldb_cache/`. Obliga a inventar si la nueva salida debe excluirse del análisis de source files.
5. “tests/test_gitignore_policy.py si hace falta” no define el disparador exacto; obliga a inventar si basta con que exista o solo si afirma algo sobre `.sldb/runtime`.

DRY-RUN
Lecturas: TaskDoc, pill-010, átomos, `export.py`, `self_reflection.py`, tests nombrados, `test_graph_cli`, `test_gitignore_policy` y resultados de grep. Cambios previstos: crear `paths.py`; reemplazar constantes por `DERIVED_ROOT` y subrutas `.sldb_cache/graphs/deskops.kg.json`, `.sldb_cache/self_reflection_findings.json`, `.sldb_cache/self_reflection_decisions.json`; actualizar expectativas de tests; actualizar pill-010 con `deskops edit pill`; avisar consumidores con `deskops message send` si corresponde; commit descriptivo. Dependencias: API `sldb.api.graph.snapshot`, pytest, git y CLI deskops. Validaciones futuras: los seis comandos listados, grep sin escrituras, suite completa y baseline en worktree limpio de `origin/main` para fallas.

FUTURO
El ejecutor produce el commit y su hash; otro nodo o un humano valida el informe de fallas preexistentes y decide aceptar el cierre. La actualización de pill y el aviso a consumidores quedan como efectos verificables del cierre.

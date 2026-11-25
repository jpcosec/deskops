## REFORMULACION

Encargo ejecutable (no agregado): en el repo `deskops`, mover las salidas derivadas de `graph export` y `self_reflection` de `.sldb/runtime/` a `.sldb_cache/`. Resultado: módulo nuevo `deskops/graph/paths.py` con `DERIVED_ROOT = Path('.sldb_cache')`, importado por `export.py` y `self_reflection.py`, conservando cada ruta relativa actual; ningún código de `deskops/` escribe en `.sldb/runtime/` (solo quedan menciones de exclusión/lectura); `pill-010` actualizada vía `deskops edit pill`; consumidores externos avisados; tests listados y suite completa en verde; commit con tests. Límites: no migrar ni borrar archivos viejos, no tocar `sldb`.

## AMBIGUEDADES

1. Alcance de búsqueda contradictorio: «grep -rnF '.sldb/runtime' en /mnt/ssd/proyectos/SLDB_1 excluyendo runs/ y .git» frente a «`grep -rn '.sldb/runtime' /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui ...`». Obliga a inventar si se busca en todo SLDB_1 o solo en `graph_ui`.
2. Destinatario del aviso: «`deskops message send --to <repo>`» frente a «`deskops message send --to graph_ui`». Obliga a inventar el mapeo repo→destinatario y el criterio si aparecen varios.
3. «si alguno fuera de deskops lee la ruta vieja»: un grep no distingue lectura de comentario/test. Obliga a inventar el criterio de “consumidor”.
4. «DERIVED_ROOT = Path('.sldb_cache')»: ruta relativa sin ancla explícita (cwd vs raíz del repo). Obliga a inventar desde dónde se resuelve, sobre todo en tests.
5. «tests/test_gitignore_policy.py se toca solo si afirma algo sobre .sldb/runtime»: no dice qué debe afirmar tras el cambio. Obliga a inventar la aserción esperada.
6. «el hash del commit de esta tarea»: el hash no existe hasta después del commit. Obliga a inventar el orden commit→aviso y qué hash usar si hay varios commits.

## DRY-RUN

Lecturas: `export.py`, `self_reflection.py`, ambos tests, `test_gitignore_policy.py`, `test_graph_cli.py`, `pill-010`, `.gitignore`.
Cambios previstos: crear `paths.py`; sustituir literales de escritura por `DERIVED_ROOT`; ajustar tests; editar pill vía comando; grep de consumidores.
Dependencias: `deskops` CLI operativo para editar pill y enviar mensajes; `.venv` y `pytest`; `git worktree` para baseline.
Validaciones futuras: los cinco comandos de pytest, el grep sin escrituras, suite completa; fallas nuevas contra `origin/main` en worktree.

## FUTURO

Otro nodo/humano debe: resolver las ambigüedades 1–4 antes de ejecutar; ejecutar el commit y aportar el hash para el aviso; decidir si procede modificar `graph_ui`; confirmar el contenido final de `pill-010`.

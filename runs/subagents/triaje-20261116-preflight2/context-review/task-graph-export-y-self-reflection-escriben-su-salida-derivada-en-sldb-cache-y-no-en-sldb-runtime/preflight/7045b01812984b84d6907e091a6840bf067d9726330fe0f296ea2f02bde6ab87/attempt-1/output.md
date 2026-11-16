## REFORMULACION
**Propósito:** que las salidas derivadas de graph export y self reflection dejen de escribirse en `.sldb/runtime/` y pasen a `.sldb_cache/`.
**Resultado:** crear `deskops/graph/paths.py` con `DERIVED_ROOT = Path('.sldb_cache')`; importarla desde `export.py` y `self_reflection.py`, conservando cada ruta relativa; ajustar tests; verificar que `deskops/` no contiene `.sldb/runtime`; avisar a `graph_ui` si consume la ruta vieja.
**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.
**Límites:** no migrar ni borrar archivos existentes, no tocar `sldb`, solo contactar fuera de `deskops` a `graph_ui`; `test_gitignore_policy.py` solo se modifica si afirma algo sobre `.sldb/runtime`. No es un agregado.

## AMBIGUEDADES
1. Alcance contradictorio: “`grep -rn 'sldb/runtime\|"runtime"' deskops/graph deskops/services`” frente a “Entra: deskops/graph/export.py, deskops/graph/self_reflection.py”. Obliga a inventar si `deskops/services` puede modificarse.
2. “cuerpo con las rutas viejas y nuevas y el hash”: no se especifica qué hash. Obliga a elegir entre hash de tarea, commit, nota `c420809c` u otro.
3. “nada en deskops/ escribe en .sldb/runtime/” frente a la validación limitada a “`grep -rnF '.sldb/runtime' deskops/ --include=*.py`”. Obliga a decidir si también deben revisarse archivos no Python.
4. “tests/test_gitignore_policy.py se toca solo si afirma algo” pero la validación lo ejecuta siempre. Obliga a decidir si basta ejecutarlo sin modificarlo.

## DRY-RUN
**Lecturas:** `export.py`, `self_reflection.py`, tests citados, `test_gitignore_policy.py`; `grep` en `deskops/` y en `graph_ui` excluyendo `runs/`.
**Cambios previstos:** nuevo `paths.py`; imports y rutas en los dos módulos; ajustes de tests solo si codifican la ruta vieja.
**Dependencias:** intérprete `../.venv`, pytest, acceso a `graph_ui`, CLI `deskops message send`.
**Validaciones futuras:** los cinco pytest indicados, el `grep` negativo y la suite completa con `-n 4`; fallas comparadas en worktree limpio de `origin/main`. No se ejecuta nada aquí.

## FUTURO
El ejecutor dejará cambios, pruebas e informe; un humano decidirá borrar manualmente archivos viejos no versionados y `graph_ui` decidirá actualizar su consumo.

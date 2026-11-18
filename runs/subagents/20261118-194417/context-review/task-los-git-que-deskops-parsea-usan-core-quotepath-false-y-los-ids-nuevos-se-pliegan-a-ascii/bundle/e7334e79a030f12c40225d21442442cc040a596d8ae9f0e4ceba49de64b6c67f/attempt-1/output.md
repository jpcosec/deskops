## REFORMULACION
Nodo ejecutable de código en el repo `deskops`. Propósito: que todo git cuyo stdout deskops parsea use `-c core.quotepath=false` y que los ids derivados de títulos se plieguen a ASCII, para que rutas citadas con escapes octales no rompan el parseo. Resultado: helper único `ascii_slug` en `deskops/slugs.py` (NFKD + descarte de marcas + regla de `drawer._slug`), tres llamadores migrados (`compiler.py`, `doc_access.py`, `drawer.py`), la opción añadida en `closure.py` e `integrate.py`, y `tests/test_ascii_ids.py`. Límites: no renombrar/migrar ids acentuados existentes, no tocar el hook externo de worktrees, no cambiar longitudes máximas, no usar `-z`, no cubrir llamadas git armadas dinámicamente. Átomos: cerrar con tests y commit; mutaciones CLI contra sandbox.

## AMBIGUEDADES
1. "Incluye además deskops/integrate.py (posterior a esta tarea)" frente a que su test entra en Validation. Obligaría a inventar si el cambio de `integrate.py` se implementa ahora o queda para otra tarea.
2. "se aplica la regla de colisión que ya tenga add task" sin nombrarla. Obligaría a inventar el comportamiento ante id plegado duplicado.
3. "la longitud maxima de cada llamador se conserva" sin indicar el límite del helper compartido (`drawer._slug` no trunca; los otros usan 100). Obligaría a inventar el truncado de `ascii_slug`.
4. "cualquier otra llamada git con salida parseada" frente a "llamadas armadas dinámicamente ... quedan fuera". Obligaría a inventar el alcance exacto de la auditoría.

## DRY-RUN
Lecturas: los cuatro archivos nombrados, `grep -rn` de llamadas git, tests existentes de closeout/cli y `tests/test_ascii_ids.py` (inexistente). Cambios previstos: crear `deskops/slugs.py`; sustituir `_slugify`, `slugify` y `_slug` por `ascii_slug`; insertar `-c core.quotepath=false` en cada argv git parseado de `closure.py` e `integrate.py`; escribir el test nuevo con los tres casos. Dependencias: `sldb.api`, pytest, git, `TMPDIR=/dev/shm`. Validaciones futuras: los cuatro comandos pytest del TaskDoc; `grep -rn quotepath deskops/`; comparación de fallas en worktree limpio de `origin/main`; commit descriptivo.

## FUTURO
Un humano decide la regla de colisión y si `integrate.py` entra ahora. Otro nodo ejecuta la suite y el worktree base. El hook externo y el renombrado de ids históricos quedan fuera de este repo.

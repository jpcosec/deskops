## REFORMULACION

**Propósito:** ejecutar la tarea `task-los-git-...` en el repo `deskops`, corrigiendo dos problemas: llamadas a git cuya salida se parsea sin desactivar el citado de rutas, y generación de ids nuevos con acentos.

**Resultado esperado:** (1) toda llamada git parseada usa `-c core.quotepath=false` o `-z`; (2) `compiler.py`, `doc_access.py` y `drawer.py` comparten un helper que pliega títulos a ASCII; (3) los ids acentuados existentes siguen resolviendo por selector exacto, sin renombrarse; (4) `tests/test_ascii_ids.py` cubre generación ASCII, resolución de ids existentes y parseo de nombres acentuados no trackeados.

**Repo:** `deskops`; archivos citados bajo `deskops/` y `tests/`.

**Límites:** no renombrar ni migrar ids ya commiteados; no tocar el hook externo de worktrees; no cambiar la longitud máxima de ids.

## AMBIGUEDADES

1. “un modulo comun” no identifica archivo ni API. Obliga a inventar dónde ubicar `ascii_slug(text)` y cómo importarlo.
2. “luego la regla de caracteres actual” no explicita esa regla. Obliga a inferirla desde `drawer.py` o inventar el tratamiento exacto de separadores y caracteres no ASCII.
3. “sin fallas nuevas respecto de main” no define baseline, comando ni entorno de comparación. Obliga a inventar el criterio de comparación.
4. “cualquier otra llamada git con salida parseada que muestre `grep -rn '\"git\"' deskops/`” no acota si incluye llamadas indirectas o construidas dinámicamente. Obliga a inventar el alcance de la auditoría.

## DRY-RUN

**Lecturas previstas:** el TaskDoc, la nota referenciada, los archivos listados, `grep` de llamadas git y tests existentes.

**Cambios previstos:** crear helper compartido; sustituir las tres implementaciones; añadir `-c core.quotepath=false` o `-z` a llamadas git parseadas; crear `tests/test_ascii_ids.py`.

**Dependencias:** entorno Python con pytest, git disponible, `TMPDIR=/dev/shm`, sandbox de desk para tests CLI.

**Validaciones futuras:** ejecutar el test nuevo, `test_closeout.py`, `test_cli.py` y la suite completa; comprobar `grep -rn quotepath deskops/`.

Sin ejecución.

## FUTURO

Otro nodo implementará y entregará el diff, los tests ejecutados y el commit. Un humano o nodo de cierre decidirá si la suite no tiene fallas nuevas respecto de `main` y aceptará que los ids acentuados existentes no se migran.

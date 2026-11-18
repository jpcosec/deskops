## REFORMULACION

Encargo de código en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Propósito:** que las salidas de git que deskops parsea no traigan rutas citadas con escapes octales y que los ids derivados de títulos se plieguen a ASCII, sin tocar ids ya existentes.

**Resultado esperado:** (1) toda llamada git cuya salida se parsea lleva `-c core.quotepath=false`; (2) un helper único `ascii_slug` en `deskops/slugs.py` (NFKD + descarte de marcas + regla `_slug` de `drawer.py`) usado por `compiler.py`, `doc_access.py` y `drawer.py`; (3) ids explícitos del usuario intactos y los acentuados existentes siguen resolviendo por selector exacto, sin renombrar ni migrar; colisión según la regla vigente de `add task`.

**Límites:** no renombrar/migrar ids commiteados, no tocar el hook externo de worktrees, no cambiar longitudes máximas; test nuevo `tests/test_ascii_ids.py`.

## AMBIGUEDADES

1. «Incluye además deskops/integrate.py (posterior a esta tarea): load_closed_task y _receipt_commit» — no queda claro si el ejecutor debe modificar `integrate.py` ahora o si solo se documenta como fallo conocido posterior; obligaría a inventar el orden de entrega.
2. «cualquier otra llamada git con salida parseada» frente a «La auditoria cubre las llamadas a subprocess cuyo argv empieza con 'git' … llamadas armadas dinamicamente … quedan fuera» — obliga a inventar el criterio ante llamadas indirectas.
3. «se aplica la regla de colision que ya tenga add task» — exige leer el código para conocerla; no obliga a inventar, pero sí a fijar cuál es la vigente si hay varias.

## DRY-RUN

**Lecturas:** `compiler.py` (155-159), `doc_access.py` (157-161), `drawer.py` (288-290), `closure.py` (~645, ~695, ~1555), `integrate.py` (~100), `grep -rn '"git"' deskops/`, tests existentes de CLI/closeout.

**Cambios previstos:** crear `deskops/slugs.py`; sustituir las tres implementaciones de slug; añadir `-c core.quotepath=false` a cada argv git auditado; crear `tests/test_ascii_ids.py` con los tres casos descritos.

**Dependencias:** `.venv` en `../.venv`, `TMPDIR=/dev/shm`, desk sandbox para el test de `add task`.

**Validaciones futuras:** los cuatro comandos pytest listados (incluida suite completa `-n 4`) y comparación de fallas en worktree limpio de `origin/main`.

## FUTURO

Un nodo ejecutor producirá el informe con la lista de fallas preexistentes verificadas en `origin/main`; un humano decidirá si `integrate.py` entra en esta entrega o en otra; el hook de worktrees queda fuera del repo.

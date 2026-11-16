REFORMULACION
Propósito: que las rutas git que deskops parsea no salgan citadas con escapes octales y que los ids derivados de títulos se plieguen a ASCII sin romper ids acentuados existentes. Resultado: helper `ascii_slug` en `deskops/slugs.py`, `-c core.quotepath=false` en las llamadas git parseadas y test `tests/test_ascii_ids.py`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no renombrar ni migrar ids, no tocar el hook externo de worktrees, no cambiar la longitud máxima; quedan fuera llamadas git armadas dinámicamente que el grep no detecte.

AMBIGUEDADES
1. "los rituales enrutados por el Board, las pills ligadas": el bundle solo aporta TaskDoc, átomos y archivos; faltan rituales y pills, así que usarlos obligaría a inventar su contenido.
2. "Toda llamada a git dentro de deskops cuya salida se parsea": no define cómo decidir qué salida se parsea; obligaría a inventar el criterio de clasificación.
3. "se aplica la regla de colision que ya tenga add task": no se muestra esa regla; obligaría a inventar su comportamiento.
4. "un archivo sin trackear con nombre acentuado en .sldb no rompe el parseo de git del cierre": no concreta qué parseo del cierre ni qué comando; obligaría a inventar el escenario.

DRY-RUN
Lecturas: TaskDoc, átomos, `deskops/specs/compiler.py`, `deskops/doc_access.py`, `deskops/services/drawer.py`, `deskops/services/closure.py` y `grep -rn '"git"' deskops/`. Cambios previstos: crear `deskops/slugs.py` con `ascii_slug` (NFKD, descarte de marcas, regla `re.sub(r'[^a-z0-9]+','-')` y `strip('-')`), sustituir `_slugify`, `slugify` y `_slug` conservando el truncado de cada llamador; añadir `-c core.quotepath=false` a cada `subprocess` con argv que empiece por `git` y salida parseada; crear `tests/test_ascii_ids.py`. Dependencias: `unicodedata`, `re`, `subprocess`, desk sandbox para mutaciones CLI. Validaciones futuras: los cuatro comandos pytest indicados, incluida la suite completa, comparación de fallas en worktree de `origin/main` y `grep -rn quotepath deskops/`.

FUTURO
Un nodo ejecutor implementará los cambios y correrá las validaciones; un humano decidirá la regla de colisión si no está documentada y confirmará que el hook externo queda fuera. El informe recogerá las fallas preexistentes aceptadas.

## REFORMULACION

**Propósito:** corregir `extend_tip` (`deskops/integrate.py:226`) para que extienda el tip sobre un merge de la rama remota cuando, tras el closeout, lo único que queda son commits de `desk/`, `.sldb/` o `runs/`. No rebasear: reescribiría los sha citados por los recibos.

**Resultado:** `extend_tip` devuelve HEAD si (a) la rama remota configurada (`cfg.remote`/`cfg.branch`, la del paso fast-forward) es ancestro de HEAD y (b) los archivos tocados por los commits de `tip..HEAD` ausentes en el remoto, sin merges, están solo bajo `desk/`, `.sldb/` o `runs/`. Sin cambio para el caso actual de commits de desk sin merge. Pruebas nuevas en `tests/test_integrate.py` y entrada en CHANGELOG.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Límites:** dentro, `extend_tip` (y, si hace falta, cómo recibe la ref remota), sus tests y CHANGELOG; fuera, el resto de pasos de integrate.

## AMBIGUEDADES

1. "si hace falta, cómo recibe la ref remota" — pueden decidir cambiar su firma; sin más input, un ejecutor debe inventar el contrato entre extend_tip y el paso fast-forward.
2. "`git log --no-merges --name-only --format= HEAD ^tip ^<remoto>`" — el placeholder y la composición exacta con `^tip` no están definidos; obliga a inventar la invocación.
3. "el remoto recibe un commit de código de otro" — no se dice qué ruta ni qué commit; obliga a inventar el fixture.
4. "un commit de código local (no del remoto)" — no se aclara si "código" equivale a no-whitelisted; obliga a inventar el criterio del test p2.
5. "los gates corren igual sobre la copia limpia del tip extendido" — no se nombran los gates; obliga a inventar cuáles son y que no hay que tocar.
6. "el caso actual de commits de desk sin merge" — no se cita el test ni el escenario; obliga a inspeccionar el repo para reconstruirlo.

## DRY-RUN

**Lecturas:** `deskops/integrate.py` (`extend_tip` y paso fast-forward, definición de `cfg`), `tests/test_integrate.py`, CHANGELOG, historial git del closeout `651a42a0`.
**Cambios previstos:** tests p1 y p2 junto a `test_tip_extends_over_later_desk_only_commits`; modificar `extend_tip` para comprobar ancestría del remoto y filtrar rutas cambiadas; CHANGELOG; commit con `git commit -- <rutas>` y trailer Task-Id.
**Dependencias:** remoto configurado y accesible, refs actualizadas, git y pytest disponibles.
**Validaciones futuras:** `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py`; que el dry-run de integrate no falle en fast-forward; suite completa.

## FUTURO

El nodo ejecutor implementará y correrá pytest; un humano revisará el commit y el CHANGELOG; el pipeline de integrate validará los gates sobre el tip extendido.

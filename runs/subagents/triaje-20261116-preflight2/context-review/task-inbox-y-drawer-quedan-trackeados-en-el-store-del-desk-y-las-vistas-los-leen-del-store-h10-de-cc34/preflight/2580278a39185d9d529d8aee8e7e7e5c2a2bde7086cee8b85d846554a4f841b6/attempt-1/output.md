## REFORMULACION

**Propósito:** que el store del desk de deskops trackee inbox y drawer, y que `deskops view` los lea vía `run_view` en lugar del disco.

**Resultado:** (1) `deskops/data/desk_declaration.yaml` con globs de `desk/inbox/*.md` y `desk/drawer/tasks/*.md`; (2) los comandos que escriben en el drawer trackean la nota/item al escribir; (3) `deskops view` obtiene drawer e inbox del store; (4) tests y aviso a `graph_ui` con el hash del commit.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Límites:** no backend ni robocop2; no verificación en navegador (la hace `graph_ui`); no migrar desks ajenos.

Es un TaskDoc: documento de encargo, no un nodo ejecutable por sí mismo.

## AMBIGUEDADES

1. «deskops/cli/commands/drawer.py si escriben en el drawer, y sus tests» — el `files:` solo lista `view.py`, `message.py`, `promote.py` y `tests/test_view.py`. Obliga a inventar si `drawer.py` y los otros tests entran en el diff.
2. «incluye los globs de inbox y drawer» — no da rutas ni sintaxis exactas. Obliga a inventar los patrones.
3. «los comandos que escriben en el drawer … trackean al escribir» — no indica API ni punto de tracking. Obliga a inventar el mecanismo.
4. «`deskops view` saca drawer e inbox de run_view como board y task» — no aclara qué colección mapea a `board` y cuál a `task`. Obliga a inventar el mapeo.
5. «el alta de items del drawer» — no nombra comando ni entrada. Obliga a inventar cuál es.
6. «el hash de la nota a graph_ui es el del commit que implementa esta tarea» — no fija si es el commit final o el de cierre. Obliga a inventar el momento.

## DRY-RUN

Un ejecutor futuro leería `desk_declaration.yaml`, `view.py`, `message.py`, `promote.py`, `drawer.py` y los tests citados. Cambiaría globs, añadiría tracking en escrituras del drawer, sustituiría lecturas de disco por `run_view` y ampliaría tests. Dependencias: API de tracking existente, semántica de `run_view`. Validaría con los pytest indicados y la suite completa, comparando fallas en worktree limpio de `origin/main`.

## FUTURO

`graph_ui` verifica en navegador drawer e inbox; un humano valida el informe de fallas y autoriza el cierre.

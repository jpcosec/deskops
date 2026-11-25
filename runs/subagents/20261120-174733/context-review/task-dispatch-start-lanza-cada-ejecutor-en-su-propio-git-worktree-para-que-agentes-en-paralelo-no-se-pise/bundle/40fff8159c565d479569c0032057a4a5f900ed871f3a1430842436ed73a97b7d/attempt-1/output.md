## REFORMULACION

**Propósito:** eliminar la colisión de árboles de trabajo cuando `dispatch start` lanza varios ejecutores en paralelo sobre un mismo repo, tal como ocurrió en SLDB (el commit 0f91540d arrastró cambios de otras tres tareas y eb42a49e quedó vacío).

**Resultado:** `dispatch start` crea por ejecutor un git worktree propio con rama `deskops/<agente>` desde la punta local, bajo `<repo>/.worktrees/<agente>` (ignorado por git); el agente trabaja y commitea ahí, el tester prueba ese worktree, y al cierre `integrate`/`closeout` trae el commit a la rama principal (cherry-pick/rebase + fast-forward), borrando worktree y rama.

**Repo:** `deskops` (cwd `/mnt/ssd/proyectos/SLDB_1/deskops`). Superficie: `dispatch.py` (start y reap), template de scion o prompt, `integrate.py`/closeout, tests, `docs/operator-manual.md`, CHANGELOG.

**Límites:** fuera de alcance: scion. Tipo `task.code`; validación acotada a `tests/test_dispatch.py` y `tests/test_integrate.py`; la suite completa la corre `integrate`.

## AMBIGUEDADES

1. «integrate (o closeout)»: no fija cuál de los dos integra ni borra. Obligaría a inventar el punto de cierre y su responsabilidad.
2. «el template de scion o el prompt»: dos superficies alternativas sin criterio de elección. Obligaría a inventar cuál se modifica.
3. «p. ej. <repo>/.worktrees/<agente>, ignorado por git»: no dice cómo se añade la ignorancia (`.gitignore` versionado, exclude local o flag). Obligaría a inventar el mecanismo.
4. «rama 'deskops/<agente>'»: no define el identificador de agente ni la colisión de nombres entre ejecutores homónimos. Obligaría a inventar la regla de nombrado/unicidad.
5. «cherry-pick o rebase y fast-forward»: operaciones alternativas sin condición de uso. Obligaría a inventar la política ante conflictos.
6. «el coordinador retiene los ejecutores de un repo mientras otro trabaja en él»: parece describir el comportamiento actual, no un requisito exigido. Obligaría a decidir si se conserva o se retira.

## DRY-RUN

**Lecturas:** `deskops/dispatch.py` (start, reap), `deskops/integrate.py`, closeout, template/prompt de scion, `tests/test_dispatch.py`, `tests/test_integrate.py`, `.gitignore`, `docs/operator-manual.md`, CHANGELOG; contexto del commit bdf06f81. **Cambios previstos:** creación/limpieza de worktrees y ramas en start/reap; instrucción al agente para operar en su worktree; integración de la rama en el cierre; tests nuevos de aislamiento, reap e integración selectiva; docs y CHANGELOG. **Dependencias:** dispatch paralelo (bdf06f81) y semántica actual de cherry-pick de `integrate`. **Validaciones futuras:** `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py tests/test_integrate.py`; después, suite completa por `integrate`. Nada ejecutado.

## FUTURO

- El informe de p1 (visibilidad del worktree en el contenedor y vía del commit a main) debe aprobarse antes de implementar.
- El tester prueba el worktree del ejecutor y el `integrate` quien cierra ejecuta la suite completa.
- Un humano decide conflictos de integración y el momento de borrar rama/worktree.

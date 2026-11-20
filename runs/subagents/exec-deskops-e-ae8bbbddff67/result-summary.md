run_id: run-deskops-e-ae8bbbddff67
session: scion://agent/deskops-e-ae8bbbddff67
session_sha256: (no session file; scion agent)

# Resultado: dispatch start/reap con worktree por ejecutor

## Diseño
- start executor: rama `deskops/<name>` desde la rama local de `integrate.branch` (main si no hay bloque), worktree `<root>/.worktrees/<name>`; `.worktrees/` se agrega a .git/info/exclude. Si el checkout principal no esta en esa rama: exit 8, no lanza. Si scion start falla, se borran worktree y rama. Tester sin worktree.
- prompt.md del ejecutor: seccion "Tu worktree" (trabajar y commitear ahi; el workspace esta montado en la misma ruta; desk/evidencia siguen en el checkout principal). Template de scion sin cambios.
- reap: por cada ejecutor terminado y detenido, integra `deskops/<name>`: fast-forward si main no se movio (conserva el sha), si no cherry-pick en orden de los commits que main no tiene; conflicto => cherry-pick --abort, deja worktree y rama, imprime conflicto, exit 8. Exito => borra worktree y rama. integrate.py no cambia.

## Archivos
deskops/dispatch.py, tests/test_dispatch.py (fixture en main + 9 tests nuevos), docs/operator-manual.md, CHANGELOG.md

## Validacion
Ver validation.log: 54 passed (test_dispatch + test_integrate).

## Para revisar
- Un cherry-pick cambia el sha del commit de codigo: el coordinador debe tomar la referencia del commit ya en main (tras reap), no el de la rama.
- El ff/cherry-pick corre en el checkout principal: falla (exit 8) si ahi hay cambios sin commitear en los archivos tocados.
- No se probo con un contenedor scion real (ruta del worktree montada igual).

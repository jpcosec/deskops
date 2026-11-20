PASA

# Resultado del tester

Tarea: task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise
Run: run-deskops-t-31247d0735b6
Commit evaluado: 9d60527943bea5a9a6935dff6937b4416728aed1 ("dispatch: cada ejecutor trabaja en su propio git worktree; reap integra la rama", con el trailer Task-Id correcto).

## Veredicto

El commit cumple el Goal y el Done When para las superficies que toca. El diseño coincide con la resolución aceptada del preflight/bundle:
`start executor` crea la rama `deskops/<name>` desde la rama local de `integrate.branch` (o `main`) y el worktree `<root>/.worktrees/<name>`; `.worktrees/` queda en `.git/info/exclude`; el prompt del ejecutor le indica trabajar y commitear ahí; el tester no recibe worktree porque `reap` integra la rama antes de que arranque; `reap` trae los commits a `main` por fast-forward o cherry-pick, borra worktree y rama, y ante conflicto aborta, conserva ambos y sale 8. `integrate.py` no requiere cambios.

## Archivos del commit

- CHANGELOG.md
- deskops/dispatch.py
- docs/operator-manual.md
- tests/test_dispatch.py

## Verificación funcional

- Dos `dispatch start executor` de tareas distintas crean worktrees y ramas separadas; los cambios y el índice de uno no aparecen en el otro (`test_two_executors_do_not_share_tree_or_index`).
- `start` rechaza lanzar si el checkout principal no está en la rama base (exit 8) y limpia worktree/rama si `scion start` falla.
- `reap` hace fast-forward cuando main no se movió, cherry-pick solo de los commits de la tarea cuando main avanzó, y en conflicto hace `cherry-pick --abort`, deja main intacta y conserva worktree y rama.
- Documentación y CHANGELOG describen el flujo y el código de salida 8.

## Tests ejecutados (de a uno, sobre un worktree limpio del commit)

Árbol evaluado: `git worktree add --detach /tmp/deskops-test-9d605279 9d605279` (sin los cambios sin commitear del checkout principal, que son de otras tareas).
Python: `/dev/shm/t311/bin/python` (3.11) con `SLDB_SRC=/workspace/sldb/src`.

```text
TMPDIR=/tmp SLDB_SRC=/workspace/sldb/src /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
-> 32 passed, 1 warning in 317.79s

TMPDIR=/tmp SLDB_SRC=/workspace/sldb/src /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider tests/test_integrate.py
-> 22 passed, 1 warning in 87.17s
```

No se corrió la suite completa: la corre integrate en el host, según el encargo del tester.

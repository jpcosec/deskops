## REFORMULACION

El nodo es una tarea de código (`task.code`) ejecutable, no un agregado. **Propósito:** que `deskops dispatch start/reap` funcione con `--root sldb` o `IR` tomando roles y template del desk de deskops, y que `deskops integrate` devuelva 0 sin push cuando el tip ya es ancestro de `origin/<branch>`. **Resultado:** campo opcional `roles_root` en el bloque dispatch del desk/config.json del desk de la tarea; `dispatch.start` lo usa para `find_role_doc` y como root del runtime template; `reap` sin cambios más test; integrate con caso "ya integrado"; tests y docs/CHANGELOG. **Repo:** deskops, con sldb e IR como consumidores. **Límites:** fuera de alcance copiar RoleDocs a otros desks.

## AMBIGUEDADES

1. "si es relativa se resuelve contra la raíz de la tarea; se guarda absoluta. Por defecto es la raíz de la tarea" — no dice qué hacer si `roles_root` no existe o no contiene `desk/roles`; obligaría a inventar validación y error.
2. "imprime 'ya integrado: <tip corto>'" — no define longitud/formato del tip corto ni canal; obligaría a inventar el abreviado.
3. "o el nombre del directorio de la raíz si falta" — no aclara si es basename de la raíz o path completo; obligaría a inventar el fallback.
4. "la rama es el campo branch del bloque integrate del desk/config.json de --root" — no define comportamiento si falta `branch`; obligaría a inventar default.
5. "con roles_root=/mnt/ssd/proyectos/SLDB_1/deskops en el config de sldb" — "el config de sldb" no fija ruta exacta; obligaría a asumir `sldb/desk/config.json`.

## DRY-RUN

Sin ejecutar. **Lecturas:** `deskops/dispatch.py` (`find_role_doc` :92, `_list_agents` :45, bloque de template), `deskops/integrate.py` (:261 fetch, :213 escritor de events.log), `tests/test_dispatch.py`, `tests/test_integrate.py`, `docs/operator-manual.md`, `CHANGELOG`, `desk/config.json` de sldb e IR. **Cambios previstos:** añadir `roles_root` a `DispatchConfig` con `expanduser`/resolución; usar `roles_root` en `find_role_doc` y runtime template (`task_root` = raíz de tarea, `task_repo` = `project_identity` o fallback); test de `reap` con `--root` sin roles; rama "ya integrado" tras el fetch en integrate (rc 0, log `ya-integrado`, sin push ni suite); docs y changelog. **Dependencias:** scion simulado en tests, esquema de config existente, función de log de eventos. **Validaciones futuras:** `TMPDIR=/dev/shm python -m pytest -q tests/test_dispatch.py tests/test_integrate.py` y suite completa.

## FUTURO

El integrador corre la suite completa. Un humano decide si fija `roles_root` en los configs de sldb/IR y con qué valor, y valida el flujo real con scion. Copiar RoleDocs queda fuera de este nodo.

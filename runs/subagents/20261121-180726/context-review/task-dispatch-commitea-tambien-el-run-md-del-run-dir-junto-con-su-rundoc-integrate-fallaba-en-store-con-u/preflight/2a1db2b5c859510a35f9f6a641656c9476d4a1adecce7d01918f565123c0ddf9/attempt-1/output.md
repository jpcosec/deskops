## REFORMULACION
Propósito: corregir dispatch para que el commit del store del RunDoc incluya también el `run.md` trackeado del run dir, evitando que integrate falle con un agente vivo. Resultado: `_run_store_paths` añade `runs/subagents/exec-<nombre>/run.md` (o variante `-testing`) si existe; `_commit_run_store` lo commitea con pathspec; tests de regresión y CHANGELOG. Repo: deskops, en el worktree entregado por dispatch. Límites: dentro `deskops/dispatch.py`, `tests/test_dispatch.py`, `tests/test_integrate.py` y CHANGELOG; fuera el gate de store de integrate.

## AMBIGUEDADES
1. «después de dispatch start (simulado)»: no define cómo simularlo; obligaría a inventar fixture, mocks o punto de inserción.
2. «el commit 'run: <agente>'»: el placeholder no fija el asunto real ni si `<agente>` es nombre, id o variante `-testing`; obligaría a inventar el formato.
3. «commit desde el worktree que dispatch te da»: no identifica ruta, rama ni de dónde obtener «<id de esta tarea>»; obligaría a inventar esos datos.
4. «CHANGELOG»: no indica sección ni formato; obligaría a inventar la convención si no se deduce del repo.

## DRY-RUN
Lecturas: `deskops/dispatch.py` (`_run_store_paths`, `_commit_run_store`, `_run_dir_for` y línea ~186), `tests/test_dispatch.py`, `tests/test_integrate.py`, CHANGELOG y estado git del worktree. Cambios previstos: primero tests que fallen (el commit de start contiene el `run.md`; el gate de store pasa), luego inclusión condicionada del `run.md` en el pathspec y actualización de CHANGELOG. Dependencias: helpers actuales de store, fixture de dispatch simulado, worktree/rama y Task-Id provistos por dispatch. Validaciones futuras: ejecutar `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py tests/test_integrate.py`, también con `LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es`; commit con `git commit -- <rutas>` y trailer `Task-Id:`.

## FUTURO
Dispatch entrega worktree, rama e id; integrate ejecuta la suite y el gate de store; el closeout posterior commitea el run dir completo; un humano o nodo de aceptación decide el cierre.

## REFORMULACION
Nodo ejecutable `task.code`, no agregado. Propósito: que inbox y drawer del desk queden trackeados en el store y que `deskops view` los lea de `run_view`, no del disco. Resultado: globs en `deskops/data/desk_declaration.yaml`; trackeo al escribir en el drawer (`promote` y alta de items); `view` obtiene drawer e inbox como board/task; tests; `deskops desk update --apply`; aviso a graph_ui. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: backend, robocop2, verificación en navegador y migración de otros desks quedan fuera.

## AMBIGUEDADES
1. «`deskops message send --to graph_ui` con el hash.» ¿Qué hash? Obliga a inventar si es el commit, la tarea o un documento.
2. «el alta de items del drawer» y «`deskops/cli/commands/drawer.py` si escriben en el drawer». No identifica el comando exacto ni si ese archivo existe; obliga a inventar la superficie a modificar.
3. «sin fallas nuevas respecto de main». No fija commit/base de `main`; obliga a inventar el baseline de comparación.

## DRY-RUN
Lecturas: task, `desk_declaration.yaml`, `view.py`, `message.py`, `promote.py`, eventual `drawer.py` y tests citados. Cambios previstos: añadir globs; instrumentar las escrituras del drawer para trackear; hacer que `view` consulte `run_view`; añadir tests de nota/item visibles sin `desk update`. Dependencias: API existente de trackeo/`run_view`, sandbox desk roots y pytest. Validaciones futuras: los cuatro comandos pytest indicados, incluida la suite completa; comprobar la vista con un item recién creado; enviar el aviso. Sin ejecutar nada.

## FUTURO
graph_ui recibe el aviso, verifica en navegador sus vistas de drawer e inbox y reporta. Un humano decide la aceptación final y, si no se aclaran antes, el hash y el baseline de `main`.

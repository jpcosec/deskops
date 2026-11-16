**REFORMULACION**

El nodo es un `task.code` ejecutable (no agregado ni paquete: no hay hijos que recorrer). Encargo: en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, hacer que inbox y drawer queden trackeados en el store del desk y que las vistas los lean del store (H10 de CC34). Resultado esperado: globs `desk/inbox/*.md` (InboxNoteDoc) y `desk/drawer/tasks/*.md` (TaskDoc) en `deskops/data/desk_declaration.yaml`; ViewDocs `drawer.md` e `inbox.md`; `view.py` obteniendo drawer e inbox de `run_view`; los comandos que escriben en el drawer trackean con la misma llamada que `message send`; tests en los tres archivos nombrados. Límites: la verificación en navegador la hace graph_ui y no condiciona el cierre; no se migran desks ajenos; cierre con tests y commit, más `deskops desk update --apply` y nota a graph_ui con el hash.

**AMBIGUEDADES**

1. «los subcomandos de deskops/cli/commands/drawer.py que creen archivos»: el `drawer.py` incluido solo implementa `remove`, que no crea archivos. Obliga a inventar qué subcomando de alta añadir o si se refiere a `promote`.
2. «drawer.md e inbox.md, con el mismo formato que board.md y task.md»: `task.md` no está en el bundle y no se detallan secciones, `select`, modelos ni params de los ViewDocs nuevos. Obliga a inventar su estructura.
3. «con la misma llamada que usa message send al escribir la nota»: `message.py` usa `_track_note` privado dentro de `transaction`; no se indica si extraer helper o replicarlo ni dónde integrarlo en `DrawerService` (código ausente). Obliga a inventar el punto de tracking.
4. «tests/test_message_delivery.py y tests/test_inbox_promote_cli_gaps.py»: no se dice qué casos nuevos; el tracking de `send` ya está cubierto. Obliga a inventar aserciones.
5. «La nota a graph_ui lleva el hash del commit»: no fija hash completo/corto ni si va en título o cuerpo. Obliga a inventar el formato.

**DRY-RUN**

Lecturas previstas: los archivos del bundle, más `deskops/data/views/task.md`, `deskops/services/drawer.py` y `tests/view_desk.py` (no incluidos). Cambios: añadir dos entradas `include`; crear los dos ViewDocs; sustituir en `view.py` las lecturas de disco por `run_view`; trackear en `promote.py`/`DrawerService` y en `drawer.py`; ampliar los tres tests. Dependencias: `sldb.api.run_view`, `transaction`/`tx.track`, `InboxNoteDoc`, `TaskDoc`, `DrawerService`. Validaciones futuras: los tres pytest, la suite completa con baseline en worktree de `origin/main`, `deskops desk update --apply` en el desk de deskops, `deskops view` mostrando un item recién creado y `message send --to graph_ui`. Nada ejecutado.

**FUTURO**

graph_ui verifica en navegador (no condiciona el cierre); un humano/CI decide si las fallas de la suite son preexistentes; el ejecutor produce el commit y envía la nota con su hash; `desk update --apply` materializa los globs en el desk.

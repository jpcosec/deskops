## REFORMULACION
**Propósito:** que inbox y drawer sean documentos trackeados del store del desk y que `deskops view` los lea con `run_view`, igual que board y task.  
**Resultado:** globs en `deskops/data/desk_declaration.yaml` para `InboxNoteDoc` y `TaskDoc`; ViewDocs `drawer.md` e `inbox.md`; `view.py` proyectándolos desde el store; promote/alta de drawer trackeando al escribir; tests.  
**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.  
**Límites:** no verificación en navegador —la hace graph_ui y no condiciona el cierre— ni migración de desks ajenos. Es `task.code` ejecutable, no agregado.

## AMBIGUEDADES
1. Cita: “los subcomandos de `deskops/cli/commands/drawer.py` que creen archivos”. El archivo mostrado solo expone `drawer remove`; no hay subcomando de alta. Obliga a inventar qué comandos crean items y si `add task --from-drawer` cuenta.
2. Cita: “trackeando con la misma llamada que usa message send al escribir la nota”. `message send` trackea `InboxNoteDoc` dentro de una transacción; el drawer escribe `TaskDoc` desde `DrawerService`. Obliga a decidir llamada exacta, modelo/nombre y comportamiento sin store.
3. Cita: “drawer e inbox salen de `run_view` con esos ViewDocs, como board y task hoy”. El `drawer_view` actual calcula `markdown`, `command` y `revision`; el esquema mostrado de ViewDoc no expresa esos campos. Obliga a inventar su representación o qué agrega todavía el CLI.

## DRY-RUN
**Lecturas:** TaskDoc, `desk_declaration.yaml`, `views/board.md`, `view.py`, `message.py`, `promote.py`, `drawer.py`, tests citados y modelos `InboxNoteDoc`/`TaskDoc`.  
**Cambios previstos:** añadir globs include; crear `views/drawer.md` e `inbox.md`; cambiar `view.py` para resolver drawer/inbox vía `run_view`/`project`; hacer que promote y el alta de drawer trackeen al escribir; ajustar tests.  
**Dependencias:** soporte de ViewDocs en sldb, transacciones/tracking del store, registro de modelos y `apply_declaration`.  
**Validaciones futuras:** ejecutar los tres pytest indicados y la suite completa con baseline en worktree limpio; comprobar `deskops view` con un item recién creado sin `desk update`; commit y nota a graph_ui.

## FUTURO
graph_ui recibe la nota con el hash del commit y verifica en navegador sus vistas de drawer e inbox; esa verificación no condiciona el cierre.

## REFORMULACION
UI02 es un nodo de código en graph_ui: construir `frontends/desk/` (servidor y shell). El servidor escucha en 127.0.0.1:8091, expone `GET /api/view/{board,task,drawer,inbox,agents}?desk=<repo>` llamando por Python a la vista de UI01, reutiliza `DeskRoutes` para `POST /api/desk/advance` y sirve el shell. El shell usa DESIGN.md en oscuro, con barra lateral (Board, Drawer, Inbox, Agentes, Inspeccionar), cabecera con desk activo y conteos derivables, selector de desks del registro y errores visibles con causa. Límites: solo graph_ui; sin CDN; sin escrituras salvo advance por la operación existente; no crea servidor HTTP en deskops ni pantallas (UI03+). Resultado comprobable por tests de rutas, paridad con `deskops view`, loopback, ausencia de URLs externas, selector y captura comparada.

## AMBIGUEDADES
1. "GET /api/view/{board,task,drawer,inbox,agents}?desk=<repo>" no define cómo recibe el id la vista `task`; obliga a inventar parámetro de query o ruta.
2. "'Inspeccionar' que abre el visor KIMUN en :8090 con el id": no dice qué id ni qué hace sin selección; obliga a inventar ambos.
3. El scope dice "repos del registro ... que tengan desk/" pero la aceptación dice "el selector lista los desks del registro"; no aclara si lista todos o solo los filtrados.
4. La aceptación exige "captura del shell comparada con The Desk - Active Board de Stitch y diferencias anotadas en el TaskDoc", mientras G_SHELL figura satisfecho con pendiente: "las capturas ... no están anotadas en los TaskDocs"; contradicción sobre si esa captura es obligatoria o ya dispensada.

## DRY-RUN
Un ejecutor leería `deskops/services/desk_view.py` y `docs/deskops-ui.md` (UI01), `frontends/mindmap/deskops_routes.py`, `DESIGN.md`, `desk/registry/repo-*.md` y el visor existente como referencia. Crearía `frontends/desk/serve.py`, `index.html`, `app.js`, `styles.css`, `tests/test_desk_ui_routes.py` y `docs/deskops-ui-client.md`. Depende de UI01 importable y de G_VIEW. Validaría con pytest: paridad de cada endpoint contra `deskops view` sobre desk temporal, rechazo de métodos no GET salvo advance, bind solo loopback, grep sin URLs externas, selector y comparación visual.

## FUTURO
UI03–UI06 consumen el shell y los endpoints para las pantallas; UI01 ya entrega el contrato de vista. Un humano debe resolver el pendiente de capturas y el estado de la suite completa registrado en G_SHELL; otro nodo o el dueño decide si esa evidencia basta.

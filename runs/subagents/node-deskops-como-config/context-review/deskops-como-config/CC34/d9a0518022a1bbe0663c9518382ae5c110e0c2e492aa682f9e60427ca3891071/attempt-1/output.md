REFORMULACION
Propósito: sustituir `services/desk_view.py` por `ViewDoc` semilla (`board`, `task`, `drawer`, `inbox`) que sldb sirve, dejando `deskops view` como `run_view` + `render_text` y graph_ui leyendo `/views` de `sldb serve`. Resultado: goldens JSON, ViewDocs en `deskops/data/views/`, CLI y graph_ui adaptados, `desk_view.py` y alias privados borrados, ETag como `revision`. Repo dueño: deskops; toca además `UIs/graph_ui` (repo aparte). Límites: no escribir en sldb, no suplir reglas con Python, no cambiar formato del desk ni gramática del CLI, sin proveedores `computed`, ViewDocs solo semillas (sin `desk/views/`), no dejar dos caminos. Nodo delivery ejecutable.

AMBIGUEDADES
1. “proxy o cliente directo”: deja dos implementaciones vivas para graph_ui; obliga a elegir una y puede violar el límite de no dejar dos caminos.
2. “sldb serve las encuentra por un store de deskops enlazado”: no define qué es “enlazado” ni si toca `store.yaml`; obliga a inventar el mecanismo y puede chocar con DP3 o la forma del desk.
3. “graph_ui (repo aparte, UIs/graph_ui)” junto a `owner_repo: deskops` y “test en graph_ui”: no dice dónde vive el commit ni quién ejecuta y valida en el repo aparte; obliga a inventar actor y worktree.
4. “lo que no es documento ni recibo (agents de Herdr, runtime/, P4) lo agrega deskops view sobre el resultado de run_view” frente a “GET /views/board de sldb serve… devuelve el mismo payload”: si el CLI agrega agents/runtime, el payload de sldb no puede ser idéntico; obliga a inventar si agents entran en board o cómo se compara.

DRY-RUN
Leería dag/brief/alcance/decisiones, `docs/deskops-ui.md`, `services/desk_view.py`, `tests/test_desk_view.py` y goldens. Capturaría goldens JSON en desk de prueba. Crearía `deskops/data/views/*`; adaptaría `cli/commands/view.py` a `run_view` + `render_text`; borraría `desk_view.py`, `task_revision/note_revision` y alias; añadiría ETag; cambiaría graph_ui `serve.py`/`deskops_routes.py` y tests; actualizaría docs/CHANGELOG. Dependencias: CC33 (recibos evidence), CC36 (semillas/scaffold), G_GD25/G_GD21 satisfechos. Validaría goldens salvo `revision`, `GET /views/board`, test graph_ui y 409, grep vacío, `test_desk_view.py`, 6 desks, tiempos, ayuda y docs. Sin ejecutar.

FUTURO
CC52 mide y verifica <1 s, suite, doctor, stores y rules en los 6 desks; CC53 documenta; CC51 mide líneas; el supervisor corre la suite completa; el TaskDoc fija archivos y tests exactos; el humano decide N y acepta DO2/DO3.

# Auditoría de átomos y pills con las tres preguntas

Informe de solo lectura (2026-11-25). Ningún átomo ni pill fue editado, retirado o movido. Base: `deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md`.

## Método

Censo con `deskops list atoms|pills --root <repo>` en los desks de `UIs/graph_ui`, `deskops`, `sldb` e `IR`. Cada documento recibe un único veredicto, el primero que aplica en el orden de las tres preguntas:

1. `codigo` / `docstring`: se puede leer del código (archivo:línea) o falta en el docstring.
2. `specir-extrae` / `specir-extraeria`: `specir extract` produce hoy ese hecho / es del tipo que extrae pero falta.
3. `decision` / `invariante`: seguiría valiendo sin el trabajo en curso. `contexto-trabajo`: no; depende de una tarea no cerrada o de un plan de drawer.

Además `no-se-sostiene` (el código lo contradice o ya no existe) y `sin-clasificar` (no se pudo abrir el código o el texto es ambiguo). En las pills los veredictos se aplican a lo que la pill afirma.

**Cómo se hizo y su límite.** La lectura la repartieron 19 subagentes, uno por tramo de ~45 documentos, cada uno abriendo el código referido con `rg`/lectura parcial. Varios `codigo` se apoyan en una o dos coincidencias sin leer la función entera, y algunos citan archivo sin línea exacta; `specir extract` no se ejecutó, así que `specir-*` es juicio por tipo de hecho, no por salida real. Los veredictos son una primera clasificación para que JP decida; los que importan para retirar algo (`no-se-sostiene`, `contexto-trabajo`) conviene revisarlos antes de actuar.

## Censo

El real difiere del de la propuesta (647 átomos, 59 pills): hoy hay **657 átomos** y **59 pills** (graph_ui 266/2, deskops 240/29, sldb 113/24, IR 38/4; la propuesta decía 265/237/107/38).

## Totales: átomos

| Veredicto | graph_ui | deskops | sldb | IR | Total |
|---|---|---|---|---|---|
| `codigo` (ya está en el código) | 158 | 125 | 94 | 22 | 399 |
| `docstring` (falta en el docstring) | 10 | 2 | 1 | 0 | 13 |
| `specir-extrae` (lo extrae specIR hoy) | 0 | 0 | 0 | 0 | 0 |
| `specir-extraeria` (lo extraería specIR) | 0 | 2 | 0 | 0 | 2 |
| `decision` (es una decisión) | 56 | 87 | 11 | 10 | 164 |
| `invariante` (es un invariante) | 15 | 15 | 3 | 2 | 35 |
| `contexto-trabajo` (es contexto de un trabajo abierto) | 1 | 2 | 1 | 0 | 4 |
| `no-se-sostiene` (no se sostiene) | 26 | 6 | 3 | 4 | 39 |
| `sin-clasificar` (sin clasificar) | 0 | 1 | 0 | 0 | 1 |
| **Total** | **266** | **240** | **113** | **38** | **657** |

## Totales: pills

| Veredicto | graph_ui | deskops | sldb | IR | Total |
|---|---|---|---|---|---|
| `codigo` (ya está en el código) | 0 | 15 | 10 | 0 | 25 |
| `docstring` (falta en el docstring) | 0 | 1 | 0 | 0 | 1 |
| `specir-extrae` (lo extrae specIR hoy) | 0 | 0 | 0 | 0 | 0 |
| `specir-extraeria` (lo extraería specIR) | 0 | 0 | 0 | 0 | 0 |
| `decision` (es una decisión) | 0 | 9 | 5 | 2 | 16 |
| `invariante` (es un invariante) | 1 | 4 | 4 | 2 | 11 |
| `contexto-trabajo` (es contexto de un trabajo abierto) | 0 | 0 | 5 | 0 | 5 |
| `no-se-sostiene` (no se sostiene) | 1 | 0 | 0 | 0 | 1 |
| `sin-clasificar` (sin clasificar) | 0 | 0 | 0 | 0 | 0 |
| **Total** | **2** | **29** | **24** | **4** | **59** |

## Lectura rápida

- Átomos que repiten el código o lo que extrae specIR (`codigo`, `docstring`, `specir-*`): **414 de 657**.
- Átomos que guardan lo que el código no puede decir (`decision`, `invariante`): **199**.
- Átomos que en realidad son contexto de un trabajo abierto (pills mal ubicadas): **4**.
- Átomos que ya no se sostienen: **39**.
- Pills sin trabajo abierto (`contexto-trabajo` es el único veredicto que justifica una pill viva): solo **5 de 59** lo son.

## Sin clasificar

- `atom-los-4-atomos-de-salud-del-desk-dejan-de-dar-ruido-estructural-en-sldb-stores-check` (atom, deskops): relato de una correccion puntual ya hecha (4 atomos editados, commit sldb a1d5527f); el chequeo existe en sldb/src/sldb/api/stores/store_surroundings.py:63 pero el hecho afirmado es un estado pasado no verificable ni durable

## Veredicto por documento

### graph_ui: átomos (266)

| id | veredicto | motivo |
|---|---|---|
| `atom-actionssection-for-whom` | `docstring` | el componente (UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/ActionsSection.tsx:40-144) ofrece botones explícitos pero sin docstring que nombre al destinatario |
| `atom-actionssection-how` | `codigo` | ActionsSection.tsx:40-97 lee stores, copy/paste con makeCopyNode (:19-38) y delete vía openDeleteConfirm |
| `atom-actionssection-how-not` | `codigo` | ActionsSection.tsx:76-97 delete pasa por openDeleteConfirm y no hay botón ni llamada de guardado en :118-144 |
| `atom-actionssection-what` | `no-se-sostiene` | dice que el cluster incluye save pero ActionsSection.tsx:118-144 solo tiene Undo, Redo, Copy, Paste, Delete |
| `atom-actionssection-when` | `codigo` | ActionsSection.tsx:121-141 enablement por undoStack/redoStack/copiedNodeId/selección; sin guardado |
| `atom-actionssection-where` | `codigo` | el archivo existe en UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/ActionsSection.tsx y usa graph-store/ui-store (:2-4) |
| `atom-actionssection-why` | `no-se-sostiene` | afirma que puentea un "shell-level save callback" pero ActionsSection.tsx no recibe props ni guarda (:40-144) |
| `atom-canvassidebar-for-whom` | `no-se-sostiene` | dice que el shell pasa un save callback; CanvasSidebar.tsx:22-26 solo tiene editable, variant, topPanel |
| `atom-canvassidebar-how` | `codigo` | CanvasSidebar.tsx:46-47 sidebarOpen/toggleSidebar, :49-62 opener, :96 topPanel, :99-110 status card, :112-136 acordeones |
| `atom-canvassidebar-how-not` | `codigo` | CanvasSidebar.tsx:112-136 solo compone secciones, sin lógica de render ni de herramientas |
| `atom-canvassidebar-what` | `codigo` | CanvasSidebar.tsx:113-135 seis paneles Actions, Filters, Creation, View, Encoding, Views |
| `atom-canvassidebar-when` | `codigo` | CanvasSidebar.tsx:46-62 abierto/cerrado según sidebarOpen del UI store |
| `atom-canvassidebar-where` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/CanvasSidebar.tsx existe, junto a sus secciones (index.ts) |
| `atom-canvassidebar-why` | `docstring` | CanvasSidebar.tsx:45-141 hace lo descrito pero sin docstring con el motivo |
| `atom-commandmenu-for-whom` | `no-se-sostiene` | promete trigger de save desde la paleta; CommandMenu.tsx:60-70 solo tiene Undo/Redo y nodos |
| `atom-commandmenu-how` | `codigo` | CommandMenu.tsx:45-51 keydown Ctrl/Cmd+K, :28-29 setFocusedNode + setEditorState('focus'), :34-39 undo/redo |
| `atom-commandmenu-how-not` | `codigo` | CommandMenu.tsx:60-65 solo acciones undo/redo y foco de nodo, sin crear ni guardar |
| `atom-commandmenu-what` | `no-se-sostiene` | dice que ofrece Save; CommandMenu.tsx:60-70 no tiene item Save |
| `atom-commandmenu-when` | `codigo` | CommandMenu.tsx:45-51 Ctrl/Cmd+K y nodos desde graph store al render |
| `atom-commandmenu-where` | `codigo` | el archivo existe en L2-canvas/components/CommandMenu.tsx |
| `atom-commandmenu-why` | `docstring` | CommandMenu.tsx:20-70 implementa la paleta pero ningún docstring dice el motivo |
| `atom-creationsection-for-whom` | `docstring` | CreationSection.tsx:57-83 permite crear nodos en el lienzo; destinatario no escrito en el código |
| `atom-creationsection-how` | `codigo` | CreationSection.tsx:25 registry.getAll, :34-51 id generado, posición aleatoria :37-38, addElements |
| `atom-creationsection-how-not` | `codigo` | CreationSection.tsx:57-83 solo Popover, sin drag-and-drop ni contextmenu (rg sin coincidencias) |
| `atom-creationsection-what` | `codigo` | CreationSection.tsx:57-63 botón "Add Node +" y lista del registry |
| `atom-creationsection-when` | `codigo` | CreationSection.tsx:28-51 crea el nodo al seleccionar el tipo |
| `atom-creationsection-where` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/CreationSection.tsx existe |
| `atom-creationsection-why` | `docstring` | CreationSection.tsx convierte el registry en acción de creación pero sin docstring del motivo |
| `atom-cómo-corre-la-ci-de-graph-ui` | `codigo` | UIs/graph_ui/.github/workflows/ci.yml:13-128 tres jobs y comandos tal cual; .github/requirements-suite.txt:1-6 ramas main sin releases |
| `atom-cómo-decide-el-layout-de-una-vista-su-estilo-de-arquitectura` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/layout/layout-strategies.ts:219-226 strategyForLayout rings->elk-rings, resto layered; :239 ringDepths |
| `atom-cómo-filtra-el-lienzo-de-review-workbench` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/GraphCanvas.tsx:136-166 applyCanvasFilters en el orden descrito y :184 uso |
| `atom-cómo-se-edita-guarda-y-apunta-una-vista-desde-la-barra-lateral-de-review-workbench` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/lib/views-provider.ts:2 y UIs/graph_ui/frontends/mindmap/views_routes.py:1-4 exponen /api/views y /api/views/evaluate; use-apply-view.ts:5 |
| `atom-dataprovider-for-whom` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/lib/sldb-provider.ts:34-36 interfaz usada por AntoniaFlowPage.tsx y NodeInspector.tsx (rg sldbProvider) |
| `atom-dataprovider-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/lib/sldb-provider.ts:38-70 getSchema/getGraph cacheados y saveDoc POST /sldb/save |
| `atom-dataprovider-how-not` | `invariante` | regla entre piezas (sin whole-graph save, L1 sin acceso directo) que el código no afirma; sldb-provider.ts:34-36 solo expone saveDoc por documento |
| `atom-dataprovider-what` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/lib/sldb-provider.ts:34-36 SldbDataProvider; no existe mock provider (no hay features/graph-editor/lib/data-provider.ts) |
| `atom-dataprovider-when` | `no-se-sostiene` | afirma save (Ctrl+S) en DataProvider; use-keyboard.ts:43-59 no maneja la tecla s, el guardado va por NodeInspector |
| `atom-dataprovider-where` | `no-se-sostiene` | cita lib/data-provider.ts y src/mock/client.ts que no existen (ls lib/ y src/mock) |
| `atom-dataprovider-why` | `decision` | el porqué de la costura única (desacoplar fuente de datos) que el código no dice; el swap mock/live ya no aplica (no hay mock) pero el motivo vale |
| `atom-deskops-spec2viz-and-knowledge-are-instances-of-the-sldb-plus-kgdb-nucleus` | `no-se-sostiene` | spec2viz está retirado y continúa como specIR (AGENTS.md), kgdb ya no existe; repopackage y knowledge no están en el workspace (ls /mnt/ssd/proyectos/SLDB_1) |
| `atom-deskops-workflow-views-delegate-state-and-gates-to-deskops` | `invariante` | regla entre UI y deskops (sin editar status/current_node ni forzar transiciones); respaldada parcialmente en frontends/mindmap/deskops_routes.py:146,252-255; tarea de origen ya cerrada |
| `atom-edgeinspector-for-whom` | `docstring` | EdgeInspector.tsx:16-52 solo edita relationType; destinatario no escrito en el código |
| `atom-edgeinspector-how` | `codigo` | EdgeInspector.tsx:16-24 focusedEdgeId, :36 draft, :41 setEditorState('browse'), :49-52 updateEdge |
| `atom-edgeinspector-how-not` | `codigo` | EdgeInspector.tsx:49-52 updateEdge solo relationType y properties sin cambios; sin edición de extremos |
| `atom-edgeinspector-what` | `codigo` | EdgeInspector.tsx:36-52 edita y guarda relationType en el graph store |
| `atom-edgeinspector-when` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/panels/EdgeInspector.tsx:59 (open = focusedEdgeId !== null) y :30-36 (reset del draft al cambiar edge) |
| `atom-edgeinspector-where` | `codigo` | la ruta existe: UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/panels/EdgeInspector.tsx (specir extrae componentes TSX) |
| `atom-edgeinspector-why` | `decision` | el porqué (superficie propia para semántica de aristas) no está en EdgeInspector.tsx; es motivación de diseño que seguiría valiendo sin trabajo abierto |
| `atom-editorengine-for-whom` | `decision` | destinatario (callers backend, no operadores) no se lee de UIs/graph_ui/src/editor.py:14; además GraphEditorEngine no tiene callers (rg solo lo encuentra en editor.py) |
| `atom-editorengine-how` | `codigo` | UIs/graph_ui/src/editor.py:17-60 (apply_node_edit CREATE/UPDATE/DELETE, colisión, cascada; apply_edge_edit verifica nodos) |
| `atom-editorengine-how-not` | `invariante` | colisión/existencia/cascada ya están en UIs/graph_ui/src/editor.py:22-24,47-49 pero la prohibición de UI concerns entre capas no está afirmada por el código; es restricción de frontera durable |
| `atom-editorengine-what` | `codigo` | UIs/graph_ui/src/editor.py:14-18,53 (clase con dos métodos apply_node_edit/apply_edge_edit) |
| `atom-editorengine-when` | `codigo` | UIs/graph_ui/src/editor.py:17,53 (aplica NodeEdit/EdgeEdit sobre GraphData); sin callers en el repo (rg GraphEditorEngine) |
| `atom-editorengine-where` | `codigo` | UIs/graph_ui/src/editor.py:14 define GraphEditorEngine; imports en cabecera del mismo archivo |
| `atom-editorengine-why` | `decision` | motivo de existir (ruta única de mutación) no se lee del código; nota: GraphEditorEngine no tiene callers fuera de src/editor.py |
| `atom-editorlifecycle-for-whom` | `decision` | destinatario (operador, persistencia por documento y no por canvas) no está en el código; apps/review-workbench/src/features/graph-editor/L2-canvas/GraphEditor.tsx:21 solo lo insinúa en comentario |
| `atom-editorlifecycle-how` | `codigo` | apps/review-workbench/src/features/antonia-flow/AntoniaFlowPage.tsx:11,64-89 (LoadState), L2-canvas/panels/NodeInspector.tsx:322 (handleTypedSave), lib/sldb-provider.ts:68 (saveDoc) |
| `atom-editorlifecycle-how-not` | `decision` | no reintroducir Save Graph/isDirty: rg isDirty¦saveGraph sin resultados en apps/review-workbench/src; el porqué está en comentario GraphEditor.tsx:58 y vale sin trabajo abierto |
| `atom-editorlifecycle-what` | `codigo` | apps/review-workbench/src/features/antonia-flow/AntoniaFlowPage.tsx:11,64 (LoadState) y docs/specs/state.editor-lifecycle.yml; sin estado dirty global (rg isDirty vacío) |
| `atom-editorlifecycle-when` | `codigo` | UIs/graph_ui/apps/review-workbench/src/App.tsx:6,25 monta AntoniaFlowPage; NodeInspector.tsx:322 handleTypedSave |
| `atom-editorlifecycle-where` | `codigo` | rutas existen: AntoniaFlowPage.tsx:11, NodeInspector.tsx:322, lib/sldb-provider.ts:68 (bajo UIs/graph_ui/apps/review-workbench/src/features) |
| `atom-editorlifecycle-why` | `decision` | por qué se quitó el guardado de grafo completo (no-op, commit 56ad840); rg isDirty¦saveGraph vacío y comentario en L2-canvas/GraphEditor.tsx:58 lo confirma |
| `atom-el-auto-layout-de-review-workbench-reserva-el-tamaño-medido-de-cada-nodo` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/hooks/use-graph-layout.ts:33 layoutNodeSize, :71 ready=everyNodeMeasured; GraphEditor.tsx:130 ReactFlowProvider |
| `atom-el-compilador-del-mindmap-escribe-solo-con-el-plantoken-de-un-plan-previo` | `codigo` | UIs/graph_ui/frontends/mindmap/compilation.py:50-55 (planToken, 409) y serve.py:390,427 (501 en remote) |
| `atom-el-estado-de-plegado-de-los-grupos-de-review-workbench-vive-en-ui-store` | `codigo` | UIs/graph_ui/apps/review-workbench/src/stores/ui-store.ts:41,59,138-139 collapsedGroups/setGroupCollapsed; hooks/use-edge-inheritance.ts:8,39,88 |
| `atom-el-store-de-graph-ui-hereda-los-modelos-de-deskops` | `codigo` | UIs/graph_ui/.sldb/core/store_index.yaml:1-3 (store deskops enlazado) y entradas deskops.models:<Model> (ya en el store) |
| `atom-el-título-de-un-nodo-de-review-workbench-sale-de-una-sola-regla` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/lib/node-title.ts:20-24 resolveNodeTitle; NodeShell.tsx:32 usa 'Untitled' |
| `atom-encodingrules-for-whom` | `decision` | destinatario (canvas y operadores) no se lee de encoding-rules.ts; es intención de diseño durable |
| `atom-encodingrules-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/encoding/encoding-rules.ts:104,138,158 (DEFAULT_ENCODING_RULES, resolveEdgeStyle, resolveNodeStyle); ui-store.ts activeEncodingRules |
| `atom-encodingrules-how-not` | `decision` | encoding secundario frente a filtering: texto en L2-canvas/sidebar/EncodingSection.tsx:146 es UI, la regla de diseño no la impone código (hay rules en encoding-rules.ts pero no la prohibición) |
| `atom-encodingrules-what` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/encoding/encoding-rules.ts:5,104,138,158 |
| `atom-encodingrules-when` | `codigo` | se lee de ui-store.ts (activeEncodingRules) y FloatingEdge.tsx/NodeShell.tsx que consumen el estilo en render; specir extraeria uso entre capas |
| `atom-encodingrules-where` | `no-se-sostiene` | afirma lib/projection-view-store.ts pero no existe (ls apps/review-workbench/src/features/graph-editor/lib; rg projection-view sin resultados); el resto sí: encoding/encoding-rules.ts y stores/ui-store.ts |
| `atom-encodingrules-why` | `decision` | motivo (reglas separadas del renderer, vistas guardan proyección visual) no está en encoding-rules.ts; es diseño durable |
| `atom-encodingsection-for-whom` | `decision` | destinatario (operador que ajusta énfasis visual/vistas) no está en L2-canvas/sidebar/EncodingSection.tsx |
| `atom-encodingsection-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/EncodingSection.tsx:44-45,59 (setActiveEncodingRules, resetActiveEncodingRules); ui-store.ts activeViewId |
| `atom-encodingsection-how-not` | `decision` | EncodingSection.tsx:146 dice "Filtering remains primary" pero es texto de UI; la regla durable es de diseño, no del código |
| `atom-encodingsection-what` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/EncodingSection.tsx (editor de reglas activas) |
| `atom-encodingsection-when` | `codigo` | EncodingSection.tsx:44-45 aplica reglas del ui-store al instante; flujo de uso legible del código |
| `atom-encodingsection-where` | `codigo` | la ruta existe: UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/EncodingSection.tsx |
| `atom-encodingsection-why` | `decision` | motivo (cambiar el estilo sin tocar datos, tras filtrar) no está en el código; EncodingSection.tsx:146 solo da pista en UI |
| `atom-filtering-is-the-primary-projection-mechanism-encoding-is-secondary` | `decision` | decisión de diseño de la gramática de proyección sin ancla; EncodingSection.tsx:146 solo la repite en texto de UI, no la impone |
| `atom-filterssection-for-whom` | `decision` | destinatario (operador con grafo grande, modo foco) no está en L2-canvas/sidebar/FiltersSection.tsx |
| `atom-filterssection-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/FiltersSection.tsx:125-126 (setFilter, hideNonNeighbors, clearFilters) |
| `atom-filterssection-how-not` | `decision` | filtering primario/encoding secundario es regla de diseño; FiltersSection.tsx:125-126 solo usa setFilter, no la afirma |
| `atom-filterssection-what` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/FiltersSection.tsx:125 (búsqueda, tipos de relación, atributo, hideNonNeighbors) |
| `atom-filterssection-when` | `codigo` | FiltersSection.tsx:125-126 usa estado del ui-store de forma continua; legible del código |
| `atom-filterssection-where` | `codigo` | la ruta existe: UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/FiltersSection.tsx |
| `atom-filterssection-why` | `decision` | por qué existe el filtrado como mecanismo primario no está en el código; la razón es de diseño y sigue valiendo |
| `atom-graph-ui-is-a-graph-editor-tool-not-defined-by-any-consuming-project` | `decision` | identidad de graph_ui (herramienta, no definida por consumidores) es decisión de frontera; frontends/mindmap/README.md:1 y apps/review-workbench existen pero no la afirman |
| `atom-graph-ui-is-a-schema-driven-typed-editor-not-a-generic-canvas` | `codigo` | UIs/graph_ui/apps/review-workbench/src/schema/registry.types.ts:18-30 (payloadSchema, renderers, allowedConnections) |
| `atom-graph-ui-must-actually-edit-and-persist-not-render-read-only` | `decision` | intención de que graph_ui edite y persista; el código lo cumple solo en parte (frontends/mindmap/source/documents.js:63-73 save; sin guardado de grafo completo en el store graph-store.ts), el porqué sigue valiendo |
| `atom-graph-ui-node-types-must-not-be-hand-written-zod-generate-them-from-sldb-models-at-build` | `decision` | elige camino build-time (scripts/generate-node-types.mjs:6-15, package.json hum:sync) frente a lecturas runtime; tipos group/simple aún manuales en src/schema/register-defaults.ts:10-45 |
| `atom-graph-ui-se-instala-como-paquete-mindmap` | `no-se-sostiene` | pyproject.toml no tiene extra opcional notation/spec2viz (solo deskops y test) y frontends/mindmap/serve.py:544-545 sí manipula sys.path contra el "nunca" |
| `atom-graph-ui-should-read-and-write-graph-data-directly-over-kgdb` | `decision` | arquitectura objetivo (store en vivo en ambos sentidos); lectura existe (src/adapters/snapshot_adapter.py:12, sldb-provider.ts:43-69) y lo pendiente (replace vs mutación incremental) está abierto |
| `atom-graphcanvas-for-whom` | `decision` | para quién es GraphCanvas (operador/shell L2), no se lee del código; GraphCanvas.tsx:174 solo muestra el uso |
| `atom-graphcanvas-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/GraphCanvas.tsx:136-190 (applyCanvasFilters en effect, stores, nodeTypes/edgeTypes) |
| `atom-graphcanvas-how-not` | `codigo` | GraphCanvas.tsx:136-176 (filtros viven en useUIStore, aplicados vía applyCanvasFilters) y sin persistencia en el archivo |
| `atom-graphcanvas-what` | `codigo` | GraphCanvas.tsx:164-215 (ReactFlow con Background, Controls, MiniMap sobre nodos/aristas del graph store) |
| `atom-graphcanvas-when` | `codigo` | GraphCanvas.tsx:182-187 (useEffect con deps edges, filters, focusMode, focusedNodeId, nodes) |
| `atom-graphcanvas-where` | `codigo` | apps/review-workbench/src/features/graph-editor/L2-canvas/GraphCanvas.tsx existe y exporta GraphCanvas (línea 164) |
| `atom-graphcanvas-why` | `decision` | por qué existe una única superficie interactiva; no se lee del código |
| `atom-graphdata-contract-for-whom` | `decision` | para quién es el contrato (backend, motor, auditor, adaptador); src/contracts/graph_data.py no lo dice |
| `atom-graphdata-contract-how` | `codigo` | UIs/graph_ui/src/contracts/graph_data.py:13-78 (Position, UINode, UIEdge, GraphData con default factories) |
| `atom-graphdata-contract-how-not` | `codigo` | UIs/graph_ui/src/contracts/graph_data.py:13-78 es Pydantic BaseModel sin estado de vista React |
| `atom-graphdata-contract-what` | `codigo` | UIs/graph_ui/src/contracts/graph_data.py:13-78 y snapshot_adapter.py:12 |
| `atom-graphdata-contract-when` | `codigo` | src/provider.py:23-28 valida a GraphData, src/adapters/snapshot_adapter.py:12 produce GraphData |
| `atom-graphdata-contract-where` | `codigo` | UIs/graph_ui/src/contracts/graph_data.py:13,23,49,64 define Position, UINode, UIEdge, GraphData |
| `atom-graphdata-contract-why` | `decision` | por qué una única forma de grafo compartida; el motivo no está en el código |
| `atom-grapheditor-de-review-workbench-dibuja-lo-que-hay-en-el-graph-store` | `codigo` | GraphEditor.tsx:19-24 ya dice que carga el grafo quien monta (loadGraph) y sus props solo de presentación; graph-store.ts:380 |
| `atom-graphprovider-for-whom` | `decision` | para quién es GraphProvider (llamadores backend y tests con fixtures); src/provider.py no lo dice |
| `atom-graphprovider-how` | `codigo` | UIs/graph_ui/src/provider.py:16-33 coincide literalmente (fixtures_dir por defecto, load_fixture, get_ecosystem_slice) |
| `atom-graphprovider-how-not` | `codigo` | UIs/graph_ui/src/provider.py:25-28 lanza FileNotFoundError y devuelve GraphData.model_validate_json |
| `atom-graphprovider-what` | `codigo` | UIs/graph_ui/src/provider.py:13-33 y desk/fixtures/ecosystem_slice.json existe |
| `atom-graphprovider-when` | `codigo` | src/provider.py:23-33 (carga de fixtures; get_ecosystem_slice llama load_fixture) |
| `atom-graphprovider-where` | `codigo` | UIs/graph_ui/src/provider.py:13-21 con desk/fixtures por defecto |
| `atom-graphprovider-why` | `decision` | por qué un único punto de entrada para fixtures; no se lee del código |
| `atom-graphstore-for-whom` | `decision` | para quién es GraphStore (AntoniaFlowPage, GraphCanvas, inspectores); no es lectura de código |
| `atom-graphstore-how` | `no-se-sostiene` | dice que loadGraph captura un saved snapshot, pero graph-store.ts:380-387 solo asigna nodes, edges y vacía undoStack/redoStack |
| `atom-graphstore-how-not` | `codigo` | apps/review-workbench/src/stores/graph-store.ts:255,287 (isVisualOnly omite undo), sin dirty/saved; la persistencia está en sldb-provider.ts:68-69 |
| `atom-graphstore-what` | `codigo` | apps/review-workbench/src/stores/graph-store.ts:27,31,196 (nodes, edges, undoStack, redoStack, acciones) sin estado dirty/saved |
| `atom-graphstore-when` | `codigo` | graph-store.ts:380 loadGraph, :310-324 onNodesChange/onEdgesChange, :349-375 undo/redo |
| `atom-graphstore-where` | `codigo` | apps/review-workbench/src/stores/graph-store.ts existe; features/antonia-flow/AntoniaFlowPage.tsx lo usa |
| `atom-graphstore-why` | `decision` | por qué centralizar la mutación y el undo/redo en un store; no se lee del código |
| `atom-kgdb-for-whom` | `decision` | para quién es la capa sldb.api.graph en graph_ui (operador, implementadores); no es lectura de código |
| `atom-kgdb-how` | `codigo` | frontends/mindmap/serve.py:4-8 (local/remote), sldb-provider.ts:43,53,68-69 (/sldb/schema,/graph,/save), src/adapters/snapshot_adapter.py:12 |
| `atom-kgdb-how-not` | `no-se-sostiene` | afirma fixtures hardcoded y guardado no-op, pero apps/review-workbench/src/features/graph-editor/lib/sldb-provider.ts:43-69 lee /sldb/schema, /sldb/graph y guarda con saveDoc |
| `atom-kgdb-s-query-language-has-no-relation-type-filter-yet` | `codigo` | sldb/src/sldb/store/graph/language/structured_query.py:9,16 (relations: list[RelationFilter]); el id dice "no filter yet" pero el contenido lo contradice, el título ya fue corregido |
| `atom-kgdb-to-ui-for-whom` | `decision` | para quién es snapshot_to_ui_graph; no se lee del código |
| `atom-kgdb-to-ui-how` | `codigo` | UIs/graph_ui/src/adapters/snapshot_adapter.py:12-33 (UIEdge por arista, snapshot_version, snapshot_created_at, helpers :35-76) |
| `atom-kgdb-to-ui-how-not` | `codigo` | UIs/graph_ui/src/adapters/snapshot_adapter.py:19-33 copia relation_type, metadata y facetas (:76 _facet_dict) |
| `atom-kgdb-to-ui-what` | `codigo` | UIs/graph_ui/src/adapters/snapshot_adapter.py:12 snapshot_to_ui_graph(GraphSnapshot)->GraphData |
| `atom-kgdb-to-ui-when` | `codigo` | src/adapters/snapshot_adapter.py:12 lado lectura; tests/test_sldb_end_to_end.py:36 construye el snapshot |
| `atom-kgdb-to-ui-where` | `codigo` | UIs/graph_ui/src/adapters/snapshot_adapter.py:1-9 (imports de sldb.api.graph y contracts.graph_data) |
| `atom-kgdb-to-ui-why` | `decision` | por qué existe el adaptador (graph_ui no consume GraphSnapshot nativamente); el porqué no está en el código |
| `atom-kgdb-what` | `codigo` | UIs/graph_ui/src/adapters/snapshot_adapter.py:7,12 importa GraphSnapshot de sldb.api.graph y adapta a GraphData; ya está en el código |
| `atom-kgdb-when` | `codigo` | lecturas/escrituras al abrir/guardar: UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/panels/NodeInspector.tsx:322 (handleTypedSave -> saveDoc) y UIs/graph_ui/src/adapters/snapshot_adapter.py:12; descripción de flujo legible del código |
| `atom-kgdb-where` | `codigo` | UIs/graph_ui/src/adapters/snapshot_adapter.py:7,12 y tests/test_snapshot_adapter.py, tests/test_sldb_end_to_end.py:23 existen; ubicación legible del código |
| `atom-kgdb-why` | `decision` | por qué graph_ui opera sobre el store real y no fixtures (y que ediciones de canvas no persisten) no se lee del código; sigue valiendo (docs/specs/sequence.data-load-target.yml) |
| `atom-l1app-for-whom` | `decision` | destinatarios de L1 (GraphEditor, registry, stores) es intención de capa, no código; UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/AntoniaFlowPage.tsx existe |
| `atom-l1app-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/AntoniaFlowPage.tsx existe; usa registerModelsFromSchema/loadGraph y renderiza GraphEditor, legible del código |
| `atom-l1app-how-not` | `invariante` | regla entre capas L1/L2 (L1 no posee interacción de canvas; lint-architecture trata features/antonia-flow como L1); docs/specs/component.graph-ui.yml |
| `atom-l1app-what` | `codigo` | AntoniaFlowPage montada por App.tsx como única página L1 (UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/AntoniaFlowPage.tsx); legible del código |
| `atom-l1app-when` | `codigo` | carga única al montar (live o ?src=fixture) en UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/AntoniaFlowPage.tsx; legible del código |
| `atom-l1app-where` | `codigo` | ruta UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/AntoniaFlowPage.tsx existe |
| `atom-l1app-why` | `decision` | por qué se separa bootstrap/dominio sobre el canvas para que el core sea reusable; no legible del código; docs/specs/component.graph-ui.yml |
| `atom-l2canvas-for-whom` | `decision` | para quién es L2 (operador y páginas L1); AntoniaFlowPage renderiza GraphEditor (UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/GraphEditor.tsx); intención de la capa |
| `atom-l2canvas-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/GraphEditor.tsx compone GraphCanvas, NodeInspector, hooks/use-keyboard.ts; legible del código |
| `atom-l2canvas-how-not` | `invariante` | L2 no obtiene datos de dominio ni se reduce a render pasivo: regla entre capas L1/L2; docs/specs/component.graph-ui.yml |
| `atom-l2canvas-what` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/ (GraphEditor.tsx, GraphCanvas.tsx, hooks/, layout/) existe; descripción de la capa legible del código |
| `atom-l2canvas-when` | `codigo` | ciclo de vida legible en UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/GraphEditor.tsx y hooks/use-graph-layout.ts |
| `atom-l2canvas-where` | `codigo` | ruta UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/ existe con GraphEditor.tsx, hooks/, layout/layout-strategies.ts |
| `atom-l2canvas-why` | `decision` | por qué toda la interacción vive en una capa reutilizable en vez de cada página; no legible del código; docs/specs/component.graph-ui.yml |
| `atom-l3content-for-whom` | `decision` | para quién es L3 (operador y registry); intención, no código; registro en UIs/graph_ui/apps/review-workbench/src/schema/register-defaults.ts |
| `atom-l3content-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/components/content/, UIs/graph_ui/apps/review-workbench/src/schema/register-defaults.ts y features/antonia-flow/lib/schema-to-registry.ts; legible del código |
| `atom-l3content-how-not` | `invariante` | L3 no obtiene datos ni posee teclado/canvas: regla entre capas L1/L2/L3; docs/specs/component.graph-ui.yml |
| `atom-l3content-what` | `codigo` | capa de render de contenido: UIs/graph_ui/apps/review-workbench/src/components/content/ y UIs/graph_ui/apps/review-workbench/src/schema/register-defaults.ts; legible del código |
| `atom-l3content-when` | `codigo` | redibujo por selección/propiedades/filtros, derivable de UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/GraphCanvas.tsx y los renderers registrados |
| `atom-l3content-where` | `codigo` | rutas UIs/graph_ui/apps/review-workbench/src/components/content/, UIs/graph_ui/apps/review-workbench/src/schema/register-defaults.ts, UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/StepCard.tsx; legibles del código |
| `atom-l3content-why` | `decision` | por qué el render varía por tipo de nodo sin que L1/L2 conozcan detalles visuales; no legible del código |
| `atom-la-capa-de-grafo-de-graph-ui-es-sldb-api-graph` | `codigo` | UIs/graph_ui/src/adapters/snapshot_adapter.py:7 from sldb.api.graph import GraphSnapshot, KnowledgeNode y :12 snapshot_to_ui_graph |
| `atom-la-vista-specs-dibuja-lo-que-resuelve-spec2viz` | `codigo` | UIs/graph_ui/frontends/mindmap/views/specs/notation/notation.mjs:4 (resuelve sldb.api.notations.resolve_view), :122-124 layouts graph/tree y aviso de no soportado, :157 carriles por partition |
| `atom-las-vistas-de-mindmap-reciben-request-y-la-url-base-en-vez-de-importar-shell-api-js` | `codigo` | UIs/graph_ui/frontends/mindmap/shell/api.js:12 export function createRequest(baseUrl) y :25 request por defecto |
| `atom-layoutstrategies-for-whom` | `decision` | para quién es (L2 y vistas guardadas) es intención; ViewSection/vistas consumen nombres de estrategia, no se lee como hecho del código |
| `atom-layoutstrategies-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/layout/layout-strategies.ts:46 DEFAULT_LAYOUT_STRATEGY_NAME, :308 LAYOUT_STRATEGIES, :322 getLayoutStrategy con fallback |
| `atom-layoutstrategies-how-not` | `invariante` | layout solo posiciona sin tocar filtros/encoding/persistencia; límite entre piezas; el registro nombrado está en UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/layout/layout-strategies.ts:308 |
| `atom-layoutstrategies-what` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/layout/layout-strategies.ts:308-314 LAYOUT_STRATEGIES con elk-layered y elk-rings |
| `atom-layoutstrategies-when` | `codigo` | invocado desde UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/hooks/use-graph-layout.ts; legible del código |
| `atom-layoutstrategies-where` | `codigo` | rutas UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/layout/layout-strategies.ts y hooks/use-graph-layout.ts existen |
| `atom-layoutstrategies-why` | `decision` | por qué un registro de estrategias en vez de un algoritmo único (jerarquías vs radiales, persistencia en vistas); no legible del código |
| `atom-nodeinspector-for-whom` | `decision` | para quién es (operador que edita nodo) es intención; UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/panels/NodeInspector.tsx existe |
| `atom-nodeinspector-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/panels/NodeInspector.tsx:241 focusedNodeId, :70 getTypedFields, :295 handleFallbackSave, :322 handleTypedSave |
| `atom-nodeinspector-how-not` | `invariante` | el inspector no cambia tipo/esquema y el guardado de grafo es de la página; límite entre piezas, parcialmente visible en NodeInspector.tsx:295,322 |
| `atom-nodeinspector-what` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/panels/NodeInspector.tsx:322 handleTypedSave y :295 fallback; legible del código |
| `atom-nodeinspector-when` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/panels/NodeInspector.tsx:241-250 se abre con focusedNodeId; legible del código |
| `atom-nodeinspector-where` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/panels/NodeInspector.tsx existe |
| `atom-nodeinspector-why` | `decision` | por qué un formulario enfocado en vez de edición JSON inline; no legible del código |
| `atom-projection-grammar` | `codigo` | la config proyección (nodos, relaciones, encoding, layout) está definida en UIs/graph_ui/apps/review-workbench/src/features/graph-editor/lib/views-provider.ts:23 ProjectionViewDoc y :15 ViewLayout |
| `atom-projection-is-layered-sldb-is-content-kgdb-is-graph-overlay-is-view` | `decision` | principio de capas ignorantes (contenido/topología/grafo/overlay) que explica el diseño; el código solo lo respeta (snapshot_adapter.py:7); menciona gemini_test cuya violación sólo queda en pill desk/contexts |
| `atom-projectionviewstore-for-whom` | `decision` | para quién es (UI de vistas y operadores); intención; el store existe como UIs/graph_ui/apps/review-workbench/src/stores/view-store.ts:22 useViewStore (nombre ProjectionViewStore ya no existe) |
| `atom-projectionviewstore-how` | `no-se-sostiene` | no existe projection-view-store.ts (rg en apps/review-workbench/src sin resultados; solo existe stores/view-store.ts:1-30, un draft zustand sin localStorage; las vistas se guardan via /api/views/save en frontends/mindmap/serve.py:332) |
| `atom-projectionviewstore-how-not` | `no-se-sostiene` | no existe projection-view-store.ts (rg en apps/review-workbench/src sin resultados; solo existe stores/view-store.ts:1-30, un draft zustand sin localStorage; las vistas se guardan via /api/views/save en frontends/mindmap/serve.py:332) |
| `atom-projectionviewstore-what` | `no-se-sostiene` | no existe projection-view-store.ts (rg en apps/review-workbench/src sin resultados; solo existe stores/view-store.ts:1-30, un draft zustand sin localStorage; las vistas se guardan via /api/views/save en frontends/mindmap/serve.py:332) |
| `atom-projectionviewstore-when` | `no-se-sostiene` | no existe projection-view-store.ts (rg en apps/review-workbench/src sin resultados; solo existe stores/view-store.ts:1-30, un draft zustand sin localStorage; las vistas se guardan via /api/views/save en frontends/mindmap/serve.py:332) |
| `atom-projectionviewstore-where` | `no-se-sostiene` | no existe projection-view-store.ts (rg en apps/review-workbench/src sin resultados; solo existe stores/view-store.ts:1-30, un draft zustand sin localStorage; las vistas se guardan via /api/views/save en frontends/mindmap/serve.py:332) |
| `atom-projectionviewstore-why` | `no-se-sostiene` | no existe projection-view-store.ts (rg en apps/review-workbench/src sin resultados; solo existe stores/view-store.ts:1-30, un draft zustand sin localStorage; las vistas se guardan via /api/views/save en frontends/mindmap/serve.py:332) |
| `atom-python-backend-for-whom` | `codigo` | consumidor snapshot_to_ui_graph visible en UIs/graph_ui/src/adapters/snapshot_adapter.py:12 y tests; lo demás es contexto de uso, no decisión |
| `atom-python-backend-how` | `codigo` | los módulos existen: UIs/graph_ui/src/contracts/graph_data.py:23, editor.py:14, auditor.py:12, provider.py:13, adapters/snapshot_adapter.py:12 |
| `atom-python-backend-how-not` | `invariante` | un solo contrato GraphData (UIs/graph_ui/src/contracts/graph_data.py:64) y backend sin render React; ninguna pieza lo afirma sola |
| `atom-python-backend-what` | `codigo` | cinco unidades presentes: UIs/graph_ui/src/contracts/graph_data.py:64, src/editor.py:14, src/auditor.py:12, src/provider.py:13, src/adapters/snapshot_adapter.py:12 |
| `atom-python-backend-when` | `codigo` | uso descrito (fixtures, ediciones, auditoría, adaptación) se lee de UIs/graph_ui/src/provider.py:13 y UIs/graph_ui/src/adapters/snapshot_adapter.py:12 |
| `atom-python-backend-where` | `codigo` | rutas listadas existen: UIs/graph_ui/src/contracts/graph_data.py, src/editor.py, src/auditor.py, src/provider.py, src/adapters/snapshot_adapter.py |
| `atom-python-backend-why` | `decision` | separar contrato y lógica del render React; el porqué no está en UIs/graph_ui/src/contracts/graph_data.py:64 |
| `atom-qué-declara-nodedata-en-review-workbench-y-cómo-se-lee-el-documento-del-nodo` | `codigo` | UIs/graph_ui/apps/review-workbench/src/stores/types.ts:7-25 declara NodeData sin firma de índice y node-data.ts:9 payloadValue (docstring/tipos ya lo dicen) |
| `atom-qué-es-una-vista-de-proyección-y-cómo-la-evalúa-graph-ui` | `no-se-sostiene` | afirma spec2viz.notation_view.resolve_documents pero UIs/graph_ui/frontends/mindmap/projection_views.py:12 usa sldb.api.notations.resolve_documents (spec2viz retirado) |
| `atom-react-editor-for-whom` | `decision` | para quién es (operador humano, AntoniaFlowPage usa GraphEditor); UIs/graph_ui/apps/review-workbench/src/App.tsx:20-26 solo muestra el montaje |
| `atom-react-editor-how` | `codigo` | stack en UIs/graph_ui/apps/review-workbench/package.json y montaje QueryClientProvider/AppShell/AntoniaFlowPage en src/App.tsx:20-26 |
| `atom-react-editor-how-not` | `invariante` | no dominio en L2/L3, fixture no es fuente, solo saveDoc persiste: UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/GraphEditor.tsx:21 y NodeInspector.tsx:349 |
| `atom-react-editor-what` | `codigo` | app React/Vite en UIs/graph_ui/apps/review-workbench/src/App.tsx:1-30; capas L1/L2/L3 en docs/specs/component.graph-ui.yml:62-64 |
| `atom-react-editor-when` | `codigo` | arranque createRoot en UIs/graph_ui/apps/review-workbench/src/App.tsx:30 con QueryClientProvider/AppShell |
| `atom-react-editor-where` | `codigo` | UIs/graph_ui/apps/review-workbench/src/App.tsx monta features/antonia-flow/AntoniaFlowPage y features/graph-editor/L2-canvas existen |
| `atom-react-editor-why` | `decision` | por qué existe un editor de grafos agnóstico de dominio; no se lee de UIs/graph_ui/apps/review-workbench/src/App.tsx |
| `atom-relations-are-their-own-content-blind-sldb-model-not-fields-inside-content` | `decision` | porqué de modelar la relación como modelo propio; código en sldb/src/sldb/models/relation_type_doc.py:12 y relation_doc.py, pero el razonamiento no está ahí |
| `atom-review-workbench-se-verifica-dentro-de-la-suite-pytest-del-repo` | `codigo` | UIs/graph_ui/tests/test_review_workbench.py:32-40 ejecuta npx tsc, npx vitest y node scripts/lint-architecture.mjs |
| `atom-reviewworkbenchspa-for-whom` | `decision` | para quién es el SPA (humano en navegador); no se lee de UIs/graph_ui/apps/review-workbench/src/App.tsx |
| `atom-reviewworkbenchspa-how` | `codigo` | bootstrap en UIs/graph_ui/apps/review-workbench/src/App.tsx:20-30 y fuente live/fixture en AntoniaFlowPage.tsx:19-24 |
| `atom-reviewworkbenchspa-how-not` | `invariante` | no confundir con fuente de datos ni persistencia; solo saveDoc escribe (UIs/graph_ui/apps/review-workbench/src/features/graph-editor/L2-canvas/GraphEditor.tsx:21, NodeInspector.tsx:349) |
| `atom-reviewworkbenchspa-what` | `codigo` | UIs/graph_ui/apps/review-workbench/src/App.tsx:20-30 monta AppShell, QueryClient y AntoniaFlowPage; docs/specs/deployment.runtime.yml:25 |
| `atom-reviewworkbenchspa-when` | `codigo` | ciclo de vida del SPA en navegador visible en UIs/graph_ui/apps/review-workbench/src/App.tsx:30 (createRoot) y package.json script dev |
| `atom-reviewworkbenchspa-where` | `codigo` | UIs/graph_ui/docs/specs/deployment.runtime.yml:25, apps/review-workbench/src/App.tsx y script dev en package.json:8 existen (specir-extrae el despliegue) |
| `atom-reviewworkbenchspa-why` | `decision` | por qué existe el contenedor SPA; sin equivalente en UIs/graph_ui/apps/review-workbench/src/App.tsx |
| `atom-saved-views-must-reference-facet-and-relation-names-never-literal-node-ids` | `invariante` | las vistas guardadas nombran modelos/relaciones, no ids (UIs/graph_ui/frontends/mindmap/projection_views.py:12; ViewDoc en stores/view-store.ts:19); vocabulario FacetFilter/RelationFilter/kgdb obsoleto pero la regla sigue |
| `atom-schemaregistry-for-whom` | `codigo` | consumidores AntoniaFlowPage/canvas del registro visibles en UIs/graph_ui/apps/review-workbench/src/schema/registry.ts:13 y features/antonia-flow/lib/schema-to-registry.ts |
| `atom-schemaregistry-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/schema/registry.ts:14 Map, :24 getRenderer lanza, :51 canConnect; register-defaults.ts:10 |
| `atom-schemaregistry-how-not` | `invariante` | registro no debe saltar validación ni aceptar tipos desconocidos: UIs/graph_ui/apps/review-workbench/src/schema/registry.ts:24-27 lanza Unknown node type |
| `atom-schemaregistry-what` | `codigo` | NodeTypeRegistry en UIs/graph_ui/apps/review-workbench/src/schema/registry.ts:13 y registry.types.ts definen NodeTypeDefinition |
| `atom-schemaregistry-when` | `codigo` | registro en arranque (App.tsx:20 registerDefaultNodeTypes) y consulta en UIs/graph_ui/apps/review-workbench/src/schema/registry.ts:24,51 |
| `atom-schemaregistry-where` | `codigo` | archivos existen: UIs/graph_ui/apps/review-workbench/src/schema/registry.ts, registry.types.ts, register-defaults.ts |
| `atom-schemaregistry-why` | `decision` | por qué centralizar el conocimiento de tipos de nodo; el código en UIs/graph_ui/apps/review-workbench/src/schema/registry.ts:13 no lo dice |
| `atom-staticfixtures-for-whom` | `no-se-sostiene` | dice que la ruta live sldb 'aún no está conectada' pero AntoniaFlowPage.tsx:19-24 usa live por defecto; mock/ no existe en review-workbench |
| `atom-staticfixtures-how` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/AntoniaFlowPage.tsx:19-24 (?src=fixture, default live) y lib/adapter.ts buildAntoniaGraph |
| `atom-staticfixtures-how-not` | `invariante` | fixture no es fuente real ni prueba persistencia; live es el default: UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/AntoniaFlowPage.tsx:19-24 |
| `atom-staticfixtures-what` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/antonia-fixture.generated.json y scripts/generate-antonia-fixture.mjs existen |
| `atom-staticfixtures-when` | `codigo` | UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/AntoniaFlowPage.tsx:19-24 y package.json:7-8 (hum:sync ahora genera node types) |
| `atom-staticfixtures-where` | `no-se-sostiene` | apps/review-workbench/src/mock/ no existe (graph_data.json/client.ts solo en apps/knowledge-workbench/src/mock/client.ts); solo antonia-fixture.generated.json existe en UIs/graph_ui/apps/review-workbench/src/features/antonia-flow/ |
| `atom-staticfixtures-why` | `no-se-sostiene` | afirma que no hay integración sldb viva ni persistencia de ediciones, pero UIs/graph_ui/apps/review-workbench/src/features/graph-editor/lib/sldb-provider.ts y L2-canvas/panels/NodeInspector.tsx usan saveDoc; el fixture (antonia-fixture.generated.json) solo sirve a ?src=fixture (docs/specs/component.graph-ui.yml:98) |
| `atom-store-core-knows-index-query-hash-lock-consumers-inject-type-and-codec` | `decision` | frontera de qué posee el núcleo del store y qué inyectan los consumidores; el protocolo está en sldb/src/sldb/store/codec.py:8-14 pero la regla "sin formato/dominio en firmas públicas" es objetivo (sldb/src/sldb/store/model_contract.py:20 aún importa StructuredNLDoc) |
| `atom-structuralauditor-for-whom` | `docstring` | auditor.py hace la anotación (UIs/graph_ui/src/auditor.py:13-45) pero su docstring (auditor.py:1-3,12) no dice quién lo consume |
| `atom-structuralauditor-how` | `codigo` | UIs/graph_ui/src/auditor.py:17-45 (mapas outgoing/incoming, _decorate_node, valid si out>0) |
| `atom-structuralauditor-how-not` | `codigo` | auditor.py:13-45 solo escribe compliance_status y metadata['signal'], no crea ni reescribe nodos/aristas |
| `atom-structuralauditor-what` | `codigo` | UIs/graph_ui/src/auditor.py:12-45 (audit y _decorate_node sobre GraphData) |
| `atom-structuralauditor-when` | `codigo` | audit(data: GraphData) opera sobre un grafo ya cargado, UIs/graph_ui/src/auditor.py:15 |
| `atom-structuralauditor-where` | `codigo` | UIs/graph_ui/src/auditor.py:8-12 (imports GraphData/UINode y la clase) |
| `atom-structuralauditor-why` | `codigo` | el docstring UIs/graph_ui/src/auditor.py:2,12 y las ramas orphan/terminal/valid (auditor.py:36-45) ya dicen el propósito |
| `atom-the-projection-grammar-belongs-in-graph-ui-not-sldb` | `decision` | decide dónde vive la gramática de proyección (graph_ui, no sldb); ancla viva UIs/graph_ui/frontends/mindmap/source/projections.mjs, pero projection-view-store.ts citado ya no existe (ahora features/graph-editor/lib/views-provider.ts:1-5) |
| `atom-the-store-is-a-generic-typed-document-engine-not-sldb-owned-infrastructure` | `decision` | decide que el store es un motor genérico y sldb un cliente; codec.py:8-14 lo respalda aunque el LOC citado (~7.9k) es ya ~10.7k en sldb/src/sldb/store y model_contract.py:20 sigue acoplado a StructuredNLDoc |
| `atom-three-incompatible-graph-node-edge-contracts-exist-across-the-ecosystem` | `codigo` | las tres formas se leen del código: UIs/graph_ui/src/contracts/graph_data.py:23,49 (UINode/UIEdge), apps/review-workbench/src/stores/types.ts:26,38 (ASTNode/ASTEdge), src/adapters/snapshot_adapter.py:12 y features/antonia-flow/lib/adapter.ts |
| `atom-uistore-for-whom` | `codigo` | consumidores en sidebar/diálogos/teclado leen useUIStore, p.ej. L2-canvas/sidebar/ViewSection.tsx:16 y stores/ui-store.ts:43-59 |
| `atom-uistore-how` | `codigo` | apps/review-workbench/src/stores/ui-store.ts:43-59,84,94-136 (setters, cloneEncodingRules(DEFAULT_ENCODING_RULES), executePendingDelete, openCommandDialog) |
| `atom-uistore-how-not` | `invariante` | UiStore no posee nodos/aristas y la persistencia va por sldbProvider.saveDoc desde NodeInspector (features/graph-editor/L2-canvas/panels/NodeInspector.tsx, lib/sldb-provider.ts); estado en stores/ui-store.ts:43-59 |
| `atom-uistore-what` | `codigo` | apps/review-workbench/src/stores/ui-store.ts:11-12,43-59 (editorState, filtros, reglas, layout, diálogos) |
| `atom-uistore-when` | `codigo` | los setters de modo/sidebar/filtros/layout/diálogo en apps/review-workbench/src/stores/ui-store.ts:43-59,94-136 |
| `atom-uistore-where` | `codigo` | apps/review-workbench/src/stores/ui-store.ts existe (ruta citada correcta) |
| `atom-uistore-why` | `decision` | separar estado de UI del historial del grafo (graph-store.ts vs ui-store.ts) es un porqué; el código solo muestra la separación en stores/ui-store.ts:43-59 |
| `atom-viewsection-for-whom` | `docstring` | ViewSection.tsx:14-72 hace layout y foco pero no declara a quién sirve |
| `atom-viewsection-how` | `codigo` | L2-canvas/sidebar/ViewSection.tsx:5,14,16,33-39 (useGraphLayout, focusedNodeId, hideNonNeighbors, setEditorState('focus')) |
| `atom-viewsection-how-not` | `codigo` | use-graph-layout.ts:17,94 escribe updateNode(..., {isVisualOnly: true}) en apps/review-workbench/src/features/graph-editor/L2-canvas/hooks/ |
| `atom-viewsection-what` | `codigo` | L2-canvas/sidebar/ViewSection.tsx:14-72 (tabs auto/manual, Apply Layout, Focus on Selected) |
| `atom-viewsection-when` | `codigo` | ViewSection.tsx:33-36,72 (foco solo si focusedNodeId; disabled={!focusedNodeId}) |
| `atom-viewsection-where` | `codigo` | L2-canvas/sidebar/ViewSection.tsx:5 importa hooks/use-graph-layout.ts; ambas rutas existen |
| `atom-viewsection-why` | `docstring` | el componente hace layout/foco (ViewSection.tsx:33-72) sin comentario del propósito |
| `atom-viewssection-for-whom` | `docstring` | ViewsSection.tsx:29-70 guarda/aplica vistas con nombre pero no dice para quién |
| `atom-viewssection-how` | `no-se-sostiene` | afirma ProjectionViewStore en localStorage, pero apps/review-workbench/src/features/graph-editor/L2-canvas/sidebar/ViewsSection.tsx:5-7,29-32,67-69 usa viewsProvider (servidor, lib/views-provider.ts:1-5) y useViewStore |
| `atom-viewssection-how-not` | `no-se-sostiene` | ProjectionViewStore ya no existe: ViewsSection.tsx:6-7 usa viewsProvider y useViewStore; lib/views-provider.ts:1-5 delega en el servidor (/api/views) |
| `atom-viewssection-what` | `codigo` | L2-canvas/sidebar/ViewsSection.tsx:5-7,29-70 guarda y carga vistas con nombre (aplica vía useApplyView) |
| `atom-viewssection-when` | `codigo` | ViewsSection.tsx:32 (estado views) y la recarga tras guardar en ViewsSection.tsx:60-70 |
| `atom-viewssection-where` | `no-se-sostiene` | la ruta features/graph-editor/lib/projection-view-store.ts no existe; ahora lib/views-provider.ts y stores/view-store.ts; ViewsSection.tsx sí existe |
| `atom-viewssection-why` | `no-se-sostiene` | afirma persistencia en localStorage; ViewsSection.tsx:6 y lib/views-provider.ts:1-5 persisten en el servidor (ViewDoc del store) |
| `atom-vitedevserver-for-whom` | `codigo` | apps/review-workbench/vite.config.js:16-26 (puerto 5173, proxy /sldb a sldb serve) y package.json:8 (script dev) |
| `atom-vitedevserver-how` | `codigo` | apps/review-workbench/package.json:7-8 (hum:sync, dev) y vite.config.js:16,23-26 (5173, /sldb -> 8787) |
| `atom-vitedevserver-how-not` | `codigo` | vite.config.js:16-26 solo sirve la SPA y proxea /sldb; es el script dev en package.json:8, no backend ni producción |
| `atom-vitedevserver-what` | `codigo` | UIs/graph_ui/docs/specs/deployment.runtime.yml:27-28 (vite_dev_server :5173) y vite.config.js:16 |
| `atom-vitedevserver-when` | `codigo` | package.json:8 "npm run hum:sync && vite" (arranca tras hum:sync) |
| `atom-vitedevserver-where` | `codigo` | UIs/graph_ui/docs/specs/deployment.runtime.yml:27-28 y apps/review-workbench/package.json:8 |
| `atom-vitedevserver-why` | `codigo` | el script dev (package.json:8) y vite.config.js:16-26 ya dicen que es el servidor local de la SPA |
| `atom-workspace-presents-document-graph-code-and-changes-as-projections-of-the-same-node` | `contexto-trabajo` | documento/grafo/código existen (UIs/graph_ui/frontends/mindmap/workspace_routes.py:1,122-138) pero Changes/staleness es la tarea abierta UIs/graph_ui/desk/tasks/task-vista-changes-arbol-de-hashes-staleness-e-impacto-en-conocimiento.md (status draft) |

### graph_ui: pills (2)

| id | veredicto | motivo |
|---|---|---|
| `pill-guardrail-no-mocks-no-stubs-no-fake-data-in-deliverables` | `invariante` | regla permanente y global (todo ejecutor, todas las tareas) sin trabajo abierto que la contenga; no es legible de código (UIs/graph_ui/apps, src) |
| `pill-guardrail-the-model-descriptor-is-a-real-contract-mirror-not-a-mock` | `no-se-sostiene` | su fuente gemini_test/kb_agent/models/knowledge/step.py no existe en el workspace (find step.py sin resultados) y no hay tarea abierta que difiera la lectura viva; descriptor en UIs/graph_ui/apps/review-workbench/src/schema/models/conversation-step.model.json |

### deskops: átomos (240)

| id | veredicto | motivo |
|---|---|---|
| `atom-001` | `no-se-sostiene` | afirma estado en .sldb/runtime/ pero sldb/src/sldb/store/layout.py:1-2 dice que lo derivado vive en .sldb_cache/ y runtime/ se retiro el 2026-11-04 (.config sigue en layout.py:29) |
| `atom-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict` | `codigo` | deskops/deskops/cli/parse_input.py:22-23,56-57 (_ensure_string_list_items rechaza items no string de --from-yaml) con docstring que lo dice |
| `atom-agents-read-by-decision-need` | `decision` | criterio de lectura segun la decision a tomar y no por cercania de archivo; norma permanente sin codigo |
| `atom-agents-read-through-semantic-tools` | `decision` | porque leer por SLDB/deskops y no texto plano; menciona spec2viz (retirado, ahora specIR) pero la decision sigue valiendo |
| `atom-al-llegar-una-nota-al-inbox-deskops-despierta-a-la-identidad-scion-del-desk-si-su-config-lo-pide` | `codigo` | deskops/deskops/wake.py:15-22 wake_identity, config.py:34-39 IdentityConfig, cli/registry.py:690 message wake |
| `atom-atom-candidates-come-from-durable-answers` | `decision` | define de donde salen los candidatos a atomo (respuestas durables, residuo de closeout); criterio de proceso permanente |
| `atom-atom-folder-axis-is-one-configurable-tag-namespace` | `codigo` | deskops/deskops/config.py:95 atom_folder_axis y doc_access.py:612-631 (eje, error si no es namespace registrado); tests/ cubre object:licitaciones |
| `atom-atom-lifecycle-includes-validate-and-delete-with-inbound-reference-guard` | `codigo` | deskops/deskops/services/atoms.py:315,330 validate_atoms/delete_atom(force) y cli/registry.py:1351 atoms validate |
| `atom-atom-lifecycle-is-complete-create-from-source-split-merge` | `codigo` | deskops/deskops/operations.py:265-275 (from_pill), 281 split_atom, 296 merge_atom |
| `atom-atom-references-carry-roles` | `codigo` | deskops/deskops/atom_references.py:17 ALLOWED_ROLES = (references, documents, specifies, constrains, validates) |
| `atom-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-message-send-y-list-atoms-aceptan-conv` | `codigo` | deskops/deskops/models/atom.py:103,147 conversation_ref y cli/registry.py:161,219,675 flag --conv |
| `atom-atoms-answer-one-question` | `invariante` | cada atomo responde exactamente una pregunta 5WH1+ y no lleva relaciones salientes; regla entre atomo y materializaciones (ver deskops/deskops/models/atom.py) |
| `atom-atoms-are-stable-documentation-core` | `decision` | afirma que todo doc duradero es atomo o materializacion de atomos; decision de modelo (la nueva definicion en desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md la acota pero no la anula aqui) |
| `atom-atoms-distill-project-knowledge` | `decision` | define que es un atomo (conocimiento destilado de decisiones, bugs, etc.); no esta en codigo, es el porque del modelo de conocimiento y sigue valiendo sin trabajo abierto |
| `atom-automatic-routines-vs-llm-tasks` | `codigo` | las post-hooks sobre transiciones ya existen en deskops/deskops/lifecycle_hooks.py y los gates en deskops/deskops/services/closeout_gates.py |
| `atom-available-tasks-are-board-routed-work` | `decision` | define tarea disponible como trabajo enrutado por el board y no nota de inbox/drawer; decision de modelo permanente |
| `atom-big-documents-need-explicit-modeling-strategy` | `decision` | porque (why) de elegir cuerpo compuesto vs secciones tipadas; ninguna pieza de deskops/deskops/ lo impone, sin tarea abierta asociada |
| `atom-board-context-uses-portable-document-names` | `invariante` | nombres de pills y rituales deben coincidir con stem/identidad rastreada para que los consumidores sldb resuelvan contexto: regla entre varias piezas |
| `atom-build-neighbours-de-absolute-paths-resuelve-el-registro-con-resolve-registered-root` | `codigo` | deskops/deskops/absolute_paths.py:34,168,179 build_neighbours usa resolve_registered_root |
| `atom-cada-ejecutor-de-dispatch-trabaja-en-su-propio-git-worktree-y-reap-integra-su-rama` | `codigo` | deskops/deskops/dispatch.py:28,133-193 (.worktrees, info/exclude) y 275-277 (cherry-pick / abort en conflicto) |
| `atom-cada-intento-de-dispatch-tiene-su-propio-rundoc-con-intencion-y-confirmacion-separadas` | `codigo` | deskops/deskops/dispatch.py:342 (exec-<name>), 479-544 intentos, 597 confirm_scion_dispatch; models/run.py:15 |
| `atom-canonical-project-identity-resolves-through-a-shared-registry-resolver` | `codigo` | deskops/deskops/identity.py:93-108 (_raise_on_duplicate_ids/_duplicate_id_message fallan por identidad duplicada), resolve_registered_root |
| `atom-cero-instancias-de-un-modelo-no-prueba-ausencia-de-la-capacidad` | `decision` | regla de razonamiento (como comprobar una negacion) que ningun codigo ni specIR dice; vale sin trabajo abierto |
| `atom-changes-flow-through-tasks-and-pills` | `decision` | por que los cambios pasan por tareas y pills (alcance, contexto, validacion, guardrails); regla de proceso permanente |
| `atom-cheap-zero-context-reviews-test-the-brief-recursively` | `decision` | metodo de revision del brief con revisor barato sin contexto y su razon; no expresado en codigo |
| `atom-clean-agents-start-from-minimum-workflow-set` | `decision` | define el conjunto minimo (README, board, pills, rituales, atomos) para un agente limpio; criterio de proceso permanente |
| `atom-clean-code-reduces-knowledge-drift` | `decision` | el porque del codigo limpio para que los atomos expliquen solo lo que el codigo no dice; coincide con el brief en desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md |
| `atom-clean-subagent-ambiguity-review` | `decision` | regla de que el subagente limpio devuelva la tarea ambigua; norma de proceso permanente, sin codigo que la fuerce |
| `atom-cli-gaps-become-tracked-work` | `decision` | los huecos del CLI se vuelven trabajo rastreado y no notas de chat; norma permanente |
| `atom-cli-is-thin-over-primitives-and-sldb` | `invariante` | el CLI delega en SLDB (lectura/escritura de documentos) y en el grafo del ciclo de vida, sin segunda implementacion; relacion entre deskops/deskops/cli/ y sldb (ver deskops/deskops/doc_access.py:467 create_doc) |
| `atom-cli-mutation-testing-uses-sandbox-desk-roots` | `decision` | norma de probar mutaciones en .tmp/deskops-cli-test y no en el desk real; ya descrito en deskops/docs/how-to-test-ux-cli.md:42, pero es la razon/norma, no codigo |
| `atom-cli-should-match-spoken-workflow-language` | `decision` | criterio de diseno del CLI (cercano al lenguaje hablado); permanente, sin codigo que lo exprese |
| `atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly` | `decision` | decision del dueno 2026-10-29 (el porque); el mecanismo ya esta en deskops/deskops/services/closeout_gates.py:29-31 y models/task_types.py:147-153 pero el atom conserva el porque |
| `atom-closeout-resolved-by-cierra-una-tarea-cuyo-trabajo-ya-entró-por-pr` | `codigo` | deskops/deskops/services/closure.py:286 close_resolved_by, :388 status resolved event resolved-by; models/task_lifecycle.py:72 |
| `atom-closeout-validates-knowledge-surfaces` | `decision` | cuando validar consistencia de docs/specs/atomos antes de cerrar; criterio de proceso, deskops/deskops/services/closeout_gates.py no comprueba todo eso |
| `atom-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-sea-nodo-del-grafo-o-missing` | `codigo` | deskops/deskops/services/closure.py:90 target_covers y :1615-1625 con docstring que lo dice |
| `atom-closeout-verify-escribe-recibos-de-evidencia-como-reviewdoc-kind-evidence` | `codigo` | deskops/deskops/models/review.py:37-39 (kind evidence, EvidenceFact) y services/closure.py:1221 escribe kind evidence |
| `atom-closing-commits-are-tool-made-and-run-linked` | `codigo` | deskops/deskops/services/closure.py:190 (Task-Id, Closeout-Mode: manual, Closeout-Reason) y doctor_findings.py:137-142 leen los trailers; closeout commit con --run-dir/--no-run |
| `atom-code-changes-close-with-tests-and-commit` | `codigo` | el gate de cierre ya lo exige: deskops/deskops/services/closeout_gates.py (tests) y deskops/deskops/services/closure.py (commit del closeout) |
| `atom-codebase-surfaces-generate-atom-candidates` | `decision` | metodo de dividir superficies de codigo y cruzar aristas para pedir candidatos a atomo; no hay codigo que lo haga (specIR podria, pero el hecho es una tecnica de trabajo) |
| `atom-contenedores-scion-venv-propio-con-uv-python-3-12-via-a` | `decision` | decision 2026-11-18 via (a) frente a (b) con medicion; el paso uv venv ya esta en deskops/deskops/runtime/scion.py:885 pero el porque de la via elegida solo vive en el atom |
| `atom-create-operations-should-rollback-on-failure` | `codigo` | ya se deshace un create fallido: deskops/deskops/doc_access.py:480 remove_created_file usado en deskops/deskops/domain_tree.py:221 y deskops/deskops/services/atoms.py:222 |
| `atom-cross-desk-inbox-delivery-is-verifiable-and-acknowledgeable` | `codigo` | deskops/deskops/cli/registry.py:720 message ack, cli/commands/message.py:65, identity.py:93-108 resolucion canonica |
| `atom-declared-materialization-targets-are-graph-nodes` | `codigo` | deskops/deskops/graph/desk_graph.py:97 source_kind declared_materialization_target; tests/test_graph_extract_sources.py:133,149 |
| `atom-desk-health-delegates-store-diagnostics-to-sldb` | `decision` | frontera de propiedad desk vs sldb (Boundary Rationale); el delegar esta en deskops/deskops/doctor_findings.py:30-64 (sldb stores check) pero el porque de la separacion no esta en codigo |
| `atom-desk-health-is-measured-by-cli-diagnostics` | `docstring` | deskops/deskops/doctor_findings.py:30-64,324 hace la clasificacion errores/alertas pero el catalogo y los exit codes (1 vs 0) no estan en un docstring |
| `atom-desk-health-is-workspace-integrity-state` | `codigo` | deskops/deskops/workspace.py:19,74 classify_desk y doctor_findings.py (estructura, no rastreados, no legibles, modelos no registrados) ya lo hacen |
| `atom-desk-is-document-data-only` | `invariante` | desk/ solo guarda documentos y el Python vive en deskops/ (find desk -name '*.py' vacio); regla de layout entre desk/ y el paquete deskops/ |
| `atom-desk-repair-is-owned-by-deskops` | `decision` | limites de que repara deskops y que no (store init, esquema, contenido) es frontera de propiedad; el codigo solo ve lo que hace, no lo que no le toca (doctor_findings.py / workspace.py:646) |
| `atom-desk-test-root-precedence-is-explicit` | `codigo` | deskops/deskops/cli/main.py:170-181 implementa y comenta flag > DESKOPS_TEST_ROOT > config.local > config.json; deskops/deskops/config.py:132 fusiona config.json antes de config.local.json |
| `atom-desk-workspaces-classify-as-absent-empty-legacy-or-current` | `codigo` | deskops/deskops/workspace.py:19 DeskClassification, :74 classify_desk, :108-127 legacy/current; cli/registry.py:1244 desk migrate |
| `atom-deskops` | `specir-extraeria` | descripcion de que es el paquete (CLI Python sobre sldb) = estructura del repo (pyproject, deskops/cli); IR hoy no describe librerias Python con CLI (plan que-es-un-atomo...) |
| `atom-deskops-architecture` | `codigo` | cuerpo 'CLI on sldb' sin porque ni invariante: pyproject/deskops/cli/main.py y los imports sldb lo muestran; sin contenido que preserve |
| `atom-deskops-automates-repeated-workflow-obligations` | `decision` | el porqué de existir de deskops (automatizar obligaciones repetidas); sigue valiendo sin trabajo abierto, no hay hecho en código que lo exprese |
| `atom-deskops-declara-el-namespace-de-tags-host` | `codigo` | deskops/deskops/data/templates/atoms/tag-namespaces.yaml:9-13 declara host (host:local, host:robocop2); el resto es historia de la tarea |
| `atom-deskops-es-un-plugin-sobre-sldb-no-una-reimplementacion` | `decision` | decision de JP 2026-11-25 (el porque y el limite de lo que queda en deskops); plan desk/drawer/plans/deskops-plugin-de-sldb/ lo ejecuta pero la decision sigue valiendo |
| `atom-deskops-exige-git-en-cada-desk` | `decision` | decision de JP 2026-11-25 (todo desk vive en git); tarea task-jp-decide-si-deskops-exige-git... la origino; no es lectura de codigo |
| `atom-deskops-imports-sldb-cli-helpers-from-their-current-modules` | `codigo` | deskops/deskops/cli/commands/repo.py:9-10 importa registered_model y get_store_context de sldb.cli.model_utils/store_context (existen: sldb/src/sldb/cli/model_utils.py:12) |
| `atom-deskops-init-agrega-deskops-log-al-gitignore-del-repo` | `codigo` | deskops/deskops/bootstrap.py:131-140 agrega .deskops.log al .gitignore sin duplicar, con docstring |
| `atom-deskops-init-id-fija-la-project-identity-repo-whoami-set-la-cambia-por-cli-y-repo-register-avisa` | `codigo` | deskops/deskops/cli/registry.py:637 init --id y :1194-1199 repo whoami --set |
| `atom-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk` | `codigo` | deskops/deskops/bootstrap.py:127,147-150 ensure_merge_driver (idempotente, fuera de git nada) y cli/commands/desk.py:212 con --apply |
| `atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk` | `codigo` | deskops/deskops/cli/registry.py:690,720 message wake/ack sin ruta ("inbox",) registrada (rg inbox en registry.py solo ayuda/ROOT_ARG) |
| `atom-deskops-models-are-sldb-documents` | `specir-extraeria` | deskops/deskops/models/review.py, run.py, base.py declaran modelos sldb con campos Pydantic; relacion modelo-StructuredNLDoc es hecho estructural extraible (IR no describe hoy librerias Python) |
| `atom-deskops-owns-workflow-not-document-infrastructure` | `decision` | frontera de propiedad deskops/sldb (coherente con AGENTS.md workspace); menciona spec2viz, hoy retirado hacia specIR, pero la decisión de frontera se sostiene |
| `atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola` | `codigo` | deskops/deskops/queue.py:177,220,338 (job set, retry_exit_codes) y data/templates/config.json:34 dispatch-reap |
| `atom-deskops-reads-and-writes-through-sldb` | `codigo` | deskops/deskops/doc_access.py:48-49,406 importa render_model_markdown y extract_model_data |
| `atom-deskops-resuelve-documentos-por-los-selectores-de-sldb` | `codigo` | deskops/deskops/doc_access.py:39,657-664 select_documents(expect="one"); drawer lee disco en services/drawer.py:137 |
| `atom-deskops-review-record-deja-recibos-reproduction-goldens-y-owner-sin-modelo` | `codigo` | deskops/deskops/services/review.py:80 RECORD_KINDS incluye reproduction/goldens/owner y cli/registry.py:979 review record |
| `atom-deskops-should-read-through-sldb-compositions` | `decision` | preferencia de diseno (componer en el modelo antes que coser documentos en codigo) y su porque; no es legible del codigo |
| `atom-deskops-still-reads-workflow-surfaces-as-files-where-it-could-compose-them` | `contexto-trabajo` | estado de deuda (lectura por archivos); lo cubre el plan desk/drawer/plans/deskops-plugin-de-sldb/ (alcance.md, diagnostico.md) |
| `atom-diagrams-generate-operational-models` | `decision` | principio de diseño (diagramas como superficie primaria) sin contraparte extraíble del código; no depende de tarea abierta |
| `atom-diagrams-project-knowledge-relations` | `decision` | afirma el papel de los diagramas como proyeccion de atoms/specs/docs; criterio de diseno sin codigo que lo contradiga ni lo exprese |
| `atom-dispatch-commitea-el-run-md-del-run-dir-junto-con-su-rundoc` | `codigo` | deskops/deskops/dispatch.py:295-314 _run_store_paths incluye run.md y _commit_run_store, docstring en :298 y :308 |
| `atom-dispatch-commitea-los-rundoc-que-escribe` | `codigo` | deskops/deskops/dispatch.py:269 _commit_run_store tras record_scion_run (:446,519) con pathspec |
| `atom-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado` | `codigo` | deskops/deskops/dispatch.py:509-515 y :627 doc_access.untrack_doc(run-<slug>) con comentario que lo explica |
| `atom-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta` | `codigo` | deskops/deskops/dispatch.py:548 llama scion templates sync con str(target.resolve()) |
| `atom-dispatch-start-solo-se-frena-por-la-memoria-de-la-maquina-o-porque-la-tarea-ya-tiene-agente` | `codigo` | deskops/deskops/dispatch.py:455-466 gate wait_reason y EXIT_BUSY (dispatch.py:23) si la tarea ya tiene agente; queue.py:119 wait_reason |
| `atom-dispatch-start-tester-espera-a-que-la-rama-del-ejecutor-este-integrada` | `codigo` | deskops/deskops/dispatch.py:471 imprime 'en espera: la rama ... no está integrada' y devuelve EXIT_BUSY |
| `atom-divide-and-conquer-persisted-operations` | `decision` | justificación (por qué unidades pequeñas persistidas + git); durable, no es hecho de código |
| `atom-do-not-atomize-a-coherent-deliverable-into-disconnected-tasks` | `decision` | regla de diseño (una entrega coherente = una tarea) sin código que la imponga; sin trabajo abierto que la contenga (grep en deskops/deskops sin enforcement) |
| `atom-do-not-use-instructional-text-as-model-documentation` | `decision` | porqué no documentar el contrato del modelo en el texto de plantilla sino en Field(description=); criterio de estilo vigente sin dependencia de tarea abierta |
| `atom-docs-are-human-facing-atom-materializations` | `decision` | define qué es un doc frente a un átomo (criterio de diseño); no hay código que lo enuncie |
| `atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea` | `codigo` | deskops/docs/configuration.md existe y deskops/tests/test_docs_recipes.py verifica las recetas |
| `atom-docs-materialize-atoms-for-humans` | `decision` | papel de los docs principales respecto a los atomos (seleccionan y ordenan); decision de modelo, vale sin trabajo en curso |
| `atom-doctor-e-init-reportan-el-layout-viejo-de-sldb-con-el-remedio-migrate-layout` | `codigo` | deskops/deskops/sldb_layout.py:43 arma el remedio 'sldb stores migrate-layout'; tests/test_doctor_sldb_layout.py:61,96; bootstrap.py:299 |
| `atom-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada` | `codigo` | deskops/deskops/doctor_findings.py:136-153 closed_task_ids reconoce 'closeout: <id>' y doctor_findings.py:66-83 separa lost_receipts |
| `atom-doctor-separates-unmodeled-desk-surfaces-from-broken-tracking` | `codigo` | deskops/deskops/doctor_findings.py:46,59 separa lost_receipts y superficies sin modelar del tracking roto (doctor_findings.py:176 moved_documents) |
| `atom-documents-point-to-atoms` | `decision` | decisión de composición doc->átomos vía sldb; durable y sin tarea abierta que lo sostenga |
| `atom-domain-crossroads-are-mandatory-parents` | `docstring` | deskops/deskops/domain_tree.py:1-10 ya dice que cada prefijo de domain: necesita un CrossroadDoc; el porqué (orden de la base) está en el docstring |
| `atom-drawer-is-not-active-work` | `codigo` | deskops/deskops/cli/registry.py:326 (--from-drawer) y :1020/:1926 ayuda: los items del drawer solo pasan a tarea con deskops add task --from-drawer |
| `atom-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-y-entradas-no-md-por-stem-y-registra-reas` | `codigo` | deskops/deskops/cli/registry.py drawer remove; golden deskops/tests/fixtures/golden/help/deskops_drawer.txt:7 describe archivo/issue con assets/plan entero |
| `atom-drawers-feed-tasks-through-promotion` | `codigo` | deskops/deskops/cli/registry.py:326,1020,1926: no hay comando de promoción, solo add task --from-drawer; la ayuda ya lo dice |
| `atom-drift-checks-are-review-surfaces-not-mutators` | `decision` | el porqué de que drift checks sean superficies de revisión y no mutadores; la mecánica está en deskops/deskops/graph/self_reflection.py:17-19 pero la regla 'nunca mutan' es decisión |
| `atom-drift-checks-compare-atoms-materializations-implementation` | `decision` | criterio de como decidir que esta obsoleto (atomo, materializacion o implementacion); deskops/deskops/graph/self_reflection.py solo reporta hallazgos de grafo, no compara las tres cosas |
| `atom-ease-of-use-requires-progressive-disclosure` | `decision` | principio de UX (comandos mínimos primero); criterio de diseño durable, no es hecho de código |
| `atom-el-board-declara-las-fases-del-dag` | `codigo` | deskops/deskops/models/board.py:17,98-123 Phase y validación de tarea única; board sin phases válido (board.py:112) |
| `atom-el-commit-de-cierre-stagea-solo-lo-que-escribio-el-cierre-en-sldb` | `codigo` | deskops/deskops/cli/commands/closeout.py (_close foto porcelain/sha256 de .sldb) y su test; staging solo de cambios del cierre |
| `atom-el-gate-atom-materialization-del-closeout-acepta-un-atomo-declarado-por-la-tarea-que-cita-el-archivo` | `codigo` | deskops/deskops/services/closure.py:1321,1558-1569 atom-cites:<atomo> -> <ruta>; test tests/test_closeout_atom_cites_file.py |
| `atom-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript` | `codigo` | deskops/deskops/services/closeout_gates.py:90,174-178 TEST_FILE_SUFFIXES incluye .test.ts/.test.tsx/.spec.ts/.spec.tsx |
| `atom-el-gate-de-tests-del-closeout-acepta-py-bajo-cualquier-tests-del-repo-o-declarados-en-files` | `codigo` | deskops/deskops/services/closeout_gates.py:174 reference_points_to_test acepta .py bajo tests o declarado en files |
| `atom-el-golden-de-help-de-deskops-drawer-refleja-la-descripcion-nueva-de-drawer-remove` | `codigo` | deskops/tests/fixtures/golden/help/deskops_drawer.txt:7 ya lista la descripción nueva de drawer remove |
| `atom-el-reap-encola-el-tester-tras-integrar-un-ejecutor` | `codigo` | deskops/deskops/dispatch.py:742-746 reap encola dispatch-tester si integró y no hay tester vivo (dispatch.py:662 _tester_queued) |
| `atom-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-deriva-el-alias-de-model` | `codigo` | deskops/deskops/runtime/scion.py:63 model_alias_for y deskops/deskops/materializers/runtime_profiles.py build_agent_spec_args |
| `atom-el-snapshot-de-contratos-de-modelo-acepta-el-cambio-solo-de-descripcion-de-ruledoc` | `codigo` | deskops/tests/fixtures/model_contract_hashes.json:16 RuleDoc = 411e41fc... ya aplicado |
| `atom-el-store-de-deskops-no-federa-el-store-de-spec2viz` | `decision` | decisión de JP 2026-11-16 de no federar spec2viz; deskops/.sldb/store.yaml:2-9 enlaces solo sldb, pron, scion |
| `atom-el-vocabulario-de-esquema-de-los-artefactos-de-deskops-vive-en-los-modelos-no-en-spec-artifacts-ni-s` | `codigo` | deskops/deskops/spec solo contiene workflows/; esquemas en models/ (__artifact__) y doc_access.py; deskops/deskops/models/board.py:54 plantillas |
| `atom-en-deskops-el-store-de-sldb-se-versiona-entero-y-solo-la-caché-se-ignora` | `decision` | regla del dueño: .sldb versionado entero y solo .sldb_cache ignorado (deskops/.gitignore:7); enforced por tests/test_gitignore_policy.py |
| `atom-en-modo-pr-la-rama-task-id-vive-en-su-propio-worktree-y-el-checkout-principal-nunca-cambia-de-rama` | `codigo` | deskops/deskops/dispatch.py:28 WORKTREES_DIR, :115-134; cli/commands/closeout.py:13-35 usa worktree task/<id> en modo pr |
| `atom-every-change-needs-descriptive-commit` | `decision` | regla de proceso con su porqué (commits explicativos); durable sin trabajo abierto |
| `atom-extensibility-is-a-contract` | `invariante` | exige puntos de extension declarados, reglas de validacion y compatibilidad entre varias piezas (modelos, ciclo de vida, CLI, materializaciones); ninguna pieza lo afirma sola |
| `atom-failed-sldb-paths-become-sldb-inbox-issues` | `decision` | regla de proceso coherente con AGENTS.md (pedir a sldb por inbox, no rodear en el consumidor); durable |
| `atom-field-oriented-document-composition` | `codigo` | deskops/deskops/specs/compiler.py:24,83 CompiledArtifactSpec: el modelo Pydantic es la única fuente de los campos |
| `atom-first-safe-action-follows-read-route` | `decision` | orden de onboarding README->Board->pills/rituales; criterio de uso durable, no extraíble |
| `atom-git-history-is-the-past` | `decision` | decisión de no conservar historia en archivos vigentes (la historia vive en git); durable |
| `atom-git-ignored-skill-trees-need-tracked-drift-guards` | `invariante` | deskops/tests/test_skill_cli_drift.py:1-13 guard rastreado exige que los SKILL.md ignorados (.pi/skills) coincidan con el CLI real |
| `atom-git-is-explanatory-surface-for-changes` | `decision` | el porqué de rastrear/ignorar todo cambio en git; durable |
| `atom-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache` | `codigo` | deskops/deskops/graph/self_reflection.py:19 DERIVED_ROOT y .gitignore:7 .sldb_cache |
| `atom-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas` | `codigo` | deskops/deskops/cli/commands/graph.py:103-104 planned_target e 'N missing, M informational (P planned_target)'; graph/checks.py:49 |
| `atom-implementation-feedback-refines-atoms` | `decision` | regla de proceso de cuando el atomo esta mal o la materializacion obsoleta; sin implementacion en codigo |
| `atom-inbox-is-coordination-intake` | `decision` | define el propósito del inbox frente al drawer (deskops/deskops/cli/registry.py:1020 lo toca solo en parte); decisión de uso durable |
| `atom-inbox-routes-external-needs-toward-work` | `decision` | propósito del inbox y su triage hacia drawer/issues/tareas; durable, no es un hecho que deskops/deskops/cli/registry.py:1020 exprese completo |
| `atom-init-y-sus-tests-asumen-la-resolucion-por-nombre-de-enlaces-de-sldb-3` | `codigo` | deskops/deskops/bootstrap.py:299 solo reemplaza enlace roto; tests/test_doctor_model_registration.py cubre los casos |
| `atom-instructional-text-makes-a-template-self-sufficient` | `decision` | el porqué de que el texto instructivo haga autosuficiente la plantilla; criterio de diseño sin código que lo imponga (deskops/deskops/models/board.py:54 solo lo aplica) |
| `atom-integrate-corre-la-suite-con-basetemp-propio-y-limpia-temporales-de-corridas-muertas` | `codigo` | deskops/deskops/integrate.py:217,238-239 owner.pid y --basetemp en PYTEST_ADDOPTS |
| `atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada` | `codigo` | deskops/deskops/integrate.py:306,439,481-504 modo pr, gh pr list/create --base --head |
| `atom-integrate-extiende-el-tip-a-head-cuando-despues-del-closeout-solo-hay-commits-de-desk` | `codigo` | deskops/deskops/integrate.py:268-285 extend_tip extiende a HEAD si solo hay commits de desk |
| `atom-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota` | `codigo` | deskops/deskops/integrate.py:268 extend_tip con remote_sha y merge-base --is-ancestor (:285) |
| `atom-integrate-no-empuja-por-separado-un-commit-de-codigo-que-no-avanza-rapido-sobre-el-remoto` | `codigo` | deskops/deskops/integrate.py:442-447 code_ff y mensaje 'código va con el tip' |
| `atom-integrate-saltea-el-push-del-sha-de-codigo-cuando-ya-es-ancestro-de-origin` | `codigo` | deskops/deskops/integrate.py:442-444 code_in_origin imprime 'código ya en origin' |
| `atom-kgdb-owns-relations-between-knowledge-surfaces` | `decision` | decisión de que las relaciones viven en el grafo sldb (existe sldb/src/sldb/api/graph/); KGDB retirado; durable |
| `atom-knowledge-graph-connects-desk-and-source-files` | `codigo` | el grafo ya enlaza desk con archivos fuente: deskops/deskops/graph/desk_graph.py:85 FileRule kind=source_file y :96 materializations target_identity |
| `atom-la-alerta-lost-de-doctor-nombra-el-remedio-real` | `codigo` | deskops/deskops/doctor_findings.py:269 mensaje 'restore it from git or close it with ...' sin desk update --apply |
| `atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc` | `codigo` | deskops/deskops/models/task_lifecycle.py:1-23 tabla de coherencia y validador en models/task.py:110 (model_validator) |
| `atom-la-copia-empaquetada-de-la-faq-deskops-data-faq-md-es-identica-a-docs-faq-md` | `invariante` | deskops/tests/test_packaging.py:57 test_packaged_faq_matches_the_human_copy exige copia idéntica deskops/data/faq.md = docs/faq.md; sin comando que la regenere |
| `atom-la-estructura-inicial-de-un-desk-se-declara-en-el-paquete-de-deskops-y-la-aplica-sldb` | `codigo` | deskops/deskops/doc_access.py:82,202 seed_desk y deskops/tests/test_scaffold_golden.py fijan la declaración en data/templates |
| `atom-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-y-deskops-owner-responde-el-dueno` | `codigo` | deskops/deskops/models/repository.py:32,64 owns_paths/owns_topics; cli/registry.py:1184; config.py:115 unowned_target |
| `atom-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal` | `codigo` | deskops/docs/operator-manual.md:266 ya dice que los cambios solo de desk van al checkout principal |
| `atom-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-redirige-por-entorno-y-los-tests-del-cli-no-tocan` | `codigo` | deskops/deskops/dispatch.py:31,646 DESKOPS_SCION_PYTEST_TMP; tests/test_dispatch.py:50 |
| `atom-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-gracias-a-una-fixture-autouse-que-limpia` | `codigo` | deskops/tests/conftest.py:66 fixture autouse _clear_global_caches |
| `atom-large-worktree-changes-need-explanatory-slices` | `decision` | regla de proceso (partir cambios grandes en rebanadas explicativas) con su porqué; durable |
| `atom-las-transiciones-del-ciclo-de-vida-de-una-tarea-son-aristas-con-efectos-declarados` | `codigo` | deskops/deskops/lifecycle.py:19-25 usa edges_holding y apply_effects de sldb.api |
| `atom-los-4-atomos-de-salud-del-desk-dejan-de-dar-ruido-estructural-en-sldb-stores-check` | `sin-clasificar` | relato de una correccion puntual ya hecha (4 atomos editados, commit sldb a1d5527f); el chequeo existe en sldb/src/sldb/api/stores/store_surroundings.py:63 pero el hecho afirmado es un estado pasado no verificable ni durable |
| `atom-los-agentes-despachados-corren-pytest-con-basetemp-en-tmp-del-contenedor-y-reap-limpia-dev-shm-pytes` | `codigo` | deskops/deskops/dispatch.py:384 (export PYTEST_ADDOPTS --basetemp=/tmp/pytest-<agente>) y :31,:646 (SCION_PYTEST_TMP limpiado por reap) |
| `atom-los-contenedores-de-scion-traen-pytest-xdist-y-la-suite-completa-corre-con-n-4` | `codigo` | deskops/pyproject.toml:23 (pytest-xdist>=3.5 en [dev]) y deskops/deskops/runtime/scion.py:888-890 (import xdist y -n 4) |
| `atom-los-gates-de-activación-de-cada-tipo-de-tarea-son-ruledoc-semilla` | `codigo` | deskops/deskops/data/rules/rule-activation-task-code.md (y -docs, -debug, -external, -aggregate): RuleDoc semilla por tipo, ya en el codigo |
| `atom-los-ids-que-deskops-deriva-de-un-título-se-pliegan-a-ascii-y-los-ids-existentes-con-tilde-siguen-val` | `codigo` | deskops/deskops/slugs.py:9 (ascii_slug), models/atom.py:41 (check_slug_id), doc_access.py:166 (slug_form), integrate.py:54 y services/closure.py:1978 (core.quotepath=false), dispatch.py:87 |
| `atom-los-rituales-context-review-y-phase-describen-la-revision-de-contexto-con-deskops-review-y-la-regla` | `codigo` | deskops/deskops/data/rules/rule-activation-task-*.md (gate de activacion) y deskops/deskops/services/review.py:646-666,911-919 (preflight/bundle/dispose, recibos); el atomo solo describe el texto de los rituales |
| `atom-main-docs-are-composed-materializations` | `invariante` | los docs principales no inventan conceptos duraderos sin atomo fuente: relacion entre doc, materializacion y atomos, vale sin trabajo abierto |
| `atom-materialization-contracts-bind-source-output-validation` | `codigo` | deskops/deskops/models/materialization.py:8 MaterializationContractDoc con source_atoms (:44) e intencion de transformacion (:55) |
| `atom-materialization-metadata-is-not-atom-content` | `decision` | el porque de no meter metadata de uso en el cuerpo del atomo (how_not); decision de modelo |
| `atom-materializations-are-projections-not-read-surfaces` | `decision` | principio de por que leer los atomos y no la proyeccion; no lo lee ningun codigo (relacionado con deskops/deskops/materializers/roles.py:70) y valdria sin trabajo en curso |
| `atom-materializations-declare-source-atoms` | `codigo` | deskops/deskops/models/materialization.py:23,44 campo source_atoms con reverso rev:source_atoms |
| `atom-message-is-the-cross-desk-transport-verb` | `codigo` | deskops/deskops/cli/registry.py:643,662,690 define deskops message send¦wake...; inbox aparece solo como vista/alias (registry.py:1932, main.py:43) |
| `atom-multi-surface-drift-is-a-core-workflow-failure-mode` | `decision` | porque el drift es un modo de falla central (por que los drift checks son superficies de revision); no es legible del codigo, no hay tarea abierta que lo contenga |
| `atom-networkx-is-first-graph-runtime` | `codigo` | sldb/src/sldb/store/graph/backend/networkx_backend.py y sldb/src/sldb/store/graph/analysis/lazy_networkx.py:11; deskops/deskops/graph/export.py:30 networkx_path_for_snapshot y graph/desk_graph.py:14 usa sldb.api |
| `atom-non-durable-notes-do-not-become-atoms` | `decision` | criterio de qué no es átomo; coherente con la definición en deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md y durable |
| `atom-operational-primitives-model` | `codigo` | deskops/deskops/lifecycle.py:5 y deskops/deskops/models/task_lifecycle.py:1-12,65-70 ya describen estados=rituales, transiciones=RelationDoc con verbo task_activates/task_completes |
| `atom-operations-py-es-una-fachada-y-cada-artefacto-declara-su-forma-en-su-modelo` | `codigo` | deskops/deskops/operations.py (307 lineas, fachada que delega), atributos de clase por modelo en deskops/deskops/models/*.py; implementado en CC30, el docstring de operations.py puede decirlo |
| `atom-orphan-artifacts-are-knowledge-system-failures` | `invariante` | todo artefacto debe tener relaciones en el grafo SLDB y materialización: regla entre varias piezas, sin comprobación hoy en deskops/deskops (rg orphan solo en domain_tree.py:129) |
| `atom-phase-closeout-reconciles-pills-and-next-work` | `decision` | regla de proceso de cierre de fase sin implementación que la codifique (rg phase closeout en deskops/deskops/services/closure.py solo 'phase' parcial); durable |
| `atom-phase-gates-prevent-agent-skipping` | `decision` | el porqué de las compuertas init/exec/test/closeout; durable |
| `atom-phases-are-dependency-layers-of-tasks` | `decision` | define qué es una fase (capa del DAG); durable aunque la tarea abierta task-el-board-declara-las-fases-del-dag la implementa |
| `atom-pills-are-reusable-across-tasks` | `decision` | postura sobre pills reutilizables; tensión con deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (pill nace y termina con un trabajo) y tarea abierta task-una-pill-declara-el-trabajo; revisar al tipar pills |
| `atom-pills-are-transient` | `decision` | pill temporal que se destila a átomo o se borra: coincide con el plan que-es-un-atomo-y-que-es-una-pill/README.md sección Pill; duplica atom-pills-carry/end-as |
| `atom-pills-carry-transitional-task-knowledge` | `decision` | definición de pill como contexto transitorio que se destila a átomo; coincide con plan README.md sección Pill; durable |
| `atom-pills-end-as-atoms-docs-or-deletion` | `decision` | destino de una pill (átomo, doc o borrado); coincide con plan README.md sección Pill y tarea abierta task-una-pill-declara-el-trabajo |
| `atom-pills-index-existing-and-bound-future-context` | `decision` | dos roles de la pill (puntero y contexto acotado); equivale a pill.pointer/pill.finding del plan README.md; durable |
| `atom-pills-reference-not-copy` | `decision` | regla de no copiar conocimiento a pills por el riesgo de deriva; durable |
| `atom-primitives-encode-operational-rules` | `codigo` | deskops/deskops/lifecycle.py:5 y models/task_lifecycle.py:9-12: reglas como RelationDoc con condición y efectos en spec/workflows/task_lifecycle.yaml; closeout_evidence_verified no aparece en deskops/deskops (rg sin resultados, detalle menor) |
| `atom-promotion-flattens-structured-source-sections-into-task-fields` | `codigo` | deskops/deskops/services/drawer.py:121 y deskops/deskops/doc_access.py:857 (from_drawer en el TaskDoc), deskops/deskops/runtime/task.py:36 |
| `atom-promotion-needs-explicit-criteria` | `decision` | por que no promover inbox/drawer sin criterios; razon de diseno permanente sin codigo que la exprese |
| `atom-protoatoms-are-free-atoms-captured-before-typing` | `codigo` | deskops/deskops/models/protoatom.py:15 (ProtoAtomDoc: titulo, contenido libre, tags) |
| `atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien` | `codigo` | deskops/deskops/queue.py:261-271 (imprime 'en espera: <id> ocupado (exit n)' y sigue con --all) |
| `atom-queue-run-deja-en-pending-un-trabajo-cuyo-codigo-de-salida-esta-en-retry-exit-codes` | `codigo` | deskops/deskops/queue.py:220 (code in spec.retry_exit_codes), deskops/deskops/config.py:28, deskops/deskops/data/templates/config.json:19 |
| `atom-raw-file-reads-flatten-knowledge-layers` | `decision` | advertencia de diseño: capas de conocimiento con roles distintos; durable |
| `atom-raw-signals-need-distillation-before-formalization` | `decision` | orden de proceso (destilar a atomo antes de formalizar) y su porque; no es legible del codigo |
| `atom-real-cli-surfaces-prove-workflow-behavior` | `decision` | regla de validación (probar por la CLI real); durable, no extraíble |
| `atom-reap-no-pierde-los-commits-del-ejecutor` | `codigo` | deskops/deskops/dispatch.py:257-262 (rev-list base..branch, nunca borra rama con punta fuera de base), :23,:246,:460-472 (EXIT_BUSY=3), :164 (worktree remove sin --force) |
| `atom-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-con-cualquier-idioma-de-git` | `codigo` | deskops/deskops/dispatch.py:84-85 (LC_ALL=C, LANGUAGE vacio) y :330 (_dirty_overwrite_hint 'would be overwritten') |
| `atom-rendered-diagrams-are-projections` | `decision` | los diagramas renderizados no son fuente canónica (coherente con AGENTS.md workspace); durable |
| `atom-repo-artifacts-need-atom-traceability` | `invariante` | todo artefacto debe trazarse a átomos vía relaciones sldb: regla entre piezas, sin comprobación hoy |
| `atom-repo-register-accepts-explicit-path-and-registry-errors-name-the-fix` | `codigo` | deskops/deskops/cli/registry.py:1177 (--path de deskops repo register) |
| `atom-reports-capture-evidence-and-next-decision-surface` | `decision` | por qué un reporte guarda intención, evidencia y siguiente decisión; durable |
| `atom-reports-carry-minimal-reproduction-evidence` | `decision` | criterio de qué debe llevar un reporte (repro, esperado, actual); durable |
| `atom-reverse-traceability-is-derived` | `codigo` | deskops/deskops/graph/atom_trace.py:1 "Derived reverse traceability for atoms" deriva los indices en vez de listas en el atomo |
| `atom-review-attestations-state-only-what-was-actually-read` | `decision` | regla de proceso de revision (no atestar lo no leido, corregir por supersesion fechada); no es legible del codigo, sigue valiendo sin trabajo abierto |
| `atom-review-status-muestra-incomplete-para-un-recibo-dispuesto-como-incomplete` | `codigo` | deskops/deskops/services/review.py:911-919 (state incomplete vs technical_failure) |
| `atom-review-status-preserves-current-dispositions` | `codigo` | deskops/deskops/services/review.py:880-906 (_state_for_key, prioridad accepted>rejected>pending, technical_failure en :666,919, hash sha256 en :880) |
| `atom-rituals-precede-routines` | `codigo` | deskops/deskops/lifecycle.py:3-5 y models/task_lifecycle.py:3: rituales como estados y RelationDoc tipadas con condición como transiciones |
| `atom-role-prompts-are-tracked-documents-agent-files-are-materializations` | `decision` | por que el prompt de rol es un documento trackeado y el archivo de agente es materializacion (deskops/deskops/materializers/roles.py:70); el porque no esta en el codigo |
| `atom-role-tool-boundaries-and-evidence-surface` | `invariante` | limites de herramientas por rol y superficie de evidencia runs/subagents/<run-dir>/ que cruzan roles, prompts y closeout (deskops/deskops/runtime/scion.py:556 solo materializa tools); no hay comprobacion unica en codigo |
| `atom-routine-based-task-execution` | `codigo` | deskops/deskops/lifecycle.py:5 y models/task_lifecycle.py:1-12: deskops advance recorre el grafo de rituales con condiciones --where |
| `atom-runtime-template-de-scion-escribe-image-resources-volumes-kubernetes-y-telemetry-en-scion-env-yaml-y` | `codigo` | deskops/deskops/runtime/scion.py:95,306-321,418 (scion-env.yaml, --config) y deskops/deskops/dispatch.py:582; cli/registry.py:2054 (--executor-role) |
| `atom-scion-coordinator-progresses-authorized-work` | `codigo` | deskops/deskops/runtime/scion.py:647-649,692,713 el prompt del coordinador ya contiene activity vs phase, un ejecutor por repo, tester independiente y prohibición de git add -A |
| `atom-se-borra-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph` | `codigo` | rg LEGACY_FIELD¦scaffold_desk¦ensure_lifecycle_graph en deskops/deskops no da coincidencias: el borrado ya esta en el codigo |
| `atom-se-borro-el-camino-legacy-de-deskops-message-sin-subcomando-es-un-error-de-uso` | `codigo` | deskops/deskops/cli/commands/message.py:39 (deskops message solo es error de uso rc 2); rg _run_legacy sin definicion |
| `atom-self-generating-spec-derived-cli` | `codigo` | deskops/deskops/doc_access.py:117 ARTIFACT_SUBJECTS y operations.py:21 derivan add/list/show/edit de los modelos registrados |
| `atom-self-reflection-is-a-feedback-loop` | `codigo` | deskops/deskops/graph/self_reflection.py:14-25 reporte de self reflection con ATOM_REFERENCE_ROLES y SOURCE_LINK_ROLES ya implementa el ciclo |
| `atom-separar-procedencia-exige-comparar-todas-las-columnas-contra-la-versión-previa` | `decision` | leccion de proceso de revision (comparar columna a columna al corregir atribucion); no esta en el codigo y vale sin trabajo en curso |
| `atom-sin-dueno-lo-que-no-tiene-dueno-en-sldb-1-va-al-inbox-de-deskops` | `contexto-trabajo` | acuerdo provisional hasta que Governance (repo-governance) este en el registro de repos, pendiente de JP: deskops/desk/tasks/task-governance-e-g-other-repo.md y tareas task-governance-* abiertas |
| `atom-sldb-extraction-reads-values-relative-to-the-template-s-own-text` | `codigo` | sldb/src/sldb/core/template_extractor.py:7 (recetas marcador+texto alrededor) y sldb/src/sldb/core/data_extractor.py:8,72 (DataExtractor las usa) |
| `atom-sldb-is-read-write-edit-surface` | `decision` | Afirma la superficie preferida (leer/escribir/editar docs modelados) como postura de diseno; ningun modulo la afirma por si solo (deskops/AGENTS.md y desk usan sldb como puerta unica, AGENTS.md raiz "one door"); sigue valiendo sin trabajo abierto |
| `atom-sldb-semantics-are-graph-inputs` | `codigo` | deskops/deskops/graph/desk_graph.py:14-17 importa sldb.api.edges.project_graph (DocumentNode, DocumentSurface...) en vez de un grafo propio |
| `atom-sldb-template-markers-declare-where-each-field-lives` | `codigo` | sldb/src/sldb/core/renderer_engine/base.py:41 (optrev None sin rastro), sldb/src/sldb/core/data_extractor.py:72 y sldb/src/sldb/examples/reference_bundle/guide_model.py:51-56 (rev/optrev/list/dict/render) |
| `atom-source-file-relations-make-knowledge-actionable` | `decision` | el porque (why) de enlazar conocimiento con archivos fuente; la mecanica esta en deskops/deskops/graph/desk_graph.py:85-96 pero la afirmacion es de valor |
| `atom-spec-driven-artifact-architecture` | `no-se-sostiene` | Dice que YAML de artefacto da id patterns/status/tags, pero hoy viven en la clase del modelo: deskops/deskops/models/board.py:19-26 (__artifact__, "formerly one YAML spec per artifact"); solo queda deskops/spec/workflows/task_lifecycle.yaml |
| `atom-spec-fields-compile-into-model-fields` | `no-se-sostiene` | No hay YAML de vocabulario de campos: deskops/deskops/specs/ solo contiene __init__.py y compiler.py y los campos viven en los modelos (deskops/deskops/models/board.py:19-26) |
| `atom-spec-to-visualization-pipeline` | `no-se-sostiene` | deskops.specs.mermaid no existe (deskops/deskops/specs/ solo tiene compiler.py; rg mermaid no lo halla ahi); solo queda el mermaid del ciclo de vida: deskops/deskops/workflow/next_actions.py:23 y --diagram en cli/registry.py:451 |
| `atom-spec2viz-mirrors-sldb-for-diagrams` | `no-se-sostiene` | spec2viz esta retirado y continua como specIR (AGENTS.md:5 del workspace); el paralelo spec2viz/sldb ya no describe una pieza vigente |
| `atom-specs-formalize-atoms-as-contracts` | `decision` | papel de las specs frente a los atomos (esquemas, estados, restricciones); decision de modelo sin codigo que la fije |
| `atom-stale-state-causes-agent-hallucination` | `decision` | por que el espacio solo debe tener estado activo (legacy y archivos sin trackear degradan a los agentes); principio no legible del codigo |
| `atom-subagent-runs-are-linked-to-session-logs-by-hash` | `invariante` | regla entre dispatcher, result-summary.md y session.jsonl (run_id, session_sha256); el campo aparece en deskops/deskops/models/run.py y services/closure.py pero la regla que cruza las piezas no la afirma una sola |
| `atom-task-board-phases` | `codigo` | La fase es objeto local del board (no documento): deskops/deskops/models/board.py:17-23 (class Phase con tasks e integration dentro de BoardDoc) |
| `atom-task-bundles-are-tracked-in-the-store-at-creation-time` | `codigo` | deskops/deskops/doc_access.py:146 (artefactos trackeados al crearse) y :245 (desk_transaction con rollback); deskops/deskops/workspace.py:784 usa track_document_file |
| `atom-task-closeout-checks-pill-knowledge-graduation` | `codigo` | Regla alerta (no gate duro) que exige referencia a AtomDoc si hay pills: deskops/deskops/data/rules/rule-closeout-alert-pill-graduation.md:3-6 (condition "not nonempty(pills) or any(references: model <= AtomDoc)", severity alert) |
| `atom-task-lifecycle-is-cli-runnable-end-to-end` | `invariante` | Exige coherencia entre docs, grafo de ciclo y automatizacion via CLI real; la comprueba un test entre varias piezas: deskops/tests/test_lifecycle_end_to_end.py y test_lifecycle_graph.py; ningun modulo lo afirma solo |
| `atom-tasks-enable-zero-context-subagents` | `decision` | Explica el porque del diseno de tareas (bundle explicito para subagente sin contexto); no lo extrae ni lo dice el codigo; vale sin trabajo abierto |
| `atom-templates-are-defined-as-model-strings` | `codigo` | deskops/deskops/models/atom.py:97 (__template__ multilinea en el modelo, deskops/models/*.py) |
| `atom-the-deskops-ui-reads-the-desk-only-through-deskops-view-and-writes-only-through-deskops-operations` | `invariante` | contrato UI-view-operations: deskops/deskops/cli/commands/view.py:1 (vista de solo lectura, contrato docs/deskops-ui.md) y cli/registry.py:1903; la regla de que la UI no lee desk/ directo cruza UI y deskops |
| `atom-toda-escritura-de-deskops-pasa-por-la-transacción-de-sldb` | `codigo` | deskops/deskops/doc_access.py:10-12,154,245 (desk_transaction, expected_source_hash, rollback de toda la transaccion) |
| `atom-todo-sustantivo-de-primer-nivel-del-cli-de-deskops-está-clasificado-una-sola-vez-en-su-gramática` | `codigo` | deskops/tests/test_cli_grammar.py:15 (TOP_LEVEL_GRAMMAR) y :58 (cada sustantivo clasificado una vez, el test lo hace cumplir) |
| `atom-typing-a-protoatom-keeps-a-redirect-stub` | `codigo` | deskops/deskops/domain_tree.py:7,15,119 (redirect stub con typed_as) |
| `atom-un-archivo-de-codigo-cita-los-atomos-que-implementa-y-deskops-atoms-citations-lo-comprueba` | `codigo` | deskops/deskops/services/atoms.py:77-105 (CITED_BY, bloque Atoms: del docstring, citas rotas) |
| `atom-un-cambio-de-contrato-de-un-modelo-se-registra-a-propósito-en-el-snapshot-y-en-el-store` | `invariante` | deskops/tests/test_model_contract_snapshot.py:11-13 (fixture model_contract_hashes.json solo se actualiza junto con la migracion de stores y el CHANGELOG); regla entre fixture, stores y changelog |
| `atom-un-dispatch-start-que-falla-antes-de-que-el-agente-arranque-no-gasta-intento` | `codigo` | deskops/deskops/dispatch.py:30 (FAILED_PHASES) y el deshacer del lanzamiento; probado en deskops/tests/test_dispatch.py |
| `atom-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-ya-presentes-en-origin` | `codigo` | deskops/deskops/integrate.py:327,338,345-346 (_resolve_failed mueve a done los integrate fallidos cuyo commit ya esta en el remoto) |
| `atom-un-límite-de-intentos-no-autoriza-aceptar-una-contradicción` | `decision` | regla de proceso de revision (no aceptar una contradiccion por agotar intentos; aclarar o descomponer el brief); no legible del codigo |
| `atom-un-pass-focal-no-prueba-el-resto-del-artefacto` | `decision` | regla de proceso del Tester (cobertura por bytes leidos, casos WS09/WS11); no legible del codigo |
| `atom-un-repo-con-tests-en-otro-lenguaje-declara-su-evidencia-de-closeout-con-un-test-py-que-corre-la-suit` | `codigo` | deskops/deskops/testing/foreign_suites.py:19-20,43 (VITEST, GO_TEST, run_foreign_suite); la decision de JP 2026-11-16 es el porque pero el mecanismo esta en el codigo |
| `atom-un-solo-vocabulario-de-tags-semanticos-en-deskops-resuelto-por-el-store-semantico-de-sldb` | `no-se-sostiene` | deskops/deskops/models/task.py:49 da board.tareas pero rg 'tareas.ui' y '\bui\b' en deskops/deskops/models y tag_vocabulary.py no hallan la semantica hija board.tareas.ui afirmada |
| `atom-una-disposicion-lee-toda-la-salida-del-revisor` | `decision` | leccion de proceso (WS12/WS34: la disposicion debe leer reformulacion, dry-run y atribuciones); no legible del codigo |
| `atom-una-invariante-de-un-solo-documento-vive-como-validador-de-su-modelo` | `decision` | principio del dueño DK6 sobre donde viven las invariantes; la implementacion esta en deskops/deskops/models/atom.py:41 y models/task.py:185 pero el porque (validador del modelo, no chequeo CLI) no se lee del codigo |
| `atom-una-nota-del-inbox-no-va-al-drawer-la-skill-el-ritual-drawer-triage-la-ayuda-de-promote-y-los-docs-l` | `codigo` | la ayuda de promote ya lo dice: deskops/deskops/cli/registry.py:1020 ("Drawer items become tasks only by authoring them with deskops add task"); el resto son materializations en desk/materializations |
| `atom-unwritten-knowledge-belongs-in-atoms-or-materializations` | `decision` | Criterio de donde capturar conocimiento no escrito (atomo vs materializacion): es el porque de una practica, no esta en codigo (CLOSEOUT_EVIDENCE_VOCABULARY solo lista tipos: deskops/deskops/services/closeout_gates.py:27-31) |
| `atom-upstream-routing-needs-convenient-command` | `codigo` | El comando existe: deskops/deskops/cli/registry.py:662 (path message send) y cli/commands/message.py:55; el motivo es solo racionalizacion del comando |
| `atom-used-source-artifacts-are-deleted` | `codigo` | promote inbox-to-drawer-task borra la nota: deskops/deskops/services/drawer.py:129,174 (source.unlink); from_drawer se conserva y bloquea borrado sin --force: services/drawer.py:121-127,194,221 |
| `atom-work-is-board-routed-to-preserve-intent` | `decision` | Justifica por que el trabajo se enruta por board (obligaciones, contexto, ritual de cierre); el porque no esta en el codigo (BoardDoc solo declara tasks/pills/rituals: deskops/deskops/models/board.py:30) |
| `atom-workflow-role-model-routing` | `codigo` | modelos ya declarados en deskops/desk/roles/deskops-supervisor.md:14, deskops-executor.md:8-10, deskops-tester.md:9-11 |
| `atom-workflow-surfaces-have-operational-lifetimes` | `decision` | Clasificacion conceptual de superficies por vida (active/deferred/durable/generated/transient), solo parcialmente reflejada en codigo (deskops/deskops/models/task_lifecycle.py:49-53 DRAWER_STATUSES); es criterio de diseno durable |
| `atom-workflow-vocabulary-separates-knowledge-and-work` | `decision` | Explica por que el vocabulario separa conocimiento, contexto transitorio, trabajo, reglas y proyecciones; razon de modelado, no legible de un solo modulo |

### deskops: pills (29)

| id | veredicto | motivo |
|---|---|---|
| `pill-001` | `codigo` | deskops/deskops/services/closure.py:3-7 documenta que todo cierre termina en `deskops closeout commit` con exactamente un commit de cierre |
| `pill-005` | `decision` | pill sobre usar un subagente fresco por tarea (porqué: reducir sobrecarga de contexto); es práctica de proceso sin código que la imponga (rg en deskops/deskops no halla gate); respaldada por deskops/desk/rituals/execution.md y por runtime/scion.py |
| `pill-006` | `codigo` | deskops/deskops/sldb_layout.py:1-7 detecta el layout .sldb viejo (runtime/ y journal dentro de .sldb/) y ignora .sldb/core y .sldb/runtime; la separación core/runtime/.config ya está en el código |
| `pill-007` | `invariante` | todas las tareas pasan por compuertas de entrada/handoff/testing/closeout y las fases abren/cierran explícitas; regla entre piezas (tarea, board, rituales deskops/desk/rituals/{execution,testing,closeout,phase}.md) que ningún código solo afirma; sigue valiendo sin trabajo abierto |
| `pill-008` | `codigo` | deskops/deskops/graph/export.py:4,91 valida con sldb.api.graph.snapshot.GraphSnapshot y deskops/deskops/cli/commands/graph.py:41-42 usa snapshot_load y save_graph de sldb; sin dependencia kgdb |
| `pill-009` | `codigo` | deskops/deskops/graph/desk_graph.py:38,85,96,156 declara nodos source_file (FileRule kind=source_file, SOURCE_FILE_NODE_EXTRACTOR) conectados a artefactos del desk |
| `pill-010` | `codigo` | deskops/deskops/graph/export.py:4 escribe el snapshot en una ruta ignorada de runtime (docstring: snapshot en ignored runtime); la política ya está implementada |
| `pill-011` | `invariante` | self-reflection debe producir átomos/issues de alta señal y no generar a granel; regla de comportamiento entre deskops/deskops/graph/self_reflection.py y el flujo de átomos/issues, sin comprobación que la fuerce; vale sin trabajo abierto |
| `pill-012` | `codigo` | deskops/deskops/doc_access.py:11,249,360-368,455-482 envuelve la creación de documentos en transacción que restaura todo ante fallo (unlink de archivos nuevos) |
| `pill-atom-lifecycle-preserves-provenance-and-materialization-links` | `invariante` | las operaciones create/split/merge/delete de átomos (deskops/deskops/cli/commands/atoms.py:85,96,118; services/atoms.py:913-924 detecta citas rotas/huérfanas) deben preservar provenance y enlaces de materialización; regla entre varias piezas, parcialmente comprobada |
| `pill-board-routed-pills-stay-minimal-and-reusable` | `decision` | criterio de curaduría del set de pills enrutadas por el board (porqué mantenerlo mínimo para no heredar contexto obsoleto); ningún código lo impone (rg en deskops/deskops sin gate de tamaño) |
| `pill-canonical-desk-identity-enables-horizontal-routing` | `codigo` | deskops/deskops/identity.py y deskops/deskops/config.py:17-23,93-94 ya declaran identidad canónica de proyecto por desk y doc_access.list_repo_task_routes (operations.py:~140) resuelve desks hermanos desde el registro |
| `pill-cli-gaps-become-tracked-work` | `decision` | práctica de proceso: los huecos hallados al validar el CLI se vuelven tareas/issues/inbox, no memoria de chat; el porqué no está en ningún código (cli/commands/issue.py solo ofrece el mecanismo) |
| `pill-closeout-knowledge-gates-require-traceable-evidence` | `codigo` | deskops/deskops/services/closure.py:3-7 y deskops/deskops/graph/checks.py, graph/atom_trace.py ya implementan los gates de closeout sobre átomos, materializaciones, enlaces de grafo y commit |
| `pill-cross-desk-inbox-needs-delivery-verification-and-follow-up` | `docstring` | deskops/deskops/cli/commands/message.py hace mensajería entre desks (repo-targeted vía list_repo_task_routes, operations.py) pero la verificación de entrega/seguimiento que la pill exige no está dicha en un docstring; sin verificación de entrega localizada |
| `pill-doctor-separates-desk-repair-from-sldb-health` | `codigo` | deskops/deskops/cli/commands/doctor.py:177 delega la salud del store a `python -m sldb stores check`; deskops/deskops/doctor_findings.py:1 separa errores y alertas del desk |
| `pill-drift-checks-are-review-surfaces-not-mutators` | `codigo` | deskops/deskops/cli/commands/drift.py y deskops/deskops/models/review.py emiten hallazgos de revisión (review) sin reescribir átomos/docs; los cambios pasan por promote.py explícito |
| `pill-durable-pill-knowledge-graduates-to-atoms-at-closeout` | `decision` | el porqué: el cierre debe destilar lo durable de las pills a átomos antes de borrarlas; hoy solo lo lleva el ritual deskops/desk/rituals/ritual-knowledge-distillation-pass.md y deskops/desk/rituals/closeout.md, sin gate en código; regla que valdría sin trabajo abierto |
| `pill-legacy-desk-formats-need-explicit-adaptation` | `codigo` | deskops/deskops/workspace.py:19,108,127 clasifica el desk como absent/empty/legacy/current y doctor_findings.py:315-331 usa legacy_task_states para migración |
| `pill-list-surfaces-must-expose-malformed-docs` | `codigo` | deskops/deskops/workspace.py:127 marca legacy cuando hay superficies malformadas y doctor_findings.py las reporta; los malformados no se saltan en silencio |
| `pill-machine-readable-cli-output-needs-stable-contract` | `codigo` | deskops/deskops/cli/registry.py:114-115 declara OUTPUT_FORMAT_ARG y OUTPUT_FORMAT_YAML_ARG (--format text¦json¦yaml) para list/show; la prueba CLI está en deskops/tests |
| `pill-materialization-contracts-declare-source-intent-and-target` | `codigo` | deskops/deskops/models/materialization.py modela la materialización con fuente, intención y target_identity (graph/desk_graph.py:96 usa field=target_identity) |
| `pill-operational-cli-grammar-follows-spoken-workflow` | `decision` | criterio de diseño del CLI (porqué: nombres según el lenguaje del operador, no los módulos internos); deskops/deskops/cli/registry.py solo materializa el resultado, la intención no se lee del código |
| `pill-pattern-supervisor-playbook-buenas-tareas-bundle-contexto-cero-y-frontera-de-modelos` | `decision` | playbook de supervisión (bundle task+pills+atoms, ambiguity review, frontera desk vs producto) con porqués; proceso humano sin código que lo contenga (rg en deskops/deskops); parcialmente sustentado por deskops/desk/rituals/execution.md |
| `pill-phase-closeout-reconciles-pills-and-surfaces-next-work` | `decision` | el porqué del pase de cierre de fase (integración, reconciliar pills, siguiente fase); vive en deskops/desk/rituals/phase.md y deskops/deskops/cli/commands/view.py solo muestra fases; tarea abierta task-el-board-declara-las-fases-del-dag... (ready_for_testing) toca el mismo tema pero la pill es permanente |
| `pill-project-local-config-carries-version-and-sandbox-policy` | `codigo` | deskops/deskops/config.py:17-23,93-94 declara SandboxPolicy y VersionExpectations (desk_format, model_version) en la config por proyecto |
| `pill-ready-phases-prove-dependencies-and-non-overlap` | `invariante` | una fase lista exige dependencias satisfechas y cambios sin solapamiento entre tareas (deskops/desk/rituals/phase.md); regla entre varias piezas sin comprobación en código (rg overlap en deskops/deskops/workflow sin resultados); la tarea task-el-board-declara-las-fases-del-dag... podría darle regla |
| `pill-real-cli-surfaces-prove-operator-contracts` | `decision` | criterio de validación (porqué probar por el CLI real y no por objetos Python); no existe en código, aplicado en deskops/tests/test_cli.py y en las pruebas de CLI |
| `pill-zero-context-preflight-precedes-executor` | `decision` | práctica: un subagente contexto-cero reformula la TaskDoc antes del ejecutor; vive en deskops/desk/rituals/execution.md y deskops/desk/rituals/context-review.md, sin gate en deskops/deskops (rg preflight solo da runtime/scion.py) |

### sldb: átomos (113)

| id | veredicto | motivo |
|---|---|---|
| `atom-agregar-un-campo-con-default-a-un-modelo-no-invalida-los-documentos-existentes` | `codigo` | sldb/src/sldb/runtime/validation.py:20-24 (_without_absent_defaults descarta la clave ausente para que aplique el default; su docstring lo dice); prueba en sldb/tests/test_campo_con_default.py |
| `atom-apply-batch-con-dry-run-valida-un-lote-completo-sin-escribir-y-devuelve-lo-mismo-que-una-corrida-rea` | `codigo` | sldb/src/sldb/api/documents/apply_batch.py:36-40,60-63 (docstring de dry_run: prevalida bajo el lock, vuelve antes de la transacción, mismos errores) |
| `atom-apply-batch-devuelve-en-batchreport-inverse-el-lote-que-lo-deshace-con-guardas` | `codigo` | sldb/src/sldb/api/documents/batch_inverse.py:1-10 y apply_batch.py:42-45 describen inverse, las guardas por hash y el ConflictError |
| `atom-apply-batch-prevalida-y-escribe-bajo-el-cerrojo-del-store-y-rechaza-con-conflicterror-un-guarda-obso` | `codigo` | sldb/src/sldb/api/documents/apply_batch.py:51-58,60,73 (store_lock(wait=True) de la prevalidación a la última escritura; ConflictError en Raises) |
| `atom-cargar-un-store-por-la-api-pública-no-aborta-por-un-documento-inválido-on-invalid-skip-devuelve-los` | `codigo` | sldb/src/sldb/api/documents/runtime_documents.py:8-9,31,42 (on_invalid raise¦skip, RuntimeDocuments) y sldb/src/sldb/store/edge_index/edge_index.py:22 (problem_details) |
| `atom-check-edges-separa-el-stale-propio-del-de-los-stores-enlazados-por-el-store-dueno-del-nodo-no-por-la` | `codigo` | sldb/src/sldb/api/edges/check_edges.py:32-34,42-46 (el docstring de _is_linked dice que el dueño sale del nombre del enlace, no de contar ':') |
| `atom-cinco-archivos-de-0f91540d-se-partieron-para-cumplir-las-reglas-de-codigo-limpio` | `codigo` | informe de un refactor ya hecho: los archivos existen partidos y chicos (sldb/src/sldb/api/rules/rule_graph.py 117 líneas, api/stores/store_check.py 94, api/rules/rules_on_write.py 74, api/notations/component_spec_graph.py 67, store/diagnostics.py 101); no guarda nada que el código no muestre |
| `atom-con-el-extra-postgres-las-claves-del-ddl-de-postgres-se-leen-con-el-parser-real-de-postgres-pglast` | `codigo` | sldb/src/sldb/code/sql_pg_keys.py:1-12 (docstring: claves PK/FK/UNIQUE con pglast, references, nombres tal como están escritos, CHECK/EXCLUDE no son claves) |
| `atom-crear-un-documento-ya-fija-sus-anclas-a-documentos-create-document-pinnea-igual-que-save-document-pa` | `codigo` | sldb/src/sldb/api/documents/create_document.py:9,54,85 (pin_payload antes de validar, pin_provenance antes de escribir) |
| `atom-docs-list-marca-con-su-causa-los-documentos-que-docs-show-no-puede-resolver` | `codigo` | sldb/src/sldb/api/stores/unresolvable_documents.py:21-27 (model-not-importable y las demás causas, con docstring) |
| `atom-docs-track-reindex-re-indexa-un-documento-trackeado-validandolo-a-diferencia-de-force` | `codigo` | sldb/src/sldb/cli/parsers/docs1.py:30 (help de --reindex: valida como un track normal, a diferencia de --force, no junto a --force) |
| `atom-drop-disk-caches-vive-en-store-disk-caches-py-y-las-dos-caches-de-disco-ven-el-roster-de-cada-modelo` | `codigo` | sldb/src/sldb/store/disk_caches.py:9-17 (drop_disk_caches), store/edge_index/cache_keys.py:27-32 (roster_state), api/stores/build_store.py:19,57 (stores build la llama) |
| `atom-el-422-de-post-save-de-sldb-serve-devuelve-exc-errors-como-details` | `codigo` | sldb/src/sldb/cli/serve/save_routes.py:95-100 (el 422 lleva details = cause.errors(...) cuando pydantic rechaza) |
| `atom-el-conjunto-de-documentos-sucios-se-persiste-en-sldb` | `codigo` | sldb/src/sldb/store/documents_dirty_persist.py:1-4,15 (persiste el conjunto en .sldb_cache/documents_dirty.json); el resto del átomo es informe de tester/commit |
| `atom-el-contrato-completo-de-un-modelo-se-declara-y-edita-por-drafts-con-validacion-y-backfill` | `codigo` | sldb/src/sldb/cli/commands/models_validate.py:56-67 (--backfill llama promote_model_draft(backfill=True)), cli/serve/models_write_routes.py:37-42, core/exceptions/sldb_model_edit_error.py; descrito en docs/architecture/model-authoring.md |
| `atom-el-desk-puede-afirmar-lo-contrario-del-repo-y-nada-falla` | `invariante` | regla que sobrevive al trabajo: una afirmación del desk verificable contra el repo necesita un chequeo ejecutable; no se lee del código (deskops/sldb no comparan estado de task con repo) ni la extrae specIR; origen en runs/subagents/reconcile-legacy-retirement-20260929 |
| `atom-el-dueño-de-un-field-es-la-sección-del-template-que-lo-contiene-no-la-línea-donde-quedó-renderizado` | `codigo` | sldb/src/sldb/api/records/map_fields.py:29-39,43-85 (dueño = heading previo en el template; _correspond rechaza si hay más de una sección y los conteos difieren; docstrings lo explican); prueba tests/test_field_ownership.py |
| `atom-el-generador-del-golden-de-d2-se-retiro-de-runs-porque-importaba-spec2viz` | `decision` | porqué se borró gen_golden.py: confirmado ausente en sldb/runs/subagents/20261116-exec-oraculo-d2/ (solo README.md, board.txt…) y commit cfa6477b8 "D2: retira gen_golden.py (importaba spec2viz)"; no es legible del código |
| `atom-el-grafo-de-un-proyecto-se-declara-en-store-yaml-y-sldb-lo-sirve` | `codigo` | sldb/src/sldb/cli/parsers/graph_project.py:1,11-18 (graph project nodes¦edges¦missing), cli/serve/routes.py:75 (/project-graph/*), api/stores/store_declaration.py; docs/architecture/project-graph.md |
| `atom-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda` | `codigo` | sldb/src/sldb/api/documents/lossy_overwrite.py:19-36 (docstring: no bloquea si el texto bajo el heading, normalizado, está en rendered; _without_kept_content) |
| `atom-el-inventario-de-código-de-sldb-se-publica-como-hechos-de-fuente-y-cada-consumidor-los-proyecta` | `codigo` | sldb/src/sldb/selfdoc/python_scanner.py y cli/parsers/selfdoc.py (python-sync/python-check, grafo de fuente); contrato escrito en docs/architecture/code-docstring-indexing.spec.md:5-7 |
| `atom-el-path-guardado-de-un-modelo-es-una-pista-model-ref-es-la-identidad` | `docstring` | sldb/src/sldb/api/model_drafts/source_location.py:50-51 usa _recorded_path y si no _imported_path(model_ref); el docstring de _recorded_path (l.58) lo insinúa pero el de locate_model_source (l.34-46) no dice que path no es portable y model_ref es la identidad |
| `atom-el-rollback-de-una-transaccion-restaura-el-conjunto-sucio-persistido` | `codigo` | sldb/src/sldb/api/documents/transaction_state.py:13,32,72-74 (snapshot de documents_dirty.json y documents_dirty.reload tras forget_caches) |
| `atom-el-spec-de-componentes-desde-python-lee-solo-archivos-py-aunque-el-árbol-tenga-otros-lenguajes` | `codigo` | sldb/src/sldb/api/notations/component_spec_python.py:7,38-40 (find_files filtrado a .py; docstring: solo .py, no .ts/.js/.sql) |
| `atom-el-store-depende-del-resto-de-sldb-solo-por-costuras-y-un-test-lo-hace-cumplir` | `invariante` | sldb/tests/test_store_seams.py:5-16 impone SEAMS={exceptions.py, runtime_codec.py, model_contract.py}; es una regla entre capas (store vs core/models/runtime/api/cli) y el átomo aporta el porqué (store empaquetable aparte); task abierta relacionada: separar el store en paquete propio (decisión 6) |
| `atom-el-template-de-un-modelo-es-estable-sus-recetas-se-calculan-una-vez-no-en-cada-extract` | `codigo` | sldb/src/sldb/runtime/validation.py:73-76 (_recipes con lru_cache; docstring: el template es estable por modelo, se parte una vez) |
| `atom-en-el-código-de-docs-contains-es-el-operador-viejo-solo-en-contexto-de-predicado-solo-es-la-relación` | `codigo` | sldb/tests/store/test_where_retired.py:9-12,24 (docstring y regex PREDICATE_CONTAINS dicen exactamente esto) |
| `atom-fields-update-y-append-aceptan-string-y-format-e-inbox-reporta-por-stderr-y-no-escribe-sin-store` | `codigo` | sldb/src/sldb/cli/parsers/fields.py:33 (--string literal), cli/commands/inbox_show.py:10 (stderr), cli/commands/inbox_core.py:23-26 (error si no hay .sldb) |
| `atom-git-sabe-si-un-índice-quedó-atrás-o-no-coincide-con-nada-se-le-pregunta-antes-de-alarmar` | `codigo` | sldb/src/sldb/store/diagnostics_models/text_history.py:1-8 (docstring: stale / unmatched / orphan / undetermined según el historial git) |
| `atom-graph-path-con-explain-devuelve-por-cada-tramo-las-aristas-que-lo-justifican-y-su-procedencia` | `codigo` | sldb/src/sldb/api/graph/analyze.py:25-36 (docstring de graph_path/graph_paths con explain: {path, steps:[{source,target,edges}]}) |
| `atom-incomplete-se-retira-del-lenguaje-de-predicados-de-sldb` | `decision` | por qué se retiró incomplete (inalcanzable con datos reales): sldb/docs/architecture/rules-language.md:182-187 lo registra como nota; en sldb/src no queda ninguna emisión de incomplete (rg solo halla usos de la palabra en otro sentido); el código no guarda el porqué |
| `atom-la-arquitectura-de-spec2viz-en-sldb-ya-no-nombra-a-spec2viz-como-consumidor-ni-lo-invoca` | `no-se-sostiene` | sldb/contracts/identity.toml:299 ya no lista spec2viz pero identity.toml:370 aún lo nombra como consumidor de producción, y docs/architecture/code-docstring-indexing.spec.md:5,7,18 y code-docstring-indexing-handoff.md:37 siguen nombrando a spec2viz (from-graph); solo python-ast.md quedó limpio |
| `atom-la-cabecera-de-rules-language-md-describe-la-semantica-bivaluada` | `codigo` | sldb/docs/architecture/rules-language.md:5 ya dice "semántica bivaluada" y rg trivaluad en docs/ y knowledge/ no halla nada; es la propia doc, no añade conocimiento |
| `atom-la-capa-runtime-edges-se-queda-es-donde-vive-la-semántica-del-grafo-que-el-snapshot-no-tiene` | `decision` | por qué se canceló el retiro (2026-10-18): docs/architecture/edges-retirement-plan.md:3-8; ojo: la carpeta sldb/src/sldb/runtime/edges ya no existe, la lógica vive ahora en src/sldb/store/edge_index/resolve.py y compose.py |
| `atom-la-escritura-por-campos-rechaza-solo-los-headings-o-claves-que-perderia` | `codigo` | sldb/src/sldb/api/documents/lossy_overwrite.py:19-28,39-43 (docstring y _lost_headings por multiconjunto con Counter; _refuse_lost_keys) |
| `atom-la-estructura-inicial-de-un-store-se-declara-como-carpetas-y-semillas` | `codigo` | sldb/src/sldb/api/stores/scaffold_store.py:18 y cli/parsers/stores.py:93-94 (scaffold [--apply]); contrato en docs/architecture/store-declaration.md |
| `atom-la-paridad-de-d2-con-spec2viz-se-comprueba-contra-un-golden-congelado-no-contra-spec2viz-en-vivo` | `codigo` | sldb/tests/notations/test_component_spec_python.py:3-5,20,50 (docstring: golden congelado component_spec_python_spec2viz.json, test sin importar spec2viz) |
| `atom-la-prueba-surface-dev-astryx-probe-responde-las-dudas-del-adr-de-surface-sobre-react-flow-y-codemirr` | `codigo` | existe sldb/surface/dev/astryx-probe/ con RESULTADO.md, package.json, src/, tests/ (el átomo solo describe su contenido); el ADR es docs/architecture/surface-is-an-editor-contract.md |
| `atom-la-puerta-de-identidad-clasifica-workbench-demo-como-store-de-demo` | `codigo` | sldb/contracts/identity.toml:391-395 ([[foreign]] path="workbench_demo", store de demo del workbench de surface) |
| `atom-la-tabla-de-la-sección-10-del-manual-es-la-lista-de-rutas-http-de-sldb-serve-y-un-test-la-compara-co` | `invariante` | sldb/tests/test_serve.py:1660 test_user_manual_lists_every_serve_route compara docs/user-manual.md §10 con las rutas de src/sldb/cli/serve/ en ambas direcciones: regla entre dos piezas (manual y código) con su comprobación |
| `atom-la-transacción-restaura-el-dirty-set-de-reglas-en-el-rollback` | `codigo` | sldb/src/sldb/api/documents/transaction_state.py:11,32 (remember copia rules_dir/dirty.json y documents_dirty al abrir la transacción, restaurado en el rollback) |
| `atom-la-transclusion-por-campo-y-los-bloques-ricos-de-diagramas-y-tablas-se-resuelven-en-document-segment` | `codigo` | sldb/src/sldb/api/segments/field_ref_resolver.py, segments/build_document_segments.py y segments/segment_enrichment.py:42-46 (resolve_view / evaluate_projection_view); docs/architecture/segments-and-transclusion.md |
| `atom-label-key-de-sldb-api-matching-normaliza-igual-que-normkey-del-catálogo-el-guion-bajo-separa-palabra` | `codigo` | sldb/src/sldb/api/matching/atom_keys.py:18-20 (re.sub(r"[\W_]+", " ", ...), docstring explica el guion bajo como separador) |
| `atom-las-caches-de-disco-de-sldb-ven-una-reescritura-in-place-de-un-documento-y-stores-build-las-invalida` | `no-se-sostiene` | afirma drop_disk_caches en store/layout.py pero hoy vive en sldb/src/sldb/store/disk_caches.py:12 (layout.py ya no la define); el resto (roster_state en store/edge_index/composed_disk.py:48 y cache_keys.py:27, build_store.py:57) sí se sostiene |
| `atom-las-pruebas-de-notaciones-paletas-vista-resuelta-y-viewdoc-que-tenía-spec2viz-viven-en-sldb-y-solo-i` | `codigo` | existen los 7 sldb/tests/notations/test_ported_from_spec2viz_*.py (docstring de test_ported_from_spec2viz_notation.py:1-6 lista los casos no portados) y fixtures en tests/notations/fixtures/docs/architecture/ |
| `atom-las-referencias-entrantes-de-un-documento-se-consultan-y-se-reescriben-en-sldb-todo-o-nada` | `codigo` | sldb/src/sldb/api/edges/referrers.py:1-12 y rewrite_references.py:31-36 describen referrers/rewrite_references, excluded/skipped (rewrite_report.py:14) |
| `atom-las-vistas-de-notacion-y-proyeccion-se-resuelven-en-sldb-api-notations-por-cli-y-por-sldb-serve` | `codigo` | sldb/src/sldb/cli/serve/notations_routes.py:22-28 y routes.py:80-87 exponen /notations y /views/projection*; resolve_view.py:32, resolve_documents.py:44, projection_view.py:41 |
| `atom-lectura-de-surface-muestra-el-nombre-del-store-servido-y-no-queda-alias-businessname` | `codigo` | sldb/surface/src/app/WorkbenchShell.tsx:54-59,189 (storeInfo -> storeTitle, cae a Documentos, wiki-index.ts:123); rg businessName en surface/src sin resultados |
| `atom-list-views-no-compone-el-índice-federado-y-compose-edge-index-compone-una-sola-vez-por-clave` | `codigo` | sldb/src/sldb/api/views/list_views.py:1-6 (view_nodes sin componer federado) y store/edge_index/compose_lock.py:1-2,13 + compose.py:55 |
| `atom-lo-que-el-código-dice-de-sí-mismo-se-publica-con-lo-que-no-se-pudo-probar-a-la-vista` | `codigo` | sldb/src/sldb/selfdoc/python_source_scan.py:38-40 (undeclared/unexplained), selfdoc/python_shadowing.py:5 (shadowed_at), selfdoc/report.py:50 y cli/commands/selfdoc_python.py:33 (purpose_conflicts) |
| `atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo` | `codigo` | sldb/src/sldb/store/model_node.py:17-37 (stamp_model_node relee family y contrato; docstring de _declared_family explica el congelado) |
| `atom-los-comandos-cli-de-stores-instalan-solos-el-merge-driver-de-sldb-y-stores-check-avisa-si-falta` | `codigo` | sldb/src/sldb/api/stores/ensure_merge_driver.py:1-4,17-25 y llamadas en cli/commands/store_init.py:31, stores_scaffold.py:18, stores_build.py:59; merge_driver_finding en store_surroundings.py:97 |
| `atom-los-facts-de-python-traen-bases-decoradores-llamadas-y-asignaciones-genéricas-que-specir-interpreta` | `codigo` | sldb/src/sldb/code/py_calls.py:1-5,62-65 (bases/extends/decorators), code/py_statements.py:4,26,55 (assignment/call) y code/scan.py:3 |
| `atom-los-facts-de-ts-y-js-traen-sus-llamadas-con-nombre-canónico-url-literal-y-handlers-jsx` | `codigo` | sldb/src/sldb/code/lang_ts.py:5,56-63 (calls canonical, handlers) y code/ts_jsx.py:7, ts_loose.py:1 |
| `atom-los-hallazgos-builtin-tag-namespace-traen-un-fix-accionable` | `codigo` | sldb/src/sldb/api/rules/builtin_tag_findings.py:45-57 (_finding/_fix arman el fix por namespace) |
| `atom-los-imports-anidados-de-un-módulo-python-son-un-hecho-aparte-de-los-de-nivel-superior-y-el-spec-de-c` | `codigo` | sldb/src/sldb/code/imports.py:1-2,26, code/py_module.py:16-19 (imports vs nested_imports) y api/notations/component_spec_python.py:65 (arista imports) |
| `atom-los-modelos-de-vocabulario-visual-viven-en-sldb-y-spec2viz-sldb-models-es-un-alias` | `codigo` | sldb/src/sldb/api/model_registry/model_reference.py:18 (spec2viz.sldb_models -> sldb.models.notation_models) y models/notation_models.py, models/notation/*.py |
| `atom-los-namespaces-de-tags-se-declaran-en-el-store-y-un-prefijo-necesita-su-documento-ancla` | `codigo` | sldb/src/sldb/api/rules/builtin_tag_rules.py:1-10 y api/stores/tag_namespace.py:1; replace_text en api/documents/replace_text.py:34 |
| `atom-notations-validate-respeta-las-reglas-de-codigo-limpio` | `codigo` | sldb/tests/test_clean_code_rules.py impone el limite de logica; funciones en sldb/src/sldb/cli/commands/notations_validate.py:103 y notations_validate_store.py:38 (nota de refactor ya cumplida, no pide mas) |
| `atom-plan-del-drawer-grafo-datalog-daemon-motor-datalog-duenio-de-las-aristas-daemon-residente-y-decision` | `contexto-trabajo` | tareas abiertas P1-P4 en sldb/desk/tasks/task-decision-para-jp-p1-que-motor-datalog-embebido-usa-sldb-cozo-datalevin-u-otro.md (status draft, y p2-p4) y plan desk/drawer/plans/grafo-datalog-daemon/ |
| `atom-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas` | `codigo` | sldb/src/sldb/api/matching/atoms_by_view.py:20-21 y 28-29 (docstring y rama atoms_dir para todas las vistas) |
| `atom-read-store-dice-store-not-found-si-el-sldb-no-existe-y-store-not-prepared-si-le-falta-el-índice` | `codigo` | sldb/src/sldb/api/stores/read_store.py:17-18,48-49 (NOT_FOUND / NOT_PREPARED y su docstring) |
| `atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent` | `codigo` | sldb/src/sldb/api/edges/referrers.py:55 y rewrite_references.py:30-36 (parametros graph y excluded_sources documentados) |
| `atom-rev-y-optrev-con-none-renderizan-null-y-se-pueden-reescribir` | `codigo` | sldb/tests/test_rev_optrev_none.py:1-2 prueba que optrev None se re-fija con fields update (comportamiento fijado por test; rev en guide_model.py:51-56) |
| `atom-save-document-payload-devuelve-las-alertas-on-write-de-la-escritura-y-la-regla-ve-las-aristas-del-pa` | `codigo` | sldb/src/sldb/api/documents/payload_save.py:16,29,44-45 y document_reference.py:17 (alerts de on_write en DocumentReference); payload_save_steps.py:77 |
| `atom-scan-heading-bodies-cumple-la-regla-de-codigo-limpio` | `codigo` | sldb/src/sldb/api/documents/heading_scan.py:31-43 (funcion corta que devuelve cuerpos por heading; limite impuesto por tests/test_clean_code_rules.py) |
| `atom-se-retiraron-las-cascaras-vacias-de-la-api-y-los-re-exports-sin-uso` | `codigo` | sldb/src/sldb/models/field_schema/descriptor.py:3 dice que sldb.api.schema.field_descriptor ya no existe (rg field_descriptor no lo halla en api/schema); resto es informe de tester de un commit pasado |
| `atom-select-documents-guarda-en-disco-las-filas-de-documentos-para-que-una-vista-no-reparsee-los-shards-e` | `codigo` | sldb/src/sldb/store/query_engine/document_rows_disk.py:1-6 (cache en disco con clave por stats) y store/io/utils.py:26 (CSafeLoader) |
| `atom-selfdoc-check-compara-el-arbol-de-argparse-con-current-cli-tree-md` | `codigo` | sldb/src/sldb/selfdoc/report_findings.py:28-29 (cli-tree-missing/cli-tree-stale como error) y report.py:52 |
| `atom-selfdoc-normaliza-el-required-de-los-posicionales-nargs-para-que-la-referencia-no-dependa-del-parche` | `codigo` | sldb/src/sldb/selfdoc/arguments.py:10-18 (_required normaliza nargs='*', docstring explica el parche de 3.12) |
| `atom-sldb-api-code-code-facts-es-la-api-pública-de-los-facts-de-código` | `codigo` | sldb/src/sldb/api/code/code_facts.py:15 (code_facts(root, paths) -> {facts, skipped}); frontera consumida por specIR |
| `atom-sldb-api-template-anchors-dice-por-campo-de-un-modelo-el-párrafo-literal-de-la-plantilla-que-ancla-s` | `codigo` | sldb/src/sldb/api/model_registry/template_anchors.py:18-25 (docstring describe el parrafo ancla por campo) |
| `atom-sldb-code-lee-ddl-de-postgres-y-migraciones-de-sqlmigrate-como-hechos-de-tablas-columnas-vistas-e-ín` | `codigo` | sldb/src/sldb/code/lang_sql.py:1-8 (hechos module/table/column/view/index, nombres sin comillas, sufijos ~N) |
| `atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos` | `codigo` | sldb/src/sldb/code/scan.py:1 (.ts/.tsx/.js/.jsx a lang_ts), code/files.py:10,14 (node_modules no se recorre), code/lang_ts.py:42 |
| `atom-sldb-evaluates-declared-rules-consumers-author-them` | `decision` | principio de diseno (decision del dueno D1 2026-11-04, desk/drawer/plans/grafo-operable/decisiones.md): sldb evalua reglas y los consumidores las escriben; no se lee de un solo codigo (evaluador en sldb/src/sldb/api/rules/, reglas fuera) |
| `atom-sldb-links-extrae-los-enlaces-del-árbol-de-markdown-it-y-no-cuenta-nada-que-esté-en-código-cercado-i` | `codigo` | sldb/src/sldb/links/scan_text.py:1-6 (markdown-it de sldb.core.ast, deja fuera fence/code_block/code_inline) |
| `atom-sldb-mcp-deshace-lotes-con-undo-changes-sobre-una-pila-de-lotes-inversos-por-sesión` | `codigo` | sldb/src/sldb/mcp/write/undo.py:1,26-37 (pila de lotes inversos por sesion, stale, nothing_to_undo) y mcp/write/apply.py:53-60 |
| `atom-sldb-move-mueve-un-archivo-o-directorio-con-git-mv-y-reescribe-en-el-mismo-repo-las-referencias-a-la` | `codigo` | sldb/src/sldb/api/documents/move_path.py:1, move_document.py:21 y relocate_file.py:1 (git mv, referencias reescritas en transaccion) |
| `atom-sldb-notations-from-graph-elige-el-campo-del-label-y-el-que-da-kind-o-estilo` | `codigo` | sldb/src/sldb/api/notations/component_spec_fields.py:1-4,36-38 (--label-field/--kind-field de notations from-graph) |
| `atom-sldb-serve-expone-una-ruta-por-superficie-guarda-por-el-modelo-y-no-simula-lo-que-no-existe` | `decision` | porque una ruta por superficie y no endpoint monolitico (acoplaria consumidores a una pantalla) y no simular lo que no existe: el porque no esta en el codigo; las rutas existen en sldb/src/sldb/cli/serve/*_routes.py y unavailable_models.py:1-6 |
| `atom-sldb-version-dice-la-versión-del-paquete-y-desde-un-checkout-git-el-describe-y-la-ruta-del-checkout` | `codigo` | sldb/src/sldb/store/package_version.py:1-25 (package_version/source_revision) y cli/parsers/core.py:19 |
| `atom-solo-la-plantilla-del-modelo-es-jinja-el-valor-de-un-campo-se-renderiza-literal` | `codigo` | sldb/src/sldb/core/renderer_engine/base.py:27-33 (replace_markers pasa valores como datos de contexto a Jinja) |
| `atom-stores-build-check-keep-dir-conserva-la-copia-verificada-y-el-job-store-del-ci-construye-el-store-un` | `codigo` | sldb/src/sldb/cli/parsers/stores.py:90 (--keep), cli/commands/stores_build.py:5-7,43-44 y .github/workflows/ci.yml:68 |
| `atom-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta` | `codigo` | sldb/src/sldb/api/stores/store_findings.py:43-49 (alert store/generated-missing: documentos generados que no estan en disco) |
| `atom-surface-trae-el-lector-de-documentos-de-minegocio-para-explorar-el-store-de-deskops` | `codigo` | sldb/surface/src/core/{doc-ref,wiki-index,rechazo,imagenes}.ts y surface/src/workbench/{WikiIndex,Ficha,NuevaPagina,AvisoGuardado}.tsx existen con tests; el resto son mediciones |
| `atom-the-store-is-sldb-versioned-plus-sldb-cache-regenerable-ignored-git-history-is-the-past` | `codigo` | sldb/src/sldb/cli/commands/help_texts_other.py:31-32 (stores/core_ignored, cache_not_ignored), cli/parsers/stores.py:50 (migrate-layout) y store/journal/__init__.py:5 |
| `atom-toda-función-pública-de-escritura-de-sldb-api-que-recibe-actor-lo-lleva-al-sello-sldb-by-o-declara-e` | `codigo` | sldb/src/sldb/api/anchors/anchor_docs.py:37-40,50-52 (actor firma write_anchor y record_reconnection) y api/documents/track_document_file.py:26 (actor aceptado sin registrar) |
| `atom-track-con-force-re-indexa-desde-el-archivo-un-documento-ya-trackeado-en-la-misma-ruta` | `codigo` | sldb/src/sldb/api/documents/track_document_file.py:31-34,45 (force re-indexa en la misma ruta, otra ruta se rechaza) y cli/parsers/docs1.py:29 |
| `atom-un-censo-de-importadores-por-substring-miente-hay-que-contarlo-sobre-el-ast` | `decision` | leccion de metodo (contar nodos ast.Import, no grep) sacada de sldb/docs/architecture/superseded-code-audit.md:11,102; no hay codigo que la diga ni specIR que la extraiga y sigue valiendo sin trabajo abierto |
| `atom-un-conflicto-de-git-en-los-índices-derivados-de-sldb-se-resuelve-con-el-merge-driver-y-sldb-stores-r` | `codigo` | sldb/src/sldb/store/io/derived_guard.py:3 (stores rebuild-index) y sldb/src/sldb/api/stores/merge_driver_install.py:15 (install_merge_driver, stores merge-driver --install) |
| `atom-un-consumidor-pregunta-al-store-por-la-api-no-leyendo-sus-archivos-de-índice` | `decision` | la regla (no parsear store_index.yaml) no está en código; la API existe en sldb/src/sldb/api/model_registry/registration_query.py:16,25 |
| `atom-un-directorio-existente-declarado-como-target-de-una-materializacion-es-un-nodo-del-grafo-con-o-sin` | `codigo` | sldb/src/sldb/api/edges/project_graph/file_nodes.py:7 y declared_target_nodes.py:44-48 hacen exactamente eso |
| `atom-un-documento-se-elige-con-un-selector-declarado-y-la-ambigüedad-es-un-error` | `codigo` | sldb/src/sldb/api/documents/select_documents.py:5,17,23,44 (docstring y errores del selector) |
| `atom-un-escaneo-por-documento-se-cachea-por-lo-que-lo-determina-texto-contrato-y-lector` | `codigo` | sldb/src/sldb/api/stores/scan_rewrite_loss.py y scan_structural_noise.py usan scan_cache; el caché por texto/contrato/lector está en el código |
| `atom-un-flag-que-casi-todos-los-subcomandos-aceptan-se-define-una-sola-vez` | `decision` | regla de diseño (definir --format una vez): se cumple en sldb/src/sldb/cli/output_format.py:18,22 pero el porqué no se lee del código |
| `atom-un-hash-consistente-no-prueba-que-el-modelo-lea-el-documento-la-prueba-es-reescribirlo` | `decision` | el porqué (hash consistente no prueba lectura) no está en código; el mecanismo es sldb/src/sldb/api/documents/rewrite_loss.py:17 |
| `atom-un-lector-que-no-debe-escribir-abre-el-store-con-read-store-que-no-migra-y-rechaza-un-store-no-prepa` | `codigo` | sldb/src/sldb/api/stores/read_store.py:17,33,49 (NOT_PREPARED y read_store sin migrar) |
| `atom-un-log-no-puede-reducirse-a-una-vista-si-el-árbol-que-mira-no-guarda-el-pasado` | `no-se-sostiene` | el journal fue retirado y git es la memoria del árbol: sldb/docs/architecture/journal-authority.md:1-10; la premisa 'el árbol no guarda el pasado' ya no rige |
| `atom-un-mapa-de-hashes-vacio-significa-no-se-pudo-calcular-nunca-nada-cambio` | `codigo` | sldb/src/sldb/store/diagnostics_models/verdict_notes.py:14-24 (docstring lo dice y devuelve [] si falta un lado) y diagnostics.py:60 |
| `atom-un-store-enlazado-ausente-es-alerta-en-stores-build-y-build-check` | `codigo` | sldb/src/sldb/api/stores/build_store.py:37,76 y cli/commands/stores_link_alert.py:16 (build/link-missing como alerta) |
| `atom-una-consulta-del-grafo-distingue-un-nodo-inexistente-de-un-nodo-sin-aristas` | `codigo` | sldb/src/sldb/cli/commands/edges_unknown_node.py:3,21 (comprueba nodo y sugiere por sufijo ':<arg>') |
| `atom-una-escritura-de-varios-documentos-en-sldb-es-todo-o-nada` | `codigo` | sldb/src/sldb/store/io/rollback.py:16 (RollbackError) y api/documents/apply_batch.py:53, transaction_state.py:16 |
| `atom-una-escritura-por-campos-falla-antes-de-borrar-ruido-estructural-o-frontmatter-no-declarado-del-arch` | `codigo` | sldb/src/sldb/api/documents/refuse_structural_noise.py:17 y lossy_overwrite.py aplicadas antes de reescribir |
| `atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si` | `codigo` | sldb/src/sldb/mcp/context.py:26 (add_batch_validator) y mcp/extension.py:13 (contrato BatchValidator) |
| `atom-una-lista-de-fricciones-conocidas-se-poda-cuando-la-fricción-se-arregla-en-el-mismo-cambio` | `decision` | práctica de mantenimiento del manual (podar fricciones al arreglarlas); sldb/docs/user-manual.md:833 §16; no se lee del código |
| `atom-una-operación-de-sldb-se-ancla-al-store-más-cercano-no-al-directorio-desde-donde-se-corre` | `codigo` | sldb/src/sldb/store/edge_index/federation.py:15 (federated_stores) y store/resolver.py resuelven el store más cercano |
| `atom-una-operación-que-crea-un-directorio-deshace-lo-que-alcanzó-a-crear-si-falla` | `codigo` | sldb/src/sldb/api/stores/init_store.py:58 (_write_or_undo) deshace lo creado |
| `atom-una-reconstrucción-de-secciones-con-documentos-trackeados-ausentes-avisa-una-vez-por-modelo-con-el-n` | `codigo` | sldb/src/sldb/store/section_sync.py:52,97 (un warning por modelo, missing_summary) |
| `atom-una-regla-de-gitignore-se-evalúa-sin-el-índice-o-un-archivo-trackeado-la-oculta` | `codigo` | sldb/src/sldb/api/stores/gitignore_policy.py:5,30 (git check-ignore --no-index) |
| `atom-una-task-de-diseno-entrega-un-documento-y-su-doc-puede-decir-que-lo-disenado-no-existe` | `decision` | lección sobre leer el desk (task de diseño vs implementación); sldb/docs/composition_modes.md:1-3 ya marca lo verificado; no es código |
| `atom-una-vista-de-todo-el-store-no-puede-depender-de-que-importen-todos-sus-modelos` | `codigo` | sldb/src/sldb/api/records/build_ast.py:38-41 registra el modelo no resuelto con su error y sigue |
| `atom-una-vista-es-un-documento-que-declara-qué-leer-y-sldb-la-ejecuta` | `codigo` | sldb/src/sldb/api/views/run_view.py:25 (run_view) ejecuta el ViewDoc declarado |
| `atom-undo-changes-de-sldb-mcp-restaura-el-mismo-contenido-salvo-procedencia-y-deshace-n-lotes-todo-o-nada` | `codigo` | sldb/src/sldb/api/documents/batch_inverse.py:4,54 y batch_prevalidate.py:69 (expected_content_hash en el inverso) |

### sldb: pills (24)

| id | veredicto | motivo |
|---|---|---|
| `pill-context-pills-carry-reasoning-not-a-copy-of-code-or-docs` | `decision` | Regla permanente de qué lleva una pill y cuándo se retira; no la expresa ningún código (sldb/desk/contexts/ solo la declara) y no depende de un trabajo abierto |
| `pill-keep-sldb-cli-output-tied-to-document-contracts` | `invariante` | CLI (sldb/src/sldb/cli/commands/) debe presentar fielmente el contrato del modelo de documento; relación entre capas CLI y modelos, sin trabajo abierto asociado |
| `pill-keep-sldb-generic-and-move-workflow-behavior-toward-deskops` | `decision` | Porqué de la frontera sldb evalúa reglas/deskops las escribe; respaldada por sldb/desk/atoms/atom-sldb-evaluates-declared-rules-consumers-author-them.md y D1 de grafo-operable/decisiones.md |
| `pill-keep-template-markers-reversible-at-the-document-boundary` | `invariante` | Render y extract deben hacer roundtrip entre sldb/src/sldb/core/template_extractor.py y handlers/; lo comprueba sldb/tests/test_marker_invariants.py |
| `pill-keep-the-text-layer-and-the-graph-layer-separate-inside-sldb` | `invariante` | Capa de texto vs capa de grafo (sldb/src/sldb/store/graph/ solo lee vía API del store); regla entre piezas, vigente sin trabajo abierto; ver docs/architecture/sldb-absorbs-kgdb.md |
| `pill-model-registration-must-be-queryable` | `decision` | Porqué el estado de registro de modelos se expone por API/CLI (sldb/src/sldb/api/model_registry/registration_query.py, cli/commands/models_check.py) y no leyendo YAML; los códigos ya existen, lo que queda es la regla de frontera |
| `pill-pill-alcance-real-del-traslado-del-parser-a-core` | `contexto-trabajo` | Precisiones del bundle-1 de la tarea abierta task-r6-el-tokenizer-y-el-parser-del-lenguaje-de-reglas-bajan-a-core; aún no hecho: no existe sldb/src/sldb/core/rules_language/ y el parser sigue en store/graph/language/ |
| `pill-pill-campo-data-de-specdoc` | `contexto-trabajo` | Bundle-1 de la tarea abierta task-specdoc-guarda-los-datos-de-un-spec-que-no-son-elementos; sldb/src/sldb/models/notation/spec_doc.py aún no tiene campo data |
| `pill-pill-dónde-se-agrupan-los-ausentes-de-sections-rebuild` | `codigo` | Ya implementado: missing_paths en sldb/src/sldb/store/semantic.py:33 y aviso único por pasada en store/section_sync.py:29-51,94; sin tarea abierta |
| `pill-pill-dónde-va-version` | `codigo` | Ya implementado: --version en sldb/src/sldb/cli/parsers/core.py:19 y _source_checkout_dir en store/package_version.py:25,49,59; sin tarea abierta |
| `pill-pill-forma-del-rechazo-de-dominio-en-sldb-mcp` | `codigo` | Ya implementado: apply.rejected(**detail) en sldb/src/sldb/mcp/write/apply.py:19, domain_alerts en mcp/write/tools.py:84-85 y tests en tests/mcp/test_extension.py:101-103; sin tarea abierta |
| `pill-pill-grafo-en-proceso-para-referrers` | `codigo` | Ya implementado: referrers acepta graph (sldb/src/sldb/api/edges/referrers.py, api/edges/rewrite_references.py:2 optional_graph) y tests/api/test_project_graph.py existe; sin tarea abierta |
| `pill-pill-imports-anidados-en-scan-tree` | `codigo` | Ya implementado: py_nested_imports en sldb/src/sldb/code/imports.py:26, attrs nested_imports en code/py_module.py:2 y uso en api/notations/component_spec_python.py:65; sin tarea abierta |
| `pill-pill-rechazados-de-la-carga-tolerante` | `codigo` | Ya implementado: parámetro rejected en sldb/src/sldb/store/query.py:55,67 y on_invalid=skip en api/documents/runtime_documents.py:8-47; sin tarea abierta |
| `pill-pill-regla-de-aristas-en-el-test-de-on-write` | `codigo` | Ya implementado: DocumentReference.alerts en sldb/src/sldb/api/documents/document_reference.py:17, test con count(depends_on: title != "") > 0 en sldb/tests/api/test_on_write_entering.py:78 y _LISTENERS en core/finding_route.py:15; sin tarea abierta |
| `pill-pill-salida-y-orden-de-sldb-notations-validate` | `codigo` | Ya implementado: sldb/src/sldb/cli/commands/notations_validate.py (_check_palette/_check_spec/_check_notation, _file_or_name_kinds) y subcomando validate en cli/parsers/notations.py:32-33; sin tarea abierta |
| `pill-pill-standards-md-es-un-documento-modelado` | `contexto-trabajo` | Bundle-1 de la tarea abierta task-decisión-de-jp-decisión-6-separar-el-store-de-sldb-en-un-paquete-propio; sldb/docs/architecture/store-extraction-proposal.md aún no tiene sección Decisión 6 |
| `pill-pill-texto-de-la-alerta-y-test-existente-de-stale` | `contexto-trabajo` | Bundle-1 de la tarea abierta task-edgeindex-stale-manda-a-la-operación-correcta; sldb/src/sldb/cli/commands/edges.py:73 aún dice 'sldb edges rebuild' y el texto antiguo |
| `pill-pill-una-carga-del-índice-en-attach-atom-edges` | `contexto-trabajo` | Precisiones sobre StoreReader (sldb/src/sldb/api/matching/store_reader.py:19) y cargas de load_edge_index (api/matching/store_edges.py:11,51); trabajo de la tarea abierta de emparejamiento de átomos de sldb/desk/tasks; incierto si ya se cerró |
| `pill-pill-validar-el-enlace-guardando-el-texto-tal-cual` | `codigo` | Ya implementado: raw en link_store (sldb/src/sldb/api/stores/link_store.py:20,39,46) y expansión en store/link_path.py:25; sin tarea abierta |
| `pill-put-a-small-onboarding-surface-before-the-deep-system` | `decision` | Porqué de mantener pequeña la superficie de entrada (help, FAQ); principio de diseño permanente, no hay código que lo diga (docs/faq.md, cli/parser.py) |
| `pill-sldb-cli-errors-must-stay-actionable-and-machine-safe` | `invariante` | Los errores del CLI deben ser accionables sin romper la salida legible por máquina: regla entre sldb/src/sldb/cli/main.py, parsers y tests de serialización; permanente |
| `pill-store-health-is-owned-by-sldb` | `decision` | Porqué la validez del store la define sldb y deskops la consume (sldb/src/sldb/store/diagnostics.py, cli/commands/store_check.py); frontera permanente |
| `pill-stores-init-must-be-idempotent-and-fail-safely` | `codigo` | Ya está en el código: exit codes 0/1/2 en sldb/src/sldb/cli/commands/store_init.py:15-33 y StoreInitError con _write_or_undo en api/stores/init_store.py:36,49 |

### IR: átomos (38)

| id | veredicto | motivo |
|---|---|---|
| `atom-cambios-del-momento-del-retiro-de-spec2viz-bpmn-de-specir-y-clave-de-localstorage-de-specir-con-migr` | `codigo` | IR/src/specir/visual/templates/default.html:565 (clave specir.catalog.annotations.v1) y :900 (migra la clave legacy); es un cambio ya hecho, no un porqué |
| `atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al` | `decision` | decisión de JP con su porqué (grafo manda, YAML subordinado); el código no la dice; IR/docs/decisiones/fuente-de-verdad-del-diagrama.md |
| `atom-el-cascaron-de-la-ui-de-specir-usa-los-tokens-de-papel-y-se-parece-a-la-maqueta` | `codigo` | IR/ui/src/shell.css:1-6 usa las variables --wb-* de paper-tokens.css, tal como afirma |
| `atom-el-consumidor-principal-de-specir-es-un-agente-por-mcp` | `decision` | para quién es specIR (agente por MCP primero); no se lee del código aunque IR/src/specir/mcp_extension.py:187 lo materializa |
| `atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas` | `codigo` | sldb/src/sldb/mcp/registry.py:30 registra undo_changes y IR/src/specir/mcp_extension.py:21-22 declara que specIR no crea tools de escritura ni undo; IR/tests/test_mcp_undo.py:292 |
| `atom-el-nivel-de-escritura-del-mcp-se-fija-al-arrancar-el-servidor` | `codigo` | sldb/src/sldb/mcp/mutability.py:8-9,13 (nivel argumento del servidor, nunca del tool) y IR/src/specir/mcp_extension.py:227 (READ por defecto) |
| `atom-el-retiro-de-spec2viz-queda-declarado-el-2026-11-23-en-el-acta` | `codigo` | ya escrito en IR/docs/spec2viz/acta-de-retiro.md:7-13 (retiro 2026-11-23, 55,8 s, punto 9 hecho); es un estado/hecho histórico, no conocimiento extra |
| `atom-el-vocabulario-visual-y-el-resolvedor-de-vistas-ya-viven-en-sldb` | `codigo` | sldb/src/sldb/models/notation/ y sldb/src/sldb/api/notations/ existen; alias en sldb/src/sldb/api/model_registry/model_reference.py:18 |
| `atom-entidad-aparición-proyección-y-notación-son-cosas-distintas` | `decision` | distinción conceptual (identidad vs aparición vs proyección vs notación vs autoría) que ninguna pieza afirma sola; el cierre del YAML ya lo decidió el atom de JP 2026-11-15 (queda un resto desactualizado) |
| `atom-ir-ignora-en-git-los-artefactos-de-instalación-editable-y-de-bytecode` | `codigo` | IR/.gitignore:4-5 contiene *.egg-info/ y __pycache__/; el porqué está en IR/desk/materializations/materialization-ir-gitignore-*.md |
| `atom-ir-no-tiene-goldens-de-spec2viz-la-paridad-se-acredita-por-pruebas-de-aceptacion` | `codigo` | IR/tests/visual/ no tiene goldens ni oracle.py y IR/pyproject.toml no define el marcador parity (rg sin resultados) |
| `atom-ir04b-specir-deshace-por-mcp-aplicando-el-lote-inverso-de-sldb-con-guard-de-contenido` | `no-se-sostiene` | afirma que mcp_extension.py expone deshacer, pero IR/src/specir/mcp_extension.py:21-22 dice que no crea ninguna tool de undo y IR/tests/test_mcp_undo.py:292 test_specir_defines_no_undo; además la tarea de cierre ya está hecha (test_mcp_undo.py:137-150) |
| `atom-la-aplicación-de-un-cambio-mcp-se-protege-con-guardas-por-documento-y-huella-global-en-nivel-2` | `codigo` | sldb/src/sldb/mcp/write/propose.py:38 rellena expected_source_hash por el servidor; sldb/src/sldb/mcp/changes/sealer.py:21 sella con store_hash; la lógica es de sldb |
| `atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla` | `codigo` | IR/src/specir/models/domain.py:28 (Origen) y :35 (PROVENANCE_FIELDS origen, verificacion, verificado_por, evidencia, desconocidos) |
| `atom-la-prueba-de-identidad-del-deshacer-por-mcp-compara-los-md-y-el-store-por-contenido-con-la-api-publi` | `codigo` | IR/tests/test_mcp_undo.py:137-150 (sha256 sin bloque sldb, api.select_documents); es un hecho de un test |
| `atom-la-ui-de-specir-vive-en-ir-ui-con-cascaron-de-pestanas-y-lentes-y-cliente-de-sldb-serve` | `codigo` | IR/ui/src/Shell.tsx:3 (pestañas Grafo, Anclajes, Composiciones) y :26-27 (Lectura, Fierros); IR/ui/vite.config.ts:11 (proxy /sldb a SLDB_TARGET); IR/ui/src/env.ts:4 |
| `atom-las-filas-de-validate-de-la-matriz-de-spec2viz-remiten-a-sldb-notations-validate` | `codigo` | IR/docs/spec2viz/matriz-de-cobertura.md:207,220 y IR/tests/visual/test_cli.py:561 test_every_equivalent_of_the_table_answers_its_help |
| `atom-las-operaciones-de-api-de-un-backend-sin-drf-salen-de-una-tabla-de-rutas-declarada-en-yaml` | `codigo` | IR/src/specir/extract/routes.py:55-72 (extract_routes, origen declarado, stale_declared) |
| `atom-las-pruebas-de-ir-encuentran-el-workspace-por-specir-workspace` | `codigo` | IR/tests/conftest.py:31-37 workspace_root() con SPECIR_WORKSPACE o REPO.parent; IR/tests/test_workspace_env.py:7 |
| `atom-las-pruebas-de-ir-no-dependen-de-spec2viz-el-marcador-parity-compara-contra-goldens` | `no-se-sostiene` | IR/tests/visual/goldens no existe (ls) y IR/pyproject.toml no define el marcador parity; contradicho por atom-ir-no-tiene-goldens |
| `atom-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz` | `no-se-sostiene` | IR/tests/visual/goldens/ no existe y no hay oracle.py; la paridad ya no se compara contra goldens (ver atom-ir-no-tiene-goldens) |
| `atom-lo-desconocido-se-nombra-y-solo-un-humano-fuera-del-mcp-o-un-chequeo-determinista-verifica` | `codigo` | IR/src/specir/models/domain.py:11,35 (desconocidos) y IR/src/specir/mcp_extension.py:41,204 (VERIFIES: el agente no escribe verificado, regla specir_agent_verifies) |
| `atom-los-nombres-de-relacion-de-specir-quedan-acotados-con-un-resumen-con-hash` | `codigo` | IR/src/specir/extract/plan.py:72-80 bounded_name (UTF-8, sha256[:12]) y :83-84 edge_name |
| `atom-omg-es-referencia-conceptual-no-dependencia` | `decision` | por qué specIR toma conceptos OMG sin adoptar EMF/Sirius/GLSP ni afirmar conformidad; no se lee del código; IR/pyproject.toml:6-10 solo confirma las dependencias |
| `atom-por-qué-existe-specir-coherencia-entre-capas-para-agentes-de-código` | `decision` | razón de ser del proyecto (coherencia entre capas para agentes); no la dice el código |
| `atom-propuesta-pendiente-de-jp-el-yaml-de-spec-queda-como-formato-de-autoría-e-intercambio-subordinado-al` | `no-se-sostiene` | stub de redirección: la propuesta pendiente ya fue fusionada en atom-decisión-de-jp-2026-11-15-el-yaml-de-spec-queda-... (la afirmación de pendiente ya no vale); no tiene contenido propio |
| `atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir` | `invariante` | principios que deben cumplirse entre varias piezas (servidor, apply_batch, guardas, procedencia): IR/src/specir/mcp_extension.py:41,194-204 + sldb/src/sldb/mcp/mutability.py:8-9; ninguna pieza lo afirma sola |
| `atom-spec2viz-continua-como-ir-en-jpcosec-specir` | `decision` | decisión de JP 2026-11-24 (spec2viz continúa como IR); consta en IR/docs/spec2viz/acta-de-retiro.md:13 pero el porqué/decisión no sale del código |
| `atom-specir-depende-solo-de-la-api-pública-de-sldb` | `invariante` | regla entre repos (specIR solo sobre sldb.api); IR/src/specir/__init__.py:3 la declara pero IR/src/specir/extract/write.py:13 e install.py importan sldb.models/notations y mcp_extension.py:32-34 sldb.mcp, así que hace falta regla que la compruebe |
| `atom-specir-es-un-repo-periférico-sobre-sldb-mcp-y-modelado-semántico` | `decision` | decisión del dueño 2026-11-11 sobre la posición de specIR respecto a sldb; IR/pyproject.toml:6-10 solo muestra la dependencia |
| `atom-specir-mcp-delega-en-mcp-extension-y-cli-py-no-importa-sldb-mcp` | `codigo` | IR/src/specir/cli.py:66 (from specir.mcp_extension import serve) y IR/src/specir/mcp_extension.py:222-227; solo mcp_extension importa sldb.mcp |
| `atom-specir-mcp-levanta-el-server-mcp-de-sldb-con-la-extension-de-specir` | `codigo` | IR/src/specir/mcp_extension.py:222-227 server.serve(store, level=..., actor=..., extensions=("specir.mcp_extension:register",)) |
| `atom-specir-no-depende-de-pron-adopta-contratos-no-código` | `decision` | decisión del dueño 2026-11-11 (pron desactualizado, se adoptan contratos no código); IR/src/specir/__init__.py:3 y IR/pyproject.toml:6-10 solo comprueban la ausencia de la dependencia |
| `atom-specir-reemplaza-a-spec2viz-y-cubre-todas-sus-funciones` | `decision` | decisión del dueño 2026-11-11: specIR cubre todas las funciones y spec2viz se retira; el porqué no sale del código (IR/docs/spec2viz/gate-de-retiro.md es su trazabilidad) |
| `atom-specir-retirement-check-da-rc-0-spec2viz-sldb-fuera-del-inventario-y-sv-a17-acreditada-con-g5-opcion` | `codigo` | IR/docs/spec2viz/acta-de-retiro.md:106 (rc 0, 0 dependencias) y IR/docs/spec2viz/matriz-de-cobertura.md:79,296 (SV-A17, G5); es un estado medido, ya escrito en el acta |
| `atom-specir-ux-extract-extrae-la-interfaz-de-un-arbol-y-avisa-de-los-archivos-saltados` | `codigo` | IR/src/specir/cli.py:221-245 (ux extract, aviso en stderr, --strict rc 1) |
| `atom-un-nodo-extraído-se-ancla-con-sldb-y-la-divergencia-con-el-código-se-calcula-según-su-origen` | `decision` | la regla de quién manda ante divergencia (código para observado/derivado, modelo para declarado/verificado) es una decisión (IR/docs/decisiones/procedencia-y-divergencia.md); el anclaje en sí está en IR/src/specir/extract/write.py:13,52 |
| `atom-una-propuesta-de-cambio-del-mcp-es-un-lote-efímero-prevalidado` | `codigo` | sldb/src/sldb/mcp/changes/batch_change.py:20 (BatchChange con guardas rellenadas por el servidor) y sldb/src/sldb/mcp/write/propose.py:38; la lógica vive en sldb |

### IR: pills (4)

| id | veredicto | motivo |
|---|---|---|
| `pill-guardrail-la-paridad-con-spec2viz-se-demuestra-con-sus-pruebas` | `decision` | decisión de JP 2026-11-25 (sin goldens de spec2viz, prueba de aceptación por capacidad); permanente, no legible de IR/src ni de IR/tests |
| `pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk` | `decision` | regla de proceso permanente sobre fronteras entre desks (el porqué: "salta sus gates"); coincide con /workspace/AGENTS.md, no está en IR/src |
| `pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo` | `invariante` | regla permanente para todo código de specIR (IR/src/specir, IR/tests/fixtures) sin trabajo abierto que la contenga |
| `pill-guardrail-specir-solo-usa-la-api-pública-de-sldb` | `invariante` | invariante entre repos comprobado por IR/tests/test_imports.py:1-30 (solo sldb.api, no pron/spec2viz); permanente |

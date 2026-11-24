# Resultado: un solo vocabulario de tags semanticos

Rama `deskops/deskops-e-e558315aff21` (worktree `.worktrees/deskops-e-e558315aff21`). Sesion retomada tras un crash del host; la migracion ya estaba aplicada en parte y se completo.

## Tabla de mapeo
| Tag | Accion | Razon |
|---|---|---|
| `workspace:desk`, `workspace:docs` | se borra de los documentos (1083 docs: 1003 reviews, 48 tareas...) | duplica `workspace.desk[.x]` que el modelo ya emite |
| `artifact:task/ritual/step/repository/...` | se borra (47 tareas) | duplica `type.workflow.*` del modelo |
| `layer:X`, `type:X` | se descarta si el modelo ya dice `layer.X`/`type.X` (ninguno aparecia en documentos de deskops) | misma regla |
| nombres de clase (`TaskDoc`...) | el validador los rechaza | la clase es el modelo; no habia ninguno en los docs de deskops |
| repetidos | el validador los quita | |
| `board.tareas` (nuevo, en `TaskDoc.__semantics__`) | padre de todas las tareas | la semantica del apartado de JP |
| `board.tareas.ui` (nuevo, tag de documento) | hija de `board.tareas` por el nombre con puntos | tareas de UI |
| `topic:*`, `system:*`, `host:*`, `pill-type:*`, `domain:*`, `source:*` | **se quedan** como `ns:valor` (vocabulario declarado de atomos/pills/hosts, `desk/atoms/tag-namespaces.yaml`) | sldb no permite declararles padre (ver "No resuelto") |

## Cambios
- `deskops/tag_vocabulary.py`: unica regla de que no se escribe (repetidos, nombre de clase, copia plana de un tag del modelo). Usa `sldb.store.semantic_tags.flatten_model_semantics`; no resuelve jerarquia.
- Validador en `PrimitiveDoc.tags`, `ReviewDoc.tags` y `AtomDoc.tags`; defaults `__artifact__["tags"]` vacios para las tareas, board, step, pill, ritual, inbox, role, repository, faq, runtime-profile; servicios closure/review/drawer y templates/declaracion de bootstrap sin `workspace:desk`.
- `TaskDoc.__semantics__` suma `"board": ["tareas"]`.
- Comando nuevo `deskops tags migrate [--apply]` (`deskops/tag_migration.py`, `deskops/cli/commands/tags.py`): reescribe cada documento por su modelo en una transaccion.
- Tarea `task-governance-ui-de-deskops-en-astro-...` etiquetada `board.tareas.ui` con `deskops edit task ... tags`.
- Store: `sldb models update` de TaskDoc y los task types (hashes de modelo) y la migracion de 1083 documentos.
- Tests: `tests/test_tag_vocabulary.py` (nuevo, 6), ajustes en test_specs, test_domain_tree, test_cli, test_cli_grammar, test_command_registry, goldens y `model_contract_hashes.json`.

## Demostracion sobre el desk (worktree, `--store .sldb`, indice reconstruido)
```
$ sldb find board.tareas --in semantic --type doc --store .sldb --format json   -> 48 documentos (todas las tareas trackeadas; ls desk/tasks = 48; `deskops list tasks` = 48)
$ sldb find board.tareas.ui --in semantic --type doc ...                       -> 1: task-governance-ui-de-deskops-en-astro-sobre-las-uis-de-sldb-1
$ sldb find type.workflow.task ...                                              -> 48
$ sldb semantic show board.tareas
{"tag":"board.tareas","parents":["board"],"children":["board.tareas.ui"],"below":["board.tareas.ui"],"above":["board"],"equivalents":[]}
$ sldb semantic show board.tareas.ui
{"tag":"board.tareas.ui","parents":["board.tareas"],"children":[],"below":[],"above":["board","board.tareas"],"equivalents":[]}
```
`sldb find` ya incluye descendientes (type.workflow = 1331 docs): deskops no agrega listas ni filtros propios.

## Medicion (`.sldb_cache/semantic_dag.yaml`)
- Antes (checkout principal): 221 nodos, 173 sin padre; planos sin padre ni hijos 167, de ellos 164 con dos puntos (incluye `workspace:desk`, `artifact:task/ritual/step/repository`).
- Despues (worktree): 194 nodos, 156 sin padre; planos 149, todos `ns:valor`. En los documentos reales ya no hay `workspace:desk` ni `artifact:*` (quedan dos nodos en el cache por fixtures y por inbox/drawer que citan el texto; el cache no borra nodos).

## No resuelto / nota a sldb
Enviada: `desk/inbox` de sldb `20261124-023754-suggestion-semantica-del-store-padres-declarados-solo-en-el-cache-...`.
1. `sldb semantic parent/equivalent add` escribe en `.sldb_cache/semantic_dag.yaml`, que esta en .gitignore: lo declarado no se versiona. Por eso aqui los padres salen de nombres con puntos y del modelo, no de `parent add`.
2. `parent add` rechaza un padre que ningun documento/modelo lleva; no se puede declarar el padre de `topic:atoms`, `system:deskops`, `host:robocop2`, `pill-type:*` (149 tags planos siguen sin padre).
3. No hay migracion de tags en bloque en sldb: `deskops tags migrate` reescribio 1083 docs por modelo (varias horas por una transaccion por documento).
Tampoco se tocaron `ci/cd`, `demo`, `test`, etc.: vienen de tests/tools, fuera de deskops.

## Validacion
Ver `validation.log`. Suite completa: 10 fallos esperados (goldens/registro/hashes), corregidos y re-corridos en verde. `deskops doctor`: sin hallazgos de tags; los errores que hay (RunDoc/ReviewDoc `lost`) ya existian. Aviso: en el worktree doctor suma entradas RunDoc `fields changed ... commit_sha` porque los runs estan commiteados distinto que en el checkout principal; no vienen de esta tarea.

## Revisar
- Los ~2200 archivos de `.sldb/core/documents` y `desk/` modificados son la migracion y el re-hash; el codigo esta en `deskops/` y `tests/`.
- Los goldens de help de add/edit/list/show no se tocaron (el wrap depende del COLUMNS).

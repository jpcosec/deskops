PASA

# Veredicto del tester (intento a2)

El fallo del intento anterior queda corregido: en el desk real `board.tareas` devuelve **50** documentos, exactamente las 50 tareas trackeadas, y `board.tareas.ui` devuelve **1** (la tarea de UI). `sldb semantic show` muestra padres, hijos y descendientes. Los tests tocados pasan y `deskops doctor` mantiene los mismos 212 hallazgos preexistentes, sin sumar ninguno de tags.

## Commits revisados

- Codigo y tests del vocabulario: `86d8608f` ("... codigo de dc391505, sin la migracion de datos"), tambien en la rama del ejecutor `dc391505`.
- Correccion a2 (reindexado de documentos con indice semantico viejo): `08dc4181` (`deskops/tag_migration.py`, `deskops/cli/commands/tags.py`, `tests/test_tag_vocabulary.py`).
- Migracion/aplicacion de datos en main y commit final con `Task-Id`: `58203c77` (reindexa `TaskDocsDoc/task-agents-md-readme...`; solo `.sldb`/desk, sin codigo). El commit de codigo a probar es `08dc4181`, porque el ultimo commit con `Task-Id` solo trae el store migrado.

## Tests ejecutados (de a uno, `TMPDIR=/tmp`, `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-458e549a77c2-a2`)

Use `/dev/shm/tester-venv/bin/python` (3.12 con `sldb`, `markdown_it` y `pytest`) porque `/workspace/.venv` esta roto en este host. No corri la suite completa.

- `tests/test_tag_vocabulary.py`: 7 passed (incluye la regresion nueva de reindexado a2)
- `tests/test_cli.py`: 103 passed
- `tests/test_cli_grammar.py`: 2 passed
- `tests/test_command_registry.py`: 3 passed
- `tests/test_domain_tree.py`: 10 passed
- `tests/test_specs.py`: 5 passed
- `tests/test_model_validators.py`: 14 passed
- `tests/test_model_templates.py`: 14 passed
- `tests/test_atom_tags.py`: 11 passed
- `tests/test_review_command.py`: 31 passed
- `tests/test_add_task_from_drawer.py`: 3 passed
- `tests/test_closeout.py`: 82 passed

Total: **285 passed, 0 fallos**.

## Criterio de JP sobre el desk real (verificado tras `58203c77`)

```text
$ sldb find board.tareas --in semantic --type doc --store .sldb --format json
50 resultados

$ sldb find board.tareas.ui --in semantic --type doc --store .sldb --format json
1 resultado: desk/tasks/task-governance-ui-de-deskops-en-astro-sobre-las-uis-de-sldb-1.md

$ sldb find type.workflow.task --in semantic --type doc --store .sldb --format json
50 resultados

$ deskops list tasks --root . --format json
50 tareas

$ sldb semantic show board.tareas --store .sldb
{"tag":"board.tareas","parents":["board"],"children":["board.tareas.ui"],
 "below":["board.tareas.ui"],"above":["board"],"equivalents":[]}

$ sldb semantic show board.tareas.ui --store .sldb
{"tag":"board.tareas.ui","parents":["board.tareas"],"children":[],
 "below":[],"above":["board","board.tareas"],"equivalents":[]}
```

Los 50 resultados de `board.tareas` son todos documentos `Task*Doc` bajo `desk/tasks/` (TaskCodeDoc, TaskDocsDoc, TaskDecisionDoc, TaskDebugDoc, TaskExternalDoc), y el documento que antes faltaba (`task-agents-md-readme...`) ya aparece con `semantic_tags` que incluyen `board.tareas`.

## Migracion y vocabulario unico

- `deskops tags migrate --root .` responde "No document carries a duplicate, class-name or model-restating tag." (exit 0), o sea que la migracion por CLI ya no tiene trabajo pendiente en el store.
- 0 documentos trackeados conservan en su frontmatter los tags planos viejos (`workspace:desk`, `workspace:docs`, `artifact:task/ritual/step/repository`) ni nombres de clase. La eliminacion de duplicados se comprobo recorriendo los 2126 documentos trackeados.
- La semantica hija `board.tareas.ui` esta escrita en el frontmatter de su tarea y sldb la situa bajo `board.tareas`.
- Notas a sldb presentes: `20261124-023754-suggestion-semantica-del-store-padres-declarados-solo-en-el-cache-namespace-sin-padre-y-migracion-de-tags-en-bloque.md` y `20261124-190859-suggestion-reindexar-tags-semanticos-de-documentos-cuando-cambia-semantics-del-modelo.md`.

## deskops doctor

```text
$ deskops doctor --root .
exit 1
212 hallazgos: 191 RunDoc "fields differ" (reextraccion de sldb), 12 ReviewDoc "changed",
6 ReviewDoc "lost", 2 entradas de registro que no resuelven.
```

Es el mismo conjunto/categorias que ya reporto el tester anterior (212); ninguno es de tags ni lo agrega esta tarea.

## Observaciones no bloqueantes

- `desk/drawer/tasks/task-e01-prueba-integral-multiagente-opsys-scion-ui-la-recibe-deskops-graph-ui-la-bota-de-su-drawer.md` sigue con `workspace:desk` y `artifact:task` y no esta trackeado en el store (los drawer tasks no entran en `deskops tags migrate`). No afecta las consultas del Done When, que hablan de tareas trackeadas; si "documentos existentes" incluyera el drawer, quedaria esa migracion puntual.
- `.sldb_cache/semantic_dag.yaml` conserva 224 nodos, 174 sin padre y 164 planos con `:`; son nodos de cache que no se borran y que citan inbox/reviews/task docs (incluido el drawer) en su texto. Los documentos trackeados ya no escriben esos tags en el frontmatter, y `board.tareas`/`board.tareas.ui` tienen padre en el DAG.
- El `result-summary` del ejecutor a2 anticipa "debe dar 50"; la salida real de 50/1 queda registrada en `58203c77` y reproducida arriba.

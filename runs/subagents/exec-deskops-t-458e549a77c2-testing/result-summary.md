FALLA

# Veredicto del tester

El codigo y los tests del vocabulario unico pasan, y la semantica hija `board.tareas.ui` se comporta como pide el criterio de JP. Pero falla el Done When en el desk real: `sldb find board.tareas --in semantic --type doc --store .sldb` devuelve **49** documentos y `deskops list tasks --root . --format json` devuelve **50**. Falta `desk/tasks/task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use.md` (modelo `TaskDocsDoc`, tags de frontmatter solo `host:robocop2`). La migracion no reescribio ese documento porque sus tags ya eran canonicos, y su indice semantico quedo vacio.

## Commits revisados

- Codigo: `86d8608f` ("... (codigo de dc391505, sin la migracion de datos)"), tambien presente en la rama del ejecutor `dc391505`.
- Migracion de datos en main: `a6d09f0d` ("store: deskops tags migrate --apply en main (1095 documentos ...)").
- Solo he verificado; no he modificado codigo ni datos del desk.

## Tests ejecutados (de a uno, `TMPDIR=/tmp`, `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-458e549a77c2`)

Use `/dev/shm/tester-venv/bin/python` (3.12 con `sldb` y `pytest`) porque `/workspace/.venv` esta roto en este host (binario 3.11 sin `markdown_it`).

- `tests/test_tag_vocabulary.py`: 6 passed
- `tests/test_cli.py`: 103 passed
- `tests/test_cli_grammar.py`: 2 passed
- `tests/test_command_registry.py`: 3 passed
- `tests/test_domain_tree.py`: 10 passed
- `tests/test_specs.py`: 5 passed
- Extra por modulos de modelo tocados: `tests/test_model_validators.py` 14 passed, `tests/test_model_templates.py` 14 passed

Total: 157 passed, 0 fallos. No hay fallos que comparar contra `origin/main`.

## Criterio de JP sobre el desk real

```text
$ sldb find board.tareas --in semantic --type doc --store .sldb --format json | count
49

$ sldb find board.tareas.ui --in semantic --type doc --store .sldb --format json | count
1   # task-governance-ui-de-deskops-en-astro-sobre-las-uis-de-sldb-1

$ deskops list tasks --root . --format json | count
50  # incluye la tarea que falta en board.tareas
```

La consulta de la semantica hija cumple; la del apartado padre no lista todas las tareas trackeadas.

`sldb semantic show` si muestra la jerarquia:

```json
{"tag":"board.tareas","parents":["board"],"children":["board.tareas.ui"],
 "below":["board.tareas.ui"],"above":["board"],"equivalents":[]}
{"tag":"board.tareas.ui","parents":["board.tareas"],"children":[],
 "below":[],"above":["board","board.tareas"],"equivalents":[]}
```

## Causa del 49/50 (investigada)

El documento faltante se escribio el **2026-11-19**, antes de que `TaskDoc.__semantics__` anadiera `board.tareas` (commit del 2026-11-24), y solo llevaba `host:robocop2`; no tenia ningun tag plano duplicado. Su entrada del store quedo con el indice semantico vacio:

```text
.sldb/core/documents/TaskDocsDoc/task-agents-md-readme-...yaml
  semantic_tags: []

.sldb_cache/semantic/TaskDocsDoc/task-agents-md-readme-...yaml
  tags: host:robocop2, representation.markdown, source.document.markdown,
        type.workflow.task, workspace.desk   # sin board.tareas
```

`deskops/tag_migration.py::plan_tag_migration` solo incluye documentos donde `after != before` (linea 70) y `apply_tag_migration` solo reescribe esos cambios (linea 79). Por eso `deskops tags migrate --apply` no toca este documento, cuyo frontmatter ya era canonico. Lo he comprobado en el desk real:

```text
$ deskops tags migrate --root .
No document carries a duplicate, class-name or model-restating tag.
exit 0
```

Es decir, la migracion documentada no repara el indice semantico de documentos que no necesitaban cambio de tags. El problema no esta en el codigo de escritura: en un desk sandbox (`deskops init /tmp/sandbox-tags-test` + `deskops add task --task-type task.docs`) la tarea nueva si nace con `board.tareas`, y `flatten_model_semantics(TaskDocsDoc)` incluye `board.tareas`. Tambien el `.sldb/core/models/TaskDocsDoc.yaml` de main conserva `semantics` sin `board.tareas`, lo que apunta a la misma falta de re-extraccion de los modelos derivados.

Nota sobre lo que vio el coordinador: `sldb find type.workflow.task --in semantic` **sin** `--type doc` menciona el documento por sus secciones; con `--type doc`, que es la forma del Done When, tambien devuelve 49 y lo excluye.

## Otras observaciones

- `deskops doctor --root .`: exit 1, 212 hallazgos, todos de clases preexistentes y ninguno de tags: 191 `RunDoc` con `fields differ ...` (re-extraccion de sldb), 18 `ReviewDoc` `lost`/`changed` y 3 rutas de registro que no resuelven. Coincide con lo que ya reportaba la validacion del ejecutor; no suma errores de tags.
- `desk/drawer/tasks/task-e01-prueba-integral-multiagente-opsys-scion-ui-la-recibe-deskops-graph-ui-la-bota-de-su-drawer.md` sigue con `workspace:desk` y `artifact:task`. No aparece en `deskops tags migrate` porque los drawer tasks no estan trackeados en el store; si "documentos existentes" incluye el drawer, queda otra migracion pendiente.
- Medicion actual de `.sldb_cache/semantic_dag.yaml` en main: 224 nodos, 174 sin padre, 167 planos sin padre ni hijos, 164 planos con `:`. No coincide con el "despues" del informe del ejecutor (194/156/149) porque el cache no borra nodos y main recibio mas documentos; por si sola esta metrica no demuestra la limpieza.

## Correccion necesaria

1. Hacer que `deskops tags migrate --apply` reextraiga/reescriba **todos** los documentos trackeados (o al menos todos los del modelo cuya semantica cambio), no solo aquellos cuyo frontmatter `tags` cambia. Alternativa: invocar la operacion de sldb que reextrae los documentos del modelo (`sldb models update` de la familia `TaskDoc`/`TaskDocsDoc`) despues de la migracion.
2. Anadir un test de regresion: documento escrito con tags ya canonicos antes del cambio de `__semantics__`; tras `tags migrate --apply`, `sldb find board.tareas --in semantic --type doc` lo incluye.
3. Si sldb no tiene reextraccion/reindexado en bloque para los documentos de un modelo, ampliar la nota a sldb ya enviada.
4. Repetir la comprobacion: `board.tareas` debe dar 50, igual que `deskops list tasks`, y `board.tareas.ui` debe seguir dando 1.

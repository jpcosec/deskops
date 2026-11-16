FILE:desk/tasks/task-deskops-atoms-citations-escanea-las-citas-codigo-atomo-reporta-citas-rotas-y-atomos-sin-cita-y-las-l.md
---
sldb:
  by: agent
  at: '2026-11-16T05:03:35Z'
  authority: generated
  via: save_document_payload
id: task-deskops-atoms-citations-escanea-las-citas-codigo-atomo-reporta-citas-rotas-y-atomos-sin-cita-y-las-l
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/atoms.py
- deskops/cli/registry.py
- tests/test_atom_citations.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-chatbot-infra-indexar-las-citas-c-digo-atom-de-los-docstrings-en-el-grafo-y-huecos-de-atoms-vistos-en-la-auditor-a.md
---

# deskops atoms citations escanea las citas codigo->atomo, reporta citas rotas y atomos sin cita, y las lleva al grafo

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (Chatbot_Infra, 2026-10-21). Convencion en Chatbot_Infra, labchile_chatbots y shared_llm-gateway: el codigo cita sus atomos al final del docstring del modulo en un bloque 'Atoms:' con un id por linea en columna 0, y en archivos no Python como comentario '# Atom: <id>'. Cada repo tiene su propio tests/test_atoms_citados.py. Hoy deskops no tiene verbo para esto (deskops/cli/registry.py:1155-1421).

## Goal

_Describe the concrete result this task must produce._

`deskops atoms citations [--check] [--write] --root .`: escanea **/*.py (bloque Atoms: del docstring de modulo) y '# Atom: <id>' en el resto de archivos versionados (git ls-files); --check sale con 1 si un id citado no existe en desk/atoms y avisa (exit 0) por cada atomo sin cita; --write registra una arista cited_by modulo->atomo en el grafo de sldb para que `deskops show atom <id>` liste los modulos que lo citan.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/atoms.py, deskops/cli/registry.py (verbo nuevo y su ayuda), el tipo de relacion cited_by si hay que declararlo, deskops/graph/checks.py si graph missing debe reportar citas rotas, y tests. No entra: cambiar los repos de AntonIA, renombrar atomos (otra tarea). Precisiones del preflight 1: --check sale con 1 si hay al menos una cita rota, aunque tambien haya huerfanos; con solo huerfanos sale con 0 y los lista como aviso. Gramatica del bloque: en el docstring de modulo, una linea exactamente 'Atoms:' seguida de lineas con un id cada una (regex ^atom-[a-z0-9-]+$, en columna 0); el bloque termina en la primera linea vacia o en el fin del docstring; una linea que no cumple la regex termina el bloque. En otros archivos: lineas que contienen '# Atom: <id>' con la misma regex para el id. Se escanean los archivos de git ls-files; los que no decodifican como UTF-8 se saltan. --write crea un RelationTypeDoc cited_by (si no existe) y un RelationDoc por cita con sujeto la ruta del archivo y objeto el id del atomo, por la API de sldb. show atom agrega una seccion 'Cited by:' con las rutas, leida de esas RelationDoc.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Parser de citas con ast para .py y regex para el resto. 2) --check con codigos de salida. 3) --write con RelationDoc cited_by por la API de sldb. 4) show atom lista los citadores. 5) Tests con un repo sandbox: cita valida, cita rota (exit 1), atomo huerfano (aviso).

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_citations.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_checks.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los tres casos del test pasan; show atom muestra los citadores tras --write; goldens de ayuda al dia.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-atoms-citations-escanea-las-citas-codigo-atomo-reporta-citas-rotas-y-atomos-sin-cita-y-las-l: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


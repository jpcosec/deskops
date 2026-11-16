FILE:desk/tasks/task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y.md
---
sldb:
  by: agent
  at: '2026-11-16T06:16:26Z'
  authority: generated
  via: save_document_payload
id: task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-012942-suggestion-project-graph-de-deskops-sldb-ya-ofrece-closed-como-predicado-y-declared-file-targets-desv-os-h1-h2-de-cc33c.md
depends_on: []
pills: []
files:
- deskops/graph/desk_graph.py
- deskops/graph/checks.py
- tests/test_graph_checks.py
- tests/test_graph_declared_edges.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-knowledge-graph-connects-desk-and-source-files
---

# deskops declara su project_graph con closed y declared_file_targets de sldb y borra los desvios H1 y H2 de CC33c

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de sldb del 2026-11-16 (triaje de su drawer). Desde GD21 (a2a0174f) sldb ofrece dos capacidades que deskops emula con codigo propio desde CC33c: H2, la superficie de documentos de project_graph acepta closed: como predicado del lenguaje de reglas (sldb src/sldb/api/edges/project_graph/document_surface.py:25, evaluado en project_texts.py:41-48; config_to_mapping rechaza un callable y apunta a closed:, project_graph_config_mapping.py:18 y 32-33); H1, declared_file_targets convierte en nodos los archivos existentes que no son documento (project_graph_config.py:38, declared_file_targets.py, declared_target_nodes.py; test tests/api/test_project_graph.py:60). deskops todavia usa declared_target_is_a_file (deskops/graph/checks.py:63) y closed_document=_closed_issue (deskops/graph/desk_graph.py:204).

## Goal

_Describe the concrete result this task must produce._

La configuracion de project_graph que deskops arma en deskops/graph/desk_graph.py usa closed: (predicado del lenguaje de reglas de sldb, con la misma condicion que hoy evalua _closed_issue) en lugar de closed_document=_closed_issue, y declara declared_file_targets para los archivos existentes que no son documento; declared_target_is_a_file y _closed_issue desaparecen. `deskops graph missing --root .` da el mismo resultado que antes del cambio en el desk de deskops (misma lista de faltantes). Si algun destino que hoy cubre declared_target_is_a_file (p. ej. dag.yaml o tests/fixtures/model_contract_hashes.json) no se puede declarar con declared_file_targets porque no sale de un campo de frontmatter de un glob de documentos, se manda deskops message send --to sldb con el caso y ese destino conserva su tratamiento actual.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/graph/desk_graph.py, deskops/graph/checks.py y sus tests (tests/test_graph_checks.py, tests/test_graph_declared_edges.py). Antes de cambiar, guardar la salida de deskops graph missing --root . en runs/subagents/<run>/graph-missing-antes.txt para comparar. No entra: cambiar sldb, declarar project_graph en .sldb/store.yaml a mano (la config se arma en codigo como hoy). Precisiones del preflight 1: la condicion de _closed_issue se lee en desk_graph.py y se traduce a la sintaxis closed: que documenta sldb (docs/architecture del repo sldb y tests/api/test_project_graph.py). DeclaredFileTargets de sldb exige directory y field: se declara uno por cada carpeta del desk cuyos documentos nombran archivos en un campo de frontmatter (al menos desk/materializations con field target_identity). Un destino es no declarable si no sale de un campo de frontmatter de documentos de una carpeta (p. ej. dag.yaml, tests/fixtures/model_contract_hashes.json): para esos se manda la nota a sldb con la ruta y quien la referencia, y conservan el tratamiento actual. La corrida se llama runs/subagents/project-graph-<AAAAMMDD>/. La comparacion de graph missing es por conjunto de lineas (orden indistinto).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer los archivos de sldb citados y desk_graph.py:180-215, checks.py:55-90. 2) Traducir _closed_issue a una condicion closed:. 3) Armar declared_file_targets. 4) Borrar el codigo viejo. 5) Comparar graph missing antes y despues (diff vacio). 6) Tests.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_checks.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_declared_edges.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (mismo conjunto de lineas que graph-missing-antes.txt)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rn 'declared_target_is_a_file\|_closed_issue' deskops
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas = cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El grep queda vacio, graph missing da la misma salida que antes y los tests pasan (o hay nota a sldb por un destino no declarable).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


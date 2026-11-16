FILE:desk/tasks/task-closeout-reconoce-una-materialization-declarada-sobre-un-golden-en-tests-fixtures-sin-dejar-entrar-e.md
---
sldb:
  by: agent
  at: '2026-11-16T04:01:11Z'
  authority: generated
  via: create_document
id: task-closeout-reconoce-una-materialization-declarada-sobre-un-golden-en-tests-fixtures-sin-dejar-entrar-e
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
- deskops/graph/desk_graph.py
- tests/test_desk_graph_runs_target.py
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-closeout-declared-fixture-materialization-coverage.md
---

# closeout reconoce una materialization declarada sobre un golden en tests/fixtures sin dejar entrar el ruido de fixtures

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (nacido en c6abcf9a): un golden genuino bajo tests/fixtures respaldado por un atomo no lo reconoce el closeout, porque deskops/graph/desk_graph.py:85 excluye tests/fixtures y, segun la auditoria del 2026-11-16, sldb src/sldb/api/edges/project_graph/declared_target_nodes.py:55 aplica esa exclusion tambien a los targets declarados. Hay que confirmar donde corta antes de cambiar.

## Goal

_Describe the concrete result this task must produce._

Reproducir y corregir: una MaterializationContractDoc cuyo target_identity es un .txt bajo tests/fixtures es nodo del grafo y cubre ese archivo en closeout; los archivos de tests/fixtures no declarados siguen excluidos. Si el corte esta en sldb, la parte de sldb se pide por `deskops message send --to sldb` y en deskops se deja el test marcado xfail con el id de esa nota.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/graph/desk_graph.py (EXCLUSIONS y MATERIALIZATION_TARGETS, alrededor de 83-93), un test de regresion y el recibo de reproduccion. No entra: modificar sldb directamente.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Desk sandbox con un atomo, una materialization a tests/fixtures/golden.txt y un cambio en ese archivo; correr `deskops graph missing` y `deskops closeout verify`; guardar la salida como recibo (`deskops review record <tarea> --kind reproduction --evidence <archivo> --reason ...`). 2) Ubicar el corte. 3) Corregir en deskops o pedir a sldb. 4) Test de regresion en tests/test_desk_graph_runs_target.py.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_desk_graph_runs_target.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_materialization_targets_outside_package.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_declared_edges.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

Hay recibo de reproduccion; el test de regresion cubre el golden declarado y un archivo de fixtures no declarado sigue excluido (o queda xfail citando la nota a sldb).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-closeout-reconoce-una-materialization-declarada-sobre-un-golden-en-tests-fixtures-sin-dejar-entrar-e: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


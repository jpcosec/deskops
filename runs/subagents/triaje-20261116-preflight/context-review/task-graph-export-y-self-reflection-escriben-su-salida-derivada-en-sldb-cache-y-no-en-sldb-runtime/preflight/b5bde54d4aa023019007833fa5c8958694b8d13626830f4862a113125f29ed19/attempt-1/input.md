FILE:desk/tasks/task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime.md
---
sldb:
  by: agent
  at: '2026-11-16T04:03:17Z'
  authority: generated
  via: save_document_payload
id: task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261104-233657-suggestion-sldb-el-store-pasa-a-sldb-versionado-y-sldb-cache-ignorada-journal-retirado.md
depends_on: []
pills:
- desk/contexts/pill-010-graph-runtime-output-policy.md
files:
- deskops/graph/export.py
- deskops/graph/self_reflection.py
- tests/test_graph_snapshot.py
- tests/test_graph_self_reflection.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# graph export y self_reflection escriben su salida derivada en .sldb_cache y no en .sldb/runtime

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de sldb (c420809c, 2026-11-04): el store es .sldb/ versionado y lo derivado vive en .sldb_cache/, ignorada. deskops todavia escribe salidas derivadas en la ruta vieja .sldb/runtime/, que ya no esta ignorada: deskops/graph/export.py:22 y deskops/graph/self_reflection.py:17-18 y 39.

## Goal

_Describe the concrete result this task must produce._

Las salidas de graph export y self_reflection van a .sldb_cache/ (misma estructura de subcarpetas); nada en deskops/ escribe en .sldb/runtime/. Si algun consumidor fuera de deskops lee la ruta vieja, se le avisa por inbox.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/graph/export.py, deskops/graph/self_reflection.py, sus tests (tests/test_graph_snapshot.py, tests/test_graph_self_reflection.py) y tests/test_gitignore_policy.py si hace falta. Consumidores a revisar con `grep -rn '.sldb/runtime' /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui --include=*.py --include=*.js` (excluyendo runs/); si hay, `deskops message send --to graph_ui`. No entra: migrar archivos viejos ya escritos (se borran a mano solo si no estan versionados), tocar sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) `grep -rn 'sldb/runtime\|"runtime"' deskops/graph deskops/services`. 2) Cambiar las rutas a una constante comun que apunte a .sldb_cache. 3) Ajustar los tests. 4) Revisar consumidores en graph_ui.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_self_reflection.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_gitignore_policy.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rn 'sldb/runtime' deskops/ --include=*.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

El grep de deskops/ no encuentra .sldb/runtime; los tests listados pasan; consumidores avisados si los hubo.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


FILE:desk/tasks/task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global.md
---
sldb:
  by: agent
  at: '2026-11-16T04:03:04Z'
  authority: generated
  via: create_document
id: task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261106-171908-suggestion-tests-fixture-autouse-que-limpia-los-caches-globales-de-sldb-despu-s-de-cada-test.md
depends_on: []
pills: []
files:
- tests/conftest.py
- deskops/doc_access.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# La suite de deskops en un solo proceso cabe en MemoryMax=2G: fixture autouse limpia los caches globales

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del 2026-11-06 (overlord): la suite completa de deskops en un proceso crece a 3-6 GB porque los caches de sldb son globales del proceso y tests/conftest.py no los limpia; con MemoryMax=2G muere por OOM. Hoy se mitiga con pytest -n 4 (xdist).

## Goal

_Describe the concrete result this task must produce._

tests/conftest.py tiene una fixture autouse que despues de cada test llama a sldb.store.runtime_cache.invalidate_runtime_cache(), sldb.store.io.invalidate_index_cache(), sldb.store.built_cache.clear() y sldb.cli.alert_sink.forget(), y vacia los caches propios de deskops en deskops/doc_access.py (alrededor de las lineas 150-154). La suite completa en un proceso termina bajo MemoryMax=2G.

## Scope

_State what is in scope and what is out of scope._

Entra: tests/conftest.py (la unica autouse hoy es _isolated_home, linea 46) y, si hace falta, una funcion publica de limpieza en deskops/doc_access.py. Las funciones de sldb existen en sldb/src/sldb/store/runtime_cache.py:105, store/io/__init__.py:53, store/built_cache.py:66 y cli/alert_sink.py:52; si alguna no existe con ese nombre en el sldb hermano, se llama a la equivalente y se anota. No entra: cambiar sldb ni la regla de correr con -n 4.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Fixture `_clear_global_caches` autouse con yield y limpieza despues. 2) Medir: correr la suite en un proceso bajo systemd-run con MemoryMax=2G. 3) Si no cabe, perfilar con tracemalloc los 3 archivos mas pesados y limpiar el cache que falte.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && systemd-run --user --scope -p MemoryMax=2G env TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:xdist tests (rc igual al de main con -n 4; sin OOM)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

La corrida en un proceso con MemoryMax=2G termina sin OOM y con las mismas fallas que main con -n 4.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


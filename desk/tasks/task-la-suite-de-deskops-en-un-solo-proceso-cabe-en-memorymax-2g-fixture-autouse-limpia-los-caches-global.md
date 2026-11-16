---
sldb:
  by: agent
  at: '2026-11-16T06:04:00Z'
  authority: generated
  via: save_document_payload
id: task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
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

Entra: tests/conftest.py (la unica autouse hoy es _isolated_home, linea 46). No se agrega API a deskops: la fixture vacia con .clear() los dicts de modulo _READ_HASHES e _INDEX_ENTRIES de deskops/doc_access.py. Las funciones de sldb son sldb.store.runtime_cache.invalidate_runtime_cache, sldb.store.io.invalidate_index_cache, sldb.store.built_cache.clear y sldb.cli.alert_sink.forget; si alguna no existe con ese nombre en /mnt/ssd/proyectos/SLDB_1/sldb/src, la tarea se detiene en ese punto y lo reporta (no se busca una equivalente). No entra: cambiar sldb ni la regla de correr con -n 4.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Fixture _clear_global_caches autouse con yield y limpieza despues. 2) Correr la suite en un proceso bajo systemd-run con MemoryMax=2G. 3) Si no cabe, medir el RSS maximo por archivo de test (un proceso por archivo con /usr/bin/time -f %M) y, en los 3 archivos de mayor RSS, buscar con tracemalloc el cache que crece y limpiarlo en la misma fixture.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && systemd-run --user --scope -p MemoryMax=2G env TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:xdist tests (sin OOM; las fallas son las mismas que da -n 4 en un worktree limpio de origin/main)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

La corrida en un proceso con MemoryMax=2G termina sin OOM y con las mismas fallas que main con -n 4.

FILE:desk/tasks/task-deskops-init-agrega-deskops-log-al-gitignore-del-repo.md
---
sldb:
  by: agent
  at: '2026-11-21T06:38:33Z'
  authority: generated
  via: save_document_payload
id: task-deskops-init-agrega-deskops-log-al-gitignore-del-repo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261119-220154-suggestion-init-no-ignora-deskops-log.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops init agrega .deskops.log al .gitignore del repo

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de hbc_latina en el inbox (20261119-220154): deskops init deja en el .gitignore la linea del cache que pone sldb, pero no .deskops.log, que OperationsService._setup_logging (deskops/operations.py:74) escribe en la raiz del repo en cada comando; en hbc_latina hubo que agregarla a mano.

## Goal

_Describe the concrete result this task must produce._

Despues de deskops init en un repo git, el .gitignore raiz contiene una linea .deskops.log (una sola vez, sin duplicarla si ya estaba) y git status no muestra .deskops.log como no trackeado tras correr cualquier comando de deskops.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/bootstrap.py (el camino de init que llama a sldb.api.init_store en _init_store, alrededor de la linea 348) y un test en tests/test_gitignore_policy.py. No entra: mover el log fuera de la raiz ni cambiar sldb (ensure_cache_ignored es de sldb; deskops agrega su propia linea con la misma idea idempotente).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer deskops/bootstrap.py y tests/test_gitignore_policy.py. 2) Tras init_store, asegurar idempotentemente la linea .deskops.log en el .gitignore raiz (crearlo si no existe). 3) Test: init en un repo temporal, la linea esta una vez; segundo init no la duplica; un .gitignore previo con la linea queda igual.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_gitignore_policy.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_runtime_initializer.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; cada falla se corre igual en un worktree limpio de origin/main y solo se acepta si falla igual ahi, listada en la entrega)

## Done When

_Name the observable condition that makes the task complete._

El test nuevo de tests/test_gitignore_policy.py pasa: init deja .deskops.log en el .gitignore una sola vez y no lo duplica en un segundo init.

FILE:instruccion
Cold-bundle de la tarea task-deskops-init-agrega-deskops-log-al-gitignore-del-repo: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_gitignore_policy.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_runtime_initializer.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; cada falla se corre igual en un worktree limpio de origin/main y solo se acepta si falla igual ahi, listada en la entrega)


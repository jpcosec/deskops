Task: task-build-neighbours-de-absolute-paths-resuelve-el-path-del-registro-con-resolve-registered-root-y-expan
Title: build_neighbours de absolute_paths resuelve el path del registro con resolve_registered_root y expande la virgulilla
Status: active
Current node: ritual-testing
Task type: task.code
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-repo-register-accepts-explicit-path-and-registry-errors-name-the-fix
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-20T11:56:46Z'
  authority: generated
  via: save_document_payload
id: task-build-neighbours-de-absolute-paths-resuelve-el-path-del-registro-con-resolve-registered-root-y-expan
status: active
summary: ''
tags:
- host:robocop2
current_node: ritual-testing
history:
- task_activates
references:
- runs/subagents/test-deskops-t-a8ebbb84ed77/verdict.md
depends_on: []
pills: []
files:
- deskops/absolute_paths.py
- tests/test_doctor_absolute_paths.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-repo-register-accepts-explicit-path-and-registry-errors-name-the-fix
---

# build_neighbours de absolute_paths resuelve el path del registro con resolve_registered_root y expande la virgulilla

## Rationale

_Explain why this task exists or the business driver behind it._

Seguimiento del cierre de repo register (24a50d44, closeout 38f92120): ahora doc_access.repository_root resuelve las entradas del registro con deskops.identity.resolve_registered_root, que expande la virgulilla y resuelve rutas relativas contra la raiz del repo del registro. build_neighbours en deskops/absolute_paths.py (fuera de los files de esa tarea) todavia resuelve el path a mano sin expandir la virgulilla, asi que una entrada vieja escrita a mano con la virgulilla da un vecino mal resuelto y doctor la reporta dos veces (por absolute_paths y por el chequeo de registro), como pasa con Chatbot_Infra.

## Goal

_Describe the concrete result this task must produce._

build_neighbours resuelve cada entrada del registro con resolve_registered_root, igual que doc_access.repository_root; una entrada con la virgulilla o relativa resuelve al mismo directorio por los dos caminos.

## Scope

_State what is in scope and what is out of scope._

Entra: build_neighbours en deskops/absolute_paths.py y tests en tests/test_doctor_absolute_paths.py. Sale: el formato de RepositoryDoc, repo register y el chequeo de registro de doctor (ya cerrados).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer build_neighbours y como arma la ruta de cada vecino. 2) Reemplazar la resolucion a mano por resolve_registered_root. 3) Test en desk sandbox (tmp_path) con una entrada de registro con la virgulilla (HOME apuntado al sandbox) y otra relativa: build_neighbours y doc_access.repository_root dan el mismo directorio.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_doctor_absolute_paths.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_registry_robustness.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa (mismo directorio por los dos caminos para una entrada con la virgulilla y una relativa) y los dos archivos de la Validation pasan.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-build-neighbours-de-absolute-paths-resuelve-el-path-del-registro-con-resolve-registered-root-y-expan"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

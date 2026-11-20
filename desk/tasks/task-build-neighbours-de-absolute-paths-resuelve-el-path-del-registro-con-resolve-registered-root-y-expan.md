---
sldb:
  by: agent
  at: '2026-11-20T12:15:43Z'
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
- deskops/absolute_paths.py
- tests/test_doctor_absolute_paths.py
- 342b22e9cb92838ad8fd8c0332af5732d47b221d
depends_on: []
pills: []
files:
- deskops/absolute_paths.py
- tests/test_doctor_absolute_paths.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-build-neighbours-de-absolute-paths-resuelve-el-registro-con-resolve-registered-root
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

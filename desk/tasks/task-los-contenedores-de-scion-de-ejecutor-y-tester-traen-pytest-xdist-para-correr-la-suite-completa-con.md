---
sldb:
  by: agent
  at: '2026-11-22T08:15:32Z'
  authority: generated
  via: save_document_payload
id: task-los-contenedores-de-scion-de-ejecutor-y-tester-traen-pytest-xdist-para-correr-la-suite-completa-con
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- deskops/runtime/scion.py
- pyproject.toml
- tests/test_scion_runtime.py
- 5270f990b113b49341ac23e25ddac76622eb0807
depends_on: []
pills: []
files:
- deskops/runtime/scion.py
- pyproject.toml
- tests/test_scion_runtime.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-los-contenedores-de-scion-traen-pytest-xdist-y-la-suite-completa-corre-con-n-4
---

# Los contenedores de scion de ejecutor y tester traen pytest-xdist para correr la suite completa con -n 4

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: los ejecutores de deskops (deskops-e-4ee2bde35767, deskops-e-e70b6cd9c7de) corrieron la suite completa sin -n 4 porque pytest-xdist no está instalado en el venv del contenedor, y tardaron más de una hora esperándola. Las tareas piden la suite completa antes de entregar con -n 4, que en el host tarda unos 22 minutos.

## Goal

_Describe the concrete result this task must produce._

El venv que usan los roles executor y tester en los contenedores de scion trae pytest-xdist instalado (en la imagen o en el paso de preparación del runtime template de scion), y el prompt de esos roles corre la suite completa con -n 4.

## Scope

_State what is in scope and what is out of scope._

Dentro: el runtime template o la imagen de scion de deskops (deskops/templates o la configuración del rol en desk/roles) y su test. Fuera: el resto.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: localizar dónde se arma el venv del contenedor (grep -rn 'venv\|pip install' en los templates de scion de deskops). p2: agregar pytest-xdist. p3: test o comprobación de que python -c 'import xdist' funciona en un contenedor lanzado con el template. p4: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

Un ejecutor lanzado con el template importa xdist y corre la suite con -n 4.

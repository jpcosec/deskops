Task: task-los-contenedores-de-scion-de-ejecutor-y-tester-traen-pytest-xdist-para-correr-la-suite-completa-con
Title: Los contenedores de scion de ejecutor y tester traen pytest-xdist para correr la suite completa con -n 4
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-22T08:03:19Z'
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
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-los-contenedores-de-scion-de-ejecutor-y-tester-traen-pytest-xdist-para-correr-la-suite-completa-con"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

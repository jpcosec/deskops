Task: task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej
Title: dispatch deja commiteados los RunDoc que escribe, para que el reap pueda traer al main commits del ejecutor que tocan el store
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
  at: '2026-11-21T07:09:26Z'
  authority: generated
  via: save_document_payload
id: task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej
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

# dispatch deja commiteados los RunDoc que escribe, para que el reap pueda traer al main commits del ejecutor que tocan el store

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21, sldb: el reap de la tarea notations validate falló al hacer cherry-pick de deskops/deskops-e-8eb91b4956b3 sobre main: 'Los cambios locales de los siguientes archivos serán sobrescritos: .sldb/core/store_index.yaml'. dispatch start (record_scion_run) escribe el RunDoc del agente en el store del checkout principal (store.yaml, store_index.yaml, models/RunDoc.yaml y el shard) y no lo commitea. Si el commit del ejecutor también toca el store (por ejemplo, selfdoc sync), el cherry-pick choca. El coordinador tuvo que commitear los RunDoc a mano y re-encolar el reap.

## Goal

_Describe the concrete result this task must produce._

Ningún reap falla porque el checkout principal tenga sin commitear el store que escribió dispatch. dispatch start commitea en la rama principal, con pathspec, solo los archivos del store que record_scion_run tocó ('git commit -- <rutas>', mensaje 'run: <agente>' y [skip ci]). Además, reap, antes del cherry-pick, commitea igual cualquier RunDoc pendiente de sus agentes. Si queda otro cambio local que choca, el mensaje de error nombra los archivos y sugiere commitearlos.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/dispatch.py (start y reap) o deskops/runtime/scion.py (record_scion_run), tests/test_dispatch.py y CHANGELOG. Fuera: el resto.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: un repo temporal con store, start escribe el RunDoc, el ejecutor (simulado) commitea en su rama un cambio a store_index.yaml, y reap trae el commit sin error. p2: implementar el commit con pathspec en start, y en reap antes del cherry-pick. p3: CHANGELOG, y commit con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo y tests/test_dispatch.py pasan.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

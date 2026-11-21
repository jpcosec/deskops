Task: task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe
Title: dispatch start no falla si el RunDoc de la identidad ya está trackeado y su run_dir no existe
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
  at: '2026-11-21T22:45:44Z'
  authority: generated
  via: save_document_payload
id: task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe
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

# dispatch start no falla si el RunDoc de la identidad ya está trackeado y su run_dir no existe

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-20, dos veces (sldb con run-deskops-e-9c1e01636d14 y deskops con run-deskops-t-1551a4c10d58): un dispatch de otra sesión dejó trackeado en el store el RunDoc de una identidad cuyo run_dir ya no existe. dispatch start ve que el run_dir no existe, usa esa identidad, crea la carpeta y falla en record_scion_run con 'Store error: Doc run-... already tracked'. La cola deja el trabajo en failed y queda una carpeta vacía. El coordinador tuvo que hacer 'sldb docs untrack', borrar la carpeta y re-encolar a mano.

## Goal

_Describe the concrete result this task must produce._

dispatch start, antes de usar una identidad cuyo run_dir no existe, mira si su RunDoc ya está trackeado. Si lo está, lo actualiza o lo re-trackea con force para el run nuevo, y sigue sin error. Si un fallo deja una carpeta vacía, se borra. Un RunDoc trackeado con su run_dir presente sigue contando como intento hecho, como hoy.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/dispatch.py (start y el paso de record_scion_run) o deskops/runtime/scion.py (record_scion_run), tests/test_dispatch.py y CHANGELOG. Fuera: el resto de dispatch.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: un store con el RunDoc run-<name> trackeado y sin run_dir; start lanza (con _scion simulado) y no falla. p2: implementar con track forzado o update del RunDoc. p3: CHANGELOG, y commit con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo y tests/test_dispatch.py pasan.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

Task: task-integrate-no-intenta-empujar-el-sha-de-codigo-cuando-ya-es-ancestro-de-origin-main
Title: integrate no intenta empujar el sha de código cuando ya es ancestro de origin/main
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
  at: '2026-11-20T05:35:54Z'
  authority: generated
  via: save_document_payload
id: task-integrate-no-intenta-empujar-el-sha-de-codigo-cuando-ya-es-ancestro-de-origin-main
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

# integrate no intenta empujar el sha de código cuando ya es ancestro de origin/main

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-20, sldb: el integrate de la tarea sldb move falló con 'fallo:push' porque git rechazó 'git push origin bc05f2ab:main' como non-fast-forward. Ese commit ya estaba en origin, porque el integrate de otra tarea empujó la punta local que lo contenía. integrate empuja primero el sha de código y después la punta; si el código ya está en origin, el primer push retrocede main y git lo rechaza. El coordinador tuvo que empujar la punta a mano.

## Goal

_Describe the concrete result this task must produce._

integrate saltea el push del sha de código cuando ya es ancestro de origin/main (git merge-base --is-ancestor), lo informa ('código ya en origin: <sha>') y sigue con la suite, los checks y el push de la punta. Si el sha no es ancestro, todo sigue como hoy.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/integrate.py (el paso de push) y su test; CHANGELOG. Fuera: el resto de integrate.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: un repo con remoto donde origin/main ya contiene el commit de código; integrate debe terminar ok y empujar solo la punta. p2: implementar con git merge-base --is-ancestor <sha> origin/<branch> después del fetch. p3: CHANGELOG; commit con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo y los de integrate pasan; la suite completa la corre integrate.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-integrate-no-intenta-empujar-el-sha-de-codigo-cuando-ya-es-ancestro-de-origin-main"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

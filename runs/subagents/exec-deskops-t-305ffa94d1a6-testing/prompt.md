Task: task-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript-test-ts-test-tsx-spec-ts-declara
Title: El gate de tests del closeout acepta archivos de test de TypeScript (*.test.ts, *.test.tsx, *.spec.ts) declarados en files
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
  at: '2026-11-23T19:27:59Z'
  authority: generated
  via: save_document_payload
id: task-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript-test-ts-test-tsx-spec-ts-declara
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

# El gate de tests del closeout acepta archivos de test de TypeScript (*.test.ts, *.test.tsx, *.spec.ts) declarados en files

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-23: sldb task-surface-trae-el-lector-de-documentos-de-minegocio-... (commit 3cc5c36b, solo surface/, tsc y vitest con 471 tests verdes) no puede cerrar: closeout verify da missing_tests_evidence porque CloseoutGates.reference_points_to_test (deskops/services/closeout_gates.py:166) solo acepta archivos .py bajo tests/ o declarados en files. Una tarea de frontend con tests de vitest queda sin forma de cerrar por el camino normal.

## Goal

_Describe the concrete result this task must produce._

reference_points_to_test acepta tambien archivos existentes con sufijo .test.ts, .test.tsx, .spec.ts o .spec.tsx dentro del repo (fuera de node_modules y directorios ocultos), en un directorio de tests o declarados en files; closeout verify de una tarea cuyo commit trae tests de vitest pasa el gate de tests.

## Scope

_State what is in scope and what is out of scope._

deskops/services/closeout_gates.py y sus tests; el mensaje de rechazo nombra los sufijos aceptados. Fuera: correr los tests de JS desde deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test: un archivo surface/src/x.test.ts declarado en files cuenta como evidencia; uno en node_modules no. 2) Ampliar la comprobacion de sufijo. 3) Actualizar el mensaje de Unresolvable --test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp pytest -q tests/test_closeout_test_paths.py tests/test_closeout_gates.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan y los del closeout siguen verdes.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript-test-ts-test-tsx-spec-ts-declara"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-305ffa94d1a6"

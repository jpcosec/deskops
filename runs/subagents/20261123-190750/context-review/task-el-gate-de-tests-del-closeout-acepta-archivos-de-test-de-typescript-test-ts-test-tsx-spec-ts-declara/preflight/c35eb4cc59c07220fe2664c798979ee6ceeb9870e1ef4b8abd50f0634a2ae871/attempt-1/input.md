FILE:desk/tasks/task-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript-test-ts-test-tsx-spec-ts-declara.md
---
sldb:
  by: agent
  at: '2026-11-23T19:07:33Z'
  authority: generated
  via: create_document
id: task-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript-test-ts-test-tsx-spec-ts-declara
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
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

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript-test-ts-test-tsx-spec-ts-declara: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


---
sldb:
  by: agent
  at: '2026-11-25T18:30:29Z'
  authority: generated
  via: save_document_payload
id: task-el-gate-de-tests-del-closeout-acepta-pruebas-de-node-test-mjs-test-js-spec-mjs-y-spec-js
status: draft
summary: ''
tags: []
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

# El gate de tests del closeout acepta pruebas de node: .test.mjs, .test.js, .spec.mjs y .spec.js

## Rationale

_Explain why this task exists or the business driver behind it._

En graph_ui las pruebas unitarias son node --test sobre tests/*.test.mjs; CloseoutGates.reference_points_to_test (deskops/services/closeout_gates.py) solo acepta .py, .test.ts(x) y .spec.ts(x), asi que una tarea con prueba node no puede cerrar por commit (G-B1 de graph_ui, 2026-11-25, se cerro por supersede).

## Goal

_Describe the concrete result this task must produce._

Que _is_test_suffix acepte tambien .test.mjs, .test.js, .spec.mjs y .spec.js, con las mismas reglas de ubicacion (bajo tests/ o declarado en files).

## Scope

_State what is in scope and what is out of scope._

deskops/services/closeout_gates.py y su test. Fuera: el resto de gates.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/deskops. Extender _is_test_suffix (y el docstring de reference_points_to_test) con .test.mjs, .test.js, .spec.mjs y .spec.js. Test: agregar casos en el test existente del gate de tests (buscar con grep reference_points_to_test en tests/) para un .test.mjs bajo tests/ que cuenta y un .mjs que no es test que no cuenta. No poner Task-Id en el commit de codigo.

Aclaraciones de la revisión: El test existente es tests/test_closeout_test_paths.py. Casos: los cuatro sufijos (.test.mjs, .test.js, .spec.mjs, .spec.js) cuentan bajo tests/ y cuentan si están declarados en files de la tarea; un .mjs que no es test no cuenta. 'Declarado en files' = la ruta aparece literal en el campo files del TaskDoc, igual que hoy para .test.ts. Mensaje del commit en el estilo del repo (feat:/fix:), sin trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=. pytest -q -k reference_points_to_test tests

## Done When

_Name the observable condition that makes the task complete._

Una referencia a tests/x.test.mjs cuenta como evidencia de tests y un .mjs comun no; el test del gate pasa.

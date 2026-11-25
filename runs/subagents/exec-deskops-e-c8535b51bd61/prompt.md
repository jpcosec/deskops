Task: task-el-gate-de-tests-del-closeout-acepta-pruebas-de-node-test-mjs-test-js-spec-mjs-y-spec-js
Title: El gate de tests del closeout acepta pruebas de node: .test.mjs, .test.js, .spec.mjs y .spec.js
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-el-gate-de-tests-del-closeout-acepta-pruebas-de-node-test-mjs-test-js-spec-mjs-y-spec-js: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") (seen: {}) (witness: ReviewDoc:review-task-el-gate-de-tests-del-closeout-acepta-pruebas-de-node-test-mjs-test-js-spec-mjs-y-spec-js-bundle-1 {"anchor_state":"changed"})

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

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-el-gate-de-tests-del-closeout-acepta-pruebas-de-node-test-mjs-test-js-spec-mjs-y-spec-js"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-c8535b51bd61"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-c8535b51bd61`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-c8535b51bd61

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

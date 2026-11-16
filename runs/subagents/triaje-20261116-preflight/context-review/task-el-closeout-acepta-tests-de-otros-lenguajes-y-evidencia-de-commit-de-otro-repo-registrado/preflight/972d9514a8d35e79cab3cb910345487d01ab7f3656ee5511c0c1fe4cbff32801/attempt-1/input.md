FILE:desk/tasks/task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado.md
---
sldb:
  by: agent
  at: '2026-11-16T04:14:28Z'
  authority: generated
  via: create_document
id: task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-005144-suggestion-closeout-el-gate-de-tests-solo-acepta-py-y-el-de-commit-solo-el-repo-del-desk-tareas-go-bash-o-con-c-digo-en-otro.md
depends_on: []
pills: []
files:
- deskops/services/closeout_gates.py
- deskops/services/closure.py
- docs/workflow-policy-reference.md
- tests/test_closeout_gates.py
- tests/test_closeout_resolved_by.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# El closeout acepta tests de otros lenguajes y evidencia de commit de otro repo registrado

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de scion del 2026-11-16 (triaje del desk de scion). Tres tareas de la fase 0 del piloto scion estan hechas y verificadas pero closeout commit las bloquea: (1) el test es Go (cmd/build_context_test.go, commit f6e623c69 en scion) y reference_points_to_test en deskops/services/closeout_gates.py (linea 148; el chequeo de sufijo .py esta en la 168) exige .py; (2) un hook bash (hooks/pre-start-deskops.sh) validado con docker run no tiene forma de declarar su test; (3) una tarea del desk de scion cuyo codigo entro en deskops (4a7707a5, 4c745c18, 881e177a) e IR (5b8ce32): reference_points_to_commit (linea 196) solo resuelve ancestros del repo del desk. resolved-by tambien exige .py.

## Goal

_Describe the concrete result this task must produce._

(1) reference_points_to_test acepta, ademas de test_*.py, archivos de test de otros lenguajes con convencion reconocible (*_test.go, *.test.sh, *.bats) que existan en el repo; (2) una referencia de validacion de la forma runs/<run>/validation.log (archivo existente con el comando y su salida) cuenta como evidencia de tests para artefactos sin framework de tests; (3) una referencia repo:<nombre>@<sha> cuenta como evidencia de commit si <nombre> esta en el registro de repos (deskops repo / registro del ecosistema), su raiz existe en esta maquina y <sha> es ancestro de su HEAD. Lo mismo vale para closeout resolved-by.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/closeout_gates.py, deskops/services/closure.py (rama resolved-by), la doc de evidencia en docs/workflow-policy-reference.md y tests nuevos en tests/test_closeout_gates.py y tests/test_closeout_resolved_by.py. No entra: cerrar las tres tareas de scion (lo hace su coordinador despues), cambiar que evidencia exige cada tipo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer closeout_gates.py:140-260. 2) Tabla de sufijos de test por lenguaje. 3) Validacion por log en runs/. 4) Resolver repo:<nombre>@<sha> con la misma funcion que usa message send --to (registro propio y luego el del ecosistema) y `git -C <raiz> merge-base --is-ancestor <sha> HEAD`. 5) Tests: un _test.go en files pasa; un .txt cualquiera no; un validation.log en runs/ pasa; repo:sldb@<sha ancestro> pasa y un sha inexistente no. 6) Nota a scion con el hash.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_resolved_by.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_test_paths.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

Los casos del paso 5 pasan, la doc de evidencia describe las tres formas nuevas y la nota a scion esta enviada con el hash.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


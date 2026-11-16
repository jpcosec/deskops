---
sldb:
  by: agent
  at: '2026-11-16T15:27:04Z'
  authority: generated
  via: save_document_payload
id: task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-095909-suggestion-closeout-marcado-ui-ts-vitest-bloqueado-por-el-gate-de-tests-solo-py-sumar-test-ts-test-tsx.md
- desk/inbox/20261116-102357-unclear-el-gate-de-tests-solo-py-bloquea-todo-el-desk-sldb-ui-vitest.md
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

(1) reference_points_to_test acepta, ademas de test_*.py, archivos con sufijo *_test.go, *.test.sh, *.bats, *.test.ts o *.test.tsx (lista cerrada; los dos ultimos son vitest/jest de los repos de UI: marcado-ui, graph_ui, sldb-ui) que existan en el repo y esten citados en references de la tarea (files sigue sirviendo solo para ampliar ubicaciones, como hoy). (2) Un archivo bajo runs/ citado en references cuya primera linea empieza con '$ ' (el comando) y cuya ultima linea no vacia es 'rc=0' cuenta como evidencia de tests para cualquier tarea. (3) La evidencia de commit de otro repo ya existe con el formato <repo-id>:<sha> (RepositoryReferences en deskops/services/closeout_gates.py, alrededor de 255-300), pero solo busca <repo-id> en desk/registry del propio desk: debe buscar tambien en el registro del ecosistema, con la misma resolucion que usa deskops message send --to (find_registered_desk en deskops/identity.py). (4) closeout resolved-by acepta en --test los sufijos de (1) y en --ref el formato <repo-id>:<sha> con la resolucion de (3).

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/closeout_gates.py, deskops/services/closure.py (rama resolved-by), la doc de evidencia en docs/workflow-policy-reference.md y tests nuevos en tests/test_closeout_gates.py y tests/test_closeout_resolved_by.py. No entra: cerrar las tres tareas de scion (lo hace su coordinador despues), cambiar que evidencia exige cada tipo. Precisiones del preflight 1: la lista de sufijos es cerrada: *_test.go, *.test.sh, *.bats, *.test.ts, *.test.tsx, y el archivo debe estar en files o references de la tarea y existir en el repo. Log de validacion: archivo bajo runs/ cuya primera linea empieza con '$ ' (el comando) y cuya ultima linea es 'rc=0'; se acepta para cualquier tarea, no hay que detectar 'sin framework'. La nota a scion es deskops message send --to scion con el hash del commit. Precisiones del preflight 3: (a) 'el repo' es siempre la raiz del desk sobre la que corre closeout (--root, la misma que ya usa reference_points_to_test para los .py): para marcado-ui o scion es la raiz de ese repo; no se resuelve otro repo para los archivos de test. (b) runs/ es <raiz del desk>/runs/; la referencia es una ruta relativa a esa raiz que empieza con runs/. (c) Vale la ultima linea no vacia: se ignoran lineas vacias o solo con espacios al final del archivo, y esa linea, sin espacios a los costados, es exactamente rc=0. (d) tests/test_closeout_test_paths.py solo se ejecuta; se modifica solo si el cambio rompe legitimamente uno de sus casos, y eso se explica en el informe.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer closeout_gates.py:140-300 y deskops/identity.py find_registered_desk. 2) Tabla de sufijos. 3) Log de validacion bajo runs/. 4) RepositoryReferences consulta tambien el registro del ecosistema. 5) Tests: un _test.go citado en references pasa; un .test.ts citado en references pasa; un .txt no; un log valido en runs/ pasa y uno con rc=1 no; <repo-id>:<sha ancestro> con <repo-id> solo en el registro del ecosistema pasa y un sha inexistente no. tests/test_closeout_test_paths.py existe y solo se corre. 6) Nota a scion y nota a marcado-ui con el hash del commit de cierre de esta tarea (deskops message send --to scion; deskops message send --to marcado-ui).

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_resolved_by.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_test_paths.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los casos del paso 5 pasan, la doc de evidencia describe las tres formas nuevas y la nota a scion esta enviada con el hash.

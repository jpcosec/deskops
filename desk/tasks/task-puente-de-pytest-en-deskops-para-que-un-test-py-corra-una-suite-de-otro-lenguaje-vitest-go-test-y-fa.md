---
sldb:
  by: agent
  at: '2026-11-16T15:33:55Z'
  authority: generated
  via: create_document
id: task-puente-de-pytest-en-deskops-para-que-un-test-py-corra-una-suite-de-otro-lenguaje-vitest-go-test-y-fa
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-102357-unclear-el-gate-de-tests-solo-py-bloquea-todo-el-desk-sldb-ui-vitest.md
- desk/inbox/20261116-095909-suggestion-closeout-marcado-ui-ts-vitest-bloqueado-por-el-gate-de-tests-solo-py-sumar-test-ts-test-tsx.md
depends_on: []
pills: []
files:
- deskops/testing/__init__.py
- deskops/testing/foreign_suites.py
- tests/test_foreign_suites.py
- docs/workflow-policy-reference.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# puente de pytest en deskops para que un test .py corra una suite de otro lenguaje (vitest, go test) y falle si ella falla

## Rationale

_Explain why this task exists or the business driver behind it._

Correccion de JP (2026-11-16, via supervisor): el gate de tests de closeout de deskops no se cambia para aceptar otros lenguajes (reference_points_to_test en deskops/services/closeout_gates.py sigue exigiendo un .py). En su lugar, pytest corre las suites de otros lenguajes y lo declarado como evidencia es un .py. Hoy esto bloquea el cierre de sldb-ui (vitest, src/**/*.test.ts; nota desk/inbox/20261116-102357-unclear-el-gate-de-tests-solo-py-bloquea-todo-el-desk-sldb-ui-vitest.md), de marcado-ui (vitest; nota desk/inbox/20261116-095909-suggestion-closeout-marcado-ui-ts-vitest-bloqueado-por-el-gate-de-tests-solo-py-sumar-test-ts-test-tsx.md) y de scion (Go, cmd/build_context_test.go). El puente es generico y vive en deskops, que es quien define el gate y esta instalado en todas las maquinas; ningun repo lo reimplementa. Reemplaza a task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado.

## Goal

_Describe the concrete result this task must produce._

Existe el modulo deskops/testing/foreign_suites.py con la funcion run_foreign_suite(command, *, cwd, timeout=None, env=None): corre command (lista de argumentos, sin shell) en cwd con subprocess; si el rc es 0 no hace nada; si el rc es distinto de 0, si el ejecutable no existe o si vence el timeout, llama a pytest.fail con un mensaje que nombra el comando, el cwd, el rc (o la causa) y las ultimas 200 lineas de stdout y stderr. Tiene dos ayudas con los comandos canonicos: VITEST = ['npx', 'vitest', 'run'] y GO_TEST = ['go', 'test', './...']. Un repo de otro lenguaje declara sus tests con un archivo tests/test_<suite>_suite.py de pocas lineas que importa run_foreign_suite y la llama con cwd = la raiz del repo; ese .py es lo que cita el closeout como evidencia de tests y el gate de deskops no cambia. docs/workflow-policy-reference.md explica en la seccion de evidencia de tests del closeout como declararlo, con el archivo de ejemplo para vitest y para go y el comando exacto para correrlo desde un repo sin entorno Python propio.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/testing/__init__.py y deskops/testing/foreign_suites.py (nuevos), tests/test_foreign_suites.py (nuevo), docs/workflow-policy-reference.md y pyproject.toml solo si hace falta declarar el paquete deskops.testing o pytest como extra. No entra: cambiar reference_points_to_test ni ningun gate de closeout, la evidencia de commit de otro repo (va en otra tarea), escribir los tests/test_<suite>_suite.py de sldb-ui, marcado-ui o scion (lo hace cada coordinador con la doc), un plugin pytest11 por entry point, ni un comando nuevo del CLI. Precisiones: el import de pytest es perezoso o a nivel de modulo, pero el modulo no se importa desde el CLI de deskops; el mensaje de falla es texto plano; timeout None significa sin limite; env None hereda el entorno; cwd es obligatorio y puede ser str o Path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer reference_points_to_test y _test_path_candidates en deskops/services/closeout_gates.py para confirmar que tests/test_<suite>_suite.py cuenta como evidencia sin cambios. 2) Escribir el modulo. 3) Tests en tests/test_foreign_suites.py con comandos de Python como suite falsa (sys.executable -c ...): rc 0 pasa; rc 3 falla y el mensaje nombra el comando, el rc y la salida; un ejecutable inexistente falla con mensaje claro; un timeout corto sobre un sleep falla; el cwd se respeta. Mas un test que construye un desk sandbox (tmp_path) con tests/test_vitest_suite.py citado en references de una tarea y comprueba que closeout verify encuentra la evidencia de tests. 4) Doc con los dos archivos de ejemplo y el comando para correrlos desde un repo sin venv propio (por ejemplo con uv y la instalacion de deskops de la maquina), comprobado a mano en una copia de prueba en /dev/shm. 5) Smoke real: un archivo temporal en /dev/shm que llama run_foreign_suite(VITEST, cwd='/mnt/ssd/proyectos/SLDB_1/UIs/sldb-ui') corrido con pytest pasa, y la salida va al informe.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_foreign_suites.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_test_paths.py
- Smoke del paso 5 contra UIs/sldb-ui con vitest real; salida y rc en el informe
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas, cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los casos del paso 3 pasan, el smoke contra sldb-ui pasa, la doc trae los ejemplos de vitest y go con su comando y git diff no toca deskops/services/closeout_gates.py.

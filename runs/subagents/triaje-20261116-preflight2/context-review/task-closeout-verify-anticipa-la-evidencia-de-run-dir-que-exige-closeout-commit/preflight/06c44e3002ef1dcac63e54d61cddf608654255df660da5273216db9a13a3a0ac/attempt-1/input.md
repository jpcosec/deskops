FILE:desk/tasks/task-closeout-verify-anticipa-la-evidencia-de-run-dir-que-exige-closeout-commit.md
---
sldb:
  by: agent
  at: '2026-11-16T05:00:10Z'
  authority: generated
  via: save_document_payload
id: task-closeout-verify-anticipa-la-evidencia-de-run-dir-que-exige-closeout-commit
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261031-195117-unclear-closeout-verify-no-anticipa-la-evidencia-que-exige-closeout-commit.md
depends_on: []
pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
files:
- deskops/cli/commands/closeout.py
- deskops/services/closure.py
- tests/test_closeout_declared_evidence.py
- tests/fixtures/golden (el golden de ayuda de closeout verify)
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# closeout verify anticipa la evidencia de run-dir que exige closeout commit

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del inbox (2026-10-31, cierres de WS02 y WS04): `deskops closeout verify` da ok:true y despues `deskops closeout commit --run-dir` falla con 'Missing required evidence ... task.txt'. verify no revisa los archivos de evidencia del run-dir, asi que su ok no anticipa el cierre.

## Goal

_Describe the concrete result this task must produce._

`deskops closeout verify --task <id> --run-dir <dir>` acepta --run-dir opcional; cuando se da, reporta como falla (ok:false) cada archivo de REQUIRED_EVIDENCE que falte en el run-dir, con el mismo texto que usa commit. Sin --run-dir, verify se comporta igual que hoy.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/closeout.py (parser de verify, alrededor de las lineas 83-86), deskops/services/closure.py (REQUIRED_EVIDENCE alrededor de la linea 104, el chequeo de commit alrededor de 539-543, verify_task_closeout alrededor de 843), el golden de ayuda de `closeout verify` que lee tests/test_output_goldens.py, y tests/test_closeout_declared_evidence.py. No entra: cambiar que evidencia exige commit ni el formato del reporte JSON fuera del nuevo hallazgo. Precisiones del preflight 1: el golden es tests/fixtures/golden/help/deskops_closeout_verify.txt; el texto de falla es el que hoy arma commit en closure.py: 'Missing required evidence in <run_dir>: <archivos separados por coma>'. Los numeros de linea son orientativos: se ubican por nombre de funcion. El atomo de sandbox implica que los tests usan un desk temporal, como los tests existentes del archivo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Extraer de commit un helper `missing_run_evidence(run_dir) -> list[str]`. 2) Usarlo en commit (sin cambio de comportamiento) y en verify cuando llega run_dir. 3) Agregar --run-dir al parser de verify y actualizar su golden de ayuda. 4) Tests: run-dir sin task.txt -> verify ok:false nombrando task.txt; run-dir completo -> ok:true; sin --run-dir -> igual que antes.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

verify con un run-dir incompleto da ok:false y nombra el archivo faltante; commit y verify usan el mismo helper; los tests listados pasan.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-closeout-verify-anticipa-la-evidencia-de-run-dir-que-exige-closeout-commit: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


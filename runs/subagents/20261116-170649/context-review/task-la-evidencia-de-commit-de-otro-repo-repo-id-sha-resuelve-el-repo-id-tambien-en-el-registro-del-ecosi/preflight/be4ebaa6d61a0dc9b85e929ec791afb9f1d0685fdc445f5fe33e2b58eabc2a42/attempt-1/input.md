FILE:desk/tasks/task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi.md
---
sldb:
  by: agent
  at: '2026-11-16T15:34:30Z'
  authority: generated
  via: create_document
id: task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
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

# la evidencia de commit de otro repo (repo-id:sha) resuelve el repo-id tambien en el registro del ecosistema, en closeout verify y en resolved-by --ref

## Rationale

_Explain why this task exists or the business driver behind it._

Parte (3) y (4) de task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado, que se reemplaza (la parte de tests la cubre el puente de pytest por correccion de JP). Nota de scion del 2026-11-16: una tarea del desk de scion cuyo codigo entro en deskops (4a7707a5, 4c745c18, 881e177a) no puede citar esos commits: la evidencia <repo-id>:<sha> ya existe (RepositoryReferences en deskops/services/closeout_gates.py, alrededor de las lineas 255-300) pero solo busca <repo-id> en desk/registry del propio desk, y closeout resolved-by --ref solo acepta ancestros del repo del desk.

## Goal

_Describe the concrete result this task must produce._

(1) En closeout verify, una referencia <repo-id>:<sha> cuenta como evidencia de commit si <repo-id> se resuelve primero en el registro del desk y, si no esta, con find_registered_desk de deskops/identity.py (el registro del ecosistema que ya usa deskops message send --to), y <sha> es un commit alcanzable en ese repo (rev-parse --verify y ancestro de su HEAD). Si el repo-id no resuelve, es ambiguo o el sha no existe, la referencia no cuenta y no hay excepcion. (2) closeout resolved-by --ref acepta ese mismo formato con la misma resolucion.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/closeout_gates.py (RepositoryReferences y su uso), deskops/services/closure.py (rama resolved-by), la seccion de evidencia de commit en docs/workflow-policy-reference.md y tests en tests/test_closeout_gates.py y tests/test_closeout_resolved_by.py. No entra: el gate de tests, cambiar que evidencia exige cada tipo, cerrar la tarea de scion (lo hace su coordinador). En los tests el registro del ecosistema es un registro sandbox (tmp_path y la variable o fixture que ya usa find_registered_desk), nunca ~/setup/desk/registry.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer RepositoryReferences, reference_points_to_commit y find_registered_desk. 2) Resolver el repo-id con el registro del desk y despues con find_registered_desk. 3) Lo mismo en resolved-by --ref. 4) Tests: repo-id solo en el registro del ecosistema con sha ancestro pasa; sha inexistente no; repo-id desconocido no; resolved-by --ref con ese formato cierra en un desk sandbox. 5) Doc. 6) Nota a scion con el hash del commit (deskops message send --to scion).

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_resolved_by.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas, cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los casos del paso 4 pasan, la doc describe la resolucion en dos registros y la nota a scion esta enviada con el hash.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


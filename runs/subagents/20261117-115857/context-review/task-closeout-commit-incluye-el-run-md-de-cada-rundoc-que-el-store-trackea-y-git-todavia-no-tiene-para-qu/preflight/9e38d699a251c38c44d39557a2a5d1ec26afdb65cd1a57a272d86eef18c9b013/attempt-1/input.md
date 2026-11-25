FILE:desk/tasks/task-closeout-commit-incluye-el-run-md-de-cada-rundoc-que-el-store-trackea-y-git-todavia-no-tiene-para-qu.md
---
sldb:
  by: agent
  at: '2026-11-17T07:06:45Z'
  authority: generated
  via: create_document
id: task-closeout-commit-incluye-el-run-md-de-cada-rundoc-que-el-store-trackea-y-git-todavia-no-tiene-para-qu
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-021713-suggestion-bug-deskops-trackea-un-rundoc-sin-archivo-y-rompe-sldb-stores-build-en-la-ci-de-graph-ui.md
depends_on: []
pills: []
files:
- deskops/services/closure.py
- tests/test_closeout.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# closeout commit incluye el run.md de cada RunDoc que el store trackea y git todavia no tiene, para que un clon limpio pase sldb stores build

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui (nota 20261117-021713): su CI clona deskops y corre sldb stores build, que falla con 'missing: runs/subagents/<run>/run.md' cuando .sldb/store.yaml registra un RunDoc cuyo run.md no esta en el repo. Pasa porque deskops runtime template registra el RunDoc en el store al anotar la intencion, y el closeout de OTRA tarea, que hace git add de .sldb, publica ese registro antes de que el run dir de esa corrida se commitee (caso real: el closeout 9dbcfc7c publico el RunDoc de exec-deskops-e-289fe7bfa1df; se arreglo a mano en 6b502362 para otros dos).

## Goal

_Describe the concrete result this task must produce._

Todo commit que hace deskops closeout commit (en cualquier modo) incluye, ademas de lo de hoy, el run.md de cada RunDoc que .sldb/store.yaml registra y que git todavia no conoce (no esta en el indice ni en HEAD), de modo que despues del cierre todo run.md registrado existe en el commit.

## Scope

_State what is in scope and what is out of scope._

Entra: el armado de rutas del commit de cierre en deskops/services/closure.py y tests en tests/test_closeout.py. Sale: deskops runtime template (sigue registrando el RunDoc al anotar la intencion), otros archivos del run dir (solo run.md, que es lo que el store exige) y la CI de graph_ui.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer en closure.py como se arman las rutas del commit de cierre y el git add de .sldb. 2) Antes de commitear, listar los path de RunDoc de .sldb/store.yaml, quedarse con los run.md que existen en disco y que git no conoce, y sumarlos a las rutas. 3) Test en desk sandbox (tmp_path): dos RunDoc registrados (uno de la tarea que se cierra y otro de otra corrida con su run.md sin commitear); despues de closeout commit, el run.md de la otra corrida esta en HEAD y git clone del sandbox + sldb stores build da rc 0.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa (el run.md de otra corrida entra en el commit de cierre y el clon limpio construye el store) y tests/test_closeout.py pasa.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-closeout-commit-incluye-el-run-md-de-cada-rundoc-que-el-store-trackea-y-git-todavia-no-tiene-para-qu: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


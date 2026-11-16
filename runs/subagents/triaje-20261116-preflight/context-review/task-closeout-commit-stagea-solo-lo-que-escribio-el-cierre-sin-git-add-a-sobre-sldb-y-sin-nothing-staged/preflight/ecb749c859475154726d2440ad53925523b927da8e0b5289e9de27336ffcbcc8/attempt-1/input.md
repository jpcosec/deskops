FILE:desk/tasks/task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged.md
---
sldb:
  by: agent
  at: '2026-11-16T04:00:34Z'
  authority: generated
  via: save_document_payload
id: task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261106-145349-suggestion-closeout-commit-arrastra-archivos-sin-trackear-de-sldb.md
- desk/inbox/inbox-note-closeout-commit-sin-paths-dice-nothing-staged-aunque-el-cli-dejó-cambios.md
depends_on: []
pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
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

# closeout commit stagea solo lo que escribio el cierre: sin git add -A sobre .sldb y sin Nothing staged mudo

## Rationale

_Explain why this task exists or the business driver behind it._

Dos notas del inbox. (1) sldb, 2026-11-06: deskops/services/closure.py hace `git add -A -- .sldb` cuando `git status --porcelain -- .sldb` no esta vacio, y eso agrega archivos SIN TRACKEAR ajenos a la tarea; en sldb el closeout de task-go03 (ec15bd27) commiteo 202 PythonSymbolDoc y dos TaskDoc huerfanos (corregido a mano en e1805fc6). (2) AntonIA, 2026-11-09: `deskops closeout commit` sin --paths responde 'Nothing staged' aunque el propio CLI dejo cambios (TaskDoc, Board, .sldb); hoy solo funciona pasando --paths a mano.

## Goal

_Describe the concrete result this task must produce._

`deskops closeout commit` agrega al commit exactamente las rutas que el cierre escribio (TaskDoc, desk/tasks/Board.md, archivos de .sldb/core y .sldb/store.yaml creados o modificados por la transaccion del cierre) mas las de --paths; nunca un archivo de .sldb que ya estaba sin trackear antes del cierre. Sin --paths el cierre funciona con esas rutas; si aun asi no hay nada que stagear, el error lista las rutas modificadas y sugiere --paths.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/closure.py (rama manual alrededor de las lineas 113-140, mensaje 'Nothing staged' alrededor de 645-657, `git add -A -- .sldb` alrededor de 695-697) y tests/test_closeout.py. Si resolved-by, retire o supersede usan el mismo helper de staging, el cambio les aplica y se prueba igual. No entra: la derrama de reglas de activacion (tarea task-advance-y-closeout-no-derraman-...), cambiar la gramatica del CLI, tocar .gitignore.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer closure.py entre las lineas 600 y 720 y ubicar el staging de .sldb. 2) Antes de escribir, tomar `git status --porcelain -z --untracked-files=all -- .sldb`; despues del cierre, stagear con `git add -u -- .sldb` mas solo los archivos nuevos que no estaban en la foto previa. 3) Sin --paths: stagear el TaskDoc, el Board y lo de .sldb del paso 2; si el indice queda vacio, error con la lista de rutas modificadas y la sugerencia --paths. 4) Dos tests nuevos en tests/test_closeout.py con un desk sandbox (ver los fixtures existentes del archivo): (a) un .yaml sin trackear ajeno en .sldb/core/documents antes del cierre sigue sin trackear despues y no esta en `git show --stat HEAD`; (b) closeout commit sin --paths cierra y el commit contiene el TaskDoc y el Board.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_atomless.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_resolved_by.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos pasan; el archivo ajeno sin trackear no aparece en el commit de cierre del test; closeout commit sin --paths ya no responde 'Nothing staged' cuando el cierre escribio archivos; suite completa sin fallas nuevas.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


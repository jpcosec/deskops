Task: task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged
Title: closeout commit stagea solo lo que escribio el cierre: sin git add -A sobre .sldb y sin Nothing staged mudo
Status: active
Current node: ritual-testing
Task type: task.code
Effective pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-23T07:06:40Z'
  authority: generated
  via: save_document_payload
id: task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
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

Entra: deskops/services/closure.py (rama manual alrededor de las lineas 113-140, mensaje 'Nothing staged' alrededor de 645-657, `git add -A -- .sldb` alrededor de 695-697) y tests/test_closeout.py. Si resolved-by, retire o supersede usan el mismo helper de staging, el cambio les aplica y se prueba igual. No entra: la derrama de reglas de activacion (tarea task-advance-y-closeout-no-derraman-...), cambiar la gramatica del CLI, tocar .gitignore. Precisiones del preflight 1: la autoria del cierre se atribuye por la foto de git (git status --porcelain -z --untracked-files=all -- .sldb antes y despues del cierre): es el criterio aceptado, no hace falta un manifiesto de escrituras. 'Rutas modificadas' del error = la salida de git status --porcelain del working tree respecto de HEAD. Para resolved-by, retire y supersede: se verifica con grep si llaman al helper de staging; por cada uno que lo llame se agrega un test igual al caso (a).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer closure.py entre las lineas 600 y 720 y ubicar el staging de .sldb. 2) Antes de escribir, tomar la foto A = git status --porcelain -z --untracked-files=all -- .sldb (ruta -> codigo de estado); despues del cierre, la foto B. Se stagean con git add -- <rutas> solo las rutas que estan en B y no estan en A, o que estan en ambas con distinto codigo de estado; una ruta trackeada ya modificada antes del cierre y que el cierre no vuelve a tocar no se stagea. No se usa git add -A ni git add -u sobre .sldb. 3) Sin --paths: stagear el TaskDoc, el Board y las rutas del paso 2; si el indice queda vacio, error con la lista de B (formato porcelain, rutas relativas al repo) y la sugerencia --paths. 4) Tests en tests/test_closeout.py con un desk sandbox: (a) un .yaml sin trackear ajeno en .sldb/core/documents antes del cierre sigue sin trackear despues y no esta en git show --stat HEAD; (b) un .yaml trackeado modificado antes del cierre y no tocado por el cierre sigue modificado sin stagear; (c) closeout commit sin --paths cierra y el commit contiene el TaskDoc y el Board.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_atomless.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_resolved_by.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos pasan; el archivo ajeno sin trackear no aparece en el commit de cierre del test; closeout commit sin --paths ya no responde 'Nothing staged' cuando el cierre escribio archivos; suite completa sin fallas nuevas.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

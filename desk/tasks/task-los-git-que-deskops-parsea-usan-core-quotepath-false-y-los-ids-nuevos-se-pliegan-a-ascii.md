---
sldb:
  by: agent
  at: '2026-11-18T19:43:12Z'
  authority: generated
  via: save_document_payload
id: task-los-git-que-deskops-parsea-usan-core-quotepath-false-y-los-ids-nuevos-se-pliegan-a-ascii
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-nombres-de-tarea-con-acentos-git-cita-las-rutas-y-el-hook-de-wt-las-rechaza.md
- desk/inbox/20261118-154919-unclear-queue-20261118t184427z-integrate-task-deskops-desk-update-apply-sobre-el-repo-de-deskops-no-vac-a-el-path-de-los-modelos-en-sldb-core-mode.md
depends_on: []
pills: []
files:
- deskops/specs/compiler.py
- deskops/doc_access.py
- deskops/services/drawer.py
- deskops/services/closure.py
- tests/test_ascii_ids.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# Los git que deskops parsea usan core.quotepath=false y los ids nuevos se pliegan a ASCII

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de AntonIA (2026-11-09): con ids que llevan acentos (p. ej. task-cc35a-transacción-...) git imprime las rutas citadas con escapes octales (core.quotepath=true por defecto) y un hook externo de worktrees las rechaza; hoy se esquiva poniendo core.quotepath=false por entorno. En deskops, `git ls-files .sldb` ya imprime rutas citadas (inbox-note-decisi\303\263n-...). deskops/services/drawer.py ya pliega los slugs a [a-z0-9], pero deskops/specs/compiler.py y deskops/doc_access.py conservan acentos (usan str.isalnum).

## Goal

_Describe the concrete result this task must produce._

(1) Toda llamada a git dentro de deskops cuya salida se parsea pasa -c core.quotepath=false (no se usa -z en esta tarea). (2) Los ids que deskops deriva de un titulo se pliegan a ASCII (á->a, ñ->n, ü->u) con un solo helper compartido por compiler.py, doc_access.py y drawer.py; un id dado explicitamente por el usuario no se toca. (3) Los ids existentes con acentos siguen resolviendo por selector exacto; no se renombran ni se migran; si el id plegado de una tarea nueva coincide con uno existente, se aplica la regla de colision que ya tenga add task.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/specs/compiler.py (alrededor de las lineas 155-159), deskops/doc_access.py (157-161), deskops/services/drawer.py (288-290), las llamadas git de deskops/services/closure.py (alrededor de 645, 695 y 1555) y cualquier otra llamada git con salida parseada que muestre `grep -rn '"git"' deskops/`; un test nuevo tests/test_ascii_ids.py. No entra: renombrar o migrar ids ya commiteados (CC35a y otros), el hook externo de worktrees (no vive en este repo), cambiar la longitud maxima de los ids. Incluye además deskops/integrate.py (posterior a esta tarea): load_closed_task y _receipt_commit (alrededor de la línea 100) parsean 'git ls-tree --name-only' y 'git log'. Con un id con tilde, ls-tree cita la ruta y el recibo evidence-commit no se encuentra. Así falló el 2026-11-18 el integrate automático de la tarea de desk update (nota de la cola en references). Test: integrate encuentra el código de una tarea cerrada cuyo id tiene tilde.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Helper `ascii_slug(text)` en un modulo comun (unicodedata.normalize('NFKD') y descarte de marcas combinantes, luego la regla de caracteres actual). 2) Reemplazar las tres implementaciones por el helper. 3) Agregar `-c core.quotepath=false` (o -z con parseo por NUL) a cada git cuya salida se parsea. 4) tests/test_ascii_ids.py: `deskops add task --title 'Transacción ñandú'` en un desk sandbox produce un id solo ASCII; un TaskDoc con id acentuado creado por la API sigue resolviendo con `deskops show task <id>`; un archivo sin trackear con nombre acentuado en .sldb no rompe el parseo de git del cierre. Precisiones del preflight 1: el helper vive en un modulo nuevo deskops/slugs.py (funcion ascii_slug); la regla de caracteres es la de deskops/services/drawer.py _slug: minusculas, re.sub(r'[^a-z0-9]+', '-', ...) y strip('-'), con el plegado NFKD aplicado antes; la longitud maxima de cada llamador se conserva. La auditoria cubre las llamadas a subprocess cuyo argv empieza con 'git' (literal o lista) en deskops/; llamadas armadas dinamicamente que no aparezcan con grep -rn "'git'\|\"git\"" quedan fuera.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_ascii_ids.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

tests/test_ascii_ids.py pasa; `grep -rn quotepath deskops/` muestra la opcion en las llamadas git parseadas; los ids acentuados existentes siguen resolviendo; suite sin fallas nuevas.

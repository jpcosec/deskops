Task: task-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict-igual-que-edit-task
Title: add task --from-yaml rechaza un item de lista que YAML leyo como dict, igual que edit task
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-21T06:39:03Z'
  authority: generated
  via: save_document_payload
id: task-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict-igual-que-edit-task
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-072606-suggestion-add-task-from-yaml-acepta-un-dict-en-validation-y-edit-task-lo-rechaza.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# add task --from-yaml rechaza un item de lista que YAML leyo como dict, igual que edit task

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de IR (20261116-072606): con deskops add task --from-yaml, un item de validation que es un escalar YAML con dos puntos y espacio (por ejemplo - Suite completa, bajo flock /dev/shm/x.lock: CMD) se parsea como dict y add task lo guarda como el repr de Python; edit task rechaza la misma lista con pydantic Input should be a valid string. Reproducido hoy en un desk temporal: la seccion Validation queda con la linea literal {'Suite completa, bajo flock /dev/shm/x.lock': 'CMD foo'}.

## Goal

_Describe the concrete result this task must produce._

add task --from-yaml (y el payload JSON inline) falla con codigo distinto de 0 si un campo de lista de strings del TaskDoc (validation, depends_on, inherits_from, atoms, evidence, references) trae un item que no es string, y el mensaje nombra el campo, el indice y sugiere entrecomillar el item; no se crea ningun archivo. Un item string no cambia de comportamiento.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/parse_input.py (_load_yaml_mapping en la linea 70 y _ensure_mapping_payload) o el punto de add task donde el payload se convierte a TaskDoc, y un test nuevo. No entra: convertir silenciosamente el dict a string, ni cambiar edit task.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ubicar por que add task acepta el dict (seguramente stringifica antes de validar con pydantic). 2) Validar los items de los campos lista contra str antes de crear la tarea, con el mensaje pedido. 3) Test con un YAML cuyo validation tiene el item con dos puntos sin comillas: falla y no deja desk/tasks/<id>.md; con el item entrecomillado se crea bien.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_add_task_from_drawer.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; cada falla se corre igual en un worktree limpio de origin/main y solo se acepta si falla igual ahi, listada en la entrega)

## Done When

_Name the observable condition that makes the task complete._

Test nuevo: el YAML con el item sin comillas hace fallar add task con un mensaje que nombra validation y el indice, sin crear la tarea; el mismo item entrecomillado crea la tarea con la linea literal.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict-igual-que-edit-task"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-e70b6cd9c7de`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-e70b6cd9c7de

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.

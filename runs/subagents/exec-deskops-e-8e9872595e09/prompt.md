Task: task-board-no-refleja-deskops-edit-task-goal
Title: Board no refleja deskops edit task goal
Status: draft
Current node: ritual-execution
Task type: task.debug
From drawer: desk/drawer/tasks/task-board-no-refleja-edit-task-goal.md
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-19T04:54:51Z'
  authority: generated
  via: save_document_payload
id: task-board-no-refleja-deskops-edit-task-goal
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
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-board-no-refleja-edit-task-goal.md
---

# Board no refleja deskops edit task goal

## Rationale

_Explain why this task exists or the business driver behind it._

Nota (12-11, inbox 20261112-132201, caso FTC-26): edit task goal actualiza la tarea pero desk/tasks/Board.md sigue con el goal viejo; edit board no encuentra el artefacto y desk replace rechaza el Board por ser documento modelado.

## Goal

_Describe the concrete result this task must produce._

Reproducir en un desk real y corregir: tras deskops edit task <id> goal, la linea de la tarea en Task Details del Board muestra el goal nuevo, o hay un verbo de deskops que refresca el Board.

## Scope

_State what is in scope and what is out of scope._

deskops/services/tasks.py, deskops/models/board.py (plantilla de Task Details), deskops edit; la vista del tablero es de sldb (CC34), no se reimplementa.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes en tests/ (desk de prueba en tmp_path): add task con goal 'viejo', edit task <id> goal 'nuevo', y desk/tasks/Board.md muestra 'nuevo' y no 'viejo' en la línea de la tarea. Lo mismo para title. status lo cambian advance y closeout; si ya refrescan el Board, el test lo deja asentado. p2: después de 'deskops edit task' sobre un campo que usa la composición task_summaries de BoardDoc (deskops/models/board.py:16-21: title, status, goal), volver a guardar el Board por la misma vía con que add task lo guarda (services/tasks.py, alrededor de las líneas 118 y 219), para que sldb re-renderice la composición. No editar Board.md a mano ni reimplementar la vista del tablero. p3: CHANGELOG. p4: commit con rutas nombradas y Task-Id. Reproducción del integrador en runs/subagents/20261119-repro-board-goal/repro.md.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider <test nuevo>
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_cli.py

## Done When

_Name the observable condition that makes the task complete._

recibo de reproduccion y test que edita el goal y lee el Board con el valor nuevo.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-board-no-refleja-deskops-edit-task-goal"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

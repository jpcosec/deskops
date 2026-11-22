---
sldb:
  by: agent
  at: '2026-11-22T08:52:13Z'
  authority: generated
  via: create_document
id: task-golden-de-help-de-deskops-drawer-al-dia-con-la-descripcion-nueva-de-drawer-remove
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Golden de help de deskops drawer al día con la descripción nueva de drawer remove

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-22: el integrate agrupado (drawer remove, doctor layout, xdist) falló en la suite con tests/test_output_goldens.py::test_help_goldens: 'golden mismatch: help/deskops_drawer.txt'. La tarea de drawer remove (closeout ea900060) cambió la descripción del subcomando, que ahora dice 'Remove one drawer entry (a file, an issue with its assets, or a whole plan directory), its tracking, and its bullets on the...'. Actualizó tests/fixtures/golden/help/deskops_drawer_remove.txt, pero no deskops_drawer.txt, el help del grupo que lista esa descripción. Bloquea todo integrate de deskops.

## Goal

_Describe the concrete result this task must produce._

tests/fixtures/golden/help/deskops_drawer.txt coincide con la salida actual de 'deskops drawer --help' con COLUMNS=80. Se regenera con el mecanismo del propio test (pytest tests/test_output_goldens.py --update-golden), y solo cambia ese archivo; si --update-golden toca otros goldens, se revierten y se explica por qué.

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/fixtures/golden/help/deskops_drawer.txt. Fuera: el código de drawer y cualquier otro golden.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py --update-golden. p2: git status: debe cambiar solo deskops_drawer.txt; revertir con git checkout -- <ruta> cualquier otro golden y anotar cuál. p3: correr tests/test_output_goldens.py sin --update-golden, en verde. p4: commit desde el worktree que dispatch te da con 'git commit -- tests/fixtures/golden/help/deskops_drawer.txt' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo. No hace falta la suite completa: la corre integrate.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_output_goldens.py pasa y el commit solo toca deskops_drawer.txt.

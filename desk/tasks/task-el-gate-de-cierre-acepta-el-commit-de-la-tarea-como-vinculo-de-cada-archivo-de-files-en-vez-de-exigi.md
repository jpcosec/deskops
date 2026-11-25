---
sldb:
  by: agent
  at: '2026-11-25T16:53:22Z'
  authority: generated
  via: create_document
id: task-el-gate-de-cierre-acepta-el-commit-de-la-tarea-como-vinculo-de-cada-archivo-de-files-en-vez-de-exigi
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261125-092140-suggestion-gate-de-cierre-exigir-un-tomo-por-cada-archivo-de-files-bloquea-las.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El gate de cierre acepta el commit de la tarea como vínculo de cada archivo de files en vez de exigir un átomo por archivo

## Rationale

_Explain why this task exists or the business driver behind it._

En MEPU, UI-122, UI-123 y TST-16 quedaron integradas pero no se pudieron cerrar porque completaron 'files': mientras más completa la tarea, menos se puede cerrar (nota 20261125-092140, pedido de JP del 25-11).

## Goal

_Describe the concrete result this task must produce._

missing_changed_file_link en deskops/services/closure.py da por vinculado un archivo de 'files' cuando lo toca un commit con el trailer Task-Id de la tarea; el átomo pasa a exigirse por tarea y no por archivo.

## Scope

_State what is in scope and what is out of scope._

Entra: closure.py (missing_changed_file_link y _changed_file_link_evidence) y sus tests. Sale: el reconocimiento de átomos que citan archivos de cualquier tipo, que ya entró con el PR #12.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) En missing_changed_file_link, antes de bloquear, buscar en git log un commit con trailer Task-Id de la tarea que toque la ruta. 2) Si existe, la ruta queda vinculada. 3) Exigir al menos un átomo por tarea cuando el tipo lo pide, no uno por archivo. 4) Tests: una tarea con files completos y su commit cierra; una ruta sin commit ni átomo sigue bloqueando.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_closeout_atom_cites_file.py tests -k closeout

## Done When

_Name the observable condition that makes the task complete._

Una tarea con files completos cuyo commit lleva Task-Id cierra sin un átomo por archivo, y un test lo prueba.

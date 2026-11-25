FILE:desk/tasks/task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase.md
---
sldb:
  by: agent
  at: '2026-11-25T01:04:46Z'
  authority: generated
  via: save_document_payload
id: task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261123-161332-suggestion-jp-el-lote-de-integraci-n-es-la-fase-del-dag-declarada-en-el-board-falta-en-la-herramienta-y-en-el-skill.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El Board declara las fases del DAG: que tareas forman cada fase y que su integracion es de la fase

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-161332-suggestion-jp-el-lote-de-integraci-n-es-la-fase-del-dag-declarada-en-el-board-falta-en-la-herramienta-y-en-el-skill (JP 2026-11-23): el lote de integracion es la fase del DAG declarada en el Board al descomponer; ritual-phase ya lo dice, pero el Board no registra fases (solo lista rituales y pills).

## Goal

_Describe the concrete result this task must produce._

BoardDoc tiene un campo de fases: cada fase con id, lista de tareas e integracion de la fase (validacion combinada y commit de cierre de fase). El modelo valida que una tarea este en una sola fase. Solo modelo y template; CLI y vista son tareas aparte.

## Scope

_State what is in scope and what is out of scope._

deskops/models/board.py, el template del Board con el marcador de fases y su test de modelo (round-trip extract/render con dos fases). Fuera: comando de CLI (task-deskops-declara-fases-del-board-por-cli), vista (task-deskops-view-board-muestra-las-fases), integrate y skill.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer ritual-phase y pill-007-phase-gated-task-flow para el vocabulario. 2) Campo phases en BoardDoc (id, tasks, integration) con su marcador en el template. 3) Validador: una tarea en una sola fase. 4) Test de modelo: un Board con dos fases hace round-trip y una tarea repetida falla. Correr solo ese test.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_board_phases.py

## Done When

_Name the observable condition that makes the task complete._

Un Board con dos fases hace round-trip por sldb y una tarea en dos fases es rechazada; el test nuevo pasa.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


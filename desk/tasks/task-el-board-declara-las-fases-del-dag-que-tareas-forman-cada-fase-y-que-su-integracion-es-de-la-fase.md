---
sldb:
  by: agent
  at: '2026-11-24T18:27:49Z'
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

BoardDoc tiene un campo de fases (id, tareas, integracion de la fase: validacion combinada y commit de cierre de fase); deskops tiene comandos para declarar una fase y agregar o quitar tareas de ella; deskops view board las muestra; el store del desk se actualiza con sldb stores update.

## Scope

_State what is in scope and what is out of scope._

deskops/models/board.py y su template, el comando de CLI para fases (add o edit board), la vista del board, goldens de ayuda y de salida, tests, y sldb stores update del desk. Fuera: integrate (tarea siguiente) y el skill.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer ritual-phase y pill-007-phase-gated-task-flow para el vocabulario. 2) Campo de fases en BoardDoc con su marcador en el template. 3) Comando para declarar fase y sus tareas, con validacion de que las tareas existen y de que una tarea esta en una sola fase. 4) Vista. 5) Tests y goldens. 6) sldb stores update y deskops doctor sin errores nuevos.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp pytest -q de los tests tocados; deskops doctor --root .

## Done When

_Name the observable condition that makes the task complete._

Se puede declarar una fase con dos tareas por CLI y la vista del board la muestra; tests y goldens verdes; deskops doctor no suma errores.

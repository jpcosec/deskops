---
sldb:
  by: agent
  at: '2026-11-25T01:05:23Z'
  authority: generated
  via: create_document
id: task-deskops-view-board-muestra-las-fases-del-dag-con-sus-tareas-y-su-estado
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on:
- task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops view board muestra las fases del DAG con sus tareas y su estado

## Rationale

_Explain why this task exists or the business driver behind it._

Parte del DAG de fases (nota 20261123-161332-suggestion-jp-el-lote-de-integraci-n-es-la-fase-del-dag-declarada-en-el-board-falta-en-la-herramienta-y-en-el-skill). Con el modelo de fases (task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase) la vista del board debe mostrar que tareas forman cada fase.

## Goal

_Describe the concrete result this task must produce._

deskops view board (texto y json) lista cada fase con sus tareas y el estado de cada una, y si la fase esta completa.

## Scope

_State what is in scope and what is out of scope._

La vista del board (deskops view board) y su golden de salida y tests. Fuera: modelo, CLI de fases, integrate.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer la vista actual del board. 2) Agregar la seccion de fases (texto y json) con estado por tarea y fase completa si o no. 3) Golden y test con un Board de dos fases. Correr solo esos tests.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_view_board_phases.py

## Done When

_Name the observable condition that makes the task complete._

Con un Board de dos fases, view board muestra ambas con sus tareas y su estado en texto y json; golden y test nuevos pasan.

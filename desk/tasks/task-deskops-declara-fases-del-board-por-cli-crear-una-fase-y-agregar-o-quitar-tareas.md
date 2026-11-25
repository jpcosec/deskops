---
sldb:
  by: agent
  at: '2026-11-25T01:05:09Z'
  authority: generated
  via: create_document
id: task-deskops-declara-fases-del-board-por-cli-crear-una-fase-y-agregar-o-quitar-tareas
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

# deskops declara fases del Board por CLI: crear una fase y agregar o quitar tareas

## Rationale

_Explain why this task exists or the business driver behind it._

Parte del DAG de fases (nota 20261123-161332-suggestion-jp-el-lote-de-integraci-n-es-la-fase-del-dag-declarada-en-el-board-falta-en-la-herramienta-y-en-el-skill, JP 2026-11-23). El modelo de fases lo trae task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase; falta como escribirlas sin editar el Board a mano.

## Goal

_Describe the concrete result this task must produce._

Un comando de deskops crea una fase en el Board y agrega o quita tareas de ella, validando que la tarea exista y que no este ya en otra fase; escribe por sldb.

## Scope

_State what is in scope and what is out of scope._

El subcomando de CLI (bajo add board o edit board, el que siga el patron existente), su golden de ayuda y sus tests. Fuera: modelo (ya hecho), vista, integrate.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ver como deskops edita hoy el Board (edit/add board) y seguir ese patron. 2) Crear fase, agregar tarea, quitar tarea; error claro si la tarea no existe o ya esta en otra fase. 3) Golden de ayuda y tests del comando. Correr solo esos tests.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_board_phases_cli.py

## Done When

_Name the observable condition that makes the task complete._

Por CLI se crea una fase con dos tareas, se quita una, y una tarea repetida da error; tests y golden de ayuda nuevos pasan.

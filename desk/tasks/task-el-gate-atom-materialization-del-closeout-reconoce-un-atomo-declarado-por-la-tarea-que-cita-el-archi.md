---
sldb:
  by: agent
  at: '2026-11-25T01:44:16Z'
  authority: generated
  via: create_document
id: task-el-gate-atom-materialization-del-closeout-reconoce-un-atomo-declarado-por-la-tarea-que-cita-el-archi
status: draft
summary: ''
tags: []
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

# El gate atom|materialization del closeout reconoce un atomo declarado por la tarea que cita el archivo cambiado, de cualquier tipo

## Rationale

_Explain why this task exists or the business driver behind it._

Piloto UI-122 de MEPU (nota PARA DESKOPS 20261124-222637 punto 11): una tarea de UI (.ts/.tsx/.css, build en src/frontend/v2/) queda bloqueada en closeout aunque declara en atoms un atomo cuyo provenance y respuesta citan esos archivos; el grafo solo tiene nodos de archivos Python de desk/ y deskops/.

## Goal

_Describe the concrete result this task must produce._

closeout verify acepta como enlace de un archivo cambiado un atomo declarado en atoms o references cuya provenance o texto cite la ruta (o su directorio); el mensaje del hallazgo dice que forma de enlace se acepta.

## Scope

_State what is in scope and what is out of scope._

deskops/services/closure.py y un test nuevo. Fuera: el grafo.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- pytest tests/test_closeout_atom_cites_file.py

## Done When

_Name the observable condition that makes the task complete._

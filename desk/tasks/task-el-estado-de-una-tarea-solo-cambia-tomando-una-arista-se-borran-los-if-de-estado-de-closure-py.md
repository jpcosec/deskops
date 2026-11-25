---
sldb:
  by: agent
  at: '2026-11-25T22:56:17Z'
  authority: generated
  via: create_document
id: task-el-estado-de-una-tarea-solo-cambia-tomando-una-arista-se-borran-los-if-de-estado-de-closure-py
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-sldb-hace-respetar-una-maquina-de-estados-el-campo-de-estado-solo-cambia-tomando-una-arista
- task-el-cierre-toma-la-arista-task-completes-desde-el-nodo-real-de-la-tarea
- task-supersede-resolved-by-y-retire-son-aristas-declaradas-del-ciclo-de-vida
pills: []
files:
- deskops/models/task.py
- deskops/services/closure.py
- .github/workflows/tests.yml
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El estado de una tarea solo cambia tomando una arista: se borran los if de estado de closure.py

## Rationale

_Explain why this task exists or the business driver behind it._

Hoy deskops protege el estado con if repartidos en closure.py y aun así hay caminos que lo escriben directo (W3, W5). Cuando sldb hace respetar la máquina de estados, esos if sobran.

## Goal

_Describe the concrete result this task must produce._

El campo status y current_node de TaskDoc está declarado como estado de la máquina en sldb y closure.py no tiene comprobaciones de estado propias.

## Scope

_State what is in scope and what is out of scope._

Entra: declarar el campo de estado en el modelo, borrar los if de estado de closure.py y el paso del CI que revisa la historia. Sale: qué aristas existen.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Declarar el campo. 2) Escenario: deskops edit task status falla. 3) Borrar los if. 4) Paso del CI.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core

## Done When

_Name the observable condition that makes the task complete._

Una escritura directa del estado falla y closure.py no compara estados.

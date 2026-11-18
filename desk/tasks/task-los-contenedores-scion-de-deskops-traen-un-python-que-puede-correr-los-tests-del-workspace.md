---
sldb:
  by: agent
  at: '2026-11-18T07:43:12Z'
  authority: generated
  via: create_document
id: task-los-contenedores-scion-de-deskops-traen-un-python-que-puede-correr-los-tests-del-workspace
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
files:
- deskops/runtime/scion.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
---

# Los contenedores scion de deskops traen un python que puede correr los tests del workspace

## Rationale

_Explain why this task exists or the business driver behind it._

El 2026-11-18 ejecutores y testers despachados por scion (imagenes scion-claude y scion-pi) no pudieron usar el entorno virtual del workspace: sus enlaces apuntan a un interprete python 3.12 que las imagenes no traen (solo tienen 3.13). Cada agente improviso un entorno con PYTHONPATH y a veces un test fallo solo por eso.

## Goal

_Describe the concrete result this task must produce._

Decidir e implementar una de dos vias y dejarla documentada en el manual del operador: (a) el template scion que genera deskops runtime template declara un paso de arranque que crea un entorno virtual propio del contenedor desde el pyproject del workspace y lo pone primero en el PATH; o (b) las imagenes traen python 3.12 en la misma ruta que usa el entorno del workspace. La tarea empieza por medir cual es viable con la version de scion instalada y registra la decision en un atom.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/runtime/scion.py, tests, manual, y el archivo de build de imagen si se elige (b). Fuera: cambios en el codigo de scion. Checkout principal, sin worktree ni rama, sin git add ni git commit.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py

## Done When

_Name the observable condition that makes the task complete._

Un tester despachado por scion corre pytest sobre un archivo de tests de deskops con el comando del TaskDoc, sin improvisar entorno.

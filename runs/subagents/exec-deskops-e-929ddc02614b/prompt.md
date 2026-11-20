Task: task-integrate-evalua-el-gate-de-grafo-en-la-punta-local-actual-no-solo-en-el-commit-de-closeout-cuando-d
Title: integrate evalúa el gate de grafo en la punta local actual, no solo en el commit de closeout, cuando después solo hay commits de desk
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-20T10:43:17Z'
  authority: generated
  via: create_document
id: task-integrate-evalua-el-gate-de-grafo-en-la-punta-local-actual-no-solo-en-el-commit-de-closeout-cuando-d
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

# integrate evalúa el gate de grafo en la punta local actual, no solo en el commit de closeout, cuando después solo hay commits de desk

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-20, sldb: integrate de la tarea del merge driver falló dos veces con 'fallo:graph faltantes 1 en el tip > 0 en origin/main'. El tip que usa integrate es el commit de closeout de la tarea (08c520c1), y la referencia colgante estaba en otra tarea vieja que se retiró en un commit de desk posterior (5900a3eb). integrate nunca ve ese arreglo y no hay forma de destrabarlo por la cola; el coordinador empujó a mano.

## Goal

_Describe the concrete result this task must produce._

Si entre el commit de closeout de la tarea y la punta local (HEAD de la rama) solo hay commits que tocan desk/, .sldb/ o runs/ (nada de código, tests ni docs), integrate usa esa punta como tip: corre los gates sobre ella y la empuja. Si hay commits con código posteriores, sigue usando el commit de closeout como hoy. Lo dice en su salida ('tip extendido a <sha>: solo commits de desk').

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/integrate.py (find_tip o el cálculo del tip) y tests/test_integrate.py; CHANGELOG. Fuera: el resto de los gates.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: closeout con una referencia colgante en otra tarea, y un commit de desk posterior que la arregla; integrate debe terminar ok y empujar la punta. Otro test: si el commit posterior toca src/, el tip sigue siendo el closeout. p2: implementar con git diff --name-only <closeout>..HEAD. p3: CHANGELOG, commit con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos y tests/test_integrate.py pasan.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-integrate-evalua-el-gate-de-grafo-en-la-punta-local-actual-no-solo-en-el-commit-de-closeout-cuando-d"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

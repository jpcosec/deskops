---
sldb:
  by: agent
  at: '2026-11-22T12:16:08Z'
  authority: generated
  via: create_document
id: task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p
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
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# reap dice 'integrado 0 commits' y borra la rama del ejecutor aunque tenga un commit fuera de main (se pierde el trabajo)

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-22, sldb: el reap de deskops-e-01426e49e09c-a2 (intento 2 del guard de sobrescritura) imprimió 'integrado 0 commit(s) de deskops/deskops-e-01426e49e09c-a2 en main' y borró la rama y el worktree. Pero el ejecutor había commiteado b424ce65 en esa rama, con su Task-Id, y el padre de ese commit (490beb90, 'run: deskops-e-01426e49e09c-a2') está en main. El commit quedó colgante: el coordinador lo encontró con git fsck --lost-found y lo trajo a mano (074bc3bc). El tester a2 probó main sin el arreglo y gastó el segundo intento. 490beb90 es el commit 'run:' que dispatch start hace en main desde el arreglo de RunDoc (d42ee663 y el de run.md): la rama del ejecutor nace antes o después de ese commit, y el cálculo de commits a integrar del reap parece no contemplarlo.

## Goal

_Describe the concrete result this task must produce._

dispatch reap nunca borra una rama deskops/<agente> que tiene commits alcanzables desde ella y no desde la rama principal. Calcula los commits con git rev-list <main>..<rama> en el momento del reap y los trae todos con cherry-pick. Si el cálculo da 0 pero la punta de la rama no está en main, no borra nada y sale con error nombrando la rama y la punta. Un test reproduce el caso del commit 'run:' hecho en main entre la creación de la rama y el commit del ejecutor.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/dispatch.py (reap y el cálculo de commits), tests/test_dispatch.py y CHANGELOG. Fuera: el resto.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: reproducir en test: crear la rama del ejecutor, hacer en main el commit 'run:' (como _commit_run_store), commitear en la rama sobre ese commit, y correr reap: hoy integra 0 y borra. Guardar la salida como reproducción en el run dir. p2: arreglar el cálculo y agregar la guarda de no borrar. p3: tests/test_dispatch.py con -n 4, en es_ES y en_US. p4: CHANGELOG; commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

El test de reproducción pasa y tests/test_dispatch.py pasa en los dos locales.

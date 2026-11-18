FILE:desk/tasks/task-deskops-desk-update-apply-sobre-el-repo-de-deskops-no-vacía-el-path-de-los-modelos-en-sldb-core-mode.md
---
sldb:
  by: agent
  at: '2026-11-18T17:43:07Z'
  authority: generated
  via: create_document
id: task-deskops-desk-update-apply-sobre-el-repo-de-deskops-no-vacía-el-path-de-los-modelos-en-sldb-core-mode
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

# deskops desk update --apply sobre el repo de deskops no vacía el path de los modelos en .sldb/core/models

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261118-102359-suggestion-deskops-desk-update-apply-sobre-el-repo-de-deskops-vac-a-el-path-de-todos-los-modelos-de-sldb-core-models (integrador, 2026-11-18): en /mnt/ssd/proyectos/SLDB_1/deskops, con herramientas en 31460a48, 'deskops desk update --apply' reescribió los 30 archivos de .sldb/core/models/*.yaml con path: '' en lugar de la ruta local del modelo (RoleDoc: 'path: deskops/models/role.py' pasó a "path: ''"). También tocó sldb/relation_types/has_model.md y agregó reltype-links_to. Se revirtió sin commitear. En sldb e IR el mismo comando no tocó los modelos. Si se commitea, el índice de modelos del store de deskops pierde la ruta de cada modelo.

## Goal

_Describe the concrete result this task must produce._

En el repo de deskops, desk update --apply deja intacto el path de cada modelo en .sldb/core/models/*.yaml, y no reescribe sldb/relation_types/ ni agrega relation types que el store no declara.

## Scope

_State what is in scope and what is out of scope._

En alcance: reproducir en una copia limpia de deskops (git clone a /dev/shm, desk update --apply, git diff -- .sldb/core/models sldb/relation_types), encontrar con archivo y línea qué parte de desk update re-registra los modelos sin la ruta local (hipótesis: en el repo de deskops los modelos son del paquete propio y se registran como instalados), y arreglarlo para que conserve la ruta del store.yaml de deskops. Si lo que agrega en sldb/relation_types es correcto (un relation type que el paquete declara), el informe lo dice con evidencia en vez de revertirlo. Fuera de alcance: cambiar el layout de .sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: reproducción en copia limpia, con la evidencia en el informe. p2: test que falla antes: desk update --apply sobre un desk de prueba cuyos modelos tienen path local no vacía ese path. p3: arreglo. p4: CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q tests/test_desk_sync.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa, la reproducción en una copia limpia de deskops ya no cambia .sldb/core/models y la suite completa pasa (la corre integrate).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-desk-update-apply-sobre-el-repo-de-deskops-no-vacía-el-path-de-los-modelos-en-sldb-core-mode: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


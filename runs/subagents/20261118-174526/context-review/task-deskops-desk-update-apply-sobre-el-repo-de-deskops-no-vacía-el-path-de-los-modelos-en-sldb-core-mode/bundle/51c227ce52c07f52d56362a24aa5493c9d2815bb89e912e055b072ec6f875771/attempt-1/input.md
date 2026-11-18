FILE:desk/tasks/task-deskops-desk-update-apply-sobre-el-repo-de-deskops-no-vacía-el-path-de-los-modelos-en-sldb-core-mode.md
---
sldb:
  by: agent
  at: '2026-11-18T17:44:28Z'
  authority: generated
  via: save_document_payload
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

En alcance: (a) reproducir en una copia limpia del HEAD local de deskops al momento del despacho (git clone --no-hardlinks /mnt/ssd/proyectos/SLDB_1/deskops /tmp/repro && git -C /tmp/repro checkout --detach <HEAD>), correr 'deskops desk update --apply --root /tmp/repro' y guardar 'git -C /tmp/repro diff --stat' y 'git -C /tmp/repro diff -- .sldb/core/models sldb/relation_types' en el run dir. (b) Encontrar, con archivo y línea, qué parte de desk update reescribe .sldb/core/models/<Modelo>.yaml con path vacío. La fuente de verdad de la ruta es la entrada models: del .sldb/store.yaml de la raíz del repo (cada modelo con su path, p. ej. RoleDoc -> deskops/models/role.py). (c) Arreglo: desk update nunca deja vacío un path de modelo que ya era no vacío ni que el store.yaml declara. (d) relation types: desk update puede escribir solo los relation types que el paquete deskops declara. El informe muestra, con la ruta del archivo de declaración, si reltype-links_to y el cambio de has_model.md están declarados. Si no lo están, el arreglo evita escribirlos; si lo están, se dejan y se explica. (e) Test que falla antes, en tests/test_desk_sync.py, sobre un desk de prueba armado en tmp_path con el mismo helper que usan los tests existentes de ese archivo, con un store.yaml que declara un modelo con path local: después de desk update --apply el path sigue igual. (f) El ejecutor corre solo tests/test_desk_sync.py y los tests de los archivos que toque; la suite completa la corre integrate. El informe va en result-summary.md del run dir que fija el despacho. Fuera de alcance: cambiar el layout de .sldb.

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
Cold-bundle de la tarea task-deskops-desk-update-apply-sobre-el-repo-de-deskops-no-vacía-el-path-de-los-modelos-en-sldb-core-mode: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/tmp python -m pytest -q tests/test_desk_sync.py


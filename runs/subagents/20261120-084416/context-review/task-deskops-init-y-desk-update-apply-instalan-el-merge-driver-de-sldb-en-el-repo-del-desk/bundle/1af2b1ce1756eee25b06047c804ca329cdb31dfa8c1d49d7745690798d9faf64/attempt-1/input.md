FILE:desk/tasks/task-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk.md
---
sldb:
  by: agent
  at: '2026-11-20T08:43:42Z'
  authority: generated
  via: create_document
id: task-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk
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

# deskops init y desk update --apply instalan el merge driver de sldb en el repo del desk

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261119-154137-suggestion-deskops-init-y-desk-update-deber-an-dejar-instalado-el-merge-driver-de-sldb-en-el-repo-del-desk (pedido de JP, 2026-11-19). sldb ya tiene install_merge_driver (sldb.api.stores.merge_driver_install) y su tarea 'se instala desde los comandos CLI de stores' (sldb 9007f78a) agrega a stores check el alert stores/merge_driver_missing. deskops prepara el store del desk por la API (deskops/bootstrap.py: init_local_store, _init_store con sldb.api.init_store), no por la CLI, así que los desks quedan sin driver. Con ese sldb, deskops doctor muestra el alert nuevo y rompe el golden tests/goldens/doctor_lifecycle_seed_out_of_date.text de tests/test_lifecycle_seed_drift.py::test_pre_cc31_edge_doctor_reports_it_advance_refuses_and_desk_update_fixes_both (verificado 3 de 3 contra sldb 9007f78a; con sldb fd3c024b pasa).

## Goal

_Describe the concrete result this task must produce._

deskops init (BootstrapService.init_local_store) y deskops desk update --apply instalan el merge driver de sldb en el repo del desk cuando el desk es un repo git, llamando a install_merge_driver de sldb sobre el store del desk. Es idempotente, fuera de git no hace nada, y si git falla avisa por stderr sin romper. Con eso, deskops doctor no muestra stores/merge_driver_missing en un desk recién creado, y el golden de doctor_lifecycle_seed_out_of_date.text queda como está, tanto con el sldb actual como con el que trae el alert.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/bootstrap.py (init_local_store o _init_store), el camino de desk update --apply (deskops/cli/commands/desk.py:200 update y lo que llame), tests (uno nuevo en tests/test_bootstrap*.py o tests/test_desk_update*.py que verifique .gitattributes y merge.sldb.driver tras init y tras update en un repo git temporal, y que fuera de git no escriba nada), docs/operator-manual.md y CHANGELOG. Fuera: sldb. Si install_merge_driver no se puede importar (sldb viejo), se omite sin error.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: deskops init en un repo git temporal deja .gitattributes con las tres líneas merge=sldb y merge.sldb.driver en la config; desk update --apply en un desk sin driver lo instala; fuera de git, nada. p2: implementar importando 'from sldb.api.stores.merge_driver_install import install_merge_driver' dentro de un try (ImportError: omitir). p3: correr tests/test_lifecycle_seed_drift.py con el sldb del workspace y, si existe /workspace/sldb, también con PYTHONPATH a un sldb que tenga el alert (sldb 9007f78a: 'git -C /workspace/sldb log --oneline -1 9007f78a'); el golden no cambia. p4: docs, CHANGELOG, commit con rutas nombradas y Task-Id, y deskops advance.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_lifecycle_seed_drift.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos y tests/test_lifecycle_seed_drift.py pasan; la suite completa la corre integrate.

FILE:instruccion
Cold-bundle de la tarea task-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_lifecycle_seed_drift.py


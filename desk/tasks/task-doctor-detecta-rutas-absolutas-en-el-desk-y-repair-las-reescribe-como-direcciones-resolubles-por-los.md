---
sldb:
  by: agent
  at: '2026-11-15T15:29:20Z'
  authority: generated
  via: save_document_payload
id: task-doctor-detecta-rutas-absolutas-en-el-desk-y-repair-las-reescribe-como-direcciones-resolubles-por-los
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

# doctor detecta rutas absolutas en el desk y --repair las reescribe como direcciones resolubles por los links de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Los desks guardan rutas de una máquina (/home/jp/..., /mnt/ssd/...): 20 campos path del registro y 30 documentos en 6 desks. En otra máquina deskops message send falla con PermissionError y resolved-by no encuentra el repo. sldb ya sabe dónde está cada repo vecino: store.yaml declara links con ruta relativa (name: sldb, path: ../sldb/.sldb).

## Goal

_Describe the concrete result this task must produce._

deskops doctor emite una alerta por cada ruta absoluta en un documento del desk (path del registro, files y references de tareas, y cualquier campo de frontmatter). doctor --repair reescribe las que puede resolver: el path del registro como ruta relativa a la raíz del ecosistema y files/references como <repo-id>:<ruta-relativa>, la forma que closeout resolved-by ya acepta.

## Scope

_State what is in scope and what is out of scope._

En alcance: el chequeo en doctor_findings, la reparación por el CLI (escritura vía sldb, nunca a mano), tests con fixtures en tmp_path, CHANGELOG y docs/operator-manual.md. Fuera: correr --repair sobre los desks reales (lo hace el coordinador después) y cambiar sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Decisiones del coordinador (revisables). 1) Fuente de verdad: los links del store.yaml del desk (sldb.api, no parseo a mano) más el registro; la raíz de un repo vecino es el padre de su .sldb enlazado. 2) Ruta que existe en esta máquina y cae bajo la raíz de un repo vecino o del propio repo: reescritura directa. 3) Ruta que no existe (otra máquina): se reescribe solo si su sufijo tras la carpeta del ecosistema nombra sin ambigüedad un repo vecino (p. ej. /home/jp/proyectos/SLDB_1/sldb -> ../sldb); si no, queda como alerta sin reparar, con el motivo. 4) Rutas del propio repo: relativas a su raíz, sin prefijo. 5) La alerta no cambia el código de salida. 6) Un test por caso: existe, de otra máquina, ambigua, del propio repo y un registro con 2 repos; y un test de que tras --repair load_repository_registry resuelve las raíces.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm python -m pytest -q tests/test_doctor_alerts.py y el archivo de tests nuevo del chequeo

## Done When

_Name the observable condition that makes the task complete._

doctor reporta y --repair reescribe las rutas absolutas resolubles en fixtures; los tests nuevos y los archivos de doctor pasan de a uno.

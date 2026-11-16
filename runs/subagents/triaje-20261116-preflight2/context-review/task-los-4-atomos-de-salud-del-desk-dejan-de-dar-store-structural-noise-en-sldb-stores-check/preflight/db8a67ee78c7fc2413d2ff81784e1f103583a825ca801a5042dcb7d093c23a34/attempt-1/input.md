FILE:desk/tasks/task-los-4-atomos-de-salud-del-desk-dejan-de-dar-store-structural-noise-en-sldb-stores-check.md
---
sldb:
  by: agent
  at: '2026-11-16T05:01:58Z'
  authority: generated
  via: save_document_payload
id: task-los-4-atomos-de-salud-del-desk-dejan-de-dar-store-structural-noise-en-sldb-stores-check
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
- desk/atoms (los 4 atomos nombrados)
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-l-nea-base-de-sldb-stores-check-en-el-desk-de-deskops-32-anchors-doc-lost-2-doc-changed-y-4-structural-noise-sin-due-o.md
---

# Los 4 atomos de salud del desk dejan de dar store/structural-noise en sldb stores check

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (linea base de sldb stores check, 2026-11-10). Medido de nuevo el 2026-11-16: rc 0, 0 errores, 121 alertas: 117 anchors/doc_lost (las cubre task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada), 0 doc_changed y 4 store/structural-noise. Estas ultimas son AtomDocs con encabezados que el modelo no declara: atom-desk-health-delegates-store-diagnostics-to-sldb (Boundary Rationale, Delegation Pattern, Evidence, Tags), atom-desk-health-is-measured-by-cli-diagnostics (Diagnostic Surface, Repairability, Evidence, Tags), atom-desk-health-is-workspace-integrity-state (Evidence, Related Atoms, Tags) y atom-desk-repair-is-owned-by-deskops (Owned Operations, Not Owned, Evidence, Tags).

## Goal

_Describe the concrete result this task must produce._

Los 4 atomos quedan sin encabezados fuera del modelo. AtomDoc solo declara id, title, five_wh_one_plus, answer y tags: el contenido de cada seccion pasa al campo answer como un parrafo que empieza con el rotulo en negrita (p. ej. '**Evidencia:** ...'), en el mismo orden que hoy; los Tags se suman al campo tags conservando los que ya tiene; los Related Atoms quedan en answer como '**Atomos relacionados:** atom-a, atom-b'. Cada edicion con deskops edit atom <id> answer "$(cat archivo)" --root . desde un archivo temporal en /dev/shm (para el multilinea) y deskops edit atom <id> tags '[...]' --root . en JSON. Sin perdida: cada linea no vacia de las secciones originales (git show HEAD:<ruta del atomo>) aparece en el answer nuevo. sldb stores check ya no emite store/structural-noise.

## Scope

_State what is in scope and what is out of scope._

Entra: esos 4 atomos en desk/atoms/, editados solo con deskops. No entra: declarar `structural_noise: allow` en .sldb/store.yaml (oculta el sintoma), las 117 alertas doc_lost (otra tarea), cambiar el modelo AtomDoc.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) `deskops show atom <id> --root .` de cada uno. 2) Redactar el answer nuevo sin encabezados. 3) `deskops edit atom` por campo. 4) stores check y graph missing.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=../sldb/src:. ../.venv/bin/python -m sldb stores check --store .sldb --format json (sin codigos store/structural-noise)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (rc 0)

## Done When

_Name the observable condition that makes the task complete._

stores check no lista store/structural-noise y cada atomo conserva su contenido original en sus campos.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-los-4-atomos-de-salud-del-desk-dejan-de-dar-store-structural-noise-en-sldb-stores-check: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


FILE:desk/tasks/task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply.md
---
sldb:
  by: agent
  at: '2026-11-16T05:04:05Z'
  authority: generated
  via: save_document_payload
id: task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply
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
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-retirar-caminos-legacy-migrar-los-datos-y-borrar-el-c-digo-de-compatibilidad.md
---

# TraderBot y sldb migran sus task_type viejos con deskops desk update --apply

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (retirar caminos legacy, punto 1, inventario del 2026-11-10): consumidores del mapa de task_type viejo: TraderBot (21 tareas) y sldb (1). TraderBot no esta en robocop2 (registro ~/setup/desk/registry/repo-traderbot.md); sldb esta en /mnt/ssd/proyectos/SLDB_1/sldb. Espejo externo de una dependencia de la tarea que borra la migracion.

## Goal

_Describe the concrete result this task must produce._

En los desks de TraderBot y sldb, `deskops desk update --apply` migro los task_type viejos y quedo commiteado; ninguna tarea de esos desks usa ya code/implementation/test/docs/spec/design/external sin prefijo task.

## Scope

_State what is in scope and what is out of scope._

Entra: pedir la migracion por inbox y registrar las respuestas. sldb: deskops message send --to sldb --title 'Migrar task_type viejos con deskops desk update --apply' con el pedido y el criterio (ningun task_type fuera de la lista de deskops add task --help). TraderBot no esta registrado con ruta valida en robocop2: el pedido va a JP en el informe del coordinador, que lo hace llegar a la maquina donde vive TraderBot. Cada respuesta se registra agregando el commit (repo:sha o URL) al campo references de esta tarea con deskops edit task. No entra: escribir en esos repos desde deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) `deskops message send --to sldb ...` y `--to traderbot ...` (si --to traderbot no resuelve en robocop2, pedirlo a JP para la maquina donde vive TraderBot). 2) Registrar los commits de respuesta.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/sldb && grep -h "^task_type:" desk/tasks/*.md desk/drawer/tasks/*.md | sort | uniq -c (solo valores task.code, task.docs, task.debug, task.refactor, task.decision, task.aggregate, task.external o subtipos locales registrados)
- TraderBot: el commit de migracion que reporte su desk, citado en references

## Done When

_Name the observable condition that makes the task complete._

Ambos desks respondieron con el commit de migracion.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


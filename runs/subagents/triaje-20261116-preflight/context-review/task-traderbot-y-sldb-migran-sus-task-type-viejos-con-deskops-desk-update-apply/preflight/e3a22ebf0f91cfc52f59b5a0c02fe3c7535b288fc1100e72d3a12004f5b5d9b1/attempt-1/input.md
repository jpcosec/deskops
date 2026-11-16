FILE:desk/tasks/task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply.md
---
sldb:
  by: agent
  at: '2026-11-16T04:03:45Z'
  authority: generated
  via: create_document
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

Entra: pedir la migracion a cada desk por inbox y registrar los commits. No entra: escribir en esos repos desde deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) `deskops message send --to sldb ...` y `--to traderbot ...` (si --to traderbot no resuelve en robocop2, pedirlo a JP para la maquina donde vive TraderBot). 2) Registrar los commits de respuesta.

## Validation

_List the checks required before this task can close._

- grep -rhoE '^task_type: [a-z]+$' <desk>/desk/tasks/*.md en cada desk (sin valores sin prefijo task.)

## Done When

_Name the observable condition that makes the task complete._

Ambos desks respondieron con el commit de migracion.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.


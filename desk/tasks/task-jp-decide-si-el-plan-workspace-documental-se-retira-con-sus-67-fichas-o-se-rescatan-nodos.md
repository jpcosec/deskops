---
sldb:
  by: agent
  at: '2026-11-16T04:04:36Z'
  authority: generated
  via: create_document
id: task-jp-decide-si-el-plan-workspace-documental-se-retira-con-sus-67-fichas-o-se-rescatan-nodos
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/cierre.md
- desk/drawer/plans/deskops-ui/decisiones.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental
- desk/drawer/tasks/workspace-documental
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# JP decide si el plan workspace-documental se retira con sus 67 fichas o se rescatan nodos

## Rationale

_Explain why this task exists or the business driver behind it._

El plan desk/drawer/plans/workspace-documental (rev 10, final_plan_reviewed, execution_authorized: false) esta parado desde 2026-11-02. Ejecutados: WS01-WS04 y WS06-WS12 (cierres 0861f9b4, 9dd027c5, ad3a21be, ff28c68c, 7b045a6f, e868178c, 85291046, b6242579, 65f76c46, 4e46f60d). Nunca ejecutados: WS05 (inventario scion), producto en graph_ui (WS13-WS16, WS19, WS21-WS30, WS35-WS37, WS39-WS42, WS48), sldb (WS20, WS45, WS47), spec2viz (WS18) y documentales/scion de deskops (WS17, WS31-WS34, WS38, WS43, WS44, WS46). En la practica lo reemplazo el plan deskops-ui (DU1, 2026-11-04: el producto es la UI de deskops y no un explorador del store), ya ejecutado. Sus 67 fichas estan en desk/drawer/tasks/workspace-documental/ y dag.yaml las cita por task_file.

## Goal

_Describe the concrete result this task must produce._

JP decide: (a) retirar el plan entero (se borran el directorio del plan y las 67 fichas en un commit que cita los cierres); o (b) rescatar nodos concretos (candidatos: WS20/WS45/WS47 escritura en sldb, WS19/WS21 edicion, WS32-WS38 scion), que se convierten en tareas en su desk, y retirar el resto.

## Scope

_State what is in scope and what is out of scope._

Entra: la decision y su ejecucion documental (borrado o tareas de rescate). No entra: implementar nodos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Presentar a JP el estado. 2) Registrar el recibo owner. 3) Ejecutar el retiro o crear las tareas de rescate (en otros desks por message send).

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (rc 0 tras el retiro)

## Done When

_Name the observable condition that makes the task complete._

La decision esta registrada y el drawer refleja el resultado (plan retirado o nodos rescatados como tareas).

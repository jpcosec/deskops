---
sldb:
  by: agent
  at: '2026-11-22T21:20:45Z'
  authority: generated
  via: save_document_payload
id: task-governance-closeout-no-borra-una-tarea-de-la-que-otras-heredan-inherits-from-o-las-herederas-siguen
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-132316-suggestion-closeout-borra-una-tarea-aunque-otras-hereden-de-ella-inherits-from-y-esas-dejan-de-cargar.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Governance: closeout no borra una tarea de la que otras heredan (inherits_from), o las herederas siguen cargando

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de Governance 20261122-132316-suggestion-closeout-borra-una-tarea-aunque-otras-hereden-de-ella-inherits-from-y-esas-dejan-de-cargar (2026-11-22): Caso en Governance (2026-11-22): task-coherencia-de-los-clientes-del-kit-con-el-kit-y-versiones se cerró con closeout el 11-11 (commit 40fc9e2, PR heyantonia/Governance#107) y su archivo se borró. Dos tareas en draft la tenían en inherits_from (task-leer-antonia-cobranza-y-pyme-chatbots… y task-satélites-relockear-uv-lock…). Desde entonces 'deskops list tasks' las saltaba con 'Warning: Failed to load task …: No task file found for selector …', y nadie lo vio en once días porque es solo un aviso. Se arregló a mano con 'deskops edit task <id> inherits_from []' y pasando la tarea cerrada a references (heyantonia/Governance#141). Lo que falta en deskops, a decidir por quien lo mantiene: (1) closeout no revisa si otras tareas heredan de la que borra; podría negarse, avisar, o reescribir la herencia; (2) una tarea con inherits_from roto deja de cargar entera en vez de cargar sin la herencia; (3) doctor no lo detecta como estado roto.

## Goal

_Describe the concrete result this task must produce._

Concretar el pedido en una tarea preparada: que closeout se niegue a borrar (o avise y conserve una referencia resoluble de) una tarea que otras abiertas tienen en inherits_from, y que list tasks no salte en silencio a las herederas. Borrador: no despachar hasta prepararlo.

## Scope

_State what is in scope and what is out of scope._



## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

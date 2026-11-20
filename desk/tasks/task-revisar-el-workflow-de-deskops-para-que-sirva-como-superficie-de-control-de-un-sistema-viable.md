---
sldb:
  by: agent
  at: '2026-11-20T02:26:09Z'
  authority: generated
  via: create_document
id: task-revisar-el-workflow-de-deskops-para-que-sirva-como-superficie-de-control-de-un-sistema-viable
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
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Revisar el workflow de deskops para que sirva como superficie de control de un sistema viable

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de JP del 2026-11-19: deskops se concibió para algo muy distinto; ahora necesita más flexibilidad, autorreflexión y servir de verdad como superficie de control, para que cada desk se comporte como un sistema viable (VSM). El diagnóstico VSM de AntonIA del 19-11 mostró que el ciclo completo cuesta más que el cambio y se salta (mepu: 172 de 177 tareas en draft), que el desk no se entera de lo que pasa en GitHub, y que no hay nivel por encima de un desk (heyantonia/Governance, docs/diagnostico-vsm-2026-11-19/).

## Goal

_Describe the concrete result this task must produce._

Un diseño revisado del workflow de deskops: qué ritos y compuertas quedan, cuáles se vuelven opcionales o livianos, cómo el desk se mira a sí mismo (autorreflexión: medir su propio estado y avisar cuando miente), y qué funciones del VSM (ejecución, coordinación, regulación, auditoría, anticipación, clausura, corte) sostiene cada pieza del desk, con recursión de un desk de repo a uno de organización.

## Scope

_State what is in scope and what is out of scope._

Dentro: el ciclo de vida de tareas, los ritos, las compuertas, el inbox, el drawer, las revisiones en frío y la relación entre desks. Fuera: implementar; las interfaces MCP y UI son otras tareas.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

El diseño está escrito, revisado por el concilio y aprobado por JP, con la lista de tareas que lo implementan.

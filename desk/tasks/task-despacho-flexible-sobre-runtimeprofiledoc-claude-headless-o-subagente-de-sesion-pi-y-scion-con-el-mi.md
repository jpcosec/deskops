---
sldb:
  by: agent
  at: '2026-11-25T19:47:57Z'
  authority: generated
  via: create_document
id: task-despacho-flexible-sobre-runtimeprofiledoc-claude-headless-o-subagente-de-sesion-pi-y-scion-con-el-mi
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-el-prompt-de-una-tarea-es-una-vista-del-nucleo-un-solo-texto-sin-contradicciones
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Despacho flexible sobre RuntimeProfileDoc: claude (headless o subagente de sesión), pi y scion, con el mismo prompt y el mismo runner que la revisión

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

deskops despacha una tarea con cualquier perfil de runtime del desk usando el prompt de la tarea, y la revisión en frío usa el mismo runner; scion queda como un adaptador más.

## Scope

_State what is in scope and what is out of scope._

Entra: un runner con adaptadores claude, pi y scion; review lo usa; el modo subagente de sesión entrega el prompt sin lanzar. Sale: decidir qué perfil usa cada desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Interfaz de adaptador. 2) Adaptadores. 3) review sobre el runner. 4) Tests con adaptadores falsos.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/ops tests/surfaces

## Done When

_Name the observable condition that makes the task complete._

Una tarea se despacha con claude, pi o scion cambiando solo el perfil.

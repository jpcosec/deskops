---
sldb:
  by: agent
  at: '2026-11-25T19:47:46Z'
  authority: generated
  via: create_document
id: task-el-prompt-de-una-tarea-es-una-vista-del-nucleo-un-solo-texto-sin-contradicciones
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-las-operaciones-de-deskops-se-definen-una-sola-vez-como-herramientas-mcp-en-una-extension-del-servid
- task-un-solo-texto-por-rito-next-actions-y-nombres-de-nodo-salen-del-ritualdoc-y-se-borra-task-lifecycle
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El prompt de una tarea es una vista del núcleo, un solo texto sin contradicciones

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Una operación devuelve el prompt de una tarea: la tarea, su contexto (pills, átomos, archivos), lo que advance exige y las reglas de entrega del RoleDoc del rol, sin las instrucciones contradictorias de hoy (N5); dispatch start --only-prompt lo escribe sin lanzar nada.

## Scope

_State what is in scope and what is out of scope._

Entra: la operación, --only-prompt, unificar prompt.md y agents.md. Sale: los adaptadores de despacho.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Vista o operación. 2) Quitar el texto duplicado de dispatch.py y runtime/scion.py. 3) Test de contrato.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/surfaces tests/core

## Done When

_Name the observable condition that makes the task complete._

dispatch start --only-prompt escribe un prompt sin contradicciones.

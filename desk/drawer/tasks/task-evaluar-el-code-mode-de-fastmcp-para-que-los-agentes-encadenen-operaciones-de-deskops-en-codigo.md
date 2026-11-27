---
sldb:
  by: agent
  at: '2026-11-25T19:48:43Z'
  authority: generated
  via: create_document
id: task-evaluar-el-code-mode-de-fastmcp-para-que-los-agentes-encadenen-operaciones-de-deskops-en-codigo
status: deferred
summary: ''
tags: []
current_node: ''
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-las-operaciones-de-deskops-se-definen-una-sola-vez-como-herramientas-mcp-en-una-extension-del-servid
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Evaluar el code mode de FastMCP para que los agentes encadenen operaciones de deskops en código

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Saber si el code mode de FastMCP sirve para que un agente encadene varias operaciones de deskops en un solo paso, con qué límites y qué cambia en las herramientas.

## Scope

_State what is in scope and what is out of scope._

Entra: prueba sobre el servidor con la extensión de deskops y un átomo con el resultado. Sale: adoptarlo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer la doc de code mode. 2) Prueba. 3) Átomo.

## Validation

_List the checks required before this task can close._

- Hay un átomo con el resultado de la prueba

## Done When

_Name the observable condition that makes the task complete._

Hay un átomo con la evaluación.

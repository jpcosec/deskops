---
sldb:
  by: agent
  at: '2026-11-25T19:50:02Z'
  authority: generated
  via: create_document
id: task-m0-estructura-deskops-por-capas-y-una-sola-capa-de-operaciones-como-herramientas-mcp
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-deskops-se-ordena-en-paquetes-por-capa-core-ops-runtime-operations-surfaces-con-contratos-de-imports
- task-verificar-fastmcp-call-generate-cli-inspect-e-install-contra-sldb-mcp-con-una-extension-de-deskops
- task-las-operaciones-de-deskops-se-definen-una-sola-vez-como-herramientas-mcp-en-una-extension-del-servid
pills: []
files: []
task_type: task.aggregate
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# M0 Estructura: deskops por capas y una sola capa de operaciones como herramientas MCP

## Rationale

_Explain why this task exists or the business driver behind it._

Macro del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md); agrupa sus subtareas por capa.

## Goal

_Describe the concrete result this task must produce._

Todas las subtareas de M0 cerradas.

## Scope

_State what is in scope and what is out of scope._

Entra: las subtareas listadas en depends_on. Sale: trabajo de otras macros.

## Implementation Path

_Outline the expected implementation route or affected surface._

Se cierra cuando cierran sus subtareas.

## Validation

_List the checks required before this task can close._

- Todas las tareas de depends_on están cerradas

## Done When

_Name the observable condition that makes the task complete._

Todas las subtareas cerradas.

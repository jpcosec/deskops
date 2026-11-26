---
sldb:
  by: agent
  at: '2026-11-25T20:28:27Z'
  authority: generated
  via: create_document
id: task-e2-pluginizacion-las-operaciones-como-herramientas-mcp-sobre-sldb-cli-generado-y-docs-que-salen-de-a
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-verificar-fastmcp-call-generate-cli-inspect-e-install-contra-sldb-mcp-con-una-extension-de-deskops
- task-las-operaciones-de-deskops-se-definen-una-sola-vez-como-herramientas-mcp-en-una-extension-del-servid
- task-el-prompt-de-una-tarea-es-una-vista-del-nucleo-un-solo-texto-sin-contradicciones
- task-el-cli-de-deskops-sale-de-fastmcp-generate-cli-y-el-cli-escrito-a-mano-queda-solo-para-bootstrap-e-i
- task-deskops-se-instala-en-claude-code-y-otros-clientes-con-fastmcp-install
- task-la-skill-deskops-workflow-es-el-skill-md-generado-por-fastmcp-mas-una-parte-corta-del-workflow-desde
- task-agents-md-sin-contradicciones
- task-los-docs-de-deskops-son-materializaciones-de-atomos-con-una-pagina-por-capa
pills: []
files: []
task_type: task.aggregate
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# E2 Pluginización: las operaciones como herramientas MCP sobre sldb, CLI generado y docs que salen de ahí

## Rationale

_Explain why this task exists or the business driver behind it._

Reorganización del 25-11 por etapas (JP): refactor, pluginización, responsabilidades a sldb, rediseño del testing y recién después los pedidos individuales (en el drawer). Base: desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md.

## Goal

_Describe the concrete result this task must produce._

Todas las subtareas de E2 cerradas.

## Scope

_State what is in scope and what is out of scope._

Entra: las subtareas de depends_on. Sale: los pedidos individuales del drawer y las otras etapas.

## Implementation Path

_Outline the expected implementation route or affected surface._

Se cierra cuando cierran sus subtareas.

## Validation

_List the checks required before this task can close._

- Todas las tareas de depends_on están cerradas

## Done When

_Name the observable condition that makes the task complete._

Todas las subtareas cerradas.

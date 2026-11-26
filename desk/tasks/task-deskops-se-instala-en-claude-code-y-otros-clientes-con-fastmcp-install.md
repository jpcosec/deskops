---
sldb:
  by: agent
  at: '2026-11-25T19:48:20Z'
  authority: generated
  via: create_document
id: task-deskops-se-instala-en-claude-code-y-otros-clientes-con-fastmcp-install
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-las-operaciones-de-deskops-se-definen-una-sola-vez-como-herramientas-mcp-en-una-extension-del-servid
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops se instala en Claude Code y otros clientes con fastmcp install

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Un comando instala el servidor de sldb con la extensión de deskops en Claude Code (y Cursor, Gemini CLI) para el desk del repo.

## Scope

_State what is in scope and what is out of scope._

Entra: el comando y su doc. Sale: nada más.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) fastmcp install. 2) Probar en Claude Code. 3) Doc.

## Validation

_List the checks required before this task can close._

- fastmcp install deja el servidor disponible en Claude Code

## Done When

_Name the observable condition that makes the task complete._

Claude Code ve las herramientas de deskops del desk.

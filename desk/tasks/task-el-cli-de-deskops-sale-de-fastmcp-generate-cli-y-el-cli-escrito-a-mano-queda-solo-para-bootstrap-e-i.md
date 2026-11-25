---
sldb:
  by: agent
  at: '2026-11-25T19:48:08Z'
  authority: generated
  via: create_document
id: task-el-cli-de-deskops-sale-de-fastmcp-generate-cli-y-el-cli-escrito-a-mano-queda-solo-para-bootstrap-e-i
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

# El CLI de deskops sale de fastmcp generate-cli y el CLI escrito a mano queda solo para bootstrap e init

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

El CLI de uso diario es el que genera fastmcp generate-cli desde las herramientas (o fastmcp call), regenerado en el build; cli/registry.py deja de existir salvo lo que no es herramienta.

## Scope

_State what is in scope and what is out of scope._

Entra: generación en el build, CLI mínimo de bootstrap e init, borrar registry.py y los goldens de ayuda. Sale: cambiar operaciones.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Generar. 2) CLI mínimo. 3) Borrar registry. 4) Test de contrato CLI = MCP.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/surfaces

## Done When

_Name the observable condition that makes the task complete._

cli/registry.py no existe y el CLI generado cubre todas las operaciones.

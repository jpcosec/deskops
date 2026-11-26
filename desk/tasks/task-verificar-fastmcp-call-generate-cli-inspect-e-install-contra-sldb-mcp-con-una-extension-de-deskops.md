---
sldb:
  by: agent
  at: '2026-11-25T19:42:06Z'
  authority: generated
  via: create_document
id: task-verificar-fastmcp-call-generate-cli-inspect-e-install-contra-sldb-mcp-con-una-extension-de-deskops
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on: []
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Verificar fastmcp call, generate-cli, inspect e install contra sldb mcp con una extensión de deskops

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Saber con una prueba real si las herramientas cliente de FastMCP v3 funcionan contra el servidor de sldb (SDK oficial mcp>=2.2) con una extensión de prueba de deskops, y qué limitaciones tienen.

## Scope

_State what is in scope and what is out of scope._

Entra: una extensión mínima con dos herramientas, fastmcp call, generate-cli (incluido el SKILL.md), inspect e install en Claude Code; anotar versiones y límites. Sale: escribir las herramientas reales.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Extensión mínima register(server, context) con dos herramientas. 2) sldb mcp --extension. 3) Probar cada comando de fastmcp. 4) Escribir el resultado en un átomo.

## Validation

_List the checks required before this task can close._

- fastmcp call contra sldb mcp devuelve el resultado de la herramienta de prueba
- fastmcp generate-cli produce un cli.py y un SKILL.md que invocan la herramienta de prueba

## Done When

_Name the observable condition that makes the task complete._

Hay un átomo que dice qué comandos de FastMCP funcionan contra sldb mcp y con qué límites.

---
sldb:
  by: agent
  at: '2026-11-20T02:23:45Z'
  authority: generated
  via: create_document
id: task-interfaz-mcp-de-deskops-compatible-con-claude-code
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
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Interfaz MCP de deskops compatible con Claude Code

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de JP del 2026-11-19 (diagnóstico VSM de AntonIA): a deskops le falta con urgencia una interfaz MCP. Hoy los agentes usan el desk solo por el CLI, y JP quiere que el desk sea el contexto común que leen los Claude de todos y el canal formal entre repos. Hay piezas para partir: sldb ya tiene un paquete mcp (sldb/src/sldb/mcp), Governance tiene vsm-state (MCP de solo lectura sobre sldb serve) y deskops view ya define el contrato de datos de la UI (docs/deskops-ui.md: board, task, drawer, inbox, agents).

## Goal

_Describe the concrete result this task must produce._

Un servidor MCP de deskops que Claude Code pueda registrar con claude mcp add: lectura del desk (board, tareas, inbox, drawer, agentes, siguiente acción de una tarea) y las escrituras que hoy hace el CLI (crear tarea, mandar y acusar notas entre desks, avanzar, cerrar), pasando por las mismas reglas y compuertas.

## Scope

_State what is in scope and what is out of scope._

Dentro: el servidor, sus herramientas sobre deskops view y los verbos del CLI, y la documentación para registrarlo. Fuera: la UI (otra tarea) y cambiar las compuertas.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- pytest de las herramientas del MCP
- Una sesión de Claude Code de prueba contra un desk temporal

## Done When

_Name the observable condition that makes the task complete._

Desde una sesión de Claude Code con el MCP registrado se puede leer el board de un desk, crear una tarea, mandar una nota a otro desk y cerrarla, y una escritura que viola una compuerta es rechazada igual que en el CLI.

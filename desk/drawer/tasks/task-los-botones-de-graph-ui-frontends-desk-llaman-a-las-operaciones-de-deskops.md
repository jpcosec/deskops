---
sldb:
  by: agent
  at: '2026-11-25T19:48:32Z'
  authority: generated
  via: create_document
id: task-los-botones-de-graph-ui-frontends-desk-llaman-a-las-operaciones-de-deskops
status: deferred
summary: ''
tags: []
current_node: ''
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-las-operaciones-de-deskops-se-definen-una-sola-vez-como-herramientas-mcp-en-una-extension-del-servid
- task-el-cli-de-deskops-sale-de-fastmcp-generate-cli-y-el-cli-escrito-a-mano-queda-solo-para-bootstrap-e-i
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Los botones de graph_ui/frontends/desk llaman a las operaciones de deskops

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Iniciar ejecución, promover y diferir de la UI de deskops en graph_ui dejan de estar deshabilitados y llaman a las operaciones; la vista board muestra lo que aplica commit, no el ok de verify (N14).

## Scope

_State what is in scope and what is out of scope._

Entra: el cableado en UIs/graph_ui (pedido por su inbox) y la vista board. Sale: rediseñar la UI.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Nota al inbox de graph_ui con las operaciones. 2) Vista board correcta.

## Validation

_List the checks required before this task can close._

- La UI ejecuta las operaciones en un desk de prueba

## Done When

_Name the observable condition that makes the task complete._

Los botones funcionan sobre un desk de prueba.

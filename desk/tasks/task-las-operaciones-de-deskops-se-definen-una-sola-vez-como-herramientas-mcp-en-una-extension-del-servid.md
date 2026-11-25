---
sldb:
  by: agent
  at: '2026-11-25T19:42:18Z'
  authority: generated
  via: create_document
id: task-las-operaciones-de-deskops-se-definen-una-sola-vez-como-herramientas-mcp-en-una-extension-del-servid
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
- ../sldb/docs/architecture/mcp.md
depends_on:
- task-deskops-se-ordena-en-paquetes-por-capa-core-ops-runtime-operations-surfaces-con-contratos-de-imports
- task-verificar-fastmcp-call-generate-cli-inspect-e-install-contra-sldb-mcp-con-una-extension-de-deskops
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Las operaciones de deskops se definen una sola vez como herramientas MCP en una extensión del servidor de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Una sola capa de operaciones (deskops/operations) expuesta como herramientas MCP con la API de extensión de sldb (build_server, extensions), con su guard, niveles y señales; CLI, MCP y UI la consumen.

## Scope

_State what is in scope and what is out of scope._

Entra: operaciones del núcleo y de operación (show, list, next, advance, closeout verify y commit, review, dispatch prompt, message, doctor). Sale: bootstrap e init, que necesitan correr antes de que exista un store.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario de operaciones desde las dos operations.py actuales y el registry. 2) Una función por operación en deskops/operations. 3) register(server, context) que las publica. 4) Tests de contrato por operación.

## Validation

_List the checks required before this task can close._

- sldb mcp --extension deskops.surfaces.mcp:register lista las herramientas de deskops
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

Cada operación existe una vez en deskops/operations y se publica como herramienta MCP.

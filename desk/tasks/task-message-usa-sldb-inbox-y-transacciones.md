---
sldb:
  by: agent
  at: '2026-11-25T19:46:39Z'
  authority: generated
  via: create_document
id: task-message-usa-sldb-inbox-y-transacciones
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-deskops-se-ordena-en-paquetes-por-capa-core-ops-runtime-operations-surfaces-con-contratos-de-imports
pills: []
files: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# message usa sldb inbox y transacciones

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

send, list, read y ack de message se apoyan en sldb inbox y transaction; deskops conserva solo --to, ack y wake.

## Scope

_State what is in scope and what is out of scope._

Entra: cli/commands/message.py. Sale: wake.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reemplazo. 2) Esquema común de InboxNoteDoc. 3) Tests.

## Validation

_List the checks required before this task can close._

- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

message.py no escribe archivos a mano.

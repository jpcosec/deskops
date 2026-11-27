---
sldb:
  by: agent
  at: '2026-11-25T20:14:36Z'
  authority: generated
  via: create_document
id: task-el-inbox-admite-avisos-kind-alert-ademas-de-unclear-y-suggestion-d5-de-governance
status: deferred
summary: ''
tags: []
current_node: ''
history: []
references:
- deskops/models/inbox.py
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El inbox admite avisos (kind alert) además de unclear y suggestion (D5 de Governance)

## Rationale

_Explain why this task exists or the business driver behind it._

JP adoptó el 25-11 la D5 del spec de Governance: InboxNoteDoc.kind admite alert (hoy deskops/models/inbox.py solo admite unclear y suggestion), para que el sistema pueda avisar a un desk por su inbox.

## Goal

_Describe the concrete result this task must produce._

Una nota de inbox puede ser de kind alert, message send la acepta y la vista del inbox la distingue.

## Scope

_State what is in scope and what is out of scope._

Entra: el valor alert en InboxNoteDoc.kind, message send --kind alert, la vista del inbox y la migración. Sale: quién emite avisos (el agente de coherencia está diferido).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Campo. 2) message send. 3) Vista. 4) Test.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core tests/surfaces

## Done When

_Name the observable condition that makes the task complete._

deskops message send --kind alert crea una nota que la vista del inbox muestra como aviso.

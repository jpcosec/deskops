---
id: task-runtime-template-el-coordinador-lanza-hijos-con-harness-auth-api-key-fijo
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# runtime template: el coordinador lanza hijos con --harness-auth api-key fijo

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261115-215933-suggestion-runtime-template-el-coordinador-lanza-hijos-con-harness-auth-api-key-fijo.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261115-215933-suggestion-runtime-template-el-coordinador-lanza-hijos-con-harness-auth-api-key-fijo.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Piloto scion en IR, fase 0 (reports/scion-piloto-ir-20261115.md). scion_start_argv y el agents.md del coordinador (_render_coordinator_agents_md) escriben 'scion start ... --harness-auth api-key' para executor y tester. Un hijo claude con la suscripción (secret de archivo CLAUDE_AUTH, auth-file) o con CLAUDE_CODE_OAUTH_TOKEN (oauth-token) no arranca así: pide ANTHROPIC_API_KEY. Desde 4b74cdcd el template del hijo ya elige su auth_selectedType con --harness-auth; falta que el argv de start y el texto del coordinador usen el auth del template del hijo (o no pasen --harness-auth y dejen que mande el template). Hace falta antes de la fase 1 (coordinador scion en IR con ejecutores claude).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.

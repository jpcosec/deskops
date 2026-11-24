---
sldb:
  by: agent
  at: '2026-11-24T18:28:11Z'
  authority: generated
  via: save_document_payload
id: task-governance-documento-de-pr-en-desk-prs-y-deskops-pr-check-en-ci
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261120-193937-suggestion-documento-de-pr-en-desk-prs-y-pr-check-en-ci.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Governance: documento de PR en desk/PRS y deskops pr check en CI

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de Governance 20261120-193937-suggestion-documento-de-pr-en-desk-prs-y-pr-check-en-ci.md (2026-11-20): Decisión de JP (19-11): todo PR a dev trae un documento en desk/PRS que explica qué, cómo, cuándo, dónde y por qué, sin el ritual completo. Pedido: un modelo para ese documento, un comando deskops pr check que corra en CI y rechace el PR sin documento, con un campo vacío o que nombre una tarea inexistente, y la generación del documento desde una tarea macro (task.aggregate con children; el campo children todavía no existe, ver data/rules/closeout-evidence.yaml). Fuente: heyantonia/Governance, rama dev, la propuesta de workflow del diagnóstico VSM (propuesta-workflow.md, en el repo Governance), sección 2.

## Goal

_Describe the concrete result this task must produce._

Concretar el pedido de la nota en una tarea preparada (goal, scope, implementation path y validación verificables) o en task.decision para JP si depende de una decisión todavía abierta. Borrador: no despachar hasta prepararlo.

## Scope

_State what is in scope and what is out of scope._



## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

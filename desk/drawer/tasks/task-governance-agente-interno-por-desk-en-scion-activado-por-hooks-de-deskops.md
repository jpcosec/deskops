---
sldb:
  by: agent
  at: '2026-11-24T18:28:01Z'
  authority: generated
  via: save_document_payload
id: task-governance-agente-interno-por-desk-en-scion-activado-por-hooks-de-deskops
status: deferred
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261120-194002-suggestion-agente-interno-por-desk-en-scion-activado-por-hooks.md
- desk/inbox/20261122-234436-suggestion-hook-que-despierta-a-la-identidad-scion-del-desk-cuando-llega-una-nota-al-inbox.md
- desk/inbox/20261122-234447-suggestion-roledoc-de-identidad-de-desk-desk-identity-y-su-traduccion-a-agente-scion.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Governance: agente interno por desk en scion activado por hooks de deskops

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de Governance 20261120-194002-suggestion-agente-interno-por-desk-en-scion-activado-por-hooks.md (2026-11-20): Decisión de JP (20-11): un agente interno por desk que hace el mantenimiento (triaje del inbox, proponer cierres, armar los PR de desk), corre en scion y se activa por hooks de deskops. Además lee el canal informal de scion y propone tareas o notas de inbox cuando detecta un compromiso. No toca código, no se audita a sí mismo y no decide lo que es de una persona. Falta: hooks por evento (hoy lifecycle_hooks.py solo corre al avanzar una transición), actor en history y una identidad propia. Fuente: heyantonia/Governance, rama dev, la propuesta de workflow del diagnóstico VSM (propuesta-workflow.md, en el repo Governance), secciones 6 y 7.

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

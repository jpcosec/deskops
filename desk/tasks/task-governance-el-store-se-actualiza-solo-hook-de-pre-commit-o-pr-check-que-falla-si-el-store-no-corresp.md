---
sldb:
  by: agent
  at: '2026-11-24T02:18:28Z'
  authority: generated
  via: save_document_payload
id: task-governance-el-store-se-actualiza-solo-hook-de-pre-commit-o-pr-check-que-falla-si-el-store-no-corresp
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261121-040315-suggestion-el-store-se-actualiza-solo-hook-de-pre-commit-o-paso-de-pr-check.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Governance: el store se actualiza solo (hook de pre-commit o pr check que falla si el store no corresponde al árbol)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de Governance 20261121-040315 (2026-11-21): Hoy nada actualiza el store cuando cambia un documento del desk o de docs: depende de que alguien corra 'sldb stores update' y 'deskops desk update --apply'. En Governance el store quedó atrasado varios días y hubo que repararlo a mano (heyantonia/Governance#130); JP: 'no veo por qué esto no es algo automático'. Pedido: que deskops instale un hook de pre-commit que registre lo editado (o, si no se quiere tocar el commit, que 'pr check' falle cuando el store no corresponde al árbol y diga el comando que lo arregla). Relacionado: en shared_llm-gateway, cada comando de deskops sembraba 11 reglas de desk/lifecycle sin registrar hasta que entraron por heyantonia/shared_llm-gateway#40; la siembra de reglas nuevas debería quedar registrada por el mismo mecanismo.

## Goal

_Describe the concrete result this task must produce._

Concretar el pedido de la nota en una tarea preparada (goal, scope, implementation path y validación verificables) o en task.decision para JP si depende de una decisión abierta. Borrador: no despachar hasta prepararlo.

## Scope

_State what is in scope and what is out of scope._



## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

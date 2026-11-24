---
sldb:
  by: agent
  at: '2026-11-24T18:28:33Z'
  authority: generated
  via: save_document_payload
id: task-governance-message-send-to-y-list-tasks-include-repos-resuelven-el-repo-por-la-ruta-del-registro-no
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261120-194034-suggestion-message-send-to-y-list-tasks-include-repos-resuelven-por-ruta-del-registro-no-por-nombre.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Governance: message send --to y list tasks --include-repos resuelven el repo por la ruta del registro, no por el nombre

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de Governance 20261120-194034-suggestion-message-send-to-y-list-tasks-include-repos-resuelven-por-ruta-del-registro-no-por-nombre.md (2026-11-20): Al despachar desde Governance: --to y --include-repos ubican el repo destino por el campo path de la ficha en desk/registry, que es una ruta relativa propia de cada máquina. Una ficha sin path (repo-votaciones) hace fallar list tasks --include-repos con «Missing required field: 'path'». JP (20-11): la identidad de un store es su nombre y es igual en todas las máquinas; la ruta es de cada una. sldb ya resuelve los enlaces por nombre contra el catálogo de la máquina (jpcosec/sldb#3, sldb.store.link_path.resolve_link). Pedido: que el registro de deskops resuelva igual, y que una ficha sin ruta se salte con aviso en vez de botar la consulta. Estos mensajes se entregaron con --desk-root a un worktree por ese motivo.

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

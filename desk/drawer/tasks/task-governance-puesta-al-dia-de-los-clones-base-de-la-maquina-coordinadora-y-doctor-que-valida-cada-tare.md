---
sldb:
  by: agent
  at: '2026-11-24T18:28:43Z'
  authority: generated
  via: save_document_payload
id: task-governance-puesta-al-dia-de-los-clones-base-de-la-maquina-coordinadora-y-doctor-que-valida-cada-tare
status: deferred
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261121-040358-suggestion-clones-base-de-una-m-quina-coordinadora-y-doctor-que-valide-cada-tarea.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Governance: puesta al día de los clones base de la máquina coordinadora y doctor que valida cada tarea contra su modelo

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de Governance 20261121-040358 (2026-11-21): robocop 1 es desde el 20-11 el coordinador de robocop 2 y el maestro de los desks: tiene clones base de los repos gobernados en /srv/repos y su catálogo ~/.sldb los conoce por nombre. Hoy esos clones se ponen al día con 'git pull' a mano, repo por repo, y no hay 'wt' instalado. Pedido 1: un comando de deskops (o un rito programado) que recorra los repos del registro, los ponga al día en su rama base, actualice el catálogo e informe los que no pudo avanzar; y que el flujo de worktrees funcione igual en esa máquina que en un laptop. Pedido 2: una migración de ciclo de vida dejó cinco tareas inválidas en shared_llm-gateway (status superseded o deferred con history vacío, o draft con historia de closeout) y 'deskops doctor' decía 'Desk is healthy'. doctor debería validar cada tarea contra su modelo: una sola inválida bota 'sldb find --global' en todos los desks que enlazan ese store. Se cerraron con closeout supersede, retire y resolved-by en heyantonia/shared_llm-gateway#40.

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

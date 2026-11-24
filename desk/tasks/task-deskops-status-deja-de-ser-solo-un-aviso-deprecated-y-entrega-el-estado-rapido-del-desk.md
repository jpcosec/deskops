---
sldb:
  by: agent
  at: '2026-11-24T18:27:33Z'
  authority: generated
  via: save_document_payload
id: task-deskops-status-deja-de-ser-solo-un-aviso-deprecated-y-entrega-el-estado-rapido-del-desk
status: draft
summary: 'No despachable desde este desk: la implementa V1 del frente velocidad-hooks
  y se cierra con resolved-by (preflight rechazado el 2026-11-21).'
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-194436-unclear-status-lento-y-obsoleto-sin-estado.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops status deja de ser solo un aviso Deprecated y entrega el estado rapido del desk

## Rationale

_Explain why this task exists or the business driver behind it._

Origen: nota de MEPU del 15-11 (no llego al inbox de deskops porque --to deskops no resolvia; transcrita en velocidad-hooks-brief.md, Parte D). MEPU midio mas de 60 s en su desk y la salida es solo 'Deprecated'; aqui tarda 13 s.

## Goal

_Describe the concrete result this task must produce._

deskops status imprime el estado rapido del desk (tareas activas, inbox abierto, alertas baratas) sin correr el doctor completo. La implementa V1 del frente velocidad-hooks (supervisor 15-11), no este desk por su cuenta; esta tarea la registra y se cierra con resolved-by cuando V1 entre.

## Scope

_State what is in scope and what is out of scope._

deskops/cli/commands (status), sin subprocess de sldb; medicion con el benchmark V0 de sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- benchmark V0 del repo sldb (deskops status, caliente y frio)

## Done When

_Name the observable condition that makes the task complete._

deskops status en el desk de deskops tarda menos de 3 s en caliente y no imprime solo Deprecated; medido con V0.

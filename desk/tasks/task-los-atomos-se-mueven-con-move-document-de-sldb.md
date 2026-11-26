---
sldb:
  by: agent
  at: '2026-11-26T02:30:16Z'
  authority: generated
  via: save_document_payload
id: task-los-atomos-se-mueven-con-move-document-de-sldb
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

# Los átomos se mueven con move_document de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

merge y reorganize de átomos usan move_document y move_path de sldb en vez de rename más untrack y track, y conservan la reescritura de links (split se retira en E1).

## Scope

_State what is in scope and what is out of scope._

Entra: services/atoms.py. Sale: citas código-átomo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reemplazo. 2) Tests.

## Validation

_List the checks required before this task can close._

- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

atoms.py no renombra archivos a mano.

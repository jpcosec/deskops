---
sldb:
  by: agent
  at: '2026-11-25T19:46:05Z'
  authority: generated
  via: create_document
id: task-identity-resuelve-repos-y-stores-con-catalog-store-y-store-links-de-sldb
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

# identity resuelve repos y stores con catalog_store y store_links de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

deskops/identity.py deja su registro propio y resuelve por el catálogo de sldb (catalog_store, store_links, get_store_context).

## Scope

_State what is in scope and what is out of scope._

Entra: identity.py y message send --to, list tasks --include-repos. Sale: nada más.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reemplazo. 2) Tests de resolución por nombre.

## Validation

_List the checks required before this task can close._

- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

identity.py no mantiene registro propio.

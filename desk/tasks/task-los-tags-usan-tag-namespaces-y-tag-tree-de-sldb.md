---
sldb:
  by: agent
  at: '2026-11-25T19:46:29Z'
  authority: generated
  via: create_document
id: task-los-tags-usan-tag-namespaces-y-tag-tree-de-sldb
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

# Los tags usan tag_namespaces y tag_tree de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

atom_tags.py, domain_tree.py, tag_migration.py y tag_vocabulary.py dejan de duplicar namespaces y árbol: usan tag_namespaces de store.yaml, tag_tree y el on_write de sldb.

## Scope

_State what is in scope and what is out of scope._

Entra: los cuatro módulos. Sale: crear namespaces nuevos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reemplazos. 2) Tests.

## Validation

_List the checks required before this task can close._

- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

Los cuatro módulos suman menos de 150 líneas o desaparecen.

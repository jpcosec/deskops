---
sldb:
  by: agent
  at: '2026-11-25T19:45:53Z'
  authority: generated
  via: create_document
id: task-model-introspection-usa-describe-model-fields-y-los-placeholders-usan-template-anchors-de-sldb
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

# model_introspection usa describe_model_fields y los placeholders usan template_anchors de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

cli/model_introspection.py y doc_access.template_placeholders se reemplazan por sldb.api.describe_model_fields y sldb.api.template_anchors; lo que falte (default, pattern) se pide a sldb.

## Scope

_State what is in scope and what is out of scope._

Entra: los dos reemplazos. Sale: el CLI generado (M4).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reemplazo. 2) Nota a sldb por default y pattern si hace falta. 3) Tests.

## Validation

_List the checks required before this task can close._

- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

deskops no tiene introspección propia de modelos ni de plantillas.

---
sldb:
  by: agent
  at: '2026-11-25T19:49:17Z'
  authority: generated
  via: create_document
id: task-los-docs-de-deskops-son-materializaciones-de-atomos-con-una-pagina-por-capa
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-el-cli-de-deskops-sale-de-fastmcp-generate-cli-y-el-cli-escrito-a-mano-queda-solo-para-bootstrap-e-i
- task-un-solo-texto-por-rito-next-actions-y-nombres-de-nodo-salen-del-ritualdoc-y-se-borra-task-lifecycle
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Los docs de deskops son materializaciones de átomos, con una página por capa

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

operator-manual.md, quickstart.md, faq.md, workflow-policy-reference.md y README.md se reescriben desde átomos, cada sección cita su átomo, y hay una página que explica núcleo, operación y uso.

## Scope

_State what is in scope and what is out of scope._

Entra: esos docs y los átomos que falten. Sale: la skill.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Átomos. 2) Reescritura. 3) Página de capas.

## Validation

_List the checks required before this task can close._

- deskops atoms validate --root .
- Cada sección de esos docs cita un átomo existente

## Done When

_Name the observable condition that makes the task complete._

Ningún doc contradice el código ni cita átomos inexistentes.

---
sldb:
  by: agent
  at: '2026-11-25T19:41:53Z'
  authority: generated
  via: create_document
id: task-deskops-se-ordena-en-paquetes-por-capa-core-ops-runtime-operations-surfaces-con-contratos-de-imports
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on: []
pills: []
files: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops se ordena en paquetes por capa (core, ops, runtime, operations, surfaces) con contratos de imports

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

El código de deskops/ vive en cinco paquetes por capa y import-linter impide que core importe git, scion o superficies, y que surfaces llame a otra cosa que operations.

## Scope

_State what is in scope and what is out of scope._

Entra: mover módulos a deskops/core, ops, runtime, operations y surfaces; configuración de import-linter con los contratos; ajustar imports. Sale: cambiar comportamiento o reescribir lógica (eso es de M2 y M3).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Asignar cada módulo actual a una capa según diagnostico.md. 2) Mover por grupos con git mv y arreglar imports. 3) Contratos de import-linter en pyproject.toml. 4) Correr la suite.

## Validation

_List the checks required before this task can close._

- lint-imports
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

Todo módulo de deskops/ está en una de las cinco capas y lint-imports pasa.

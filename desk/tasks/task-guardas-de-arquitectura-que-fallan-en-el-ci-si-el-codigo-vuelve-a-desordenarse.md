---
sldb:
  by: agent
  at: '2026-11-25T19:42:54Z'
  authority: generated
  via: create_document
id: task-guardas-de-arquitectura-que-fallan-en-el-ci-si-el-codigo-vuelve-a-desordenarse
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-deskops-se-ordena-en-paquetes-por-capa-core-ops-runtime-operations-surfaces-con-contratos-de-imports
- task-ruff-configurado-un-commit-solo-de-formato-errores-arreglados-pre-commit-y-paso-de-ruff-en-el-ci
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Guardas de arquitectura que fallan en el CI si el código vuelve a desordenarse

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Tests de arquitectura que fallan si aparece un parseo de frontmatter fuera de sldb, un subprocess a sldb, include_linked=False, un test que importa funciones privadas o un módulo público sin docstring.

## Scope

_State what is in scope and what is out of scope._

Entra: tests/arquitectura con esas comprobaciones sobre el AST del paquete, y su lugar en el CI. Sale: arreglar las violaciones existentes (lo hace M3; las guardas arrancan con una lista de excepciones que M3 vacía).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Un test por regla sobre ast. 2) Lista de excepciones actual, con fecha. 3) El test falla si la lista crece.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/arquitectura

## Done When

_Name the observable condition that makes the task complete._

Las guardas corren en el CI y la lista de excepciones solo puede achicarse.

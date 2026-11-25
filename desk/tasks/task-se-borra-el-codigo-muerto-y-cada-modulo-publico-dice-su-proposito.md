---
sldb:
  by: agent
  at: '2026-11-25T22:52:30Z'
  authority: generated
  via: save_document_payload
id: task-se-borra-el-codigo-muerto-y-cada-modulo-publico-dice-su-proposito
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-ruff-configurado-un-commit-solo-de-formato-errores-arreglados-pre-commit-y-paso-de-ruff-en-el-ci
pills: []
files:
- deskops/services/closure.py
- deskops/graph/atom_trace.py
- deskops/testing/foreign_suites.py
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Se borra el código muerto y cada módulo público dice su propósito

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

ClosureService.close_auto (services/closure.py:720), graph/atom_trace.py, testing/foreign_suites.py y las funciones sin llamadores se borran antes de la mudanza por capas; cada módulo público tiene un docstring que dice qué hace y quién lo usa.

## Scope

_State what is in scope and what is out of scope._

Entra: borrado y docstrings. Sale: refactors.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Confirmar sin llamadores. 2) Borrar. 3) Docstrings.

## Validation

_List the checks required before this task can close._

- ruff check deskops
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

ruff D1 pasa en módulos públicos y no hay funciones sin llamadores en la lista del diagnóstico.

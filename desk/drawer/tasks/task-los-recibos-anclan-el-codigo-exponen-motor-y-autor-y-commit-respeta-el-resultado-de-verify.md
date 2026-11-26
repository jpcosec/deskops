---
sldb:
  by: agent
  at: '2026-11-25T19:44:22Z'
  authority: generated
  via: create_document
id: task-los-recibos-anclan-el-codigo-exponen-motor-y-autor-y-commit-respeta-el-resultado-de-verify
status: deferred
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-toda-compuerta-de-cierre-y-de-activacion-es-una-clausula-de-ruledoc-con-severidad-que-declara-el-wor
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Los recibos anclan el código, exponen motor y autor, y commit respeta el resultado de verify

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Los recibos de evidencia anclan el árbol o los archivos que evaluaron (no solo el contrato de la tarea), exponen engine y disposed_by para que una regla exija revisión en frío o autor distinto, y closeout commit no ignora un verify rechazado.

## Scope

_State what is in scope and what is out of scope._

Entra: ReviewDoc, review record y dispose, la evaluación en commit. Sale: decidir qué exige cada desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ancla del recibo. 2) Campos engine y disposed_by legibles por reglas. 3) Commit respeta verify. 4) Quitar xfail de N2 y N9.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core

## Done When

_Name the observable condition that makes the task complete._

Los escenarios de N2 y N9 pasan con el gate exigido.

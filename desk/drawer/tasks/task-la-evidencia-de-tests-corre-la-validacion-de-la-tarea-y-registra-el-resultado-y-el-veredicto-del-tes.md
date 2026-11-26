---
sldb:
  by: agent
  at: '2026-11-25T20:10:57Z'
  authority: generated
  via: save_document_payload
id: task-la-evidencia-de-tests-corre-la-validacion-de-la-tarea-y-registra-el-resultado-y-el-veredicto-del-tes
status: deferred
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-toda-compuerta-de-cierre-y-de-activacion-es-una-clausula-de-ruledoc-con-severidad-que-declara-el-wor
- task-antes-del-ci-se-corren-solo-los-tests-que-corresponden-a-lo-que-muto
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La evidencia de tests corre la validación de la tarea y registra el resultado, y el veredicto del tester es un recibo

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Un productor de evidencia corre los comandos de validación de la tarea y registra el código de salida en un recibo; el veredicto PASA o FALLA del tester también queda como recibo; el workflow decide si los exige.

## Scope

_State what is in scope and what is out of scope._

Entra: el productor, el recibo del tester y la cláusula correspondiente. Sale: reemplazar la validación de la tarea por una genérica.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Productor en ops (corre comandos). 2) Recibo. 3) Cláusula. 4) Quitar xfail de N3.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core tests/ops

## Done When

_Name the observable condition that makes the task complete._

El escenario de N3 pasa: con el gate exigido, una tarea con tests rojos no cierra.

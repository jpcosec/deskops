---
sldb:
  by: agent
  at: '2026-11-25T22:54:25Z'
  authority: generated
  via: save_document_payload
id: task-suite-de-tests-nueva-por-capa-escenarios-del-nucleo-operacion-con-repos-git-temporales-y-contrato-de
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
files:
- tests/README.md
- tests/conftest.py
- tests/core/
- tests/ops/
- tests/surfaces/
- tests/fixtures/golden/help/
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Suite de tests nueva por capa: escenarios del núcleo, operación con repos git temporales y contrato de superficies

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Existe la estructura tests/core, tests/ops y tests/surfaces con sus fixtures y convenciones: el núcleo se prueba con escenarios contra las reglas sin git ni scion, operación contra repos git temporales, superficies verificando que CLI y MCP llegan a la misma operación.

## Scope

_State what is in scope and what is out of scope._

Entra: estructura, fixtures base, convención escrita y retiro de los 153 goldens de --help. Sale: escribir todos los tests (cada tarea de E2 y E3 trae los suyos).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Fixtures: desk mínimo en tmp, repo git temporal, servidor MCP en proceso. 2) Convención en tests/README.md. 3) Borrar tests/fixtures/golden/help y su test.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core tests/ops tests/surfaces

## Done When

_Name the observable condition that makes the task complete._

La estructura y las fixtures existen, hay un test de ejemplo por capa y no quedan goldens de --help.

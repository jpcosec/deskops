---
sldb:
  by: agent
  at: '2026-11-25T19:45:05Z'
  authority: generated
  via: create_document
id: task-verificar-y-arreglar-dependencias-inexistentes-n7-y-la-autorreferencia-que-exime-del-gate-de-vinculo
status: deferred
summary: ''
tags: []
current_node: ''
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-escenarios-del-workflow-escritos-para-fallar-hoy-cerrar-desde-ejecucion-con-tests-rojos-fuera-del-bo
pills: []
files: []
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Verificar y arreglar dependencias inexistentes (N7) y la autorreferencia que exime del gate de vínculos (N11)

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Saber con un escenario si una dependencia inexistente satisface all(depends_on: status = closed) y si una referencia a la propia tarea exime del gate de vínculos, y arreglar lo que se confirme.

## Scope

_State what is in scope and what is out of scope._

Entra: dos escenarios y sus arreglos. Sale: otras reglas.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Escenario N7. 2) Escenario N11. 3) Arreglo de lo confirmado.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core

## Done When

_Name the observable condition that makes the task complete._

Los dos escenarios pasan.

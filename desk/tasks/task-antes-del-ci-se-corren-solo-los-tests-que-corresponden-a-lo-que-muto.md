---
sldb:
  by: agent
  at: '2026-11-25T20:10:31Z'
  authority: generated
  via: create_document
id: task-antes-del-ci-se-corren-solo-los-tests-que-corresponden-a-lo-que-muto
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
- desk/tasks/task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Antes del CI se corren solo los tests que corresponden a lo que mutó

## Rationale

_Explain why this task exists or the business driver behind it._

JP, 25-11: falta un paso previo al CI que tome los tests que corresponden a lo que mutó; conversa con las fases paralelas: cada tarea de una fase corre los tests de lo que tocó y la integración de la fase corre la suite completa en el CI.

## Goal

_Describe the concrete result this task must produce._

Una operación que, a partir de lo que cambió (git diff contra la base y git status), elige los tests que lo cubren y los corre, y deja el resultado como recibo de evidencia de la tarea; el CI y la integración de la fase corren la suite completa.

## Scope

_State what is in scope and what is out of scope._

Entra: el mapa de lo que mutó a sus tests (por capa y módulo de la estructura nueva, por los files y la validación de la tarea, y por las aristas del grafo del proyecto entre código y tests), la operación que los corre, el recibo de evidencia y su uso en hooks locales y en el cierre de la tarea. Sale: la suite completa (es del CI) y decidir si un desk la exige (es del workflow).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Lo que mutó: git diff --name-only contra la base de la tarea más git status. 2) Mapa a tests: convención de la suite nueva (tests/core, tests/ops, tests/surfaces por módulo), files y validación de la tarea, grafo del proyecto. 3) Operación que corre y registra el recibo. 4) Engancharla al cierre y al hook local. 5) Escenario: un cambio en un módulo corre solo sus tests.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/ops
- un cambio en un solo módulo corre solo los tests de ese módulo y deja un recibo

## Done When

_Name the observable condition that makes the task complete._

La operación elige y corre los tests de lo que mutó y deja el recibo; el CI sigue corriendo la suite completa.

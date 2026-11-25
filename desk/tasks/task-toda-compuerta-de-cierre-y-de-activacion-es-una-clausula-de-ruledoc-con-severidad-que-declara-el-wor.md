---
sldb:
  by: agent
  at: '2026-11-25T19:44:00Z'
  authority: generated
  via: create_document
id: task-toda-compuerta-de-cierre-y-de-activacion-es-una-clausula-de-ruledoc-con-severidad-que-declara-el-wor
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-escenarios-del-workflow-escritos-para-fallar-hoy-cerrar-desde-ejecucion-con-tests-rojos-fuera-del-bo
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Toda compuerta de cierre y de activación es una cláusula de RuleDoc con severidad que declara el workflow

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Cada compuerta (incluidas _closeout_link_gate, _changed_file_link_evidence, _skill_guard_test_evidence y _generated_artifact_source_finding) es una cláusula de una RuleDoc y el workflow del desk decide si es error, alerta o apagada; el sistema permite exigirla o no.

## Scope

_State what is in scope and what is out of scope._

Entra: mover las compuertas de Python a reglas, la severidad configurable por desk, borrar data/rules/closeout-evidence.yaml. Sale: decidir qué exige cada desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario de compuertas en closure.py y closeout_gates.py. 2) Cada una a cláusula. 3) Severidad por desk. 4) Escenarios con el gate exigido y apagado.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core
- sldb rules explain muestra cada compuerta

## Done When

_Name the observable condition that makes the task complete._

Ninguna compuerta vive solo en Python y cada una se puede exigir o apagar por desk.

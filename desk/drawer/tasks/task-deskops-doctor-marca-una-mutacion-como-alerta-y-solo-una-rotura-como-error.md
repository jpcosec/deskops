---
sldb:
  by: agent
  at: '2026-11-25T19:42:30Z'
  authority: generated
  via: create_document
id: task-deskops-doctor-marca-una-mutacion-como-alerta-y-solo-una-rotura-como-error
status: deferred
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops doctor marca una mutación como alerta y solo una rotura como error

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Un clon limpio de main pasa deskops doctor sin errores; una edición, un cambio de extractor o un cambio de datos salen como alertas con el comando que las registra.

## Scope

_State what is in scope and what is out of scope._

Entra: averiguar si las mutaciones llegan como error desde sldb o desde deskops/doctor_findings.py:86-90 y arreglarlo donde corresponde (si es sldb, nota a su inbox). Sale: rediseñar doctor (eso es del agente de coherencia).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reproducir: doctor en un clon limpio da rc=1 y 220 errores (195 cambio de extractor, 25 cambio de datos en RunDoc). 2) Ver el código y la severidad de sldb. 3) Arreglar. 4) Test con una mutación.

## Validation

_List the checks required before this task can close._

- deskops doctor --root . en un clon limpio de main sale con 0
- un test edita una tarea y doctor la reporta como alerta

## Done When

_Name the observable condition that makes the task complete._

Doctor en un clon limpio sale con 0 y una mutación es alerta.

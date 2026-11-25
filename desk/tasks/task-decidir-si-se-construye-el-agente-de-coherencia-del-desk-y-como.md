---
sldb:
  by: agent
  at: '2026-11-25T19:47:35Z'
  authority: generated
  via: create_document
id: task-decidir-si-se-construye-el-agente-de-coherencia-del-desk-y-como
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
- desk/drawer/plans/deskops-plugin-de-sldb/propuesta-agente-coherencia.md
depends_on:
- task-deskops-doctor-marca-una-mutacion-como-alerta-y-solo-una-rotura-como-error
pills: []
files: []
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Decidir si se construye el agente de coherencia del desk y cómo

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

JP decide sobre la propuesta desk/drawer/plans/deskops-plugin-de-sldb/propuesta-agente-coherencia.md: si vale la parte con modelo, si es un comando nuevo o doctor corregido más hooks, y qué disparadores vienen activados.

## Scope

_State what is in scope and what is out of scope._

Entra: la decisión y, si se aprueba, las tareas que salgan. Sale: implementarlo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) JP revisa la propuesta. 2) Átomo con la decisión. 3) Tareas.

## Validation

_List the checks required before this task can close._

- La decisión queda en un átomo

## Done When

_Name the observable condition that makes the task complete._

Hay un átomo con la decisión de JP.

---
sldb:
  by: agent
  at: '2026-11-25T19:44:44Z'
  authority: generated
  via: create_document
id: task-un-solo-texto-por-rito-next-actions-y-nombres-de-nodo-salen-del-ritualdoc-y-se-borra-task-lifecycle
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

# Un solo texto por rito: next_actions y nombres de nodo salen del RitualDoc y se borra task_lifecycle.yaml

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

deskops next y los prompts dicen lo que dice el rito; los nombres de nodo y los estados que escriben las aristas coinciden con los ritos; deskops/spec/workflows/task_lifecycle.yaml no existe.

## Scope

_State what is in scope and what is out of scope._

Entra: RitualDoc, aristas, migración de desks existentes. Sale: cambiar el contenido de los ritos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Campos en RitualDoc. 2) next lee de ahí. 3) Renombres con migración. 4) Borrar el YAML.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core
- deskops next <tarea> imprime el texto del rito

## Done When

_Name the observable condition that makes the task complete._

No hay dos textos para un rito y los nombres coinciden.

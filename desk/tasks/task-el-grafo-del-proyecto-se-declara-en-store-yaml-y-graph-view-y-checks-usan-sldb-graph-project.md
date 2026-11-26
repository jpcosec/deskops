---
sldb:
  by: agent
  at: '2026-11-25T19:46:51Z'
  authority: generated
  via: create_document
id: task-el-grafo-del-proyecto-se-declara-en-store-yaml-y-graph-view-y-checks-usan-sldb-graph-project
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
files: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El grafo del proyecto se declara en store.yaml y graph view y checks usan sldb graph project

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

SURFACES, FILE_RULES y EXCLUSIONS de graph/desk_graph.py pasan a project_graph: en store.yaml; graph view y graph checks usan sldb graph project; atom_trace.py se borra.

## Scope

_State what is in scope and what is out of scope._

Entra: graph/. Sale: self_reflection (lo absorbe el agente de coherencia).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) project_graph. 2) Reemplazos. 3) Borrar atom_trace.

## Validation

_List the checks required before this task can close._

- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

graph/desk_graph.py no tiene configuración en Python.

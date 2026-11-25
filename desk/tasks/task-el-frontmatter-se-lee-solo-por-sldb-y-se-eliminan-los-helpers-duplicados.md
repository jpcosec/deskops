---
sldb:
  by: agent
  at: '2026-11-25T19:47:13Z'
  authority: generated
  via: create_document
id: task-el-frontmatter-se-lee-solo-por-sldb-y-se-eliminan-los-helpers-duplicados
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-deskops-se-ordena-en-paquetes-por-capa-core-ops-runtime-operations-surfaces-con-contratos-de-imports
- task-guardas-de-arquitectura-que-fallan-en-el-ci-si-el-codigo-vuelve-a-desordenarse
pills: []
files: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El frontmatter se lee solo por sldb y se eliminan los helpers duplicados

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Los siete parseos a mano de frontmatter usan la API de sldb, y _git, _yaml_scalar, _coerce_list, _now y _under quedan una sola vez.

## Scope

_State what is in scope and what is out of scope._

Entra: doctor_findings, integrate, lifecycle, doc_access, absolute_paths, models/task_lifecycle, services/issues. Sale: nada más.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reemplazos. 2) Helpers comunes en ops. 3) Vaciar su excepción en las guardas.

## Validation

_List the checks required before this task can close._

- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

La guarda de frontmatter no tiene excepciones.

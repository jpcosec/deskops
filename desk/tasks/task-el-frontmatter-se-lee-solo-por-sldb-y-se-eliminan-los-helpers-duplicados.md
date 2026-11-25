---
sldb:
  by: agent
  at: '2026-11-25T22:54:17Z'
  authority: generated
  via: save_document_payload
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
pills: []
files:
- deskops/doctor_findings.py
- deskops/integrate.py
- deskops/lifecycle.py
- deskops/doc_access.py
- deskops/absolute_paths.py
- deskops/models/task_lifecycle.py
- deskops/services/issues.py
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

1) Reemplazar los siete parseos por la API de sldb. 2) Los helpers comunes, una vez en core. 3) grep de yaml.safe_load sobre frontmatter fuera de sldb no da resultados.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/acceptance
- ningún módulo de deskops/ parte un documento en '---' para leer su frontmatter

## Done When

_Name the observable condition that makes the task complete._

El frontmatter se lee solo por sldb y cada helper existe una vez.

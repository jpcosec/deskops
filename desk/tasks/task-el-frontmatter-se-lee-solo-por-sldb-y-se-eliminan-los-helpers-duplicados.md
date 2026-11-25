---
sldb:
  by: agent
  at: '2026-11-25T23:07:11Z'
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
- deskops/ops/doctor.py
- deskops/runtime/integrate.py
- deskops/core/lifecycle.py
- deskops/core/doc_access.py
- deskops/ops/absolute_paths.py
- deskops/core/models/task_lifecycle.py
- deskops/core/issues.py
- deskops/core/util.py
- deskops/runtime/git.py
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

Los siete parseos a mano de frontmatter leen con sldb.api.extract_document_payload (o load_runtime_documents cuando leen el store entero), y _git queda una sola vez en runtime/git.py y _yaml_scalar, _coerce_list, _now y _under una sola vez en core/util.py.

## Scope

_State what is in scope and what is out of scope._

Entra: los siete módulos en sus rutas después de la mudanza: ops/doctor.py, runtime/integrate.py, core/lifecycle.py, core/doc_access.py, ops/absolute_paths.py, core/models/task_lifecycle.py y core/issues.py. Sale: nada más.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reemplazar los siete parseos por la API de sldb. 2) Los helpers comunes, una vez en core. 3) grep de yaml.safe_load sobre frontmatter fuera de sldb no da resultados.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/acceptance
- grep -rnE "split\(['\"]---" deskops no da resultados
- cada uno de _git, _yaml_scalar, _coerce_list, _now y _under tiene una sola definición (grep -rn 'def _git\b' deskops y similares)

## Done When

_Name the observable condition that makes the task complete._

El frontmatter se lee solo por sldb y cada helper existe una vez.

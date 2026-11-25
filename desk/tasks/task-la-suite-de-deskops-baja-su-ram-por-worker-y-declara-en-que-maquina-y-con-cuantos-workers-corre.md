---
sldb:
  by: agent
  at: '2026-11-25T16:52:53Z'
  authority: generated
  via: create_document
id: task-la-suite-de-deskops-baja-su-ram-por-worker-y-declara-en-que-maquina-y-con-cuantos-workers-corre
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261125-014936-suggestion-suite-de-deskops-6-gb-de-ram-con-n-4-el-25-11-01-00-en-johanes-16.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La suite de deskops baja su RAM por worker y declara en qué máquina y con cuántos workers corre

## Rationale

_Explain why this task exists or the business driver behind it._

El 25-11 en johanes la suite con -n 4 llegó a ~6 GB de RSS (2,4+1,8+1,5+0,4 GB), duró ~33 min y llenó el swap (nota 20261125-014936).

## Goal

_Describe the concrete result this task must produce._

Medir qué tests o fixtures hacen crecer el RSS de cada worker de xdist, bajar los que más pesan y dejar escrito en qué máquina y con cuántos workers corre la suite completa.

## Scope

_State what is in scope and what is out of scope._

Entra: medición de RSS por test (plugin o pytest-memray), arreglo de los fixtures/stores/cachés que no se liberan, y la regla de máquina/workers (queue_min_available_gb / CI_WORKERS). Sale: reescribir tests que no aparezcan en la medición.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Medir RSS por test con un plugin de conftest o pytest-memray. 2) Atacar los 5 tests o fixtures más pesados. 3) Documentar máquina y workers en el faq del desk o AGENTS.md.

## Validation

_List the checks required before this task can close._

- python -m pytest -q -n 4 tests con RSS total bajo 3 GB, medido y anotado en el commit

## Done When

_Name the observable condition that makes the task complete._

La suite completa con -n 4 no pasa de 3 GB de RSS y la regla de máquina/workers está escrita.

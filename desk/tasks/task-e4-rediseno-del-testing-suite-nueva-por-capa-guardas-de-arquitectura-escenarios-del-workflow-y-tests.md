---
sldb:
  by: agent
  at: '2026-11-25T20:28:52Z'
  authority: generated
  via: create_document
id: task-e4-rediseno-del-testing-suite-nueva-por-capa-guardas-de-arquitectura-escenarios-del-workflow-y-tests
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-suite-de-tests-nueva-por-capa-escenarios-del-nucleo-operacion-con-repos-git-temporales-y-contrato-de
- task-guardas-de-arquitectura-que-fallan-en-el-ci-si-el-codigo-vuelve-a-desordenarse
- task-escenarios-del-workflow-escritos-para-fallar-hoy-cerrar-desde-ejecucion-con-tests-rojos-fuera-del-bo
- task-antes-del-ci-se-corren-solo-los-tests-que-corresponden-a-lo-que-muto
- task-la-suite-vieja-se-retira-a-medida-que-cada-modulo-se-muda-a-su-capa
- task-la-suite-de-deskops-baja-su-ram-por-worker-y-declara-en-que-maquina-y-con-cuantos-workers-corre
pills: []
files: []
task_type: task.aggregate
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# E4 Rediseño del testing: suite nueva por capa, guardas de arquitectura, escenarios del workflow y tests de lo que mutó

## Rationale

_Explain why this task exists or the business driver behind it._

Reorganización del 25-11 por etapas (JP): refactor, pluginización, responsabilidades a sldb, rediseño del testing y recién después los pedidos individuales (en el drawer). Base: desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md.

## Goal

_Describe the concrete result this task must produce._

Todas las subtareas de E4 cerradas.

## Scope

_State what is in scope and what is out of scope._

Entra: las subtareas de depends_on. Sale: los pedidos individuales del drawer y las otras etapas.

## Implementation Path

_Outline the expected implementation route or affected surface._

Se cierra cuando cierran sus subtareas.

## Validation

_List the checks required before this task can close._

- Todas las tareas de depends_on están cerradas

## Done When

_Name the observable condition that makes the task complete._

Todas las subtareas cerradas.

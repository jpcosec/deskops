---
sldb:
  by: agent
  at: '2026-11-25T19:50:14Z'
  authority: generated
  via: create_document
id: task-m1-senales-y-guardas-ci-en-verde-y-rapido-doctor-confiable-lint-guardas-de-arquitectura-y-suite-nuev
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-el-ci-de-deskops-vuelve-a-verde-y-baja-de-1h30-a-menos-de-20-minutos
- task-la-suite-de-deskops-baja-su-ram-por-worker-y-declara-en-que-maquina-y-con-cuantos-workers-corre
- task-deskops-doctor-marca-una-mutacion-como-alerta-y-solo-una-rotura-como-error
- task-ruff-configurado-un-commit-solo-de-formato-errores-arreglados-pre-commit-y-paso-de-ruff-en-el-ci
- task-guardas-de-arquitectura-que-fallan-en-el-ci-si-el-codigo-vuelve-a-desordenarse
- task-suite-de-tests-nueva-por-capa-escenarios-del-nucleo-operacion-con-repos-git-temporales-y-contrato-de
- task-la-suite-vieja-se-retira-a-medida-que-cada-modulo-se-muda-a-su-capa
pills: []
files: []
task_type: task.aggregate
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# M1 Señales y guardas: CI en verde y rápido, doctor confiable, lint, guardas de arquitectura y suite nueva

## Rationale

_Explain why this task exists or the business driver behind it._

Macro del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md); agrupa sus subtareas por capa.

## Goal

_Describe the concrete result this task must produce._

Todas las subtareas de M1 cerradas.

## Scope

_State what is in scope and what is out of scope._

Entra: las subtareas listadas en depends_on. Sale: trabajo de otras macros.

## Implementation Path

_Outline the expected implementation route or affected surface._

Se cierra cuando cierran sus subtareas.

## Validation

_List the checks required before this task can close._

- Todas las tareas de depends_on están cerradas

## Done When

_Name the observable condition that makes the task complete._

Todas las subtareas cerradas.

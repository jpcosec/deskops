---
sldb:
  by: agent
  at: '2026-11-25T22:57:10Z'
  authority: generated
  via: save_document_payload
id: task-e1-refactor-deskops-ordenado-por-capas-con-lint-sin-codigo-muerto-ni-helpers-duplicados-y-sin-legacy
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-el-ci-de-deskops-vuelve-a-verde-y-baja-de-1h30-a-menos-de-20-minutos
- task-ruff-configurado-un-commit-solo-de-formato-errores-arreglados-pre-commit-y-paso-de-ruff-en-el-ci
- task-se-borra-el-codigo-muerto-y-cada-modulo-publico-dice-su-proposito
- task-se-retira-deskops-atoms-split
- task-cada-capacidad-del-cli-de-deskops-tiene-un-test-de-aceptacion-de-caja-negra-antes-de-mover-codigo
- task-deskops-se-ordena-en-paquetes-por-capa-core-ops-runtime-operations-surfaces-con-contratos-de-imports
- task-el-frontmatter-se-lee-solo-por-sldb-y-se-eliminan-los-helpers-duplicados
- task-suite-de-tests-nueva-por-capa-escenarios-del-nucleo-operacion-con-repos-git-temporales-y-contrato-de
- task-escenarios-del-workflow-escritos-para-fallar-hoy-cerrar-desde-ejecucion-con-tests-rojos-fuera-del-bo
- task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply
- task-borrar-la-migracion-de-task-type-viejo-legacy-task-type-keys-y-migrate-task-types-y-sus-tests
pills: []
files: []
task_type: task.aggregate
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# E1 Refactor: CI en verde, lint, red de tests de aceptación y deskops ordenado por capas, sin código muerto ni legacy

## Rationale

_Explain why this task exists or the business driver behind it._

Reorganización del 25-11 por etapas (JP): refactor, pluginización, responsabilidades a sldb, rediseño del testing y recién después los pedidos individuales (en el drawer). Base: desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md.

## Goal

_Describe the concrete result this task must produce._

Todas las subtareas de E1 cerradas.

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

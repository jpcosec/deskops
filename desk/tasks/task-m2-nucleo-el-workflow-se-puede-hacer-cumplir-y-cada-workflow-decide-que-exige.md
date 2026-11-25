---
sldb:
  by: agent
  at: '2026-11-25T19:57:35Z'
  authority: generated
  via: save_document_payload
id: task-m2-nucleo-el-workflow-se-puede-hacer-cumplir-y-cada-workflow-decide-que-exige
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-escenarios-del-workflow-escritos-para-fallar-hoy-cerrar-desde-ejecucion-con-tests-rojos-fuera-del-bo
- task-el-cierre-toma-la-arista-task-completes-desde-el-nodo-real-de-la-tarea
- task-supersede-resolved-by-y-retire-son-aristas-declaradas-del-ciclo-de-vida
- task-toda-compuerta-de-cierre-y-de-activacion-es-una-clausula-de-ruledoc-con-severidad-que-declara-el-wor
- task-la-evidencia-de-tests-corre-la-validacion-de-la-tarea-y-registra-el-resultado-y-el-veredicto-del-tes
- task-los-recibos-anclan-el-codigo-exponen-motor-y-autor-y-commit-respeta-el-resultado-de-verify
- task-la-activacion-puede-exigirse-antes-del-despacho-y-el-ruteo-por-board-es-una-regla
- task-un-solo-texto-por-rito-next-actions-y-nombres-de-nodo-salen-del-ritualdoc-y-se-borra-task-lifecycle
- task-la-coherencia-de-status-current-node-e-history-es-una-regla-on-write-que-lee-el-grafo-del-desk
- task-verificar-y-arreglar-dependencias-inexistentes-n7-y-la-autorreferencia-que-exime-del-gate-de-vinculo
- task-el-board-es-una-vista-calculada-sobre-las-tareas-y-deja-de-ser-un-documento-que-reescriben-todas-las
- task-integrate-encuentra-el-cierre-por-el-trailer-task-id-y-distingue-closeout-mode
- task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase
- task-integrate-por-lote-una-sola-integracion-por-desk-con-todo-lo-cerrado-pendiente-un-tip-una-suite-un-g
- task-governance-closeout-no-borra-una-tarea-de-la-que-otras-heredan-inherits-from-o-las-herederas-siguen
- task-el-gate-de-cierre-acepta-el-commit-de-la-tarea-como-vinculo-de-cada-archivo-de-files-en-vez-de-exigi
- task-como-se-hace-respetar-la-maquina-de-estados-del-workflow
pills: []
files: []
task_type: task.aggregate
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# M2 Núcleo: el workflow se puede hacer cumplir y cada workflow decide qué exige

## Rationale

_Explain why this task exists or the business driver behind it._

Macro del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md); agrupa sus subtareas por capa.

## Goal

_Describe the concrete result this task must produce._

Todas las subtareas de M2 cerradas.

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

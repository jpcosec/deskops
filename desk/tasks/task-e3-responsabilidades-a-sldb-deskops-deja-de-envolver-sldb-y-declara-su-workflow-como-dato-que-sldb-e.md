---
sldb:
  by: agent
  at: '2026-11-25T22:57:21Z'
  authority: generated
  via: save_document_payload
id: task-e3-responsabilidades-a-sldb-deskops-deja-de-envolver-sldb-y-declara-su-workflow-como-dato-que-sldb-e
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-deskops-lee-las-aristas-del-ciclo-de-vida-desde-el-store-enlazado-y-deja-de-copiarlas-donde-sldb-ya
- task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph
- task-identity-resuelve-repos-y-stores-con-catalog-store-y-store-links-de-sldb
- task-bootstrap-workspace-y-desk-update-usan-apply-declaration-y-la-api-de-stores-de-sldb-sin-subprocess
- task-los-tags-usan-tag-namespaces-y-tag-tree-de-sldb
- task-message-usa-sldb-inbox-y-transacciones
- task-el-grafo-del-proyecto-se-declara-en-store-yaml-y-graph-view-y-checks-usan-sldb-graph-project
- task-los-atomos-se-mueven-con-move-document-de-sldb
- task-inbox-y-drawer-quedan-trackeados-en-el-store-del-desk-y-las-vistas-los-leen-del-store-h10-de-cc34
- task-toda-compuerta-de-cierre-y-de-activacion-es-una-clausula-de-ruledoc-con-severidad-que-declara-el-wor
- task-el-cierre-toma-la-arista-task-completes-desde-el-nodo-real-de-la-tarea
- task-supersede-resolved-by-y-retire-son-aristas-declaradas-del-ciclo-de-vida
- task-la-coherencia-de-status-current-node-e-history-es-una-regla-on-write-que-lee-el-grafo-del-desk
- task-un-solo-texto-por-rito-next-actions-y-nombres-de-nodo-salen-del-ritualdoc-y-se-borra-task-lifecycle
- task-el-board-es-una-vista-calculada-sobre-las-tareas-y-deja-de-ser-un-documento-que-reescriben-todas-las
- task-sldb-aplica-las-ruledoc-de-un-store-enlazado-parte-de-reglas-del-pedido-c1
- task-sldb-ofrece-la-primitiva-tomar-transicion-en-su-cli-y-su-api-pedido-c2
- task-el-lenguaje-de-reglas-de-sldb-lee-el-ultimo-elemento-de-una-lista-pedido-c3
- task-sldb-hace-respetar-una-maquina-de-estados-el-campo-de-estado-solo-cambia-tomando-una-arista
- task-se-borra-la-copia-de-reglas-de-ciclo-de-vida-en-cada-desk-las-aplica-sldb-desde-el-paquete-enlazado
- task-advance-y-el-cierre-toman-la-transicion-con-la-primitiva-de-sldb-y-se-borra-lifecycle-advance
- task-el-estado-de-una-tarea-solo-cambia-tomando-una-arista-se-borran-los-if-de-estado-de-closure-py
pills: []
files: []
task_type: task.aggregate
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# E3 Responsabilidades a sldb: deskops deja de envolver sldb y declara su workflow como dato que sldb evalúa

## Rationale

_Explain why this task exists or the business driver behind it._

Reorganización del 25-11 por etapas (JP): refactor, pluginización, responsabilidades a sldb, rediseño del testing y recién después los pedidos individuales (en el drawer). Base: desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md.

## Goal

_Describe the concrete result this task must produce._

Todas las subtareas de E3 cerradas.

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

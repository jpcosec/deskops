---
sldb:
  by: agent
  at: '2026-11-25T20:19:09Z'
  authority: generated
  via: save_document_payload
id: task-m3-mantenimiento-deskops-usa-sldb-en-vez-de-envolverlo-y-cada-modulo-se-muda-a-su-capa
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
- task-model-introspection-usa-describe-model-fields-y-los-placeholders-usan-template-anchors-de-sldb
- task-identity-resuelve-repos-y-stores-con-catalog-store-y-store-links-de-sldb
- task-bootstrap-workspace-y-desk-update-usan-apply-declaration-y-la-api-de-stores-de-sldb-sin-subprocess
- task-los-tags-usan-tag-namespaces-y-tag-tree-de-sldb
- task-desk-update-en-seco-lista-los-tags-de-tareas-con-namespace-sin-declarar-y-apply-no-mete-taskdoc-en-t
- task-message-usa-sldb-inbox-y-transacciones
- task-el-grafo-del-proyecto-se-declara-en-store-yaml-y-graph-view-y-checks-usan-sldb-graph-project
- task-los-atomos-se-mueven-con-move-document-de-sldb
- task-inbox-y-drawer-quedan-trackeados-en-el-store-del-desk-y-las-vistas-los-leen-del-store-h10-de-cc34
- task-el-frontmatter-se-lee-solo-por-sldb-y-se-eliminan-los-helpers-duplicados
- task-se-borra-el-codigo-muerto-y-cada-modulo-publico-dice-su-proposito
- task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply
- task-borrar-la-migracion-de-task-type-viejo-legacy-task-type-keys-y-migrate-task-types-y-sus-tests
- task-huecos-de-atomos-de-la-auditoria-de-chatbot-infra-renombrar-id-retire-de-atomos-validate-all-y-edita
- task-governance-registro-en-el-desk-de-los-artefactos-generados-por-claude-y-por-el-desk
- task-el-inbox-admite-avisos-kind-alert-ademas-de-unclear-y-suggestion-d5-de-governance
- task-se-retira-deskops-atoms-split
pills: []
files: []
task_type: task.aggregate
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# M3 Mantenimiento: deskops usa sldb en vez de envolverlo y cada módulo se muda a su capa

## Rationale

_Explain why this task exists or the business driver behind it._

Macro del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md); agrupa sus subtareas por capa.

## Goal

_Describe the concrete result this task must produce._

Todas las subtareas de M3 cerradas.

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

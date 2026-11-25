---
sldb:
  by: agent
  at: '2026-11-25T20:09:45Z'
  authority: generated
  via: save_document_payload
id: task-m4-uso-prompt-como-vista-despacho-flexible-cli-generado-instalacion-en-clientes-y-ui
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-el-prompt-de-una-tarea-es-una-vista-del-nucleo-un-solo-texto-sin-contradicciones
- task-despacho-flexible-sobre-runtimeprofiledoc-claude-headless-o-subagente-de-sesion-pi-y-scion-con-el-mi
- task-el-runner-de-revisiones-lanza-al-revisor-con-stdin-devnull-cuando-la-entrada-va-por-archivo
- task-el-cli-de-deskops-sale-de-fastmcp-generate-cli-y-el-cli-escrito-a-mano-queda-solo-para-bootstrap-e-i
- task-deskops-se-instala-en-claude-code-y-otros-clientes-con-fastmcp-install
- task-governance-interfaz-mcp-de-deskops-compatible-con-claude-code-delgada-sobre-las-operaciones-del-cli
- task-los-botones-de-graph-ui-frontends-desk-llaman-a-las-operaciones-de-deskops
- task-evaluar-el-code-mode-de-fastmcp-para-que-los-agentes-encadenen-operaciones-de-deskops-en-codigo
- task-migrar-los-repos-que-consumen-deskops-a-la-version-refactorizada
- task-el-reap-del-intento-n-de-un-ejecutor-encola-el-tester-aunque-la-tarea-ya-este-en-ritual-testing
- task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar
- task-las-rutas-y-credenciales-de-maquina-de-dispatch-e-integrate-salen-de-desk-config-json-versionado-a-d
- task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa
- task-deskops-list-tasks-y-deskops-next-filtran-por-maquina-con-host-tag-host-valor-y-la-salida-de-list-ta
- task-governance-concilio-y-pruebas-sin-contexto-como-mecanismos-que-deskops-levanta-en-scion
pills: []
files: []
task_type: task.aggregate
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# M4 Uso: prompt como vista, despacho flexible, CLI generado, instalación en clientes y UI

## Rationale

_Explain why this task exists or the business driver behind it._

Macro del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md); agrupa sus subtareas por capa.

## Goal

_Describe the concrete result this task must produce._

Todas las subtareas de M4 cerradas.

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

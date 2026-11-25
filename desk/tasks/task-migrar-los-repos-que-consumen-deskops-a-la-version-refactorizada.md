---
sldb:
  by: agent
  at: '2026-11-25T22:51:31Z'
  authority: generated
  via: save_document_payload
id: task-migrar-los-repos-que-consumen-deskops-a-la-version-refactorizada
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-e1-refactor-deskops-ordenado-por-capas-con-lint-sin-codigo-muerto-ni-helpers-duplicados-y-sin-legacy
- task-e2-pluginizacion-las-operaciones-como-herramientas-mcp-sobre-sldb-cli-generado-y-docs-que-salen-de-a
- task-e3-responsabilidades-a-sldb-deskops-deja-de-envolver-sldb-y-declara-su-workflow-como-dato-que-sldb-e
- task-e4-rediseno-del-testing-suite-nueva-por-capa-guardas-de-arquitectura-escenarios-del-workflow-y-tests
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Migrar los repos que consumen deskops a la versión refactorizada

## Rationale

_Explain why this task exists or the business driver behind it._

El refactor del 25-11 (etapas E1 a E4) cambia el CLI, las aristas y la forma de leer el store; los repos que usan deskops (MEPU, TraderBot, sldb, graph_ui y los demás del registro) hay que migrarlos.

## Goal

_Describe the concrete result this task must produce._

Cada repo del registro de deskops usa la versión refactorizada y pasa deskops doctor.

## Scope

_State what is in scope and what is out of scope._

Entra: la versión refactorizada sale como 0.3.0 (el tag v0.2.0 existente no se toca); fijar esa versión en cada repo consumidor; la lista de repos desde desk/registry; un desk update por repo y lo que cada uno necesite; avisar a la sesión de cada repo qué cambió. Sale: cambios de código propios de cada repo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Lista de repos consumidores. 2) Por repo, desk update y doctor. 3) Avisar a la sesión de cada repo qué cambió.

## Validation

_List the checks required before this task can close._

- deskops doctor --root <repo> sale con 0 en cada repo del registro

## Done When

_Name the observable condition that makes the task complete._

Todos los repos del registro migrados y con doctor en verde.

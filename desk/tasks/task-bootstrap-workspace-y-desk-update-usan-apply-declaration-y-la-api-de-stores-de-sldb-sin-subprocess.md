---
sldb:
  by: agent
  at: '2026-11-26T02:57:01Z'
  authority: generated
  via: save_document_payload
id: task-bootstrap-workspace-y-desk-update-usan-apply-declaration-y-la-api-de-stores-de-sldb-sin-subprocess
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
files: []
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# bootstrap, workspace y desk update usan apply_declaration y la API de stores de sldb, sin subprocess

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

La instalación y actualización del desk se declaran con sldb.api.StoreDeclaration (links, models con origin) y se aplican con sldb.api.build_store (apply_declaration es un módulo interno de sldb, no una API pública); desk update no llama a sldb por subprocess; workspace.py se parte por responsabilidad.

## Scope

_State what is in scope and what is out of scope._

Entra: bootstrap.py, workspace.py, cli/commands/desk.py. Sale: las migraciones legacy (otra tarea).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) StoreDeclaration del desk. 2) Aplicarla con build_store y scaffold_store. 3) Partir workspace.py. 4) Tests en repos temporales.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/ops

## Done When

_Name the observable condition that makes the task complete._

Un desk nuevo se crea y se actualiza solo con la API de sldb.

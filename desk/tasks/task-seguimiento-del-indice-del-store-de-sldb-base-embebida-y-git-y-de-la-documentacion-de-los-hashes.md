---
sldb:
  by: agent
  at: '2026-11-25T19:49:39Z'
  authority: generated
  via: create_document
id: task-seguimiento-del-indice-del-store-de-sldb-base-embebida-y-git-y-de-la-documentacion-de-los-hashes
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
- ../sldb/desk/inbox/20261125-155542-suggestion-propuesta-concreta-para-el-ndice-del-store-complementa-la-nota-de-los-hashes-y-la-p4-de-grafo-datalog-daemon.md
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Seguimiento del índice del store de sldb (base embebida y git) y de la documentación de los hashes

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

La propuesta del índice (sqlite, detección por git, blob ids, caché por contenido) y el pedido de documentar el propósito de cada hash quedan resueltos en sldb, y deskops adopta lo que cambie.

## Scope

_State what is in scope and what is out of scope._

Entra: seguimiento y adopción. Sale: implementarlo en sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Revisar el inbox de sldb. 2) Adoptar.

## Validation

_List the checks required before this task can close._

- La decisión de sldb sobre el índice existe

## Done When

_Name the observable condition that makes the task complete._

sldb decidió sobre el índice y deskops lo adoptó.

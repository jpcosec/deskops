---
sldb:
  by: agent
  at: '2026-11-25T20:28:03Z'
  authority: generated
  via: save_document_payload
id: task-seguimiento-de-lo-que-deskops-necesita-de-sldb-tomar-transicion-ultimo-elemento-de-una-lista-on-dele
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
- ../sldb/desk/inbox/20261125-155202-unclear-correcci-n-de-los-pedidos-c1-c9-de-deskops-del-25-11-c7-y-c8-ya-existen.md
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Seguimiento de lo que deskops necesita de sldb: tomar transición, último elemento de una lista, on_delete y reglas enlazadas

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Los pedidos C2, C3, C4, la parte de reglas de C1 y el pedido de que una máquina de estados se haga respetar (inbox de sldb 20261125-172648) están en sldb; cuando sldb entrega cada uno, deskops lo adopta y borra lo que reemplaza (lifecycle.advance, el validador, el borrado protegido, la siembra de reglas, los if de estado en closure.py).

## Scope

_State what is in scope and what is out of scope._

Entra: seguimiento y el borrado en deskops de cada entrega. Sale: implementarlo en sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Revisar el estado en el inbox de sldb. 2) Por cada entrega, su borrado en deskops.

## Validation

_List the checks required before this task can close._

- Cada entrega de sldb tiene su borrado cerrado en deskops

## Done When

_Name the observable condition that makes the task complete._

Las cuatro entregas tienen su borrado o siguen pedidas.

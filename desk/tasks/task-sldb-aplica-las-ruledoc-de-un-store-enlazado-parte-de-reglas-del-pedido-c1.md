---
sldb:
  by: agent
  at: '2026-11-25T22:55:07Z'
  authority: generated
  via: create_document
id: task-sldb-aplica-las-ruledoc-de-un-store-enlazado-parte-de-reglas-del-pedido-c1
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- ../sldb/desk/inbox/20261125-143612-suggestion-c1-aplicar-ruledoc-y-relationdoc-de-un-store-enlazado.md
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb aplica las RuleDoc de un store enlazado (parte de reglas del pedido C1)

## Rationale

_Explain why this task exists or the business driver behind it._

E3 espera esto de sldb para borrar la copia que deskops mantiene hoy. Es trabajo de sldb; esta tarea solo deja declarado el bloqueo para que no se despache una hoja que lo necesita.

## Goal

_Describe the concrete result this task must produce._

sldb integra en su main que rules_of y RuleGraph.domain dejan de filtrar por store local, como ya pasa con las aristas.

## Scope

_State what is in scope and what is out of scope._

Entra: seguir el pedido en el inbox de sldb y cerrar con el commit o PR de sldb que lo entrega. Sale: implementarlo (es de sldb) y adoptarlo en deskops (es la hoja que depende de esta).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Revisar el inbox y el desk de sldb. 2) Cuando sldb lo integre, cerrar con la URL del commit o del PR.

## Validation

_List the checks required before this task can close._

- la URL del commit o PR de sldb que lo entrega

## Done When

_Name the observable condition that makes the task complete._

sldb lo tiene integrado en main.

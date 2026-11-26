---
sldb:
  by: agent
  at: '2026-11-25T22:55:19Z'
  authority: generated
  via: create_document
id: task-sldb-ofrece-la-primitiva-tomar-transicion-en-su-cli-y-su-api-pedido-c2
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- ../sldb/desk/inbox/20261125-143642-suggestion-c2-primitiva-tomar-transici-n-en-cli-y-api.md
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb ofrece la primitiva tomar transición en su CLI y su API (pedido C2)

## Rationale

_Explain why this task exists or the business driver behind it._

E3 espera esto de sldb para borrar la copia que deskops mantiene hoy. Es trabajo de sldb; esta tarea solo deja declarado el bloqueo para que no se despache una hoja que lo necesita.

## Goal

_Describe the concrete result this task must produce._

sldb integra en su main que una llamada evalúa la arista, mueve el nodo, anota la historia y corre los hooks.

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

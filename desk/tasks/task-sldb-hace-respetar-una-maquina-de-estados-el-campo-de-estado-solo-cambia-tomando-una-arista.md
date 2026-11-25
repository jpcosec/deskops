---
sldb:
  by: agent
  at: '2026-11-25T22:55:42Z'
  authority: generated
  via: create_document
id: task-sldb-hace-respetar-una-maquina-de-estados-el-campo-de-estado-solo-cambia-tomando-una-arista
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- ../sldb/desk/inbox/20261125-172648-suggestion-que-una-m-quina-de-estados-se-haga-respetar-el-campo-de-estado-solo-cambia-tomando-una-arista.md
depends_on: []
pills: []
files: []
task_type: task.external
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb hace respetar una máquina de estados: el campo de estado solo cambia tomando una arista

## Rationale

_Explain why this task exists or the business driver behind it._

E3 espera esto de sldb para borrar la copia que deskops mantiene hoy. Es trabajo de sldb; esta tarea solo deja declarado el bloqueo para que no se despache una hoja que lo necesita.

## Goal

_Describe the concrete result this task must produce._

sldb integra en su main que una escritura que cambia el campo de estado sin tomar una arista se rechaza, y el CI lo comprueba sobre la historia de git.

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

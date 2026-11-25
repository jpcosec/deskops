---
sldb:
  by: agent
  at: '2026-11-25T20:11:06Z'
  authority: generated
  via: save_document_payload
id: task-como-se-hace-respetar-la-maquina-de-estados-del-workflow
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on: []
pills: []
files: []
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Cómo se hace respetar la máquina de estados del workflow

## Rationale

_Explain why this task exists or the business driver behind it._

Diagnóstico del 25-11: el workflow declarado es bueno pero el código no lo hace cumplir (W3, N3, W4, N9, N4). JP, 25-11: deskops es una herramienta para crear workflows, no un workflow fijo; la pregunta no es qué gates exige un desk sino cómo se hace que los gates que declare se respeten.

## Goal

_Describe the concrete result this task must produce._

Una decisión de diseño escrita, con su átomo, sobre el mecanismo que hace respetar las transiciones y gates que un desk declare, y las tareas que salen de ella.

## Scope

_State what is in scope and what is out of scope._

Entra: comparar los mecanismos posibles y combinarlos: (a) la máquina de estados como única vía de escritura de status, current_node e history (una regla on_write que rechaza cambios a esos campos que no vengan de tomar una arista; depende de los pedidos C2 y C3 a sldb); (b) centralizar la escritura del desk en deskops o sldb (operaciones MCP como único camino); (c) git: pre-commit o pre-push locales, que se pueden saltar, y una comprobación en el CI que no se puede saltar y que recorre el historial de git de cada tarea verificando que cada cambio de estado corresponde a una arista válida. (d) antes del CI, correr solo los tests de lo que mutó y dejar su recibo, como gate local de cada tarea de una fase, con la suite completa en el CI para la integración de la fase. Sale: qué gates exige cada desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Escribir para cada mecanismo qué garantiza, cómo se salta y qué cuesta. 2) Proponer una combinación. 3) JP decide. 4) Átomo y tareas.

## Validation

_List the checks required before this task can close._

- La decisión queda en un átomo y cada mecanismo elegido tiene su tarea

## Done When

_Name the observable condition that makes the task complete._

Hay un átomo con el mecanismo elegido y sus tareas creadas.

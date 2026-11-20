---
sldb:
  by: agent
  at: '2026-11-20T02:24:32Z'
  authority: generated
  via: create_document
id: task-ui-de-deskops-sobre-astro-con-las-uis-de-sldb-1-y-la-estructura-de-mepu-y-ft-courier
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# UI de deskops sobre Astro con las UIs de SLDB_1 y la estructura de mepu y FT Courier

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de JP del 2026-11-19 (diagnóstico VSM de AntonIA): a deskops le falta con urgencia una UI. Gian administra sin todo el contexto y necesita ver el estado sin abrir archivos. Piezas para partir: deskops view y su contrato (docs/deskops-ui.md, con un mapeo de una pantalla de Stitch); en SLDB_1/UIs, sldb-ui ya es Astro con React y marcado-ui es React con Tailwind; y la estructura de UI que están sacando mepu y FT Courier (FT Courier reutilizó la UI v2 de mepu, ftcourier #23).

## Goal

_Describe the concrete result this task must produce._

Una UI web de deskops en Astro que muestre board, tareas, inbox, drawer y agentes de uno o varios desks, leyendo deskops view, con los componentes y la estructura compartida con mepu y FT Courier en vez de un diseño aparte.

## Scope

_State what is in scope and what is out of scope._

Dentro: la UI de solo lectura primero, y la decisión de qué componentes se comparten con mepu, FT Courier y sldb-ui. Fuera: escribir desde la UI en la primera versión.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- Playwright contra un desk de prueba

## Done When

_Name the observable condition that makes the task complete._

La UI levanta contra el desk de Governance y el de mepu y muestra lo mismo que deskops view; está documentado de qué paquete compartido salen sus componentes.

---
sldb:
  by: agent
  at: '2026-11-26T02:29:46Z'
  authority: generated
  via: create_document
id: task-el-despacho-no-lanza-un-intento-2-de-ejecutor-si-el-intento-1-ya-dejo-result-summary-md-lo-manda-al
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- ../sala/2026-11-25-planificacion/robocop2.md
- ../sala/2026-11-25-planificacion/deskops.md
depends_on: []
pills: []
files:
- deskops/dispatch.py
- deskops/queue.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El despacho no lanza un intento 2 de ejecutor si el intento 1 ya dejó result-summary.md: lo manda al reap

## Rationale

_Explain why this task exists or the business driver behind it._

Bug del despacho que hoy rompe trabajo en robocop2 (informe del despacho en la sala de planificación, 2026-11-25). JP decidió el 2026-11-25 que entra antes de E1, como excepción al orden de etapas. Un ejecutor que entregó y terminó por limits_exceeded fue relanzado como -a2; el -a2 rehízo el trabajo sin commitear y le bloqueó el reap al bueno (graph_ui, modo local).

## Goal

_Describe the concrete result this task must produce._

deskops dispatch start de un ejecutor, cuando el run_dir del intento anterior tiene result-summary.md, no crea el intento 2: imprime que la entrega está hecha, encola el reap de la tarea y sale con un código propio que la cola no reintenta.

## Scope

_State what is in scope and what is out of scope._

Entra: la elección de intento en dispatch.py (start) y el reintento de la cola en queue.py (retry_exit_codes no debe incluir ese código). Sale: el reap mismo (ya reconoce result-summary.md, dispatch.py:684) y los topes de los templates (son de scion).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Test de aceptación: run_dir del intento 1 con result-summary.md y dispatch start del ejecutor no crea el -a2 y deja un job de reap. 2) Comprobación en start antes de escoger el intento. 3) Código de salida propio, fuera de retry_exit_codes.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests -k 'dispatch and attempt'
- un dispatch start con result-summary.md en el intento 1 no crea agente -a2

## Done When

_Name the observable condition that makes the task complete._

Con result-summary.md en el intento 1, el despacho hace reap y nunca lanza -a2.

---
sldb:
  by: agent
  at: '2026-11-26T02:29:56Z'
  authority: generated
  via: create_document
id: task-una-parada-pedida-por-el-despacho-sigterm-exit-255-queda-como-detenida-y-no-como-falla
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- ../sala/2026-11-25-planificacion/scion.md
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

# Una parada pedida por el despacho (SIGTERM, exit 255) queda como detenida y no como falla

## Rationale

_Explain why this task exists or the business driver behind it._

Bug del despacho que hoy rompe trabajo en robocop2 (informe del despacho en la sala de planificación, 2026-11-25). JP decidió el 2026-11-25 que entra antes de E1, como excepción al orden de etapas. scion informa exit 255 cuando el contenedor termina después de un SIGTERM pedido desde fuera, con crash=false; el despacho lo lee como falla.

## Goal

_Describe the concrete result this task must produce._

Cuando el despacho o la cola detienen un agente y scion informa exit 255 con crash=false, el job y el RunDoc quedan como stopped, no failed, y no cuentan como intento fallido.

## Scope

_State what is in scope and what is out of scope._

Entra: donde dispatch.py y queue.py leen el código de salida y la fase del agente. Sale: cambiar cómo scion informa el código (es de scion).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Ubicar dónde se interpreta el exit del agente. 2) Distinguir parada pedida (stop propio o crash=false) de caída. 3) Test con un agente simulado que sale 255 tras stop.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests -k 'dispatch or queue'

## Done When

_Name the observable condition that makes the task complete._

Una parada pedida no aparece como falla en la cola ni en el RunDoc.

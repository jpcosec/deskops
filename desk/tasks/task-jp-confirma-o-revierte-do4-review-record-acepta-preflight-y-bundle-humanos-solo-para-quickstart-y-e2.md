---
sldb:
  by: agent
  at: '2026-11-24T18:29:05Z'
  authority: generated
  via: save_document_payload
id: task-jp-confirma-o-revierte-do4-review-record-acepta-preflight-y-bundle-humanos-solo-para-quickstart-y-e2
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-decisión-revisable-por-jp-review-record-firma-preflight-bundle-humano-contradice-pill-zero-context-p.md
depends_on: []
pills:
- desk/contexts/pill-zero-context-preflight-precedes-executor.md
files:
- desk/drawer/plans/deskops-como-config/decisiones.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# JP confirma o revierte DO4: review record acepta preflight y bundle humanos solo para quickstart y e2e del CI

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del 2026-11-09 (coordinador de proyecto, revisable por JP; DO4 en desk/drawer/plans/deskops-como-config/decisiones.md). Para dejar main en verde, `deskops review record` acepta kind preflight y bundle con evidencia del operador (engine human, operador y motivo 'no model available'; deskops/services/review.py alrededor de las lineas 74 y 683-690). Contradice la pill pill-zero-context-preflight-precedes-executor. Condiciones del overlord: el recibo deja visible engine human; solo se usa en el quickstart y los e2e del CI y no para activar tareas reales hasta que JP confirme. Hoy el codigo no impide usarlo en un desk real.

## Goal

_Describe the concrete result this task must produce._

Queda registrada la decision de JP entre: (a) confirmar DO4 tal cual; (b) confirmar y que el codigo rechace `review record --kind preflight|bundle` fuera del CI (p. ej. si no hay CI=true); (c) revertir: quitar esos kinds de review record y dar al e2e otra via. Si elige (b) o (c), se crea la tarea task.code correspondiente.

## Scope

_State what is in scope and what is out of scope._

Entra: la decision, su registro en decisiones.md (DO4) y, si aplica, crear la tarea de codigo. No entra: implementar el cambio.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Presentar a JP las tres opciones con este contexto. 2) Registrar el recibo owner con su respuesta. 3) Anotar la decision con fecha en DO4. 4) Si (b)/(c), `deskops add task` con el cambio.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -n 'DO4' desk/drawer/plans/deskops-como-config/decisiones.md (muestra la decision del dueño con fecha)

## Done When

_Name the observable condition that makes the task complete._

DO4 dice que eligio JP y cuando; si corresponde, existe la tarea de codigo.

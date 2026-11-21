---
id: task-e01-prueba-integral-multiagente-opsys-scion-ui-la-recibe-deskops-graph-ui-la-bota-de-su-drawer
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# E01 prueba integral multiagente opsys-scion-UI: la recibe deskops (graph_ui la bota de su drawer)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261116-004716-suggestion-e01-prueba-integral-multiagente-opsys-scion-ui-la-recibe-deskops-graph-ui-la-bota-de-su-drawer.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261116-004716-suggestion-e01-prueba-integral-multiagente-opsys-scion-ui-la-recibe-deskops-graph-ui-la-bota-de-su-drawer.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Desde graph_ui, triaje 2026-11-16. El drawer de graph_ui tenía desde el 2026-10-31 'Prueba integral multiagente Opsys-Scion-UI' (E01 de softfactory_spec): validar de punta a punta crear y avanzar una tarea en deskops, despacharla y ejecutarla en Scion, y verla en la UI. graph_ui es solo un cliente de ese flujo: el contrato de la UI es de deskops (docs/deskops-ui.md) y la ejecución es de scion, que hoy está en piloto en el desk de IR (fase 1 de scion en pausa). Por eso graph_ui no puede ser dueño de E01 y lo saca de su drawer. Si deskops la toma, la parte de graph_ui es una verificación en el navegador sobre el desk real (host:local); pídanla por inbox con el contrato de lo que la UI debe mostrar y graph_ui la convierte en tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.

---
sldb:
  by: agent
  at: '2026-11-16T02:20:48Z'
  authority: generated
  via: create_document
id: task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados
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

# La regla de desk_graph sobre specs deja de nombrar spec2viz y reconoce los specs YAML sincronizados con sldb notations sync

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15 (G7 aceptada y recomendación del coordinador aceptada): el YAML del spec queda subordinado al grafo y spec2viz se archiva cuando specir retirement check salga con 0; deskops/graph/desk_graph.py:75 es la última regla de deskops que espera a G7.

## Goal

_Describe the concrete result this task must produce._

La regla de desk_graph.py reconoce los specs YAML como artefactos de autoría que se sincronizan al store con sldb notations sync, sin nombrar ni depender de spec2viz.

## Scope

_State what is in scope and what is out of scope._

Entra: la regla de desk_graph.py:75 y sus tests. Sale: las habilidades y el script render_diagram.py (pedido aparte de IR13 en el inbox).

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer la regla actual, reemplazar la referencia a spec2viz por los specs sincronizados vía sldb (SpecDoc), test real sobre un desk con un spec sincronizado.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q del test de la regla de desk_graph

## Done When

_Name the observable condition that makes the task complete._

grep de spec2viz en deskops/graph/desk_graph.py sin coincidencias y el test de la regla en verde.

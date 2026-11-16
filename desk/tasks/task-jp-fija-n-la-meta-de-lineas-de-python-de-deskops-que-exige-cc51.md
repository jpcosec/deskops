---
sldb:
  by: agent
  at: '2026-11-16T04:08:01Z'
  authority: generated
  via: save_document_payload
id: task-jp-fija-n-la-meta-de-lineas-de-python-de-deskops-que-exige-cc51
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-como-config/dag.yaml
depends_on: []
pills: []
files:
- desk/drawer/plans/deskops-como-config/decisiones.md
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# JP fija N, la meta de lineas de Python de deskops que exige CC51

## Rationale

_Explain why this task exists or the business driver behind it._

Plan deskops-como-config, nodo CC51 y decision DA3: N la fija el dueno despues de CC30 y antes de promover CC51. No esta fijado en decisiones.md. Base (827f3db7): 18,732 lineas (`find deskops -name '*.py' | xargs wc -l`). Medicion aproximada del 2026-11-16 en main: ~22,422; crecio respecto de la base.

## Goal

_Describe the concrete result this task must produce._

JP fija N (o decide quitar la meta numerica de CC51) y queda registrado en decisiones.md del plan.

## Scope

_State what is in scope and what is out of scope._

Entra: la decision. No entra: medir de nuevo ni escribir docs/config-vs-code.md (es CC51).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Presentar a JP la base y la medicion actual. 2) Registrar el recibo owner. 3) Anotar N en decisiones.md.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -n 'DA3' desk/drawer/plans/deskops-como-config/decisiones.md (muestra N fijado con fecha)

## Done When

_Name the observable condition that makes the task complete._

N (o la eliminacion de la meta) esta registrada con fecha en decisiones.md.

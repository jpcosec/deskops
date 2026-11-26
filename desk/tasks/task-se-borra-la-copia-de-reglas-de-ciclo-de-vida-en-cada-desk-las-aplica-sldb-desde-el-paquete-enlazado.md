---
sldb:
  by: agent
  at: '2026-11-25T22:55:54Z'
  authority: generated
  via: create_document
id: task-se-borra-la-copia-de-reglas-de-ciclo-de-vida-en-cada-desk-las-aplica-sldb-desde-el-paquete-enlazado
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-sldb-aplica-las-ruledoc-de-un-store-enlazado-parte-de-reglas-del-pedido-c1
- task-deskops-lee-las-aristas-del-ciclo-de-vida-desde-el-store-enlazado-y-deja-de-copiarlas-donde-sldb-ya
pills: []
files:
- deskops/lifecycle.py
- deskops/workspace.py
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Se borra la copia de reglas de ciclo de vida en cada desk: las aplica sldb desde el paquete enlazado

## Rationale

_Explain why this task exists or the business driver behind it._

deskops copia sus RuleDoc de activación y de cierre a cada desk porque sldb aplica solo las reglas locales; las copias derivan. Con C1 la copia sobra.

## Goal

_Describe the concrete result this task must produce._

desk update e init dejan de sembrar RuleDoc de ciclo de vida y un desk sin copias locales aplica las reglas del paquete.

## Scope

_State what is in scope and what is out of scope._

Entra: la siembra de reglas en lifecycle.py y workspace.py, y borrar las copias de los desks con desk update --apply. Sale: las aristas (ya las cubre la tarea de aristas enlazadas).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Escenario: un desk sin copias rechaza un cierre que la regla del paquete rechaza. 2) Quitar la siembra. 3) desk update --apply borra las copias.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core tests/ops

## Done When

_Name the observable condition that makes the task complete._

Ningún desk tiene copias de reglas de ciclo de vida y los escenarios pasan.

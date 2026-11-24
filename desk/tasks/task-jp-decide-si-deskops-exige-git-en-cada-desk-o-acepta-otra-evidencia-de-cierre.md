---
sldb:
  by: agent
  at: '2026-11-24T02:19:21Z'
  authority: generated
  via: save_document_payload
id: task-jp-decide-si-deskops-exige-git-en-cada-desk-o-acepta-otra-evidencia-de-cierre
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-004653-unclear-desk-sin-git-closeout-resolved-by-y-task-decision-piden-un-commit-imposible.md
- desk/inbox/20261116-005408-unclear-desk-sin-git-sldb-ui-supersede-tambi-n-hace-commit-drawer-remove-no-acepta-el-stem.md
depends_on: []
pills: []
files: []
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# JP decide si deskops exige git en cada desk o acepta otra evidencia de cierre

## Rationale

_Explain why this task exists or the business driver behind it._

Notas del 2026-11-16 de UIs/marcado (20261116-004653) y UIs/sldb-ui (20261116-005408): en un desk sin git, closeout resolved-by, task.decision (evidencia commit) y supersede (deskops/services/closure.py hace git add/commit) no se pueden cumplir, y no queda verbo para retirar una tarea. Ambos desks se volvieron repos git ese mismo dia (marcado 39e1ca7, sldb-ui 56a552b), asi que hoy no hay desk bloqueado, pero la regla general no esta decidida.

## Goal

_Describe the concrete result this task must produce._

Decision registrada de JP entre: (A) deskops exige git: init falla o avisa y doctor da issue si la raiz no es un repo git; (B) deskops admite desks sin git con otra evidencia de cierre (document/external) y supersede sin commit. Segun la opcion, el coordinador crea la tarea task.code que la implementa.

## Scope

_State what is in scope and what is out of scope._

Solo la decision; la implementacion es otra tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

JP responde A o B; el coordinador registra la respuesta como documento y cierra con closeout.

## Validation

_List the checks required before this task can close._

- Decision de JP registrada con la opcion elegida

## Done When

_Name the observable condition that makes the task complete._

La decision esta registrada y, si corresponde, existe la tarea que la implementa.

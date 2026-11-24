---
sldb:
  by: agent
  at: '2026-11-24T18:29:23Z'
  authority: generated
  via: save_document_payload
id: task-jp-decide-si-deskops-promote-inbox-to-drawer-task-se-retira
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-003032-unclear-la-skill-y-ritual-drawer-triage-mandan-el-inbox-al-drawer-los-atoms-dicen-que-no.md
depends_on: []
pills: []
files:
- deskops/cli/commands/promote.py
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# JP decide si deskops promote inbox-to-drawer-task se retira

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del 2026-11-16 (contradiccion inbox/drawer). promote inbox-to-drawer-task borra la nota de origen y la tarea pierde su origen; el camino que confirmo JP para una nota que es trabajo es add task con references y ack, y el drawer se captura directamente. La nota pide decidir si el comando se retira.

## Goal

_Describe the concrete result this task must produce._

JP elige: (a) retirar promote inbox-to-drawer-task (se crea la tarea de codigo que borra el comando, sus goldens y sus tests, tests/test_inbox_promote_cli_gaps.py incluido); (b) mantenerlo con la advertencia en su ayuda (la cubre la tarea de alineacion de skill y ritual); (c) cambiarlo para que conserve la nota y la referencie.

## Scope

_State what is in scope and what is out of scope._

Entra: la decision y el alta de la tarea que corresponda. No entra: implementar.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Presentar las opciones a JP. 2) Registrar el recibo owner. 3) Crear la tarea de la opcion elegida.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops list tasks --root . (aparece la tarea de la opcion elegida, salvo con (b))

## Done When

_Name the observable condition that makes the task complete._

La opcion de JP esta registrada y, si es (a) o (c), existe su tarea.

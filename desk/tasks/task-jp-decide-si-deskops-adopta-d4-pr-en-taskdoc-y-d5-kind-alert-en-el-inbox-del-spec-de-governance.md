---
sldb:
  by: agent
  at: '2026-11-16T04:07:26Z'
  authority: generated
  via: save_document_payload
id: task-jp-decide-si-deskops-adopta-d4-pr-en-taskdoc-y-d5-kind-alert-en-el-inbox-del-spec-de-governance
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
files:
- deskops/models/task.py
- deskops/models/inbox.py
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-requisitos-d4-d6-de-governance-pr-en-taskdoc-alertas-en-el-inbox-y-rundoc.md
---

# JP decide si deskops adopta D4 (PR en TaskDoc) y D5 (kind alert en el inbox) del spec de Governance

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (Governance, 2026-10-20). El spec docs/spec/spec-procesos-modelables.md (draft) de heyantonia/Governance pide: D4, que TaskDoc declare el PR o la rama que la realiza como referencia a un PullRequestDoc; D5, que InboxNoteDoc.kind admita 'alert' (hoy deskops/models/inbox.py:44 solo admite unclear y suggestion) o una via para enrutar un AlertDoc al inbox. D6 (RunDoc al lanzar un subagente) lo cubre la tarea de RunDoc por intento. Ninguno bloquea hoy y el spec sigue en draft.

## Goal

_Describe the concrete result this task must produce._

JP decide, por separado para D4 y D5: adoptarlo ahora (se crea la tarea de codigo), esperar a que el spec de Governance salga de draft, o descartarlo.

## Scope

_State what is in scope and what is out of scope._

Entra: la decision y, si corresponde, el alta de las tareas. No entra: implementar ni cambiar modelos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Presentar D4 y D5 a JP. 2) Registrar el recibo owner. 3) Crear las tareas que correspondan.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops list tasks --root . (aparecen las tareas de lo adoptado, si lo hay)

## Done When

_Name the observable condition that makes the task complete._

La decision sobre D4 y D5 esta registrada y existen las tareas de lo adoptado.

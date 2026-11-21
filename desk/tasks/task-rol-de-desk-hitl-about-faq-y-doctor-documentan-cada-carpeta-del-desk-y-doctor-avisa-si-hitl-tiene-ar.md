---
sldb:
  by: agent
  at: '2026-11-21T07:52:25Z'
  authority: generated
  via: save_document_payload
id: task-rol-de-desk-hitl-about-faq-y-doctor-documentan-cada-carpeta-del-desk-y-doctor-avisa-si-hitl-tiene-ar
status: draft
summary: 'Borrador sin preparar: preflight rechazado el 2026-11-21 (ver desk/reviews/task-rol-de-desk-hitl-about-faq-y-doctor-documentan-cada-carpeta-del-desk-y-doctor-avisa-si-hitl-tiene-ar/).
  Falta Implementation Path concreto, decisiones de diseno y nombre del test antes
  de revisar de nuevo.'
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-194443-unclear-rol-de-desk-hitl-y-carpetas-no-modeladas.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# rol de desk/hitl: about, faq y doctor documentan cada carpeta del desk y doctor avisa si hitl tiene archivos que no son para el humano

## Rationale

_Explain why this task exists or the business driver behind it._

Origen: nota de MEPU del 15-11 (no llego al inbox de deskops porque --to deskops no resolvia; transcrita en velocidad-hooks-brief.md, Parte D). No esta escrito para que sirve desk/hitl ni el resto de carpetas; en MEPU hitl/ acumula archivos de agentes.

## Goal

_Describe the concrete result this task must produce._

deskops about y deskops faq describen cada carpeta de desk/ (incluida hitl/), y doctor emite una alerta cuando desk/hitl contiene archivos que no son para el humano.

## Scope

_State what is in scope and what is out of scope._

deskops/about.py, faq del paquete, deskops doctor; criterio de 'para el humano' declarado como dato, no a mano en el codigo.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- test nuevo de deskops (nombre a fijar al promover) con un archivo de agente y uno humano en desk/hitl

## Done When

_Name the observable condition that makes the task complete._

about y faq nombran cada carpeta; un test con un archivo de agente en hitl/ produce la alerta y uno humano no.

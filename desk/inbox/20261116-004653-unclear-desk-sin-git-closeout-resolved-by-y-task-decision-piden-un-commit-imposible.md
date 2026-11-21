---
sldb:
  by: agent
  at: '2026-11-21T06:42:32Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: marcado
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:46:53'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:42:25'
# why the note was acknowledged; empty when no reason was given
ack_reason: Marcado es repo git desde 39e1ca7 (2026-11-16); la regla general (exigir
  git o aceptar otra evidencia) queda en task.decision task-jp-decide-si-deskops-exige-git-en-cada-desk-o-acepta-otra-evidencia-de-cierre.
---

# Desk sin git: closeout resolved-by y task.decision piden un commit imposible

_Describe the incoming message with enough evidence to triage._

De: coordinador de UIs/marcado, 2026-11-16. UIs/marcado no es un repo git. Para las 56 tareas legacy inválidas, el doctor propone closeout resolved-by --ref <commit>, y task.decision cierra con evidencia commit + document; en un desk sin git ninguna de las dos se puede cumplir y solo queda supersede. Falta decidir si deskops exige git en cada desk (y lo avisan deskops init y doctor) o si acepta otra evidencia. JP decide en marcado si hace git init: task.decision creada hoy.

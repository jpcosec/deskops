---
sldb:
  by: agent
  at: '2026-11-20T23:29:47Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-20T19:40:46'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-20T20:29:40'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en tarea borrador task-governance-e-g-other-repo, para prepararla
  con la propuesta completa de Governance.
---

# Versionar deskops y fijarlo en quienes lo usan

_Describe the incoming message with enough evidence to triage._

Del diagnóstico: las herramientas no tienen versiones publicadas y cada repo las instala desde un commit distinto (robocop-ci usa deskops en 4904ddf). Pedido: tags cuando un cambio rompe compatibilidad y CI de main en verde, para que los repos fijen versión. Reemplaza, en lo que toca a deskops, la tarea de Governance «versionar sldb, deskops y spec2viz».

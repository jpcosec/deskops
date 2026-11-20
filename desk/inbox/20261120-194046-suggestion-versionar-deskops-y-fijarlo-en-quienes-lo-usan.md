---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-20T19:40:46'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# Versionar deskops y fijarlo en quienes lo usan

_Describe the incoming message with enough evidence to triage._

Del diagnóstico: las herramientas no tienen versiones publicadas y cada repo las instala desde un commit distinto (robocop-ci usa deskops en 4904ddf). Pedido: tags cuando un cambio rompe compatibilidad y CI de main en verde, para que los repos fijen versión. Reemplaza, en lo que toca a deskops, la tarea de Governance «versionar sldb, deskops y spec2viz».

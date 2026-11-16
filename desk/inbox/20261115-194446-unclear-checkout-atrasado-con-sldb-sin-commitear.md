---
sldb:
  by: agent
  at: '2026-11-16T04:11:44Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-15T19:44:46'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T01:11:42'
---

# checkout atrasado con .sldb sin commitear

_Describe the incoming message with enough evidence to triage._

Desde MEPU (2026-11-15): con el checkout principal atrasado (48 commits detrás de dev) y cambios de .sldb/core sin commitear de tareas anteriores (Board.yaml, TaskCodeDoc, store_index), el agente no sabe si puede ponerse al día sin pisar trabajo de otra sesión, y posterga registrar tareas. Pedido: guía en doctor (o un `deskops sync`) que diga de qué tarea es cada cambio de .sldb y cómo ponerse al día sin perderlo.

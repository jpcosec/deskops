---
sldb:
  by: agent
  at: '2026-11-19T12:49:58Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-19T09:27:30'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-19T09:49:52'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Recibido: sldb ahora acepta directorios existentes como target declarado
  (con o sin barra final); graph missing de deskops deja de reportarlos al actualizar
  herramientas.'
---

# sldb: un directorio existente declarado como target es un nodo del grafo

_Describe the incoming message with enough evidence to triage._

sldb main 53b1dc87 (código 6f14a3b5 y 4bd45239). Un target declarado de una materialización que es un directorio existente dentro de la raíz del proyecto ahora es un FileNode con file_kind directory, sin expandirse por archivo. Se resuelve con o sin barra final (dir y dir/). deskops graph missing deja de reportarlo como missing_declared_target; un directorio inexistente o fuera de la raíz sigue reportándose. Llega a herramientas en 53b1dc87.

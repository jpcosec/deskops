---
sldb:
  by: agent
  at: '2026-11-17T01:30:18Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T22:24:01'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T22:30:10'
---

# deskops message ack no admite una razón, y InboxNote no tiene un campo para guardarla

_Describe the incoming message with enough evidence to triage._

Al cerrar notas del inbox con 'deskops message ack <selector>' no hay forma de dejar el porqué: ack no acepta --reason, y el modelo InboxNote solo tiene kind, sender_project, target_project, created_at, status, acknowledged_by y acknowledged_at, así que 'deskops edit inbox-note' tampoco puede escribirlo. Caso real: en IR había que cerrar 8 avisos de sldb con la razón «llegaron por un pedido erróneo del supervisor» (IR aún no está en marcha y no debía recibirlos). Quedó solo en un reporte fuera del desk. Pedido: un campo opcional, ack_reason o resolution, y 'deskops message ack --reason'.

---
sldb:
  by: agent
  at: '2026-11-23T04:42:32Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-23T02:43:25'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T01:42:25'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en tarea task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt
  (campo conversation_ref, --conv en add atom y message send, filtro en list atoms
  y aviso de duplicado).
---

# Campo propio para la referencia de conversacion scion en atoms y notas

_Describe the incoming message with enough evidence to triage._

Hoy la referencia conv/#thread de un acuerdo va en --provenance y en el texto; se pide un campo o comando propio (por ejemplo deskops add agreement --conv <ref> --message <id>) para poder listar acuerdos por conversacion. Origen: hilo #acuerdos-sldb1 del proyecto scion wf-desks, encargo de JP via scion-coordination.

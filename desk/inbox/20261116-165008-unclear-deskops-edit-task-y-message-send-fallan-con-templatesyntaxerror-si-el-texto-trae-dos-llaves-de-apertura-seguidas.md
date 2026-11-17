---
sldb:
  by: agent
  at: '2026-11-17T01:27:40Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T16:50:08'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T22:27:33'
---

# deskops edit task y message send fallan con TemplateSyntaxError si el texto trae dos llaves de apertura seguidas

_Describe the incoming message with enough evidence to triage._

En sldb-ui, 'deskops edit task <id> scope <texto>' falla con 'TemplateSyntaxError: unexpected char' cuando el valor contiene dos o tres llaves de apertura seguidas. El caso real era un input de prueba citado: el texto 'this is not valid json' seguido de tres llaves. Con 'deskops message send' pasa lo mismo: esta misma nota falló en su primera versión. Parece que el valor se pasa por Jinja al renderizar la plantilla del documento. Un campo de texto debería guardarse literal; hoy hay que reescribir la cita para poder guardarla.

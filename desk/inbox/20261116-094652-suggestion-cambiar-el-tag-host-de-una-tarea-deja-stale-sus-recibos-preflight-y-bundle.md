---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T09:46:52'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Cambiar el tag host:* de una tarea deja stale sus recibos preflight y bundle

_Describe the incoming message with enough evidence to triage._

En graph_ui (c3664af), JP mudó las tareas de host:local a host:robocop2 con 'deskops edit task <t> tags ...'. Con eso, deskops review status marcó stale los recibos preflight y bundle de todas, aunque el contrato (why, goal, scope, path, validation, done_when) no cambió. Como 'review record' no puede reemplazar a una revisión de modelo, hubo que re-correr las revisiones pi con --force. Propuesta: sacar tags (o al menos el namespace host:) del input del digest de contexto o de __contract__, o tener un verbo que re-ancle un recibo aceptado cuando solo cambian campos de ruteo. Hace falta además que exista el namespace host: en tag_namespaces.

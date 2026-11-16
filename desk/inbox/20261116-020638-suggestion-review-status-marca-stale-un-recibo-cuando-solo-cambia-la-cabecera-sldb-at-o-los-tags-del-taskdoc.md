---
sldb:
  by: agent
  at: '2026-11-16T06:11:43Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: pron-repair
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T02:06:38'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T03:11:37'
---

# review status marca stale un recibo cuando solo cambia la cabecera sldb.at o los tags del TaskDoc

_Describe the incoming message with enough evidence to triage._

En pron (2026-11-16), con preflight-3 y bundle-2 aceptados para task-pron-docs-spec2viz-build-py-invoca-specir-…, un 'deskops edit task <id> tags [...]' (tags no es campo del contrato) y luego revertirlo al valor original deja 'deskops review status' en stale para ambos: el input_sha256 se calcula sobre el texto del TaskDoc, que incluye la cabecera sldb.at (cambia en cada save, git diff solo muestra esa línea) y los tags. Efecto: rutear por host con tags (pedido del supervisor: tareas con host:robocop2) obliga a repetir las revisiones pi forzando el tope de intentos. Propuesta: que el hash del input de preflight/bundle excluya la cabecera sldb y los campos que no son del contrato (tags, status, current_node, history), igual que el anchor_state del recibo.

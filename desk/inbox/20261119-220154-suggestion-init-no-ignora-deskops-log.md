---
sldb:
  by: agent
  at: '2026-11-21T06:40:49Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: hbc_latina
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-19T22:01:54'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:40:41'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en tarea task-deskops-init-agrega-deskops-log-al-gitignore-del-repo
  (bootstrap.py no asegura .deskops.log; operations.py:74 lo escribe en la raiz).
---

# init no ignora .deskops.log

_Describe the incoming message with enough evidence to triage._

deskops init (vía sldb stores init) agrega .sldb_cache/ al .gitignore del proyecto, pero no .deskops.log, que OperationsService._setup_logging (deskops/operations.py:74) escribe en la raíz del repo en cada comando. Visto en hbc_latina el 2026-11-19: hubo que agregarlo a mano. Propuesta: que deskops init asegure también la línea .deskops.log, como sldb hace con ensure_cache_ignored (o que el log salga de la raíz del repo).

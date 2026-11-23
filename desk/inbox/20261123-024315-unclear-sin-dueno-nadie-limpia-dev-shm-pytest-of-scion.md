---
sldb:
  by: agent
  at: '2026-11-23T04:42:43Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-23T02:43:15'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T01:42:35'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Dueño: deskops (dispatch arma el encargo y reap borra los agentes). Convertida
  en tarea task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt;
  la parte del host (pytest-of-robocop) va en task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas.'
---

# SIN DUENO: nadie limpia /dev/shm/pytest-of-scion

_Describe the incoming message with enough evidence to triage._

Los testers despachados dejan /dev/shm/pytest-of-scion (5.9 GB el 2026-11-22); lo borra a mano el coordinador de SLDB_1. Falta un encargado y un mecanismo de limpieza. Origen: handoff scion-coordination 2026-11-23.

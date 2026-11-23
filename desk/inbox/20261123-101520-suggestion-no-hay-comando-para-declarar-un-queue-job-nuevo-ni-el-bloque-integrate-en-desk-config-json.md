---
sldb:
  by: agent
  at: '2026-11-23T13:16:00Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-23T10:15:20'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T10:15:51'
# why the note was acknowledged; empty when no reason was given
ack_reason: anexada a task-las-rutas-y-credenciales-de-maquina-de-dispatch-e-integrate-salen-de-desk-config-json-versionado-a-d
  (referencia agregada)
---

# No hay comando para declarar un queue_job nuevo ni el bloque integrate en desk/config.json

_Describe the incoming message with enough evidence to triage._

Visto por Governance al preparar heyantonia/shared_llm-gateway (~/coordinacion/governance-a-scion-coordination-2026-11-23.md, seccion del 23-11 tarde): deskops queue job set solo edita trabajos ya declarados y no hay comando para declarar integrate (mode, branch, suite, remote_url), asi que desk/config.json se escribio a mano. Pedido: que la tarea de config por maquina cubra crear un queue_job y declarar integrate por CLI, ademas de escribir config.local.json.

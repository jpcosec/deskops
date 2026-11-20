---
sldb:
  by: agent
  at: '2026-11-20T23:23:14Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-20T19:39:37'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-20T20:23:04'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en tarea borrador , para prepararla con la propuesta completa
  de Governance.
---

# Documento de PR en desk/PRS y pr check en CI

_Describe the incoming message with enough evidence to triage._

Decisión de JP (19-11): todo PR a dev trae un documento en desk/PRS que explica qué, cómo, cuándo, dónde y por qué, sin el ritual completo. Pedido: un modelo para ese documento, un comando deskops pr check que corra en CI y rechace el PR sin documento, con un campo vacío o que nombre una tarea inexistente, y la generación del documento desde una tarea macro (task.aggregate con children; el campo children todavía no existe, ver data/rules/closeout-evidence.yaml). Fuente: heyantonia/Governance, rama dev, docs/diagnostico-vsm-2026-11-19/revision-deskops/propuesta-workflow.md, sección 2.

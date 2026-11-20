---
sldb:
  by: agent
  at: '2026-11-20T23:24:08Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-20T19:40:02'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-20T20:23:59'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en tarea borrador , para prepararla con la propuesta completa
  de Governance.
---

# Agente interno por desk, en scion, activado por hooks

_Describe the incoming message with enough evidence to triage._

Decisión de JP (20-11): un agente interno por desk que hace el mantenimiento (triaje del inbox, proponer cierres, armar los PR de desk), corre en scion y se activa por hooks de deskops. Además lee el canal informal de scion y propone tareas o notas de inbox cuando detecta un compromiso. No toca código, no se audita a sí mismo y no decide lo que es de una persona. Falta: hooks por evento (hoy lifecycle_hooks.py solo corre al avanzar una transición), actor en history y una identidad propia. Fuente: heyantonia/Governance, rama dev, docs/diagnostico-vsm-2026-11-19/revision-deskops/propuesta-workflow.md, secciones 6 y 7.

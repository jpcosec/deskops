---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-20T19:40:40'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# Migración del workflow nuevo: los diez desks a la vez, con vuelta atrás probada

_Describe the incoming message with enough evidence to triage._

Decisión de JP (20-11): el workflow nuevo se lleva a los diez desks a la vez. Con el cierre dentro del PR y pr check obligatorio, un error en la migración frena los merges a dev en todos los repos el mismo día. Pedido: que desk update tenga una vuelta atrás probada antes de correr la migración. Además los topes del despachador (deskops dispatch) los decide scion según el hardware; deskops no fija umbrales a priori. Fuente: heyantonia/Governance, rama dev, docs/diagnostico-vsm-2026-11-19/revision-deskops/propuesta-workflow.md, secciones 5, 9 y 11.

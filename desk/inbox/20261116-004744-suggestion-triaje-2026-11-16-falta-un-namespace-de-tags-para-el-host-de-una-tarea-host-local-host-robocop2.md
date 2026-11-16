---
sldb:
  by: agent
  at: '2026-11-16T04:13:10Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:47:44'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T01:13:07'
---

# Triaje 2026-11-16: falta un namespace de tags para el host de una tarea (host:local, host:robocop2)

_Describe the incoming message with enough evidence to triage._

Brief de triaje de JP (SLDB_1/triaje-drawers-inbox-brief.md, «Dónde corre cada tarea»): TaskDoc.tags debe decir en qué máquina corre la tarea; lo que tiene UI va a la máquina local y el resto a robocop2. sldb tags namespaces --store .sldb en spec2viz solo declara domain, layer, system y topic: no hay namespace para host. Propuesta: declarar el namespace host con los valores host:local y host:robocop2 en la semilla de deskops (deskops desk update --apply), para que cada coordinador lo ponga con deskops edit task <id> tags. Mientras tanto, spec2viz anota el host en su informe (reports/triaje-spec2viz-20261116.md): su única tarea creada, la task.decision G5, es de robocop2 (sin UI).

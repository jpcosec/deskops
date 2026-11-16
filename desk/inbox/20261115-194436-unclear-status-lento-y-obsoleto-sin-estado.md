---
sldb:
  by: agent
  at: '2026-11-16T04:11:58Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-15T19:44:36'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T01:11:56'
---

# status lento y obsoleto sin estado

_Describe the incoming message with enough evidence to triage._

Desde MEPU (2026-11-15): `deskops status --root .` tardó más de 60 s y se cortó por timeout; con más tiempo terminó pero solo imprimió «Deprecated: use `deskops doctor`». Un agente que necesita orientarse rápido lo salta y termina escribiendo a mano en desk/. Pedido: que status/doctor respondan en pocos segundos (o un modo rápido) y que el aviso de obsoleto, además de redirigir, entregue el estado.

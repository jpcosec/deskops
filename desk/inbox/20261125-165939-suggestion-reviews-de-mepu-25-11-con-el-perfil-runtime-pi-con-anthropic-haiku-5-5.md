---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-25T16:59:39'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Reviews de MEPU (25-11) con el perfil runtime-pi-con-anthropic-haiku-5-5

_Describe the incoming message with enough evidence to triage._

Reviews de MEPU (25-11) con el perfil runtime-pi-con-anthropic-haiku-5-5-revisor-barato-…: 4 corridas terminaron en «timeout after 900s» con output.md vacío (preflight-1 de INC-2, bundle-1 de TST-18, bundle-1 de TST-19 y la primera de TST-17, que cortó el timeout del CLI) y hubo que repetirlas con --force. El recibo queda con technical_ok=false pero se puede disponer igual. Pedidos: (1) que review preflight/bundle reintente una vez sola si el motor corta por tiempo sin salida, o que el timeout sea configurable por perfil; (2) que dispose rechace (o avise) disponer un recibo con output vacío.

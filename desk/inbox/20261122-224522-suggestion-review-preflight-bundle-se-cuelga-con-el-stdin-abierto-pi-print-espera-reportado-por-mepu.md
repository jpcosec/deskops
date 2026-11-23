---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: mepu_ocs_dev
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T22:45:22'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# review preflight/bundle se cuelga con el stdin abierto: pi --print espera (reportado por mepu)

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de mepu (nota 20261114-091248, triaje del 22-11). El 14-11 varias revisiones de mepu (Q15b1, Q15c, Q16) terminaron en technical_failure por «timeout after 900s/1800s» con salida vacía. El mismo argv del manifest, lanzado a mano, responde en 14 s, y deskops review bundle con </dev/null terminó en 28 s. Causa probable: el runner de revisiones lanza pi con el stdin heredado y pi --print queda esperando stdin cuando corre en segundo plano. Sigue así en origin/main (b3ea3d95): deskops/services/review.py línea 592 llama subprocess.run(argv, input=command["stdin"], ...) y, cuando la entrega es por archivo, command["stdin"] es None (línea 272), así que el proceso hereda el stdin. Arreglo pedido: lanzar el revisor con stdin=subprocess.DEVNULL cuando no hay entrada por stdin. Mientras, en mepu se corre con </dev/null.

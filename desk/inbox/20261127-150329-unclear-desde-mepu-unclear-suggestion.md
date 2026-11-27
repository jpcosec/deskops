---
sldb:
  by: agent
  at: '2026-11-27T18:06:12Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-27T15:03:29'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Desde mepu: piloto UI-122 (4) un start fallido consume intento y commitea el RunDoc en dev

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de mepu (triage del 27-11; nota original desk/inbox/20261124-220541-unclear-para-deskops-piloto-ui-122-en-johanes-4-dispatch-start-executor-si.md en heyantonia/mepu). # PARA DESKOPS (piloto UI-122 en johanes): (4) dispatch start executor: si


PARA DESKOPS (piloto UI-122 en johanes): (4) dispatch start executor: si scion start devuelve 0 pero el agente queda en error (broker no disponible, clon fallido), el intento se consume, queda el worktree .worktrees/<name> y la rama deskops/<name>, y ya se commiteó el RunDoc ('run: <name>') en la rama base del checkout principal (dev, compartido y protegido): commit local que diverge de origin. Con dos fallos de infraestructura la tarea queda 'sin intentos' sin haber trabajado; hubo que mover a mano los run_dir. Pedido: comprobar la fase del agente tras scion start y deshacer worktree/RunDoc si no llegó a running, sin gastar intento. (5) Modo pr: reap hace checkout de task/<id> en el checkout principal; en MEPU ese checkout lo comparten varias sesiones sobre dev, así que cambiarle la rama es peligroso. Pedido: traer los commits a task/<id> en un worktree propio, no en el checkout principal.

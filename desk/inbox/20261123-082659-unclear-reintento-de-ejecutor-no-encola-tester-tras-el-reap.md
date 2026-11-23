---
sldb:
  by: agent
  at: '2026-11-23T11:27:57Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-23T08:26:59'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T08:27:48'
# why the note was acknowledged; empty when no reason was given
ack_reason: convertida en task-el-reap-del-intento-n-de-un-ejecutor-encola-el-tester-aunque-la-tarea-ya-este-en-ritual-testing
---

# reintento de ejecutor no encola tester tras el reap

_Describe the incoming message with enough evidence to triage._

Visto 2026-11-23 con closeout-commit-stagea (a2, f629463d) y deskops-init-id (a2, 91626206): tras un FALLA, el coordinador encola dispatch-executor (intento 2); el ejecutor commitea, hace advance y el reap integra el commit, pero no se encola dispatch-tester. Sospecha: la tarea ya estaba en ritual-testing desde el intento 1, así que el advance del intento 2 no dispara la transición que encola el tester. El coordinador lo encola a mano. Además, cuando scion corta un agente por max_duration 2h, el ejecutor queda con cambios sin commitear en el worktree; scion resume lo retoma, pero una vez retomó con la sesión equivocada (49e965aad6ef reportó el trabajo de init-id) y hubo que mandarle un mensaje con su tarea.

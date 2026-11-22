---
sldb:
  by: agent
  at: '2026-11-22T21:38:03Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T18:27:18'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-22T18:37:55'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el;
  entra a la cola de deskops justo después de la tarea en curso (pedido de Governance).
---

# dispatch reap e integrate empujan directo: no sirven en repos con dev protegida ni cumplen la regla de PR

_Describe the incoming message with enough evidence to triage._

Regla de JP del 19-11: todo cambio entra por worktree → PR a dev → QA → main, sin excepción. Hoy el despacho no la cumple: 'dispatch reap' trae los commits del ejecutor a la rama local con 'merge --ff-only' o 'cherry-pick' (deskops/dispatch.py:187-189) e 'integrate' empuja directo al remoto (deskops/integrate.py:360). En deskops y sldb funciona porque main no está protegida; en los repos de heyantonia con dev protegida (Chatbot_Infra, ftcourier, labchile_chatbots) o falla o se salta la regla. Los tres agentes del concilio lo marcaron el 22-11 como lo que impide configurar dispatch en otros desks (acta: heyantonia/Governance, docs/diagnostico-vsm-2026-11-19/concilio/acta-2026-11-22-gobierno-por-desks.md). Pedido: que reap/integrate puedan terminar en un PR a la rama base declarada en vez de un push, y que la rama base por defecto del ejecutor sea la de integración del repo (dev), no main. Mientras no exista, Governance no configura dispatch en los desks de heyantonia.

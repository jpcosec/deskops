---
sldb:
  by: agent
  at: '2026-11-20T02:25:10Z'
  authority: generated
  via: create_document
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-19T23:25:05'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Documento de PR en desk/PRS: un modelo para explicar cada PR a dev

_Describe the incoming message with enough evidence to triage._

Pedido de Governance, del diagnóstico VSM de AntonIA del 2026-11-19 (heyantonia/Governance, docs/diagnostico-vsm-2026-11-19/hallazgos/x-critica-deskops-y-sldb.md). Decisión de JP del 19-11: todo PR de un worktree a dev trae un documento en desk/PRS con qué, cómo, cuándo, dónde y por qué, sin el ritual completo de una tarea; para el trabajo que viene de tareas de deskops, una tarea macro lo explica sola. Pedido: un modelo de documento de PR, un comando que lo cree o lo genere desde la tarea macro, y un check que diga si un PR lo tiene.

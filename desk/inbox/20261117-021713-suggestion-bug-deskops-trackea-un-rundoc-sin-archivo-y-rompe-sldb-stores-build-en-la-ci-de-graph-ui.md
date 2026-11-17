---
sldb:
  by: agent
  at: '2026-11-17T07:06:55Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-17T02:17:13'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-17T04:06:51'
---

# Bug: deskops trackea un RunDoc sin archivo y rompe sldb stores build en la CI de graph_ui

_Describe the incoming message with enough evidence to triage._

Bug que rompe la CI de graph_ui. deskops origin/main (0bc4206a) trackea el RunDoc runs/subagents/exec-deskops-e-289fe7bfa1df/run.md: aparece en .sldb/store.yaml:420 y en .sldb/core/documents/RunDoc/run-deskops-e-289fe7bfa1df.yaml. Lo agregó el commit 9dbcfc7c, closeout de task-deskops-review-node-acepta-ids-de-nodo-con-punto. Ese run.md no está en el repo, porque runs/ no se versiona. Como la CI de graph_ui clona deskops y corre '(cd ../../deskops && sldb stores build)', sale con 'missing: runs/subagents/exec-deskops-e-289fe7bfa1df/run.md' y exit 1 antes de correr ninguna prueba. Los 4 jobs fallan; ejemplo: run 44022701292 sobre graph_ui ca08ae0. En graph_ui nos pasó lo mismo (c3664af) y se arregló con 'sldb docs untrack' del RunDoc (343acd0). Pedido: untrack de ese RunDoc en deskops y push. Después relanzo la CI de graph_ui.

---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T09:50:54'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Respuesta a 20261116-011047: la UI del desk no muestra findings de gates ni recibos; tarea abierta en graph_ui

_Describe the incoming message with enough evidence to triage._

Verificado en el código de graph_ui (master c3664af): deskops view task/board entregan gates[].findings, pero renderGateBoxes de frontends/desk/board.js no los dibuja. graph_ui abrió task-ui-del-desk-cada-gate-muestra-los-findings-de-sus-reglas-nivel-código-y-mensaje-no-solo-cumple-o-pen. Los recibos (ReviewDoc con kind, verdict, anchor_state) no se pueden mostrar porque deskops view task no los entrega: solo aparecen dentro del texto del finding ('seen: {...}'). Si G_GC_RECEIPTS pide verlos en la UI, hace falta un campo en el contrato de deskops view (docs/deskops-ui.md), por ejemplo task.receipts: [{id, kind, verdict, anchor_state, at}]; avisen y graph_ui lo dibuja.

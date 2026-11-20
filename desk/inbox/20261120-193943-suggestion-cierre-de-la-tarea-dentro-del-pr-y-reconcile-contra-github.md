---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-20T19:39:43'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# Cierre de la tarea dentro del PR y reconcile contra GitHub

_Describe the incoming message with enough evidence to triage._

Decisión de JP (20-11): el cierre ocurre dentro del PR que trae el código, no en un commit posterior. Pedido: que el diff del PR pueda marcar la tarea cerrada y CI corra sus compuertas de cierre; y un deskops reconcile que cruce los PR y merges de gh con los documentos de PR y los Task-Id, y avise las tareas abiertas cuyo PR ya se integró. Las tareas cerradas se borran: la historia vive en git y en desk/PRS. Reemplaza la tarea de Governance «el desk se entera de GitHub». Fuente: heyantonia/Governance, rama dev, docs/diagnostico-vsm-2026-11-19/revision-deskops/propuesta-workflow.md, secciones 2 y 3.

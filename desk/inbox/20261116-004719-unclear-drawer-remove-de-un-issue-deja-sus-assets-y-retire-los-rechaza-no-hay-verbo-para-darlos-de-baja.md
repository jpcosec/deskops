---
sldb:
  by: agent
  at: '2026-11-21T06:42:12Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:47:19'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:42:05'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en tarea task-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-entradas-no-md-por-stem-y-registra-reason
  (punto 2: assets de un issue; retire.py:70-74 sigue rechazandolos).'
---

# drawer remove de un issue deja sus assets y retire los rechaza: no hay verbo para darlos de baja

_Describe the incoming message with enough evidence to triage._

Desde graph_ui, triaje 2026-11-16. Di de baja con 'deskops drawer remove' los 24 issues cerrados de desk/drawer/issues/ (G1-G7, R1-R15, RW1). Quedaron 49 capturas trackeadas en desk/drawer/issues/assets/specs-legibility-*/ (png y un REPORTE-r13.md) que ya no cita nadie. 'deskops retire <png> --reason ... --ref ...' responde: 'has its own retirement verb: use deskops issue close (open issues), then deskops retire', pero los issues ya estaban cerrados y ahora no existen. Falta una vía: que drawer remove de un issue lleve sus assets, o que retire acepte los assets huérfanos de un issue que ya no existe. Mientras tanto quedan en el árbol.

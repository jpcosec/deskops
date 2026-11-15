---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-15T19:53:17'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# corrección: sí hay supertareas (task.aggregate)

_Describe the incoming message with enough evidence to triage._

Desde MEPU (2026-11-15), corrige la nota «supertareas y alta en lote»: deskops sí tiene task.aggregate, --depends-on, --inherits-from y --from-yaml (estaba en add task --help y el agente no lo revisó). Lo que queda en pie: que el concepto de supertarea sea visible en status/doctor/board (cómo ver una agregada con sus hijas) y un alta en lote de varias tareas desde un solo YAML.

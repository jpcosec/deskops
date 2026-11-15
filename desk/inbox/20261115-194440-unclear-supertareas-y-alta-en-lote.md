---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-15T19:44:40'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# supertareas y alta en lote

_Describe the incoming message with enough evidence to triage._

Desde MEPU (2026-11-15): falta (o no es visible en `deskops add task --help`) una forma de agrupar tareas en supertareas (tarea madre/épica) y de dar de alta muchas de una vez. Caso: 19 comentarios del dueño desde un marcador de UI → 19 tareas en 9 supertareas; con una llamada lenta por tarea, el agente hizo un índice Markdown a mano en desk/hitl (error del agente, pero la herramienta lo empujó). Pedido: campo parent/supertarea y alta en lote desde un YAML.

---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:30:32'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# La skill y ritual-drawer-triage mandan el inbox al drawer; los atoms dicen que no

_Describe the incoming message with enough evidence to triage._

Contradicción encontrada el 2026-11-16 al preparar el triaje de drawers e inbox. 1) La skill deskops-workflow (.claude/skills/deskops-workflow/SKILL.md) dice: 'Inbox notes move into the drawer with deskops promote inbox-to-drawer-task'. 2) desk/rituals/ritual-drawer-triage.md, en su paso 1, dice que las notas de otros desks llegan al drawer con promote. 3) Pero atom-inbox-is-coordination-intake dice que una nota del inbox es un mensaje al proyecto y no un lugar donde estacionar trabajo diferido, y atom-drawers-feed-tasks-through-promotion dice que el drawer se captura directamente. Además, promote borra la nota y la tarea pierde su origen. Camino que confirmó JP: si la nota es trabajo, add task con references hacia la nota y después message ack; si no, solo ack con la razón. Pedido: alinear la skill, el ritual y la ayuda de promote con los atoms. También decidir si promote inbox-to-drawer-task se retira.

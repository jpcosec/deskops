---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-27T04:23:38'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# desk update --apply no recorre desk/drawer/tasks: _task_files solo mira 

_Describe the incoming message with enough evidence to triage._

desk update --apply no recorre desk/drawer/tasks: _task_files solo mira desk/tasks/*.md, asi que no repara tareas del drawer con status deferred y current_node puesto (33 en la conciliacion del 26-11), aunque legacy_state_migration ya decide ese caso (current_node ''). Ademas edit task no permite current_node. Se arreglaron con desk replace en ed6eba1b8. Pedido: que desk update cubra el drawer.

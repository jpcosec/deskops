---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-26T00:05:34'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# deskops edit task <id> references '[…]' deja vacío el campo tags de la t

_Describe the incoming message with enough evidence to triage._

deskops edit task <id> references '[…]' deja vacío el campo tags de la tarea (antes workspace:desk y artifact:task), y reponerlo con deskops edit task <id> tags '[…]' no hace nada. Visto en MEPU el 25/26-11 en REG-13 (commit 3b53b21bd), LAT-1 y EST-1. Editar un campo no debería tocar otros.

---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T09:46:50'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Editar tags de una tarea deja stale sus recibos preflight y bundle

_Describe the incoming message with enough evidence to triage._

En sldb-ui (robocop2), 'deskops edit task <id> tags [...]' para cambiar host:local por host:robocop2 dejó en stale los 39 recibos preflight y bundle del desk, que antes estaban accepted o technical_failure (comparado con un clon de HEAD en /dev/shm). Motivo: services/review.py _preflight_input y _bundle_input hashean el texto completo del TaskDoc, incluido el sldb.at de procedencia y campos de ruteo como tags, status, current_node e history. Propuesta: que el input de preflight/bundle sea el __contract__ (title, goal, scope, implementation_path, files, validation, done_when) más pills y atoms, sin metadatos de ruteo ni procedencia; así un cambio de host o de fase no obliga a pagar otra revisión. Mientras tanto, re-taggear un desk entero cuesta una ronda completa de preflights.

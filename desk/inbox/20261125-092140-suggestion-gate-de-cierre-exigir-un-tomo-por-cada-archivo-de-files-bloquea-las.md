---
sldb:
  by: agent
  at: '2026-11-25T16:54:04Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-25T09:21:40'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-25T13:53:56'
# why the note was acknowledged; empty when no reason was given
ack_reason: triada en task-el-gate-de-cierre-acepta-el-commit-de-la-tarea...
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Gate de cierre: exigir un átomo por cada archivo de 'files' bloquea las

_Describe the incoming message with enough evidence to triage._

Gate de cierre: exigir un átomo por cada archivo de 'files' bloquea las tareas bien escritas (pedido de JP, 25-11: arreglarlo; el vínculo debería poder ser a un archivo). Dónde: deskops/services/closure.py, missing_changed_file_link (introducido en 5bd2304d1, 31-08, 'closeout verify strict all-of evidence gate'; movido en 93cc1943d CC30). Hoy, para cada ruta de 'files' busca _changed_file_link_evidence en el grafo (un átomo o materialización que la cite) o un follow-up en references; si no, bloquea, y solo cuando el repo tiene átomos locales (if not has_local_atoms: continue). Efecto en MEPU (24/25-11): UI-122, UI-123 y TST-16 quedaron integradas pero sin poder cerrarse justamente por haber completado 'files' para dar contexto al ejecutor; las tareas con files vacío cierran (incentivo perverso: mientras más completa la tarea, menos se puede cerrar). Pedido: que un archivo pueda vincularse directamente (p. ej. el commit de la tarea con trailer Task-Id que toca ese archivo, o la propia lista 'files' + el diff del commit, como evidencia suficiente) y que el átomo sea opcional o se exija por tarea y no por archivo; o que el gate acepte átomos que citen archivos de cualquier tipo (ver PR #12, punto 2). Ver también las notas 1cacbade (suite 6 GB) y 078a310b (skill).

---
sldb:
  by: agent
  at: '2026-11-21T06:41:11Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T07:26:06'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:41:03'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en tarea task-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict-igual-que-edit-task;
  reproducido hoy en un desk temporal (Validation queda con el repr del dict).
---

# add task --from-yaml acepta un dict en validation y edit task lo rechaza

_Describe the incoming message with enough evidence to triage._

Desde IR (2026-11-16). Al crear una tarea con 'deskops add task --from-yaml', si un ítem de la lista validation es un escalar YAML plano con ': ' dentro (por ejemplo '- Suite completa una vez, bajo flock /dev/shm/x.lock: CMD ...'), YAML lo parsea como un dict. add task no lo rechaza: lo guarda como el repr de Python "{'Suite ...': 'CMD ...'}" y la tarea pasa preflight y bundle así. En cambio, 'deskops edit task <t> validation <lista>' rechaza la misma lista con pydantic 'validation.5 Input should be a valid string'. Casos en IR: task-ir13e-… (ya corregido con edit task) y task-quitar-el-xfail-obsoleto-de-label-key-… (línea 64, se deja así porque ya está en ejecución). Propuesta: que add task --from-yaml valide los ítems de lista como string igual que edit task, y que falle con un mensaje que sugiera entrecomillar el ítem.

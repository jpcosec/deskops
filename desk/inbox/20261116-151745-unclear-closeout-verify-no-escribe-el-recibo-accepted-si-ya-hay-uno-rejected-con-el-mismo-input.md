---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T15:17:45'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout verify no escribe el recibo accepted si ya hay uno rejected con el mismo input

_Describe the incoming message with enough evidence to triage._

En sldb-ui, task-ui-rebase-sldb-actual: el primer closeout verify (con el gate en rojo por otros motivos) escribió evidence-atom-1 con verdict rejected e input_sha256 d01a504f..., calculado sobre los 4 atoms de la tarea. Una vez en verde, el verify calcula el mismo input para atom (accepted, los mismos 4 atoms), y _write_evidence_receipts lo salta porque ya existe un recibo intacto con ese input, sin mirar el verdict. closeout commit queda bloqueado por rule-closeout-task-code (seen: {}). Destrabé la tarea bindeando un atom pertinente (atom-why-json-output-from-cli), que cambia el input. Propuesta: el dedup de closure.py:1050 debería exigir también el mismo verdict.

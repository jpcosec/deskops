---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T14:18:53'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout commit amienda el HEAD cuando trae el mismo Task-Id (closure.py

_Describe the incoming message with enough evidence to triage._

closeout commit amienda el HEAD cuando trae el mismo Task-Id (closure.py: head_task_id == task_id), pero closeout verify ya grabo ese sha en el recibo evidence-commit; tras el amend el recibo cita un commit inalcanzable. Caso: task-puente-de-pytest, verify cito 9f7d4f13 y el closeout lo amendo a 3f613469. Propuesta: que commit refresque el recibo con el sha final, o que no amende un commit citado como evidencia.

---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-25T15:35:01'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# closeout commit mete archivos ajenos al commit (MEPU, 25-11): al cerrar 

_Describe the incoming message with enough evidence to triage._

closeout commit mete archivos ajenos al commit (MEPU, 25-11): al cerrar UI-122 (commit fb7bc72e9 en heyantonia/mepu dev) agregó por su cuenta una línea de tag (workspace:desk) en 7 ReviewDoc de otras tareas (alm-1, hom-22) que otra sesión tenía sin commitear. En un checkout compartido, closeout commit debería stagear solo los archivos de la tarea que cierra (o los que se pasan en --paths) y no reescribir ni incluir documentos ajenos. Relacionado: en MEPU la evidencia de tests sigue sin aceptar vitest (.test.tsx) salvo con un recibo del tester; UI-127/129/132 quedan en closeout por missing_tests_evidence aunque references cita frontend/src/pendientes/PendientesView.test.tsx.

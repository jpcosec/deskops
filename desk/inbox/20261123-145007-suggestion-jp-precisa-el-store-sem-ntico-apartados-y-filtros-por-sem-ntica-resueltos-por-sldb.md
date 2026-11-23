---
sldb:
  by: agent
  at: '2026-11-23T17:52:13Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-23T14:50:07'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T14:52:04'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'aplicada: la tarea task-un-solo-vocabulario-de-tags-semanticos-en-deskops-padres-declarados-en-sldb-add-sin-duplicados-y-mig
  se ajusto a este criterio de aceptacion (goal, done_when, scope); el ejecutor que
  corria con el criterio anterior se detuvo y se redespacha tras nuevas revisiones'
# conversation thread/message the note came from, e.g. #hilo/1234
---

# JP precisa el store semántico: apartados y filtros por semántica resueltos por sldb

_Describe the incoming message with enough evidence to triage._

Corrige y precisa la nota 20261123-142641 con las palabras de JP (2026-11-23): 'Necesito probar que funcione. La idea es que si dejo un apartado que dice board.tareas pueda listar todas las tareas. Si filtro por tareas de UI puedan salir las de la UI y así; hoy en día no está funcionando (y es porque deskops implementó un sistema que no usaba sldb)'. Es decir, el problema de fondo no es solo de vocabulario: los tags de deskops (workspace:desk, artifact:task, topic:*) son un sistema propio que no pasa por el store semántico de sldb. Evidencia: en el store de deskops, sldb semantic show workspace:desk devuelve sin padres, hijos ni equivalentes, y sldb semantic show type.workflow.task devuelve below vacío. Criterio de aceptación de JP, demostrable sobre el desk real y desde el lector de surface: (1) un apartado declarado con una semántica (el ejemplo de JP: board.tareas) lista todas las tareas; (2) filtrar por una semántica más específica (tareas de UI) devuelve solo esas; (3) ambas consultas se resuelven con el store semántico de sldb (tags, padres, descendientes), sin listas ni filtros propios de deskops. Regla del workspace: deskops es configuración sobre sldb y nunca reimplementa lo que sldb tiene; si a sldb le falta una operación (consulta por tag con descendientes, migración de tags en bloque), va como nota a sldb. La tarea de tags semánticos ya revisada debe ajustarse a este criterio antes de despacharse.

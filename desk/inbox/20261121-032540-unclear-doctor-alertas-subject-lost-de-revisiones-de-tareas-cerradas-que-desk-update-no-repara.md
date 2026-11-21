---
sldb:
  by: agent
  at: '2026-11-21T06:29:32Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-21T03:25:40'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:29:26'
# why the note was acknowledged; empty when no reason was given
ack_reason: Cubierta por la tarea task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
  (ya existia, de la nota de ftcourier 20261114-022915); se le agrego al goal/done_when
  el backfill de los recibos lost existentes y que la alerta deje de sugerir desk
  update --apply, y la referencia a esta nota. El .gitattributes de 41614491 es del
  repo IR, nada que hacer en deskops.
---

# doctor: alertas 'subject lost' de revisiones de tareas cerradas que desk update no repara

_Describe the incoming message with enough evidence to triage._

Sesión local de JP, 2026-11-20. En el desk de IR, deskops status (alias deprecado de doctor) reporta ~107 alertas en el checkout local y 254 en robocop2, casi todas 'ReviewDoc ... subject -> TaskCodeDoc ...: lost': son revisiones de tareas ya cerradas. El mensaje dice que se registran con deskops desk update --apply, pero deskops desk update responde 'Desk is up to date' y no repara nada. Falta decidir qué pasa con la revisión de una tarea cerrada (que el closeout reancle o archive sus ReviewDoc, o que doctor no las cuente) y que el mensaje apunte a un comando que sí lo resuelva. Aparte: 41614491 agregó .gitattributes (merge driver de sldb) a este repo, instalado a mano.

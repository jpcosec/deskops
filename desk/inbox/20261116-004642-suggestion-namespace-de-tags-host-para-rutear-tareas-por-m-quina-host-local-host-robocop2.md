---
sldb:
  by: agent
  at: '2026-11-21T06:42:50Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: marcado
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:46:42'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:42:44'
# why the note was acknowledged; empty when no reason was given
ack_reason: Cubierta por la tarea existente task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea
  (referencia agregada).
---

# Namespace de tags host para rutear tareas por máquina (host:local, host:robocop2)

_Describe the incoming message with enough evidence to triage._

De: coordinador de UIs/marcado, triaje 2026-11-16. JP pidió rutear las tareas por máquina vía TaskDoc.tags: lo que tiene UI va a la local y el resto a robocop2. Ningún store declara hoy un namespace 'host'; marcado declara concept, constraint, domain, layer, namespace, role, specpart, system y topic. Propuesta: declarar en la semilla de tag_namespaces de deskops un namespace 'host' no jerárquico con host:local y host:robocop2, para que deskops desk update --apply lo propague. Mientras tanto, la tarea de marcado quedó con host:local, y deskops edit task lo aceptó sin el namespace declarado: es otro hueco, porque no valida el namespace.

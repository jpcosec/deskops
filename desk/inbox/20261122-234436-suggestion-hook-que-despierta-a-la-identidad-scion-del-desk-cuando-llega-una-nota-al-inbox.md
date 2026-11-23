---
sldb:
  by: agent
  at: '2026-11-23T04:41:50Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T23:44:36'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T01:41:42'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en tarea task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf
  (hook por nota con identity.wake en config.local.json y gate de memoria). También
  quedó en las references del paraguas task-governance-agente-interno-por-desk-en-scion-activado-por-hooks-de-deskops.
  El uso real espera el arreglo de --wake en el fork de scion (nota 20261122-233912
  del desk de scion).
---

# Hook que despierta a la identidad scion del desk cuando llega una nota al inbox

_Describe the incoming message with enough evidence to triage._

Pedido: al quedar una nota nueva en desk/inbox (deskops message send, o al procesar la cola), deskops ejecuta un comando configurable por desk, por defecto: scion message --wake @desk-<repo> --project <proyecto scion> 'nota nueva: <tracked_name>'. Config propuesta en desk/config.local.json (es de la maquina): identity.scion_project, identity.agent, identity.wake (true/false). Debe respetar el gate de RAM del despacho (available >= 8 G, presion avg60 < 10, 5 agentes vivos) y, si no pasa, dejar la nota sin despertar y reintentar en el siguiente ciclo de la cola. Depende del arreglo de resume/wake en el fork de scion (nota 20261122-233912 en el desk de scion): hoy --wake falla. JP: 'uno por desk, pero en scion y se activa por hook en deskops', y la identidad se prende y se apaga, queda parada por defecto. Referencia, no duplicar: task-governance-agente-interno-por-desk-en-scion-activado-por-hooks-de-deskops. Origen: scion-coordination (encargo de JP, workflow scion + deskops), estado en ~/coordinacion/estado-scion-coordination.md; piloto en /mnt/ssd/proyectos/wf-desks. Enviada con sender deskops porque el desk de workflow no esta registrado.

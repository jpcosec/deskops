---
sldb:
  by: agent
  at: '2026-11-23T04:42:22Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T23:45:09'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T01:42:14'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en tarea task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar,
  con depends_on task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale:
  no corre antes de que las plantillas deskops-executor/tester declaren sus propios
  volumes. Quitar el montaje global de settings.yaml es decisión de JP y lo hace scion-coordination
  en ventana.'
---

# Seguridad: todo agente claude del broker recibe SLDB_1 y /dev/shm en escritura, sea del proyecto que sea

_Describe the incoming message with enough evidence to triage._

Medido el 2026-11-23 con agentes de los proyectos scion wf-spike, wf-spike-plain y wf-desks: docker inspect muestra /mnt/ssd/proyectos/SLDB_1 y /dev/shm montados rw, memoria 6 Gi y red del host, aunque se pase otro --config con menos recursos. Viene de profiles.local.harness_overrides.claude en ~/.scion/settings.yaml (piloto IR). Efecto: un agente de cualquier otro proyecto (mepu, ftcourier, un desk de heyantonia) puede escribir en deskops y sldb. Governance lo marca como bloqueante para usar scion con los desks de heyantonia. Pedido: que los volumes, la imagen y los recursos salgan de la config por desk o por plantilla (lo que ya pide la tarea runtime-template: image, resources y volumes de scion en config; no duplicar) y que al cerrarla se quite el montaje global de settings.yaml; el retiro y el reinicio del server los hace scion-coordination en ventana. El piloto wf-desks depende hoy de ese montaje para llegar a los desks: al quitarlo necesita declarar sus propios volumes. Origen: scion-coordination (encargo de JP, workflow scion + deskops), estado en ~/coordinacion/estado-scion-coordination.md; piloto en /mnt/ssd/proyectos/wf-desks. Enviada con sender deskops porque el desk de workflow no esta registrado.

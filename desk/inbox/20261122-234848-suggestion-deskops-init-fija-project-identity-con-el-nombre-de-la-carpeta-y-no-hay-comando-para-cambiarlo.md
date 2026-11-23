---
sldb:
  by: agent
  at: '2026-11-23T04:42:54Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: wf-desks
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T23:48:48'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T01:42:46'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en tarea task-deskops-init-id-fija-project-identity-deskops-repo-whoami-set-la-cambia-por-cli-y-repo-register-avis
  (init --id, repo whoami --set y aviso en repo register), compartida con la nota
  20261122-222005 de labchile_chatbots.
---

# deskops init fija project_identity con el nombre de la carpeta y no hay comando para cambiarlo

_Describe the incoming message with enough evidence to triage._

Caso: 'deskops init /mnt/ssd/proyectos/wf-desks' dejo project_identity 'wf-desks' en desk/config.json; despues 'deskops repo register workflow <ruta> --id workflow' registro el repo como 'workflow'. 'deskops repo whoami' en ese desk responde 'wf-desks', distinto del id registrado. desk/ no se edita a mano, y no encontre un comando para fijar project_identity. Pedido: 'deskops init --id <identidad>' o que 'repo register' alinee project_identity con --id (o avise de la diferencia). Origen: desk de workflow (scion-coordination), 2026-11-23.

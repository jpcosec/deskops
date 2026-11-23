---
sldb:
  by: agent
  at: '2026-11-23T04:42:00Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T23:44:47'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T01:41:53'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en tarea task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa
  (RoleDoc empaquetado, instalación por desk update --apply y runtime template --mode
  identity), que depende de task-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-el-alias-de-modelo-sale.
  También en las references de task-governance-agente-interno-por-desk-en-scion-activado-por-hooks-de-deskops.
---

# RoleDoc de identidad de desk (desk-identity) y su traduccion a agente scion

_Describe the incoming message with enough evidence to triage._

Hoy no hay RoleDoc para la identidad de un desk: deskops tiene executor, supervisor y tester; sldb no tiene desk/roles. El piloto usa las reglas de /mnt/ssd/proyectos/wf-desks/bin/desk-prompt.sh pegadas delante de deskops-supervisor.md. Pedido: un RoleDoc desk-identity (triar el inbox propio, reenviar lo ajeno por inbox, registrar acuerdos de un hilo como atom con la referencia, mandar lo sin dueno a su destino, dejar abierto lo que pide decision de JP, no implementar codigo ni despachar), instalable en cualquier desk, y que runtime-profile lo materialice como agente scion persistente en un proyecto de carpeta sin git con workspace relativo (unico modo que admite reincarnate; el modo worktree por agente no lo admite). Texto base vigente, autorizado por Governance: /srv/wt/labchile_chatbots/.encargo-triaje-inbox.txt y /srv/wt/shared_llm-gateway/.encargo-triaje-inbox.txt. Referencias, no duplicar: las tareas runtime-profile (tools del RoleDoc a Claude) y runtime-template (image, resources y volumes en config). Origen: scion-coordination (encargo de JP, workflow scion + deskops), estado en ~/coordinacion/estado-scion-coordination.md; piloto en /mnt/ssd/proyectos/wf-desks. Enviada con sender deskops porque el desk de workflow no esta registrado.

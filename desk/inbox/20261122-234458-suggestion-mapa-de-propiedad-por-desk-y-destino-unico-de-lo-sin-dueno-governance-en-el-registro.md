---
sldb:
  by: agent
  at: '2026-11-23T04:42:11Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T23:44:58'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T01:42:03'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en tarea task-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-deskops-owner-responde-el-dueno-de-un
  (owns_paths/owns_topics, deskops owner, unowned_target y --to unowned). Fuera de
  la tarea: registrar Governance con deskops repo register y fijar el valor de unowned_target,
  que confirma JP; el atom provisional atom-sin-dueno-lo-que-no-tiene-dueno-en-sldb-1-va-al-inbox-de-deskops
  queda referenciado.'
---

# Mapa de propiedad por desk y destino unico de lo sin dueno (Governance en el registro)

_Describe the incoming message with enough evidence to triage._

Falta donde declarar que rutas y temas son de cada desk, y a donde va lo que no es de nadie. Pedido: (1) en la ficha de desk/registry/repo-<x>.md, campos owns_paths y owns_topics, y un comando deskops owner <ruta|tema> que responda el repo dueno o 'sin dueno'; (2) una clave de config unowned_target (repo registrado) que deskops message send use con --to unowned; (3) registrar Governance (project_identity repo-governance, heyantonia/Governance) en el registro para poder enviarle. Acuerdo provisional ya registrado por el piloto: atom-sin-dueno-lo-que-no-tiene-dueno-en-sldb-1-va-al-inbox-de-deskops (hasta que Governance este registrado; JP no lo ha confirmado). Caso de prueba real: heyantonia/mepu#459, dos notas que eran de etlkit (shared_etl-plataforma) y quedaron en tareas de mepu. Origen: scion-coordination (encargo de JP, workflow scion + deskops), estado en ~/coordinacion/estado-scion-coordination.md; piloto en /mnt/ssd/proyectos/wf-desks. Enviada con sender deskops porque el desk de workflow no esta registrado.

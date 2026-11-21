---
sldb:
  by: agent
  at: '2026-11-21T15:11:22Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-21T04:03:58'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T12:11:15'
# why the note was acknowledged; empty when no reason was given
ack_reason: Convertida en tarea borrador task-governance-puesta-al-dia-de-los-clones-base-de-la-maquina-coordinadora-y-doctor-que-valida-cada-tare.
---

# Clones base de una máquina coordinadora y doctor que valide cada tarea

_Describe the incoming message with enough evidence to triage._

robocop 1 es desde el 20-11 el coordinador de robocop 2 y el maestro de los desks: tiene clones base de los repos gobernados en /srv/repos y su catálogo ~/.sldb los conoce por nombre. Hoy esos clones se ponen al día con 'git pull' a mano, repo por repo, y no hay 'wt' instalado. Pedido 1: un comando de deskops (o un rito programado) que recorra los repos del registro, los ponga al día en su rama base, actualice el catálogo e informe los que no pudo avanzar; y que el flujo de worktrees funcione igual en esa máquina que en un laptop. Pedido 2: una migración de ciclo de vida dejó cinco tareas inválidas en shared_llm-gateway (status superseded o deferred con history vacío, o draft con historia de closeout) y 'deskops doctor' decía 'Desk is healthy'. doctor debería validar cada tarea contra su modelo: una sola inválida bota 'sldb find --global' en todos los desks que enlazan ese store. Se cerraron con closeout supersede, retire y resolved-by en heyantonia/shared_llm-gateway#40.

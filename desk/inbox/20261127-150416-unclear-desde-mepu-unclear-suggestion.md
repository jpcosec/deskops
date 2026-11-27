---
sldb:
  by: agent
  at: '2026-11-27T18:06:27Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-27T15:04:16'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Desde mepu: piloto UI-122 (10) reap en modo pr cambia la rama del checkout compartido; el gate de átomos no enlaza archivos no Python

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de mepu (triage del 27-11; nota original desk/inbox/20261124-222637-unclear-para-deskops-piloto-ui-122-en-johanes-10-choque-visto-en-vivo-disp.md en heyantonia/mepu). # PARA DESKOPS (piloto UI-122 en johanes): (10) Choque visto en vivo: disp


PARA DESKOPS (piloto UI-122 en johanes): (10) Choque visto en vivo: dispatch reap en modo pr hizo checkout de task/<id> en el checkout principal de MEPU, que comparten otras sesiones (UI-125, ALM-1) para sus commits del desk; esos commits habrían caído en la rama del PR. Hubo que volver a dev a mano antes del closeout. El modo pr no debería tomar el checkout principal: debería trabajar en un worktree propio de task/<id>. (11) closeout verify de una tarea de UI: el gate atom|materialization exige un enlace de átomo o de materialización para cada archivo cambiado (frontend/src/..., src/frontend/v2). Citar el átomo en atoms/references, o crear uno nuevo con provenance y las rutas en el answer, no basta, y el closeout commit queda bloqueado. Ni el manual ni el error dicen qué forma de enlace acepta para archivos que no son de Python (tampoco qué es una 'routed follow-up reference').

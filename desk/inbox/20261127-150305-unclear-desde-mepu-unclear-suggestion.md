---
sldb:
  by: agent
  at: '2026-11-27T18:06:05Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-27T15:03:05'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Desde mepu: piloto UI-122 (1) DeskConfig exige campos de máquina, queue job set y --max-attempts 2 silencioso

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de mepu (triage del 27-11; nota original desk/inbox/20261124-220515-unclear-para-deskops-piloto-despacho-ui-en-johanes-mepu-ui-122-1-dispatchc.md en heyantonia/mepu). # PARA DESKOPS (piloto despacho UI en johanes, MEPU UI-122): (1) DispatchC


PARA DESKOPS (piloto despacho UI en johanes, MEPU UI-122): (1) DispatchConfig exige project/workspace/templates_dir/context_file e IntegrateConfig exige remote_url; si config.json versiona solo lo común (roles, roles_root, quick_gates, mode, branch, suite) como pide el manual, DeskConfig.load falla con ValidationError en todo checkout sin config.local.json (worktrees, robocop2, CI) y rompe todos los comandos de deskops. En MEPU quedó dispatch entero en config.local.json. Pedido: validar los campos de máquina solo al usar dispatch/integrate. (2) queue job set solo edita kinds ya declarados; para crear dispatch-*/integrate hay que editar el JSON (el manual no lo dice). (3) review preflight con --max-attempts 2 por defecto no corre la 3a revisión tras corregir la tarea y no avisa nada (sale 0 sin salida); hubo que pasar --max-attempts 4.

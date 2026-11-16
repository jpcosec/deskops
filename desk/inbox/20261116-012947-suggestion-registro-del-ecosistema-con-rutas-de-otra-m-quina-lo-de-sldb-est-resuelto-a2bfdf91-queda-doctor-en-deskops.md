---
sldb:
  by: agent
  at: '2026-11-16T06:11:34Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T01:29:47'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T03:11:28'
---

# Registro del ecosistema con rutas de otra máquina: lo de sldb está resuelto (a2bfdf91); queda doctor en deskops

_Describe the incoming message with enough evidence to triage._

Triaje del inbox de sldb (2026-11-16), nota de mepu 'El registro del ecosistema guarda rutas absolutas de una máquina'. Lo de sldb está resuelto en a2bfdf91: desk/registry/*.md de sldb usa rutas relativas (path: ., ../deskops, ../UIs/graph_ui...). Lo que queda es de deskops: (1) que deskops doctor nombre como hallazgo del registro una entrada cuyo path no resuelve en esta máquina, en lugar de solo 'the linked store is missing'; (2) que deskops repo register guarde la ruta relativa a la raíz del ecosistema y no la absoluta de la máquina que registra (hoy registrar desde robocop guarda /mnt/ssd/..., que se rompe en la laptop). La nota se cierra en el inbox de sldb.

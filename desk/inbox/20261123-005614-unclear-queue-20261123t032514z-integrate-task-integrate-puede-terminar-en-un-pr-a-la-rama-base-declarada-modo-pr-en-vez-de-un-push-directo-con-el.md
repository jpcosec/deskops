---
sldb:
  by: agent
  at: '2026-11-23T04:41:22Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-23T00:56:14'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T01:41:14'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Causa del intento 20261123T032514Z: 6 ENOSPC en tests/test_view*.py porque
  /dev/shm estaba al 99 % (13 GB de basetemps pytest-of-robocop de integrates anteriores);
  la prevención va en task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas.
  resuelto: integrate ok a7694665 en el intento 20261123T035659Z (código ca7ecfc5,
  closeout 63618d69, en origin/main).'
---

# queue: 20261123T032514Z-integrate-task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el

_Describe the incoming message with enough evidence to triage._

Tipo: integrate. Tarea: task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el. Codigo de salida: 1. Log: /mnt/ssd/proyectos/SLDB_1/deskops/runs/queue/logs/20261123T032514Z-integrate-task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el.log

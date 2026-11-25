---
sldb:
  by: agent
  at: '2026-11-25T16:53:41Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-25T01:49:36'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-25T13:53:34'
# why the note was acknowledged; empty when no reason was given
ack_reason: triada en task-la-suite-de-deskops-baja-su-ram-por-worker...
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Suite de deskops: ~6 GB de RAM con -n 4. El 25-11 ~01:00 en johanes (16

_Describe the incoming message with enough evidence to triage._

Suite de deskops: ~6 GB de RAM con -n 4. El 25-11 ~01:00 en johanes (16 GB), un agente de la sesión de MEPU corrió 'python -m pytest -q -n 4 -rf -p no:cacheprovider tests' en este repo (por error: no debía editar deskops; ver PR #12). Los 4 workers de xdist llegaron a 2,4 + 1,8 + 1,5 + 0,4 GB de RSS (~6 GB), duró ~33 min y llenó el swap (4/4 GB). Pedido: medir qué tests o fixtures crecen así (p. ej. pytest-memray o RSS por test con un plugin, stores de sldb cargados enteros, cachés de módulo o fixtures de sesión que no se liberan, subprocesos que no terminan) y bajarlo; y decidir en qué máquina corre la suite (¿robocop2?) y con cuántos workers (queue_min_available_gb / CI_WORKERS).

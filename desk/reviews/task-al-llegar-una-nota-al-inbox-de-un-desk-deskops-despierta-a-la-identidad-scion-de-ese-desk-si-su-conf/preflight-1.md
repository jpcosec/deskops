---
sldb:
  by: agent
  at: '2026-11-23T05:04:49Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf@sha256:476ce6448fa4f1656d4fba86818556da3310c53979f4601dcee93f0fbf972028
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261123-044929/context-review/task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf/preflight/ced53671ef0972f08d7de5590097f2eb2fedf4718f561f2b5bb75d364f501ad2/attempt-1
input_sha256: ced53671ef0972f08d7de5590097f2eb2fedf4718f561f2b5bb75d364f501ad2
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: a4116e615da1fa5e21372c62c86673bd700067909c17879646ad9f7294684ba2
output_sha256: 327f699d65aaa9b350a2f4a948c31473ae640c2ee34a880793e622ec092dd087
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones de la preflight:

  1) Modulo nuevo: deskops/identity_wake.py (no deskops/identity.py, que ya existe
  y resuelve project_identity), con wake_identity(root, note_name). El modelo IdentityConfig
  (scion_project, agent, wake=False, command con el default del Goal) va en deskops/config.py
  y DeskConfig gana identity: IdentityConfig | None = None; asi no hay import circular
  (identity_wake importa deskops.queue, que importa deskops.config).

  2) Goldens: tests/fixtures/golden/help/deskops_message.txt (cambia el epilog/lista
  de subcomandos) y uno nuevo deskops_message_wake.txt, generados por test_help_goldens
  con --update-golden (comando exacto en la base comun). El subcomando se declara
  en deskops/cli/registry.py como Command(path=("message", "wake"), ...) con --note
  y los args de destino de message; el despacho va en MessageCLI._run_message_command.
  registry.py entra en el alcance aunque no este en files.

  3) Esquema de queue_jobs: dict nombre -> QueueJob {run: [argv], timeout, retry_exit_codes}.
  Para los tests el desk temporal declara en su desk/config.json: "queue_jobs": {"wake-identity":
  {"run": ["deskops", "message", "wake", "--root", "."], "retry_exit_codes": [3]}}.
  La tarea no edita el desk/config.json real de deskops.

  4) Sustitucion: por cada elemento del argv, str.replace de "{agent}", "{project}"
  y "{note}" (no str.format: textos con otras llaves no deben romper). {note} es el
  stem del archivo de la nota (nombre sin .md, el selector que acepta message read);
  en message wake sin --note se reemplaza por cadena vacia.

  5) wait_reason(config) recibe el DeskConfig.load(<repo destino>/desk) y su motivo
  es el texto que devuelve (ver base comun); wake_identity devuelve "bloqueado: "
  + ese texto.

  6) retry_exit_codes [3] no se configura en el desk real: lo declara quien quiera
  el reintento (en los tests, el config temporal del punto 3). message wake solo garantiza
  rc 3 al bloquear.

  Gate en tests: los tests corren el CLI en subproceso (_cli de tests/test_message_delivery.py
  linea 28), asi que "wait_reason parcheado" se logra con el config: bloqueado = "queue_min_available_gb":
  1000000 en config.local.json del desk temporal; no bloqueado = "queue_min_available_gb":
  0 y "queue_max_psi_avg60": 1000.

  Commit desde el worktree que dispatch le da al ejecutor, con git commit -- <rutas>
  y el trailer en el cuerpo:

  Task-Id: task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf


  Base comun: Hechos verificados (HEAD 40964f50): DeskConfig.load(desk_root) en deskops/config.py
  linea 106 mezcla config.json y luego config.local.json (deep merge). QueueJob (config.py
  linea 25): run list[str] (argv sin shell), timeout int=3600, retry_exit_codes list[int];
  DeskConfig.queue_jobs dict[str, QueueJob] (linea 85); queue_min_available_gb int=8
  (linea 97) y queue_max_psi_avg60 float=10 (linea 98). deskops/queue.py: enqueue(root,
  kind, task_id, transition) linea 55 lee root/desk/config.json (root = raiz del repo,
  no desk/), exige kind declarado en queue_jobs y task_id no vacio; wait_reason(config:
  DeskConfig) -> str|None linea 119 devuelve el motivo (memoria disponible < minimo,
  o PSI avg60 >= maximo) o None; _execute (linea 176) deja pendiente un trabajo cuyo
  rc esta en retry_exit_codes. deskops/cli/commands/message.py: _deliver_note linea
  72; _resolve_target devuelve desk_root = <repo>/desk; en message --root es la raiz
  del repo (ROOT_ARG_MESSAGE, deskops/cli/registry.py linea 105). Los subcomandos
  de message se declaran en deskops/cli/registry.py (Command path ("message", "send")
  linea 651, ("message", "ack") linea 694). Goldens de ayuda: tests/fixtures/golden/help/*.txt
  (deskops_message.txt, deskops_message_ack.txt, ...), se regeneran con TMPDIR=/dev/shm
  ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
  --update-golden y se revisa el diff. Ya existe deskops/identity.py (identidad de
  proyecto, otra cosa).'
# ISO 8601 timestamp
created_at: '2026-11-23T04:49:41.605757+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:04:41.148266+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-044929/context-review/task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf/preflight/ced53671ef0972f08d7de5590097f2eb2fedf4718f561f2b5bb75d364f501ad2/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones de la preflight:
1) Modulo nuevo: deskops/identity_wake.py (no deskops/identity.py, que ya existe y resuelve project_identity), con wake_identity(root, note_name). El modelo IdentityConfig (scion_project, agent, wake=False, command con el default del Goal) va en deskops/config.py y DeskConfig gana identity: IdentityConfig | None = None; asi no hay import circular (identity_wake importa deskops.queue, que importa deskops.config).
2) Goldens: tests/fixtures/golden/help/deskops_message.txt (cambia el epilog/lista de subcomandos) y uno nuevo deskops_message_wake.txt, generados por test_help_goldens con --update-golden (comando exacto en la base comun). El subcomando se declara en deskops/cli/registry.py como Command(path=("message", "wake"), ...) con --note y los args de destino de message; el despacho va en MessageCLI._run_message_command. registry.py entra en el alcance aunque no este en files.
3) Esquema de queue_jobs: dict nombre -> QueueJob {run: [argv], timeout, retry_exit_codes}. Para los tests el desk temporal declara en su desk/config.json: "queue_jobs": {"wake-identity": {"run": ["deskops", "message", "wake", "--root", "."], "retry_exit_codes": [3]}}. La tarea no edita el desk/config.json real de deskops.
4) Sustitucion: por cada elemento del argv, str.replace de "{agent}", "{project}" y "{note}" (no str.format: textos con otras llaves no deben romper). {note} es el stem del archivo de la nota (nombre sin .md, el selector que acepta message read); en message wake sin --note se reemplaza por cadena vacia.
5) wait_reason(config) recibe el DeskConfig.load(<repo destino>/desk) y su motivo es el texto que devuelve (ver base comun); wake_identity devuelve "bloqueado: " + ese texto.
6) retry_exit_codes [3] no se configura en el desk real: lo declara quien quiera el reintento (en los tests, el config temporal del punto 3). message wake solo garantiza rc 3 al bloquear.
Gate en tests: los tests corren el CLI en subproceso (_cli de tests/test_message_delivery.py linea 28), asi que "wait_reason parcheado" se logra con el config: bloqueado = "queue_min_available_gb": 1000000 en config.local.json del desk temporal; no bloqueado = "queue_min_available_gb": 0 y "queue_max_psi_avg60": 1000.
Commit desde el worktree que dispatch le da al ejecutor, con git commit -- <rutas> y el trailer en el cuerpo:
Task-Id: task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf

Base comun: Hechos verificados (HEAD 40964f50): DeskConfig.load(desk_root) en deskops/config.py linea 106 mezcla config.json y luego config.local.json (deep merge). QueueJob (config.py linea 25): run list[str] (argv sin shell), timeout int=3600, retry_exit_codes list[int]; DeskConfig.queue_jobs dict[str, QueueJob] (linea 85); queue_min_available_gb int=8 (linea 97) y queue_max_psi_avg60 float=10 (linea 98). deskops/queue.py: enqueue(root, kind, task_id, transition) linea 55 lee root/desk/config.json (root = raiz del repo, no desk/), exige kind declarado en queue_jobs y task_id no vacio; wait_reason(config: DeskConfig) -> str|None linea 119 devuelve el motivo (memoria disponible < minimo, o PSI avg60 >= maximo) o None; _execute (linea 176) deja pendiente un trabajo cuyo rc esta en retry_exit_codes. deskops/cli/commands/message.py: _deliver_note linea 72; _resolve_target devuelve desk_root = <repo>/desk; en message --root es la raiz del repo (ROOT_ARG_MESSAGE, deskops/cli/registry.py linea 105). Los subcomandos de message se declaran en deskops/cli/registry.py (Command path ("message", "send") linea 651, ("message", "ack") linea 694). Goldens de ayuda: tests/fixtures/golden/help/*.txt (deskops_message.txt, deskops_message_ack.txt, ...), se regeneran con TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py --update-golden y se revisa el diff. Ya existe deskops/identity.py (identidad de proyecto, otra cosa).

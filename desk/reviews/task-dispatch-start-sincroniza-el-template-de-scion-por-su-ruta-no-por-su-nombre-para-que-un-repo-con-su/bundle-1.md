---
sldb:
  by: agent
  at: '2026-11-23T19:19:50Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta-no-por-su-nombre-para-que-un-repo-con-su-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta-no-por-su-nombre-para-que-un-repo-con-su@sha256:beb228065e1c670f064bbf7a1c0dda84fd430b1d5abf2871d1f6af86570ff612
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261120-192319/context-review/task-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta-no-por-su-nombre-para-que-un-repo-con-su/bundle/7403b809f4edf70cd87737368bc1fa11347a455f0eaeda17ca11eaf6d4172605/attempt-1
input_sha256: 7403b809f4edf70cd87737368bc1fa11347a455f0eaeda17ca11eaf6d4172605
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: f47ddc36eb375d0e1534d9dbb2daaf10bf2db4faf26d8c2cbf83188fcc09942f
output_sha256: f9939ff0d83f8ab8a80625e3b22adbb26fc9587f60974a25afad6ba12d79dc80
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador. 1) y bundle 3) El punto es la llamada
  ''_scion(["scion", "templates", "sync", role_name, "--project", cfg.project])''
  de start en deskops/dispatch.py, justo después de materialize_scion_template; target
  es ''Path(cfg.templates_dir).expanduser() / role_name'', unas líneas antes. No hay
  otra llamada a sync. 2), 3) y bundle 1) y 4) Contrato verificado por el coordinador
  con scion v0.2.21: ''scion templates sync --help'' dice ''The template may also
  be given as a directory path: ... an absolute path ... The directory is synced as
  is, and the Hub name defaults to its base name''. Sync sube el template al hub del
  proyecto (--project sldb-1). ''scion start -t <nombre> --project sldb-1'' lo toma
  del hub del proyecto, no del grove local, así que start no cambia. Solo se cambia
  el sync, que pasa a recibir str(target). Si al relanzar el dispatch de IR start
  fallara igual, el integrador lo informa en una tarea nueva; no es parte de esta.
  ''Se informa'' significa en result-summary.md del ejecutor. 4) y bundle 2) _scion
  está en deskops/dispatch.py:30 (''The only place that runs scion''). El test usa
  monkeypatch.setattr(dispatch, ''_scion'', fake), con fake que guarda los argv y
  devuelve subprocess.CompletedProcess(argv, 0, '''', ''''), como los tests de tests/test_dispatch.py.
  El test arma un root temporal con .scion/settings.yaml y verifica que el argv del
  sync contenga la ruta absoluta del template. 5) Trailer: ''Task-Id: task-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta-no-por-su-nombre-para-que-un-repo-con-su'';
  commit con ''git commit -- <rutas>''.'
# ISO 8601 timestamp
created_at: '2026-11-20T19:23:31.097312+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T19:24:17.773589+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Bundle review of task-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta-no-por-su-nombre-para-que-un-repo-con-su

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261120-192319/context-review/task-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta-no-por-su-nombre-para-que-un-repo-con-su/bundle/7403b809f4edf70cd87737368bc1fa11347a455f0eaeda17ca11eaf6d4172605/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador. 1) y bundle 3) El punto es la llamada '_scion(["scion", "templates", "sync", role_name, "--project", cfg.project])' de start en deskops/dispatch.py, justo después de materialize_scion_template; target es 'Path(cfg.templates_dir).expanduser() / role_name', unas líneas antes. No hay otra llamada a sync. 2), 3) y bundle 1) y 4) Contrato verificado por el coordinador con scion v0.2.21: 'scion templates sync --help' dice 'The template may also be given as a directory path: ... an absolute path ... The directory is synced as is, and the Hub name defaults to its base name'. Sync sube el template al hub del proyecto (--project sldb-1). 'scion start -t <nombre> --project sldb-1' lo toma del hub del proyecto, no del grove local, así que start no cambia. Solo se cambia el sync, que pasa a recibir str(target). Si al relanzar el dispatch de IR start fallara igual, el integrador lo informa en una tarea nueva; no es parte de esta. 'Se informa' significa en result-summary.md del ejecutor. 4) y bundle 2) _scion está en deskops/dispatch.py:30 ('The only place that runs scion'). El test usa monkeypatch.setattr(dispatch, '_scion', fake), con fake que guarda los argv y devuelve subprocess.CompletedProcess(argv, 0, '', ''), como los tests de tests/test_dispatch.py. El test arma un root temporal con .scion/settings.yaml y verifica que el argv del sync contenga la ruta absoluta del template. 5) Trailer: 'Task-Id: task-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta-no-por-su-nombre-para-que-un-repo-con-su'; commit con 'git commit -- <rutas>'.

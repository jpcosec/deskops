---
sldb:
  by: agent
  at: '2026-11-21T18:09:10Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-dispatch-commitea-tambien-el-run-md-del-run-dir-junto-con-su-rundoc-integrate-fallaba-en-store-con-u-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-dispatch-commitea-tambien-el-run-md-del-run-dir-junto-con-su-rundoc-integrate-fallaba-en-store-con-u@sha256:1c6f77337c5aa01fe74ea7e6c344ef51400acf7693f50332ff722b898348e186
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-180726/context-review/task-dispatch-commitea-tambien-el-run-md-del-run-dir-junto-con-su-rundoc-integrate-fallaba-en-store-con-u/preflight/2a1db2b5c859510a35f9f6a641656c9476d4a1adecce7d01918f565123c0ddf9/attempt-1
input_sha256: 2a1db2b5c859510a35f9f6a641656c9476d4a1adecce7d01918f565123c0ddf9
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: f706f6bff638190a039eb843b913b90a2c547f76b7a6a1c86233e42f9f0ba2b0
output_sha256: 555b39cba5503d77cdfae1ee0f84d127c06139a72ddd488950b0741b21dc2717
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador.


  P1 y B2) Se simula como lo hace el test que ya existe, test_start_commits_the_rundoc_so_reap_brings_an_executor_commit_touching_the_store
  (tests/test_dispatch.py:490), con su fixture env. Reusar ese escenario: un dispatch
  start real contra el scion falso del fixture.


  P2) El asunto real es el que arma _commit_run_store (deskops/dispatch.py:212): "run:
  <nombres separados por coma>", donde cada nombre es el nombre del agente de scion
  (por ejemplo deskops-e-xxxx o deskops-t-xxxx). El test verifica con git show --name-only
  HEAD que el commit contiene runs/subagents/exec-<nombre>/run.md (o exec-<nombre>-testing/run.md
  para un tester) además del shard .sldb/core/documents/RunDoc/run-<slug>.yaml.


  B1) _run_dir_for (deskops/dispatch.py:228) devuelve f"runs/subagents/exec-{name}"
  más "-testing" si role == "tester". El sufijo se agrega al final del nombre del
  agente. _run_store_paths recibe hoy solo el nombre; se le agrega el rol, o se prueban
  las dos rutas y se queda la que exista.


  B3) El chequeo de integrate está en deskops/integrate.py:320-331. Lee .sldb/store.yaml
  del commit y, para cada ruta de _collect_paths(store) que no empiece con ''../'',
  exige que git cat-file -e HEAD:<ruta> dé 0. El test p2 replica ese chequeo sobre
  el commit ''run:'': cada ruta que el store declara existe en ese commit. Se puede
  extraer la función o llamarla.


  B4) Sí: un caso donde el run.md no existe (agente sin run dir) y el commit sale
  igual sin error, solo con el store.


  P3) El worktree es el que dispatch le da al ejecutor. El trailer es ''Task-Id: <id
  de esta tarea>'' en el cuerpo.


  P4) CHANGELOG.md en la raíz: una viñeta en la sección superior sin publicar, en
  el estilo de las vecinas.'
# ISO 8601 timestamp
created_at: '2026-11-21T18:07:51.980082+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T18:09:03.512172+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-dispatch-commitea-tambien-el-run-md-del-run-dir-junto-con-su-rundoc-integrate-fallaba-en-store-con-u

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-180726/context-review/task-dispatch-commitea-tambien-el-run-md-del-run-dir-junto-con-su-rundoc-integrate-fallaba-en-store-con-u/preflight/2a1db2b5c859510a35f9f6a641656c9476d4a1adecce7d01918f565123c0ddf9/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador.

P1 y B2) Se simula como lo hace el test que ya existe, test_start_commits_the_rundoc_so_reap_brings_an_executor_commit_touching_the_store (tests/test_dispatch.py:490), con su fixture env. Reusar ese escenario: un dispatch start real contra el scion falso del fixture.

P2) El asunto real es el que arma _commit_run_store (deskops/dispatch.py:212): "run: <nombres separados por coma>", donde cada nombre es el nombre del agente de scion (por ejemplo deskops-e-xxxx o deskops-t-xxxx). El test verifica con git show --name-only HEAD que el commit contiene runs/subagents/exec-<nombre>/run.md (o exec-<nombre>-testing/run.md para un tester) además del shard .sldb/core/documents/RunDoc/run-<slug>.yaml.

B1) _run_dir_for (deskops/dispatch.py:228) devuelve f"runs/subagents/exec-{name}" más "-testing" si role == "tester". El sufijo se agrega al final del nombre del agente. _run_store_paths recibe hoy solo el nombre; se le agrega el rol, o se prueban las dos rutas y se queda la que exista.

B3) El chequeo de integrate está en deskops/integrate.py:320-331. Lee .sldb/store.yaml del commit y, para cada ruta de _collect_paths(store) que no empiece con '../', exige que git cat-file -e HEAD:<ruta> dé 0. El test p2 replica ese chequeo sobre el commit 'run:': cada ruta que el store declara existe en ese commit. Se puede extraer la función o llamarla.

B4) Sí: un caso donde el run.md no existe (agente sin run dir) y el commit sale igual sin error, solo con el store.

P3) El worktree es el que dispatch le da al ejecutor. El trailer es 'Task-Id: <id de esta tarea>' en el cuerpo.

P4) CHANGELOG.md en la raíz: una viñeta en la sección superior sin publicar, en el estilo de las vecinas.

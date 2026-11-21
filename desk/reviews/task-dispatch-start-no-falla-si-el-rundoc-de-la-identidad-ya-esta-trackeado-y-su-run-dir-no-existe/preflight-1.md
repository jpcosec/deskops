---
sldb:
  by: agent
  at: '2026-11-21T07:07:54Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe@sha256:4dd97eed5c81b0e3ae19b4f15a997f2141dcccdaa9e7e56cf0ad45253dfe5a68
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-070358/context-review/task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe/preflight/f419a62f36462e08628603ee311cb5b5924c3661a2c88e14c1bd1b8df391063b/attempt-1
input_sha256: f419a62f36462e08628603ee311cb5b5924c3661a2c88e14c1bd1b8df391063b
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 36e3405824d905c4654383751d4d1768fcc4eee11023a825571f581eac2aa184
output_sha256: 3df053e98a1e8ad79c3507a7dbeda081ad6e2ba5098a848dd1b9c309e2e17bbb
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones: 1) Se elige re-trackear: si el run_dir elegido no
  existe pero el store ya trackea el documento run-<agente> (el id que arma record_scion_run,
  scion.py:~962), start lo saca con deskops.doc_access.untrack_doc(root, ''run-<agente>'')
  (doc_access.py:373, Transaction.untrack) y despues record_scion_run lo crea normal;
  record_scion_run no cambia. 2) El cambio va en deskops/dispatch.py start (entre
  la eleccion de identidad, ~lineas 269-281, y la llamada a record_scion_run, ~309).
  3) La carpeta es root/<run_dir> (runs/subagents/exec-<agente>[-testing]); si start
  falla despues de crearla y queda vacia, start la borra antes de devolver el error
  (rmdir solo si esta vacia). 4) El doble es el scion falso de tests/test_dispatch.py
  (clase Env con FAKE_SCION en bin/scion, env.agents(...), env.cli(''dispatch'',''start'',...));
  no hace falta otro mock. 5) p1 significa: antes del fix el test falla porque start
  sale con error ''Store error: Doc run-... already tracked''; despues del fix start
  devuelve 0 y el RunDoc nuevo apunta al run_dir nuevo. Commit con ''Task-Id: task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe''
  en el cuerpo, en el worktree que dispatch le da al ejecutor.'
# ISO 8601 timestamp
created_at: '2026-11-21T07:04:06.663849+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T07:07:46.510944+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-070358/context-review/task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe/preflight/f419a62f36462e08628603ee311cb5b5924c3661a2c88e14c1bd1b8df391063b/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones: 1) Se elige re-trackear: si el run_dir elegido no existe pero el store ya trackea el documento run-<agente> (el id que arma record_scion_run, scion.py:~962), start lo saca con deskops.doc_access.untrack_doc(root, 'run-<agente>') (doc_access.py:373, Transaction.untrack) y despues record_scion_run lo crea normal; record_scion_run no cambia. 2) El cambio va en deskops/dispatch.py start (entre la eleccion de identidad, ~lineas 269-281, y la llamada a record_scion_run, ~309). 3) La carpeta es root/<run_dir> (runs/subagents/exec-<agente>[-testing]); si start falla despues de crearla y queda vacia, start la borra antes de devolver el error (rmdir solo si esta vacia). 4) El doble es el scion falso de tests/test_dispatch.py (clase Env con FAKE_SCION en bin/scion, env.agents(...), env.cli('dispatch','start',...)); no hace falta otro mock. 5) p1 significa: antes del fix el test falla porque start sale con error 'Store error: Doc run-... already tracked'; despues del fix start devuelve 0 y el RunDoc nuevo apunta al run_dir nuevo. Commit con 'Task-Id: task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe' en el cuerpo, en el worktree que dispatch le da al ejecutor.

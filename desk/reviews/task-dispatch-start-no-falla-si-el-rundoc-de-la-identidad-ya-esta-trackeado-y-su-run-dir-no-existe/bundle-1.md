---
sldb:
  by: agent
  at: '2026-11-23T19:19:19Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
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
run_dir: runs/subagents/20261121-071008/context-review/task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe/bundle/d52a2513ec9fc80810c4a43cb8d6e9a5adc2978390bb996ef609936e58d3596f/attempt-1
input_sha256: d52a2513ec9fc80810c4a43cb8d6e9a5adc2978390bb996ef609936e58d3596f
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 13b3cff472c7573c3d0fa9472ec687cd9c7592dc6b727ce47ee23c3cd6dd68b3
output_sha256: 333692b986ff79ad9ab364069b436b398f45531ded38b77c742dca0032c43097
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones (las mismas de preflight-1): 1-3) Re-trackear: deskops.doc_access.untrack_doc(root,
  ''run-<agente>'') (doc_access.py:373) y despues record_scion_run normal; no se usa
  update. 2) Capa: deskops/dispatch.py start; deskops/runtime/scion.py no cambia.
  4) Limpieza en start: si start falla despues de crear root/<run_dir> (runs/subagents/exec-<agente>[-testing])
  y la carpeta quedo vacia, start la borra antes de devolver el codigo de error; cualquier
  fallo de start cuenta. 5) Hoy (dispatch.py ~275-281) un run_dir existente cuenta
  como intento hecho y pasa al intento 2 o sale EXIT_NO_ATTEMPTS; eso no cambia. 6)
  ''Lanza'' = start lanza el agente (llama a scion start del scion falso) y devuelve
  0; antes del fix devolvia error con ''Store error: Doc run-... already tracked''.
  7) run-<agente> es el id que arma record_scion_run (f''run-{_slug(agent_slug)}'',
  scion.py ~962); el store de prueba es el desk temporal de tests/test_dispatch.py
  (clase Env), donde el test trackea antes un RunDoc con ese id sin crear su run_dir.
  Commit con ''Task-Id: task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe''
  en el cuerpo, en el worktree que dispatch le da al ejecutor.'
# ISO 8601 timestamp
created_at: '2026-11-21T07:10:17.560838+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T07:12:00.886254+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Bundle review of task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-071008/context-review/task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe/bundle/d52a2513ec9fc80810c4a43cb8d6e9a5adc2978390bb996ef609936e58d3596f/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones (las mismas de preflight-1): 1-3) Re-trackear: deskops.doc_access.untrack_doc(root, 'run-<agente>') (doc_access.py:373) y despues record_scion_run normal; no se usa update. 2) Capa: deskops/dispatch.py start; deskops/runtime/scion.py no cambia. 4) Limpieza en start: si start falla despues de crear root/<run_dir> (runs/subagents/exec-<agente>[-testing]) y la carpeta quedo vacia, start la borra antes de devolver el codigo de error; cualquier fallo de start cuenta. 5) Hoy (dispatch.py ~275-281) un run_dir existente cuenta como intento hecho y pasa al intento 2 o sale EXIT_NO_ATTEMPTS; eso no cambia. 6) 'Lanza' = start lanza el agente (llama a scion start del scion falso) y devuelve 0; antes del fix devolvia error con 'Store error: Doc run-... already tracked'. 7) run-<agente> es el id que arma record_scion_run (f'run-{_slug(agent_slug)}', scion.py ~962); el store de prueba es el desk temporal de tests/test_dispatch.py (clase Env), donde el test trackea antes un RunDoc con ese id sin crear su run_dir. Commit con 'Task-Id: task-dispatch-start-no-falla-si-el-rundoc-de-la-identidad-ya-esta-trackeado-y-su-run-dir-no-existe' en el cuerpo, en el worktree que dispatch le da al ejecutor.

---
sldb:
  by: agent
  at: '2026-11-24T17:54:44Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo@sha256:469c0d7dbe14b686824bb9ed9a2897722b27f4be49b71f3578998e33420f5920
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261117-025359/context-review/task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo/preflight/d3d167f0ff0730037bc2e034b7a920bc2e875ff31ad9bc97951b665de4f4a5bd/attempt-1
input_sha256: d3d167f0ff0730037bc2e034b7a920bc2e875ff31ad9bc97951b665de4f4a5bd
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: d11e910f297838efff21b1c124eff39d493213e460fa8005936302948907230b
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Precisiones del coordinador (preflight 1): (1) El patron vive solo en deskops/models/review.py
  (SUBJECT_REF_PATTERN, usado como pattern del campo subject_ref de ReviewDoc); .sldb/core/models/ReviewDoc.yaml
  no declara pattern, asi que no hay nada que tocar ahi. (2) REVIEW_ID_PATTERN ya
  admite cualquier caracter en el medio (review-.+-node-N) y el review_id se arma
  con node_id.lower() en deskops/services/review.py, asi que el punto no choca; si
  el ejecutor ve que choca, lo dice en result-summary.md, sin cambiar el formato.
  (3) El pi falso es la fixture fake_pi de tests/test_review_command.py (linea 74)
  y el desk sandbox es la fixture lifecycle_desk de tests/conftest.py; el test de
  review node existente (test_node_writes_one_review_doc_per_node) muestra como se
  usan. (4) El dag.yaml de prueba se escribe dentro del sandbox en desk/drawer/plans/<nombre>/dag.yaml
  con la estructura minima que acepta review node (ROOT con children y un nodo con
  id con punto); el ejecutor la toma del plan gates-por-tipo.'
# ISO 8601 timestamp
created_at: '2026-11-17T02:54:08.663285+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T02:56:47.913233+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-025359/context-review/task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo/preflight/d3d167f0ff0730037bc2e034b7a920bc2e875ff31ad9bc97951b665de4f4a5bd/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Precisiones del coordinador (preflight 1): (1) El patron vive solo en deskops/models/review.py (SUBJECT_REF_PATTERN, usado como pattern del campo subject_ref de ReviewDoc); .sldb/core/models/ReviewDoc.yaml no declara pattern, asi que no hay nada que tocar ahi. (2) REVIEW_ID_PATTERN ya admite cualquier caracter en el medio (review-.+-node-N) y el review_id se arma con node_id.lower() en deskops/services/review.py, asi que el punto no choca; si el ejecutor ve que choca, lo dice en result-summary.md, sin cambiar el formato. (3) El pi falso es la fixture fake_pi de tests/test_review_command.py (linea 74) y el desk sandbox es la fixture lifecycle_desk de tests/conftest.py; el test de review node existente (test_node_writes_one_review_doc_per_node) muestra como se usan. (4) El dag.yaml de prueba se escribe dentro del sandbox en desk/drawer/plans/<nombre>/dag.yaml con la estructura minima que acepta review node (ROOT con children y un nodo con id con punto); el ejecutor la toma del plan gates-por-tipo.

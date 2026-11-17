---
sldb:
  by: agent
  at: '2026-11-17T03:18:07Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-closeout-gates-review-model

  materialization-materializa-recibos-de-evidencia-cc33a-en-models-review

  materialization-materializa-recibos-de-evidencia-cc33a-en-tests-test-review-doc

  materialization-review-status-regression-tests'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo@sha256:469c0d7dbe14b686824bb9ed9a2897722b27f4be49b71f3578998e33420f5920
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 8f70d11add844078eab769bacde572786f48f68759df04a73e70ce3298eccc5a
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-closeout-gates-review-model

  materialization-materializa-recibos-de-evidencia-cc33a-en-models-review

  materialization-materializa-recibos-de-evidencia-cc33a-en-tests-test-review-doc

  materialization-review-status-regression-tests'
# ISO 8601 timestamp
created_at: '2026-11-17T03:17:50.479983+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T03:17:50.479983+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-closeout-gates-review-model, materialization-materializa-recibos-de-evidencia-cc33a-en-models-review, materialization-materializa-recibos-de-evidencia-cc33a-en-tests-test-review-doc, materialization-review-status-regression-tests

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-closeout-gates-review-model
materialization-materializa-recibos-de-evidencia-cc33a-en-models-review
materialization-materializa-recibos-de-evidencia-cc33a-en-tests-test-review-doc
materialization-review-status-regression-tests

---
sldb:
  by: agent
  at: '2026-11-24T18:11:04Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n-reproduction-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: reproduction
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n@sha256:d8f26ba1d4f452699992ed883776fb482dad1f05241bb94e3280759ca57d24e9
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: human
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 0c4a2583e5f74f600ed19e222de8629a81b5b66c3e60f110045e0d0afef8da0b
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Reproduccion verificada en el log del integrate 20261123T114518Z: falla test_reap_scion_error_continues_and_fails
  con la linea extra ''limpieza: /dev/shm/pytest-of-scion''.'
# ISO 8601 timestamp
created_at: '2026-11-23T14:41:17.204810+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T14:42:58.142772+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Reproduction review of task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n

## Summary

_Summarize what was reviewed and the evidence this receipt records._

reproduction receipt recorded by deskops; evidence: runs/queue/logs/integrate-task-borrar-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph-que-no.log

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Reproduccion verificada en el log del integrate 20261123T114518Z: falla test_reap_scion_error_continues_and_fails con la linea extra 'limpieza: /dev/shm/pytest-of-scion'.

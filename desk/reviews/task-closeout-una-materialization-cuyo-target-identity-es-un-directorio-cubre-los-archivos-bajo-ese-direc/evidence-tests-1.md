---
sldb:
  by: agent
  at: '2026-11-23T19:05:03Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: tests/test_materialization_targets_outside_package.py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc@sha256:43b73822020fe52da9fbe98b86c48d67426e43d38b663bb8bfa01c6ea91d170b
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 5af404c6c002b2ebfcd99764c454b2889b8d60492e37f38615e22d8fdce01bbd
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/test_materialization_targets_outside_package.py'
# ISO 8601 timestamp
created_at: '2026-11-16T10:47:01.608345+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T10:47:01.608345+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/test_materialization_targets_outside_package.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/test_materialization_targets_outside_package.py

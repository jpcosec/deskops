---
sldb:
  by: agent
  at: '2026-11-24T18:18:21Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-closeout-gates-changelog

  materialization-dispatch-deskops-dispatch-py

  materialization-dispatch-paralelo-deskops-dispatch-py

  materialization-dispatch-paralelo-tests-test-dispatch-py

  materialization-dispatch-tests-test-dispatch-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p@sha256:49da69f2b1db80704997c2c7309ea8d5123514845f0d7eb1110d888f77f82a9f
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: cdd329d52cb4dd3d3425d04a3fd24ca0b8587d63eb224076e8a30a658ae2930c
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-closeout-gates-changelog

  materialization-dispatch-deskops-dispatch-py

  materialization-dispatch-paralelo-deskops-dispatch-py

  materialization-dispatch-paralelo-tests-test-dispatch-py

  materialization-dispatch-tests-test-dispatch-py'
# ISO 8601 timestamp
created_at: '2026-11-22T15:03:05.893562+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T15:03:05.893562+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-closeout-gates-changelog, materialization-dispatch-deskops-dispatch-py, materialization-dispatch-paralelo-deskops-dispatch-py, materialization-dispatch-paralelo-tests-test-dispatch-py, materialization-dispatch-tests-test-dispatch-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-closeout-gates-changelog
materialization-dispatch-deskops-dispatch-py
materialization-dispatch-paralelo-deskops-dispatch-py
materialization-dispatch-paralelo-tests-test-dispatch-py
materialization-dispatch-tests-test-dispatch-py

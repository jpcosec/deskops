---
sldb:
  by: agent
  at: '2026-11-24T18:17:45Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-queue-run-sigue-con-los-trabajos-siguientes-cuando-uno-queda-en-espera-por-retry-exit-codes-en-vez-d-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-closeout-gates-changelog

  materialization-closeout-gates-operator-manual

  materialization-cola-sigue-tras-retry-deskops-queue-py

  materialization-cola-sigue-tras-retry-docs-operator-manual-md

  materialization-cola-sigue-tras-retry-tests-test-queue-py

  materialization-dispatch-paralelo-docs-operator-manual-md

  materialization-host-queue-runner

  materialization-retry-exit-codes-operator-manual

  materialization-retry-exit-codes-queue

  materialization-retry-exit-codes-test-queue'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-queue-run-sigue-con-los-trabajos-siguientes-cuando-uno-queda-en-espera-por-retry-exit-codes-en-vez-d@sha256:a0ccdece73d952d1d36229efcc827d55a09aed50a01435507345fd9c53e6810b
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 980a1da99714cea8c43751254218513381caa597679c96ddab742475f244c0bf
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-closeout-gates-changelog

  materialization-closeout-gates-operator-manual

  materialization-cola-sigue-tras-retry-deskops-queue-py

  materialization-cola-sigue-tras-retry-docs-operator-manual-md

  materialization-cola-sigue-tras-retry-tests-test-queue-py

  materialization-dispatch-paralelo-docs-operator-manual-md

  materialization-host-queue-runner

  materialization-retry-exit-codes-operator-manual

  materialization-retry-exit-codes-queue

  materialization-retry-exit-codes-test-queue'
# ISO 8601 timestamp
created_at: '2026-11-20T01:48:00.632758+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T01:48:00.632758+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-queue-run-sigue-con-los-trabajos-siguientes-cuando-uno-queda-en-espera-por-retry-exit-codes-en-vez-d

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-closeout-gates-changelog, materialization-closeout-gates-operator-manual, materialization-cola-sigue-tras-retry-deskops-queue-py, materialization-cola-sigue-tras-retry-docs-operator-manual-md, materialization-cola-sigue-tras-retry-tests-test-queue-py, materialization-dispatch-paralelo-docs-operator-manual-md, materialization-host-queue-runner, materialization-retry-exit-codes-operator-manual, materialization-retry-exit-codes-queue, materialization-retry-exit-codes-test-queue

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-closeout-gates-changelog
materialization-closeout-gates-operator-manual
materialization-cola-sigue-tras-retry-deskops-queue-py
materialization-cola-sigue-tras-retry-docs-operator-manual-md
materialization-cola-sigue-tras-retry-tests-test-queue-py
materialization-dispatch-paralelo-docs-operator-manual-md
materialization-host-queue-runner
materialization-retry-exit-codes-operator-manual
materialization-retry-exit-codes-queue
materialization-retry-exit-codes-test-queue

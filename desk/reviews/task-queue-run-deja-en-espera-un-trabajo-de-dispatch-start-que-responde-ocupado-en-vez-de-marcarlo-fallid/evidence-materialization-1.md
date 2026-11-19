---
sldb:
  by: agent
  at: '2026-11-19T13:28:42Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-closeout-gates-changelog

  materialization-closeout-gates-operator-manual

  materialization-host-queue-config

  materialization-host-queue-runner

  materialization-retry-exit-codes-config

  materialization-retry-exit-codes-operator-manual

  materialization-retry-exit-codes-queue

  materialization-retry-exit-codes-test-queue'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid@sha256:a9d1a90b4a4ef385713717fb22eb454dbd6dc611d0bb254c47ac1c4889ae110e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: c1d79a9f6fe91c59d9cbec6dd27c48020454b6214c6696d03d6307b82f5e1d72
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-closeout-gates-changelog

  materialization-closeout-gates-operator-manual

  materialization-host-queue-config

  materialization-host-queue-runner

  materialization-retry-exit-codes-config

  materialization-retry-exit-codes-operator-manual

  materialization-retry-exit-codes-queue

  materialization-retry-exit-codes-test-queue'
# ISO 8601 timestamp
created_at: '2026-11-19T13:28:28.686277+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T13:28:28.686277+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-closeout-gates-changelog, materialization-closeout-gates-operator-manual, materialization-host-queue-config, materialization-host-queue-runner, materialization-retry-exit-codes-config, materialization-retry-exit-codes-operator-manual, materialization-retry-exit-codes-queue, materialization-retry-exit-codes-test-queue

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-closeout-gates-changelog
materialization-closeout-gates-operator-manual
materialization-host-queue-config
materialization-host-queue-runner
materialization-retry-exit-codes-config
materialization-retry-exit-codes-operator-manual
materialization-retry-exit-codes-queue
materialization-retry-exit-codes-test-queue

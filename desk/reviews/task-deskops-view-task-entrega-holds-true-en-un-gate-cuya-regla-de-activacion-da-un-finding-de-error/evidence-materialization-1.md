---
sldb:
  by: agent
  at: '2026-11-24T17:56:09Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-closeout-graph-desk-view-snapshot

  materialization-deskops-ui-view-command

  materialization-deskops-ui-view-service

  materialization-deskops-ui-view-tests

  materialization-forced-advance-never-closes

  materialization-golden-de-salida-de-view-board

  materialization-golden-de-salida-de-view-task'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error@sha256:4999867bd29ca115d2a8a70bfe9ad7d06b06a5ca53324b68b6bcc93ed3965876
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: f8dd430a650b40135116e9cb0920e423df2c2e6fcde83b3fb510e333d2e0905a
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-closeout-graph-desk-view-snapshot

  materialization-deskops-ui-view-command

  materialization-deskops-ui-view-service

  materialization-deskops-ui-view-tests

  materialization-forced-advance-never-closes

  materialization-golden-de-salida-de-view-board

  materialization-golden-de-salida-de-view-task'
# ISO 8601 timestamp
created_at: '2026-11-17T16:19:27.956917+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T16:19:27.956917+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-closeout-graph-desk-view-snapshot, materialization-deskops-ui-view-command, materialization-deskops-ui-view-service, materialization-deskops-ui-view-tests, materialization-forced-advance-never-closes, materialization-golden-de-salida-de-view-board, materialization-golden-de-salida-de-view-task

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-closeout-graph-desk-view-snapshot
materialization-deskops-ui-view-command
materialization-deskops-ui-view-service
materialization-deskops-ui-view-tests
materialization-forced-advance-never-closes
materialization-golden-de-salida-de-view-board
materialization-golden-de-salida-de-view-task

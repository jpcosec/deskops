---
sldb:
  by: agent
  at: '2026-11-25T05:06:47Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-integrate-cleanup-deskops-integrate-py

  materialization-integrate-cleanup-tests-test-integrate-py

  materialization-integrate-codigo-en-origin-deskops-integrate-py

  materialization-integrate-codigo-en-origin-tests-test-integrate-py

  materialization-integrate-deskops-integrate-py

  materialization-integrate-tests-test-integrate-py

  materialization-tip-extendido-deskops-integrate-py

  materialization-tip-extendido-tests-test-integrate-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin@sha256:fed34b27c077266e8f98cdf81ccd4533aabbeb5b81926e1377ca56bcc7431798
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: d995115df88aa23587e89ddd0d2296d304a7bde562e243837d7e46cf6c57916b
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-integrate-cleanup-deskops-integrate-py

  materialization-integrate-cleanup-tests-test-integrate-py

  materialization-integrate-codigo-en-origin-deskops-integrate-py

  materialization-integrate-codigo-en-origin-tests-test-integrate-py

  materialization-integrate-deskops-integrate-py

  materialization-integrate-tests-test-integrate-py

  materialization-tip-extendido-deskops-integrate-py

  materialization-tip-extendido-tests-test-integrate-py'
# ISO 8601 timestamp
created_at: '2026-11-25T05:06:32.175854+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T05:06:32.175854+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-integrate-cleanup-deskops-integrate-py, materialization-integrate-cleanup-tests-test-integrate-py, materialization-integrate-codigo-en-origin-deskops-integrate-py, materialization-integrate-codigo-en-origin-tests-test-integrate-py, materialization-integrate-deskops-integrate-py, materialization-integrate-tests-test-integrate-py, materialization-tip-extendido-deskops-integrate-py, materialization-tip-extendido-tests-test-integrate-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-integrate-cleanup-deskops-integrate-py
materialization-integrate-cleanup-tests-test-integrate-py
materialization-integrate-codigo-en-origin-deskops-integrate-py
materialization-integrate-codigo-en-origin-tests-test-integrate-py
materialization-integrate-deskops-integrate-py
materialization-integrate-tests-test-integrate-py
materialization-tip-extendido-deskops-integrate-py
materialization-tip-extendido-tests-test-integrate-py

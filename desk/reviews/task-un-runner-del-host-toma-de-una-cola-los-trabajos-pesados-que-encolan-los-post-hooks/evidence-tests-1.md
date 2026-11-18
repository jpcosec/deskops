---
sldb:
  by: agent
  at: '2026-11-18T07:39:38Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: tests/test_queue.py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks@sha256:ca65178c42c1f293a6ffc24424a3391c60ba64af462b6f2c2612120be4897305
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: b4cd7550db02e3dca1a207f15eabb7b8c1e4d8a70352ec8a25a43a80cfb9fae3
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/test_queue.py'
# ISO 8601 timestamp
created_at: '2026-11-18T07:39:37.218985+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-18T07:39:37.218985+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/test_queue.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/test_queue.py

---
sldb:
  by: agent
  at: '2026-11-25T02:56:15Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-el-modo-pr-de-dispatch-e-integrate-trabaja-en-un-worktree-propio-de-task-id-y-nunca-cambia-la-rama-d-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'tests/test_dispatch.py

  tests/test_integrate.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-modo-pr-de-dispatch-e-integrate-trabaja-en-un-worktree-propio-de-task-id-y-nunca-cambia-la-rama-d@sha256:95b66c2e4bea968300a0bb9189bb356ab7be9f693f661f1a28960c7686f9e55d
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 03db8cf5e5338ddf0cc9b54e29eb466fff7e411f581aeafa33fd5814f7565c68
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/test_dispatch.py

  tests/test_integrate.py'
# ISO 8601 timestamp
created_at: '2026-11-25T02:56:14.470976+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T02:56:14.470976+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-el-modo-pr-de-dispatch-e-integrate-trabaja-en-un-worktree-propio-de-task-id-y-nunca-cambia-la-rama-d

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/test_dispatch.py, tests/test_integrate.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/test_dispatch.py
tests/test_integrate.py

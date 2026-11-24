---
sldb:
  by: agent
  at: '2026-11-24T18:12:01Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-merge-driver-tests-conftest-py

  materialization-tests-tests-conftest-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global@sha256:d8a61abf23f274657a0b8f01812d7e0043dfe2ea767316f7c073c3b1208100a6
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 3f9bf0b874f0f5107c3de50f5007f502ededd9542b187a25128198d940e7f9e9
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-merge-driver-tests-conftest-py

  materialization-tests-tests-conftest-py'
# ISO 8601 timestamp
created_at: '2026-11-23T16:12:42.194435+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T16:12:42.194435+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-merge-driver-tests-conftest-py, materialization-tests-tests-conftest-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-merge-driver-tests-conftest-py
materialization-tests-tests-conftest-py

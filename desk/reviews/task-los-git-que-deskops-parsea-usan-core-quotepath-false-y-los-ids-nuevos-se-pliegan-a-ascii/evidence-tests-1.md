---
sldb:
  by: agent
  at: '2026-11-24T18:15:16Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-los-git-que-deskops-parsea-usan-core-quotepath-false-y-los-ids-nuevos-se-pliegan-a-ascii-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: tests/test_ascii_ids.py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-los-git-que-deskops-parsea-usan-core-quotepath-false-y-los-ids-nuevos-se-pliegan-a-ascii@sha256:4e6187dec47b1ca6c380404dd46af8a45761aef557bcd35616b5f1e0eac69aee
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 2a4faeb6cb1d9b186a02f1a8b1e2649213aeb091f37cc02fd93d9c56c2ae3a4c
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/test_ascii_ids.py'
# ISO 8601 timestamp
created_at: '2026-11-18T21:25:42.895267+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-18T21:25:42.895267+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-los-git-que-deskops-parsea-usan-core-quotepath-false-y-los-ids-nuevos-se-pliegan-a-ascii

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/test_ascii_ids.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/test_ascii_ids.py

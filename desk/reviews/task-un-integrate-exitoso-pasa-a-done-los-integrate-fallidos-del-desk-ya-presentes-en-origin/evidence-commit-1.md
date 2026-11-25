---
sldb:
  by: agent
  at: '2026-11-25T05:06:38Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: 58ce512897651a6bce9e7169bca0d42a1b481466
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin@sha256:fed34b27c077266e8f98cdf81ccd4533aabbeb5b81926e1377ca56bcc7431798
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: a0a5a7d00db9b5a1be02a0a5c9ff0d01b207173ee989b8cd55c32b49b1b88eb9
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 58ce512897651a6bce9e7169bca0d42a1b481466'
# ISO 8601 timestamp
created_at: '2026-11-25T05:06:32.175854+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T05:06:32.175854+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence commit of task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 58ce512897651a6bce9e7169bca0d42a1b481466

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 58ce512897651a6bce9e7169bca0d42a1b481466

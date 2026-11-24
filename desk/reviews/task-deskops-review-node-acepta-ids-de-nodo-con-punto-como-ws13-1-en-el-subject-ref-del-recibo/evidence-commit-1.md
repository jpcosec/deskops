---
sldb:
  by: agent
  at: '2026-11-23T19:14:52Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: 4fe3d0c60963264ed346e4fa51eb0f4e32f23613
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo@sha256:469c0d7dbe14b686824bb9ed9a2897722b27f4be49b71f3578998e33420f5920
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 943938bbe951111d11727ec463e989850e3517c2caebab4bae409eb66868bbff
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 4fe3d0c60963264ed346e4fa51eb0f4e32f23613'
# ISO 8601 timestamp
created_at: '2026-11-17T03:17:50.479983+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T03:17:50.479983+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence commit of task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 4fe3d0c60963264ed346e4fa51eb0f4e32f23613

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 4fe3d0c60963264ed346e4fa51eb0f4e32f23613

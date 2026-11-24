---
sldb:
  by: agent
  at: '2026-11-24T18:00:31Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: '91f44d0d1710c2c428d5edebb8a9e8424c42f89f

  c0df7045058dc5c4ddd6d5f143f9fae4038cd47f'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada@sha256:bd572673b5989cc38db6fb86882b88f4364b77ab4a33850866907013534a3a4e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: b2feec3efd1018ec40509398e2b453858951bb35fbb4b8a23d1adf34af802c38
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 91f44d0d1710c2c428d5edebb8a9e8424c42f89f

  c0df7045058dc5c4ddd6d5f143f9fae4038cd47f'
# ISO 8601 timestamp
created_at: '2026-11-22T00:18:37.502179+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T00:18:37.502179+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence commit of task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 91f44d0d1710c2c428d5edebb8a9e8424c42f89f, c0df7045058dc5c4ddd6d5f143f9fae4038cd47f

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 91f44d0d1710c2c428d5edebb8a9e8424c42f89f
c0df7045058dc5c4ddd6d5f143f9fae4038cd47f

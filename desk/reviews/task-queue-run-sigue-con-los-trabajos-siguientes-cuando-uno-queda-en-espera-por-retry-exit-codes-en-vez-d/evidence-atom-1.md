---
sldb:
  by: agent
  at: '2026-11-24T18:17:39Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-queue-run-sigue-con-los-trabajos-siguientes-cuando-uno-queda-en-espera-por-retry-exit-codes-en-vez-d-evidence-atom-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: atom
# kind evidence only: what the producer verified, one item per line
value: atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-queue-run-sigue-con-los-trabajos-siguientes-cuando-uno-queda-en-espera-por-retry-exit-codes-en-vez-d@sha256:a0ccdece73d952d1d36229efcc827d55a09aed50a01435507345fd9c53e6810b
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 7cedfd0f54c2ce0467adef8a5e4db79153a9c780792a09079b0e1ebb7fb6a0c9
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: atom atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien'
# ISO 8601 timestamp
created_at: '2026-11-20T01:48:00.632758+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T01:48:00.632758+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence atom of task-queue-run-sigue-con-los-trabajos-siguientes-cuando-uno-queda-en-espera-por-retry-exit-codes-en-vez-d

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked atom: atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: atom atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien

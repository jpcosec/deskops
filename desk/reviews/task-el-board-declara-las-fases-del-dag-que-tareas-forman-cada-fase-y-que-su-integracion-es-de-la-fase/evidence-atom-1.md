---
sldb:
  by: agent
  at: '2026-11-25T12:38:50Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase-evidence-atom-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: atom
# kind evidence only: what the producer verified, one item per line
value: atom-el-board-declara-las-fases-del-dag
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase@sha256:194a9406df87288ad2a63dd242f7d810fde8c96e372b4dd6312e786ca093020e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 5079dfa0ac24a7d0f6da5407bd12d71cc083e8b6ade1b256db7fd82b96a5ac4f
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: atom atom-el-board-declara-las-fases-del-dag'
# ISO 8601 timestamp
created_at: '2026-11-25T12:38:38.785180+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T12:38:38.785180+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence atom of task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked atom: atom-el-board-declara-las-fases-del-dag

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: atom atom-el-board-declara-las-fases-del-dag

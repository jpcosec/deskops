---
sldb:
  by: agent
  at: '2026-11-24T18:03:12Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-el-template-scion-de-pi-pasa-tools-como-opcion-y-valor-separados-y-no-con-signo-igual-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-cc35a-runtime-scion

  materialization-scion-autonomy-tests'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-el-template-scion-de-pi-pasa-tools-como-opcion-y-valor-separados-y-no-con-signo-igual@sha256:18f2037ba4299bc83a8a58e8edcefa2bbcc1a5f65bb764fae848373157819e26
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: b986e6defce1eab0b924e41a7ef32b2f784590d2ac60816c023f6fde5ae5c3e6
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-cc35a-runtime-scion

  materialization-scion-autonomy-tests'
# ISO 8601 timestamp
created_at: '2026-11-18T07:54:35.699140+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-18T07:54:35.699140+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-el-template-scion-de-pi-pasa-tools-como-opcion-y-valor-separados-y-no-con-signo-igual

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cc35a-runtime-scion, materialization-scion-autonomy-tests

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-cc35a-runtime-scion
materialization-scion-autonomy-tests

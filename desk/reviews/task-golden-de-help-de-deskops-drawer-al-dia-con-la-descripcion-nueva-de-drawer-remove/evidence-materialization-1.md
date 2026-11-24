---
sldb:
  by: agent
  at: '2026-11-23T19:24:27Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-golden-de-help-de-deskops-drawer-al-dia-con-la-descripcion-nueva-de-drawer-remove-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: materialization-cli-tests-fixtures-golden-help-deskops-drawer-txt
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-golden-de-help-de-deskops-drawer-al-dia-con-la-descripcion-nueva-de-drawer-remove@sha256:bdf65c83cad0ad4aed35bd00cc7daa64ad70d9ba2ac7d1c0d3e854b24ea164bb
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 092db8f1fb6efd440e77bb609d073d7dca8f6e304faf4dfd16a952215e8a793d
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-cli-tests-fixtures-golden-help-deskops-drawer-txt'
# ISO 8601 timestamp
created_at: '2026-11-22T09:27:02.394839+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T09:27:02.394839+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-golden-de-help-de-deskops-drawer-al-dia-con-la-descripcion-nueva-de-drawer-remove

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cli-tests-fixtures-golden-help-deskops-drawer-txt

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-cli-tests-fixtures-golden-help-deskops-drawer-txt

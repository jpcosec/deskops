---
sldb:
  by: agent
  at: '2026-11-22T09:28:39Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-golden-de-help-de-deskops-drawer-al-dia-con-la-descripcion-nueva-de-drawer-remove-evidence-materialization-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-cc30-tests-test-output-goldens

  materialization-cli-tests-fixtures-golden-help-deskops-drawer-txt

  materialization-cli-tests-test-output-goldens-py

  materialization-graph-tests-test-output-goldens-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-golden-de-help-de-deskops-drawer-al-dia-con-la-descripcion-nueva-de-drawer-remove@sha256:753b4e0cc945e59fe068cc55189c678039d69854e333b8aeb5c4b414cf5af78d
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: e1fe78a074c75be4422ed18d6b2f7d1ae75c84c79f6f030c50a300fe5ba3dbf3
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-cc30-tests-test-output-goldens

  materialization-cli-tests-fixtures-golden-help-deskops-drawer-txt

  materialization-cli-tests-test-output-goldens-py

  materialization-graph-tests-test-output-goldens-py'
# ISO 8601 timestamp
created_at: '2026-11-22T09:28:26.483408+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T09:28:26.483408+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-golden-de-help-de-deskops-drawer-al-dia-con-la-descripcion-nueva-de-drawer-remove

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cc30-tests-test-output-goldens, materialization-cli-tests-fixtures-golden-help-deskops-drawer-txt, materialization-cli-tests-test-output-goldens-py, materialization-graph-tests-test-output-goldens-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-cc30-tests-test-output-goldens
materialization-cli-tests-fixtures-golden-help-deskops-drawer-txt
materialization-cli-tests-test-output-goldens-py
materialization-graph-tests-test-output-goldens-py

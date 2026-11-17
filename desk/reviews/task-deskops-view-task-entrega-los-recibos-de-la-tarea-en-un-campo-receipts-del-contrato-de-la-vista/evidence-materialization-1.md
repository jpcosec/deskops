---
sldb:
  by: agent
  at: '2026-11-17T14:59:23Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-cli-help-speaks-the-declared-evidence-workflow

  materialization-closeout-graph-desk-view-snapshot

  materialization-deskops-ui-view-command

  materialization-deskops-ui-view-contract-doc

  materialization-deskops-ui-view-registration

  materialization-deskops-ui-view-service

  materialization-deskops-ui-view-tests'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista@sha256:f272868e94c69a3858c33268b5869de91a14286716dd3237013fbdf934b32e04
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 6607c84223f149a7389a270a107aceb6b7d17b8aeacd77ec47add39794c14803
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: rejected
reason: Changed file has no atom/materialization link and no routed follow-up reference.;
  Changed file has no atom/materialization link and no routed follow-up reference.
# ISO 8601 timestamp
created_at: '2026-11-17T14:59:05.969124+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T14:59:05.969124+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cli-help-speaks-the-declared-evidence-workflow, materialization-closeout-graph-desk-view-snapshot, materialization-deskops-ui-view-command, materialization-deskops-ui-view-contract-doc, materialization-deskops-ui-view-registration, materialization-deskops-ui-view-service, materialization-deskops-ui-view-tests

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict rejected: Changed file has no atom/materialization link and no routed follow-up reference.; Changed file has no atom/materialization link and no routed follow-up reference.

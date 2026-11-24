---
sldb:
  by: agent
  at: '2026-11-23T19:26:45Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-closeout-gates-changelog

  materialization-init-tests-test-doctor-model-registration-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk@sha256:011151011a076913df525537649fc7609815c9605ca5511e4c8aab19ace884ee
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 41ed7b708385081d0930375889ff6d4c11ab49d40a4d36b98c7a4160070a20f5
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-closeout-gates-changelog

  materialization-init-tests-test-doctor-model-registration-py'
# ISO 8601 timestamp
created_at: '2026-11-21T10:43:54.815997+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T10:43:54.815997+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-closeout-gates-changelog, materialization-init-tests-test-doctor-model-registration-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-closeout-gates-changelog
materialization-init-tests-test-doctor-model-registration-py

---
sldb:
  by: agent
  at: '2026-11-24T18:07:48Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-integrate-no-empuja-el-commit-de-codigo-por-separado-cuando-no-avanza-rapido-sobre-el-remoto-lo-llev-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-closeout-gates-changelog

  materialization-integrate-codigo-en-origin-deskops-integrate-py

  materialization-integrate-codigo-en-origin-tests-test-integrate-py

  materialization-integrate-deskops-integrate-py

  materialization-integrate-tests-test-integrate-py

  materialization-tip-extendido-deskops-integrate-py

  materialization-tip-extendido-tests-test-integrate-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-integrate-no-empuja-el-commit-de-codigo-por-separado-cuando-no-avanza-rapido-sobre-el-remoto-lo-llev@sha256:816c419f8dc7ce16ed8df7a3fdf8717cc7c87a2e739d0fe8daaa5a9ff4d384bb
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: db1d7e1763bd2da0ced7f7dffbc56409c18247fc8999d925425ef29b5ee483d9
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-closeout-gates-changelog

  materialization-integrate-codigo-en-origin-deskops-integrate-py

  materialization-integrate-codigo-en-origin-tests-test-integrate-py

  materialization-integrate-deskops-integrate-py

  materialization-integrate-tests-test-integrate-py

  materialization-tip-extendido-deskops-integrate-py

  materialization-tip-extendido-tests-test-integrate-py'
# ISO 8601 timestamp
created_at: '2026-11-21T05:35:47.159686+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T05:35:47.159686+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-integrate-no-empuja-el-commit-de-codigo-por-separado-cuando-no-avanza-rapido-sobre-el-remoto-lo-llev

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-closeout-gates-changelog, materialization-integrate-codigo-en-origin-deskops-integrate-py, materialization-integrate-codigo-en-origin-tests-test-integrate-py, materialization-integrate-deskops-integrate-py, materialization-integrate-tests-test-integrate-py, materialization-tip-extendido-deskops-integrate-py, materialization-tip-extendido-tests-test-integrate-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-closeout-gates-changelog
materialization-integrate-codigo-en-origin-deskops-integrate-py
materialization-integrate-codigo-en-origin-tests-test-integrate-py
materialization-integrate-deskops-integrate-py
materialization-integrate-tests-test-integrate-py
materialization-tip-extendido-deskops-integrate-py
materialization-tip-extendido-tests-test-integrate-py

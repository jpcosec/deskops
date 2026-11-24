---
sldb:
  by: agent
  at: '2026-11-23T19:27:29Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-integrate-evalua-el-gate-de-grafo-en-la-punta-local-actual-no-solo-en-el-commit-de-closeout-cuando-d-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-closeout-gates-changelog

  materialization-integrate-codigo-en-origin-deskops-integrate-py

  materialization-integrate-codigo-en-origin-tests-test-integrate-py

  materialization-tip-extendido-deskops-integrate-py

  materialization-tip-extendido-tests-test-integrate-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-integrate-evalua-el-gate-de-grafo-en-la-punta-local-actual-no-solo-en-el-commit-de-closeout-cuando-d@sha256:1a7405c7b691be79268cd27d18e42521c383499d4013367e28b5aafa033edee9
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 27837e7f884e58b4075a0901b66111167822c0a3a238711f2b0060d0a818519d
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-closeout-gates-changelog

  materialization-integrate-codigo-en-origin-deskops-integrate-py

  materialization-integrate-codigo-en-origin-tests-test-integrate-py

  materialization-tip-extendido-deskops-integrate-py

  materialization-tip-extendido-tests-test-integrate-py'
# ISO 8601 timestamp
created_at: '2026-11-20T11:05:35.373312+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T11:05:35.373312+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-integrate-evalua-el-gate-de-grafo-en-la-punta-local-actual-no-solo-en-el-commit-de-closeout-cuando-d

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-closeout-gates-changelog, materialization-integrate-codigo-en-origin-deskops-integrate-py, materialization-integrate-codigo-en-origin-tests-test-integrate-py, materialization-tip-extendido-deskops-integrate-py, materialization-tip-extendido-tests-test-integrate-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-closeout-gates-changelog
materialization-integrate-codigo-en-origin-deskops-integrate-py
materialization-integrate-codigo-en-origin-tests-test-integrate-py
materialization-tip-extendido-deskops-integrate-py
materialization-tip-extendido-tests-test-integrate-py

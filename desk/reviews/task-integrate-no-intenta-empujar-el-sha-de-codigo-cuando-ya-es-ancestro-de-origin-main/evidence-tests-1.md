---
sldb:
  by: agent
  at: '2026-11-23T19:28:38Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-integrate-no-intenta-empujar-el-sha-de-codigo-cuando-ya-es-ancestro-de-origin-main-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'deskops/integrate.py

  tests/test_integrate.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-integrate-no-intenta-empujar-el-sha-de-codigo-cuando-ya-es-ancestro-de-origin-main@sha256:dc8f438dcb8ff84276fe741ce3a40683d8d49f92f9ab8bcd7ff5a78c82593472
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: bc8c4d3bff8c8f350fe87874176b36483e53180b8b2d6f900103133829889eed
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests deskops/integrate.py

  tests/test_integrate.py'
# ISO 8601 timestamp
created_at: '2026-11-20T05:48:23.152125+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T05:48:23.152125+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-integrate-no-intenta-empujar-el-sha-de-codigo-cuando-ya-es-ancestro-de-origin-main

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: deskops/integrate.py, tests/test_integrate.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests deskops/integrate.py
tests/test_integrate.py

---
sldb:
  by: agent
  at: '2026-11-23T19:27:10Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'deskops/integrate.py

  tests/test_integrate.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas@sha256:405d06862240cfa1110fd232b161f017102676154df583a5a34d5685600d8ebe
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 54568c8577c94120e1192e2a6be2b584a52108f4b466f98163b2619e7554a7ad
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests deskops/integrate.py

  tests/test_integrate.py'
# ISO 8601 timestamp
created_at: '2026-11-23T06:15:54.967416+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T06:15:54.967416+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: deskops/integrate.py, tests/test_integrate.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests deskops/integrate.py
tests/test_integrate.py

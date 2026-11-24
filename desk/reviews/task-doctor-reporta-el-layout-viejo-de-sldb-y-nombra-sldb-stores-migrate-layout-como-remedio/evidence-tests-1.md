---
sldb:
  by: agent
  at: '2026-11-24T18:01:05Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'deskops/bootstrap.py

  deskops/cli/commands/core.py

  deskops/cli/commands/doctor.py

  deskops/sldb_layout.py

  tests/test_doctor_sldb_layout.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio@sha256:830c29e3cf1dfaa7e6d9fd17ea7f4d5ca6e993e3c4fb501595915c7cb33ee891
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 4b8bd4a68822357b436a8f0b4c456d0962bf774d30ae180fedcd31ad7171bbd5
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests deskops/bootstrap.py

  deskops/cli/commands/core.py

  deskops/cli/commands/doctor.py

  deskops/sldb_layout.py

  tests/test_doctor_sldb_layout.py'
# ISO 8601 timestamp
created_at: '2026-11-22T07:47:07.377780+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T07:47:07.377780+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: deskops/bootstrap.py, deskops/cli/commands/core.py, deskops/cli/commands/doctor.py, deskops/sldb_layout.py, tests/test_doctor_sldb_layout.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests deskops/bootstrap.py
deskops/cli/commands/core.py
deskops/cli/commands/doctor.py
deskops/sldb_layout.py
tests/test_doctor_sldb_layout.py

---
sldb:
  by: agent
  at: '2026-11-24T18:18:18Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: '43b17685326610719574807f78044110330af4b9

  67f55538ddc6ce8bb025ab49f928e3aa9eaeb91c'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p@sha256:49da69f2b1db80704997c2c7309ea8d5123514845f0d7eb1110d888f77f82a9f
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 022b2d3406b4245191fad3f96d522360feed5e95cdb4ec66b8b8ff0923676963
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 43b17685326610719574807f78044110330af4b9

  67f55538ddc6ce8bb025ab49f928e3aa9eaeb91c'
# ISO 8601 timestamp
created_at: '2026-11-22T15:03:05.893562+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T15:03:05.893562+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence commit of task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 43b17685326610719574807f78044110330af4b9, 67f55538ddc6ce8bb025ab49f928e3aa9eaeb91c

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 43b17685326610719574807f78044110330af4b9
67f55538ddc6ce8bb025ab49f928e3aa9eaeb91c

---
sldb:
  by: agent
  at: '2026-11-22T00:18:49Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-cc36-commands-doctor

  materialization-doctor-deskops-cli-commands-doctor-py

  materialization-doctor-deskops-doctor-findings-py

  materialization-doctor-tests-test-doctor-lost-receipts-py

  materialization-post-hooks-doctor-seeds'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada@sha256:bd572673b5989cc38db6fb86882b88f4364b77ab4a33850866907013534a3a4e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 1134ce07b3f18218134f09d02832f6b73e80fbd964b761d28e773a1679976db0
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-cc36-commands-doctor

  materialization-doctor-deskops-cli-commands-doctor-py

  materialization-doctor-deskops-doctor-findings-py

  materialization-doctor-tests-test-doctor-lost-receipts-py

  materialization-post-hooks-doctor-seeds'
# ISO 8601 timestamp
created_at: '2026-11-22T00:18:37.502179+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T00:18:37.502179+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cc36-commands-doctor, materialization-doctor-deskops-cli-commands-doctor-py, materialization-doctor-deskops-doctor-findings-py, materialization-doctor-tests-test-doctor-lost-receipts-py, materialization-post-hooks-doctor-seeds

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-cc36-commands-doctor
materialization-doctor-deskops-cli-commands-doctor-py
materialization-doctor-deskops-doctor-findings-py
materialization-doctor-tests-test-doctor-lost-receipts-py
materialization-post-hooks-doctor-seeds

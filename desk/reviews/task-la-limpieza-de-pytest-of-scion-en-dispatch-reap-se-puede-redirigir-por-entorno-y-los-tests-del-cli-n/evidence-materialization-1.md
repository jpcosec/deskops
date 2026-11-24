---
sldb:
  by: agent
  at: '2026-11-23T19:31:13Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-dispatch-deskops-dispatch-py

  materialization-dispatch-paralelo-deskops-dispatch-py

  materialization-dispatch-paralelo-tests-test-dispatch-py

  materialization-dispatch-tests-test-dispatch-py

  materialization-integrate-deskops-dispatch-py

  materialization-integrate-tests-test-dispatch-py

  materialization-runtime-deskops-dispatch-py

  materialization-runtime-tests-test-dispatch-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n@sha256:200d68e3a73b4ed03b1b90f3cc1aca0c63720dfcdef9118750f4c322c14e4362
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 0ee0decc660bedde10194fbcbeba015fd3392c679fe6de9d7cc12e2aec20556f
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-dispatch-deskops-dispatch-py

  materialization-dispatch-paralelo-deskops-dispatch-py

  materialization-dispatch-paralelo-tests-test-dispatch-py

  materialization-dispatch-tests-test-dispatch-py

  materialization-integrate-deskops-dispatch-py

  materialization-integrate-tests-test-dispatch-py

  materialization-runtime-deskops-dispatch-py

  materialization-runtime-tests-test-dispatch-py'
# ISO 8601 timestamp
created_at: '2026-11-23T15:12:06.472018+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T15:12:06.472018+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-dispatch-deskops-dispatch-py, materialization-dispatch-paralelo-deskops-dispatch-py, materialization-dispatch-paralelo-tests-test-dispatch-py, materialization-dispatch-tests-test-dispatch-py, materialization-integrate-deskops-dispatch-py, materialization-integrate-tests-test-dispatch-py, materialization-runtime-deskops-dispatch-py, materialization-runtime-tests-test-dispatch-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-dispatch-deskops-dispatch-py
materialization-dispatch-paralelo-deskops-dispatch-py
materialization-dispatch-paralelo-tests-test-dispatch-py
materialization-dispatch-tests-test-dispatch-py
materialization-integrate-deskops-dispatch-py
materialization-integrate-tests-test-dispatch-py
materialization-runtime-deskops-dispatch-py
materialization-runtime-tests-test-dispatch-py

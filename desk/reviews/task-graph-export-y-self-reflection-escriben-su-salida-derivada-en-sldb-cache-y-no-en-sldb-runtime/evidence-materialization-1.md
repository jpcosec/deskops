---
sldb:
  by: agent
  at: '2026-11-24T18:04:44Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-cc30-tests-test-output-goldens

  materialization-graph-deskops-graph-export-py

  materialization-graph-deskops-graph-paths-py

  materialization-graph-deskops-graph-self-reflection-py

  materialization-graph-tests-fixtures-golden-graph-snapshot-kg-json

  materialization-graph-tests-fixtures-golden-self-reflection-findings-json

  materialization-graph-tests-test-graph-self-reflection-py

  materialization-graph-tests-test-graph-snapshot-py

  materialization-graph-tests-test-output-goldens-py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime@sha256:c699392b1c24814f3b6d772f858a73f39896c317471b74cd87a735329dcc04e7
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 5a4f74df4d2ce209b2322958046dbbb27e1ef04b7be15196ff006acef8c627d1
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-cc30-tests-test-output-goldens

  materialization-graph-deskops-graph-export-py

  materialization-graph-deskops-graph-paths-py

  materialization-graph-deskops-graph-self-reflection-py

  materialization-graph-tests-fixtures-golden-graph-snapshot-kg-json

  materialization-graph-tests-fixtures-golden-self-reflection-findings-json

  materialization-graph-tests-test-graph-self-reflection-py

  materialization-graph-tests-test-graph-snapshot-py

  materialization-graph-tests-test-output-goldens-py'
# ISO 8601 timestamp
created_at: '2026-11-21T21:56:51.295922+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T21:56:51.295922+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cc30-tests-test-output-goldens, materialization-graph-deskops-graph-export-py, materialization-graph-deskops-graph-paths-py, materialization-graph-deskops-graph-self-reflection-py, materialization-graph-tests-fixtures-golden-graph-snapshot-kg-json, materialization-graph-tests-fixtures-golden-self-reflection-findings-json, materialization-graph-tests-test-graph-self-reflection-py, materialization-graph-tests-test-graph-snapshot-py, materialization-graph-tests-test-output-goldens-py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-cc30-tests-test-output-goldens
materialization-graph-deskops-graph-export-py
materialization-graph-deskops-graph-paths-py
materialization-graph-deskops-graph-self-reflection-py
materialization-graph-tests-fixtures-golden-graph-snapshot-kg-json
materialization-graph-tests-fixtures-golden-self-reflection-findings-json
materialization-graph-tests-test-graph-self-reflection-py
materialization-graph-tests-test-graph-snapshot-py
materialization-graph-tests-test-output-goldens-py

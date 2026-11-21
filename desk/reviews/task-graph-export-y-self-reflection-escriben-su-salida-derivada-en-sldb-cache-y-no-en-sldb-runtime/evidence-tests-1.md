---
sldb:
  by: agent
  at: '2026-11-21T21:56:52Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: 'deskops/graph/export.py

  deskops/graph/paths.py

  deskops/graph/self_reflection.py

  tests/test_graph_self_reflection.py

  tests/test_graph_snapshot.py

  tests/test_output_goldens.py'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime@sha256:c699392b1c24814f3b6d772f858a73f39896c317471b74cd87a735329dcc04e7
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: f586649bd1e811efd075709e3bfaa51b6d9cd5c565e203c7ae6e7cd7c8e46f4d
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests deskops/graph/export.py

  deskops/graph/paths.py

  deskops/graph/self_reflection.py

  tests/test_graph_self_reflection.py

  tests/test_graph_snapshot.py

  tests/test_output_goldens.py'
# ISO 8601 timestamp
created_at: '2026-11-21T21:56:51.295922+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T21:56:51.295922+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: deskops/graph/export.py, deskops/graph/paths.py, deskops/graph/self_reflection.py, tests/test_graph_self_reflection.py, tests/test_graph_snapshot.py, tests/test_output_goldens.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests deskops/graph/export.py
deskops/graph/paths.py
deskops/graph/self_reflection.py
tests/test_graph_self_reflection.py
tests/test_graph_snapshot.py
tests/test_output_goldens.py

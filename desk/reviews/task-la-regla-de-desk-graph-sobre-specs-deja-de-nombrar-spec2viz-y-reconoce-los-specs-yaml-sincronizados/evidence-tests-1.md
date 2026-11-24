---
sldb:
  by: agent
  at: '2026-11-24T18:11:22Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados-evidence-tests-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: tests/test_graph_extract_sources.py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados@sha256:426e382fcf394616c5ca95f401fee6df593d1929086b825b0df9433e5ddabc26
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 45a139720b955cf808729a7216a9db7ff84d549ae1b639f786699398da283d8e
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/test_graph_extract_sources.py'
# ISO 8601 timestamp
created_at: '2026-11-16T20:45:44.953952+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T20:45:44.953952+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence tests of task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/test_graph_extract_sources.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/test_graph_extract_sources.py

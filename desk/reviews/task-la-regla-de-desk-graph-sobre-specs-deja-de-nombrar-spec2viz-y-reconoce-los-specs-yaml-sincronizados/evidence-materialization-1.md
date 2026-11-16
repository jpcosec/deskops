---
sldb:
  by: agent
  at: '2026-11-16T20:45:52Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-closeout-graph-desk-config

  materialization-closeout-graph-snapshot

  materialization-extract-sources-declared-targets

  materialization-graph-extract-sources-unit-tests'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados@sha256:426e382fcf394616c5ca95f401fee6df593d1929086b825b0df9433e5ddabc26
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: c6b6c90f3a1a0cc0d0e374d6e421b4724b3aa92bfc7fad3f99c40297fac38a99
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-closeout-graph-desk-config

  materialization-closeout-graph-snapshot

  materialization-extract-sources-declared-targets

  materialization-graph-extract-sources-unit-tests'
# ISO 8601 timestamp
created_at: '2026-11-16T20:45:44.953952+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T20:45:44.953952+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-closeout-graph-desk-config, materialization-closeout-graph-snapshot, materialization-extract-sources-declared-targets, materialization-graph-extract-sources-unit-tests

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-closeout-graph-desk-config
materialization-closeout-graph-snapshot
materialization-extract-sources-declared-targets
materialization-graph-extract-sources-unit-tests

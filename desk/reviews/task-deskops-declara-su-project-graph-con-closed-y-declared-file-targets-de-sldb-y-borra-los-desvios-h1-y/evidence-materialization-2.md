---
sldb:
  by: agent
  at: '2026-11-24T17:49:41Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y-evidence-materialization-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-chequeos-del-grafo-del-desk

  materialization-closeout-graph-desk-config

  materialization-closeout-graph-snapshot

  materialization-extract-sources-declared-targets

  materialization-tests-de-aristas-declaradas-del-grafo

  materialization-tests-de-los-chequeos-del-grafo

  materialization-tests-del-cli-del-grafo'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y@sha256:4f03ef7ed3394a57eeb8bc9b956da103a5aa949ec5f46ac272e3bdae308b2c16
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: d7269fd87780621900614a3136fcaf950a546925cf3f87120079e9a98836e816
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-chequeos-del-grafo-del-desk

  materialization-closeout-graph-desk-config

  materialization-closeout-graph-snapshot

  materialization-extract-sources-declared-targets

  materialization-tests-de-aristas-declaradas-del-grafo

  materialization-tests-de-los-chequeos-del-grafo

  materialization-tests-del-cli-del-grafo'
# ISO 8601 timestamp
created_at: '2026-11-17T11:17:26.384993+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T11:17:26.384993+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-chequeos-del-grafo-del-desk, materialization-closeout-graph-desk-config, materialization-closeout-graph-snapshot, materialization-extract-sources-declared-targets, materialization-tests-de-aristas-declaradas-del-grafo, materialization-tests-de-los-chequeos-del-grafo, materialization-tests-del-cli-del-grafo

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-chequeos-del-grafo-del-desk
materialization-closeout-graph-desk-config
materialization-closeout-graph-snapshot
materialization-extract-sources-declared-targets
materialization-tests-de-aristas-declaradas-del-grafo
materialization-tests-de-los-chequeos-del-grafo
materialization-tests-del-cli-del-grafo

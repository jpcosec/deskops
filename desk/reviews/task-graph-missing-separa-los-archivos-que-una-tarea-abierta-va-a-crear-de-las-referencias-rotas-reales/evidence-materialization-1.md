---
sldb:
  by: agent
  at: '2026-11-24T18:05:19Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas-reales-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-chequeos-del-grafo-del-desk

  materialization-graph-deskops-cli-commands-graph-py

  materialization-graph-deskops-graph-checks-py

  materialization-graph-tests-test-graph-checks-py

  materialization-graph-tests-test-graph-declared-edges-py

  materialization-tests-de-aristas-declaradas-del-grafo

  materialization-tests-de-los-chequeos-del-grafo'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas-reales@sha256:b51303590b87c5ee1ba91d8df586cce62a7fdf5e789f6dab2e07ba30fbb7e43a
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 1d4d42ec717eb5dbd8da9aed762916b021c0fea825bc5999e70cd4bad5105355
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-chequeos-del-grafo-del-desk

  materialization-graph-deskops-cli-commands-graph-py

  materialization-graph-deskops-graph-checks-py

  materialization-graph-tests-test-graph-checks-py

  materialization-graph-tests-test-graph-declared-edges-py

  materialization-tests-de-aristas-declaradas-del-grafo

  materialization-tests-de-los-chequeos-del-grafo'
# ISO 8601 timestamp
created_at: '2026-11-22T19:54:21.060612+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T19:54:21.060612+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas-reales

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-chequeos-del-grafo-del-desk, materialization-graph-deskops-cli-commands-graph-py, materialization-graph-deskops-graph-checks-py, materialization-graph-tests-test-graph-checks-py, materialization-graph-tests-test-graph-declared-edges-py, materialization-tests-de-aristas-declaradas-del-grafo, materialization-tests-de-los-chequeos-del-grafo

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-chequeos-del-grafo-del-desk
materialization-graph-deskops-cli-commands-graph-py
materialization-graph-deskops-graph-checks-py
materialization-graph-tests-test-graph-checks-py
materialization-graph-tests-test-graph-declared-edges-py
materialization-tests-de-aristas-declaradas-del-grafo
materialization-tests-de-los-chequeos-del-grafo

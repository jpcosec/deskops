---
sldb:
  by: agent
  at: '2026-11-23T19:06:05Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-que-ahora-es-nodo-del-grafo-de-sldb-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-cc30-services-closure

  materialization-closeout-gates-changelog

  materialization-materializa-recibos-de-evidencia-cc33a-en-services-closure

  materialization-resolved-by-services-closure

  materialization-verify-directorio-nodo-closure'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-que-ahora-es-nodo-del-grafo-de-sldb@sha256:a06181a800077dec3a9aeaa26fc001e750bc5848ce59e6861b7ca663dc5e9571
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 4c520d8b291dd62637bcbdcce9d93acaee432e67263db8a384839ac8bca25515
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-cc30-services-closure

  materialization-closeout-gates-changelog

  materialization-materializa-recibos-de-evidencia-cc33a-en-services-closure

  materialization-resolved-by-services-closure

  materialization-verify-directorio-nodo-closure'
# ISO 8601 timestamp
created_at: '2026-11-19T14:54:54.923232+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T14:54:54.923232+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-que-ahora-es-nodo-del-grafo-de-sldb

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cc30-services-closure, materialization-closeout-gates-changelog, materialization-materializa-recibos-de-evidencia-cc33a-en-services-closure, materialization-resolved-by-services-closure, materialization-verify-directorio-nodo-closure

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-cc30-services-closure
materialization-closeout-gates-changelog
materialization-materializa-recibos-de-evidencia-cc33a-en-services-closure
materialization-resolved-by-services-closure
materialization-verify-directorio-nodo-closure

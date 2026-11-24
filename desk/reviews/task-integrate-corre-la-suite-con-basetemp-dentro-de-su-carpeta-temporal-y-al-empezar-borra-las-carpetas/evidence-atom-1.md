---
sldb:
  by: agent
  at: '2026-11-24T18:06:37Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas-evidence-atom-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: atom
# kind evidence only: what the producer verified, one item per line
value: atom-integrate-corre-la-suite-con-basetemp-propio-y-limpia-temporales-de-corridas-muertas
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas@sha256:405d06862240cfa1110fd232b161f017102676154df583a5a34d5685600d8ebe
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 4a11b8d61d134bb4fdd396081a0a00f4b13bfddcf1ebe6afad2e5d27e9a57b98
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: atom atom-integrate-corre-la-suite-con-basetemp-propio-y-limpia-temporales-de-corridas-muertas'
# ISO 8601 timestamp
created_at: '2026-11-23T06:15:54.967416+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T06:15:54.967416+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence atom of task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked atom: atom-integrate-corre-la-suite-con-basetemp-propio-y-limpia-temporales-de-corridas-muertas

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: atom atom-integrate-corre-la-suite-con-basetemp-propio-y-limpia-temporales-de-corridas-muertas

---
sldb:
  by: agent
  at: '2026-11-18T22:20:34Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-los-contenedores-scion-de-deskops-traen-un-python-que-puede-correr-los-tests-del-workspace-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: materialization-cc35a-runtime-scion
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-los-contenedores-scion-de-deskops-traen-un-python-que-puede-correr-los-tests-del-workspace@sha256:66356700a28e2561dede2678b3306923926faf09936354714cfe6ee83bc747ea
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: aa5722bf8a8851eab84e7e8cbe7a700cff2880dc28672694b27eb25034c51cf8
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-cc35a-runtime-scion'
# ISO 8601 timestamp
created_at: '2026-11-18T22:20:21.150047+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-18T22:20:21.150047+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-los-contenedores-scion-de-deskops-traen-un-python-que-puede-correr-los-tests-del-workspace

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cc35a-runtime-scion

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-cc35a-runtime-scion

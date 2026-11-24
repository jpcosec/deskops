---
sldb:
  by: agent
  at: '2026-11-24T17:56:20Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error-reproduction-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: reproduction
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error@sha256:1fadc09bd5e07d955a98a04eacf681ea178a6a10616271a69d1d417f1d4903d2
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: human
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 0ac5cec42f4558779eacd8477863ddd917c38b9b23e61db1d6ba39b8a08ebd00
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Coordinador: reproduccion verificada en runs/subagents/repro-holds-20261117/repro.log
  (gate task_activates con holds true y finding de nivel error). Atribucion a deskops
  aceptada: TaskService._lifecycle_gates (deskops/services/tasks.py) calcula holds
  solo con la condicion de la arista e ignora los findings; sin nota a sldb ni xfail.
  Fase 2: el arreglo va en _lifecycle_gates, para que show task, next y view task
  coincidan (holds false si el gate tiene al menos un finding de nivel error); view.py
  solo si hace falta. Se amplia files con deskops/services/tasks.py.'
# ISO 8601 timestamp
created_at: '2026-11-17T15:05:24.397089+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T15:07:29.579873+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Reproduction review of task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error

## Summary

_Summarize what was reviewed and the evidence this receipt records._

reproduction receipt recorded by deskops; evidence: runs/subagents/repro-holds-20261117/attribution.md, runs/subagents/repro-holds-20261117/repro.log, runs/subagents/repro-holds-20261117/repro.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Coordinador: reproduccion verificada en runs/subagents/repro-holds-20261117/repro.log (gate task_activates con holds true y finding de nivel error). Atribucion a deskops aceptada: TaskService._lifecycle_gates (deskops/services/tasks.py) calcula holds solo con la condicion de la arista e ignora los findings; sin nota a sldb ni xfail. Fase 2: el arreglo va en _lifecycle_gates, para que show task, next y view task coincidan (holds false si el gate tiene al menos un finding de nivel error); view.py solo si hace falta. Se amplia files con deskops/services/tasks.py.

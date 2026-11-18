---
sldb:
  by: agent
  at: '2026-11-18T12:44:27Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-cli-help-speaks-the-declared-evidence-workflow

  materialization-cli-tests-exercise-the-real-command-surface

  materialization-closeout-gates-operator-manual

  materialization-deskops-ui-view-registration

  materialization-host-queue-config

  materialization-registro-de-comandos-declara-atoms-citations-como-mutante

  materialization-rg-tests-test-cli-grammar'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip@sha256:6d13b90fb29778f0c642d7e6e98926204889c04ef2cdd4d4b988b5fcaa3bf78f
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: d882d3ecba28dde9c157d8c3ae3d3d9359b7d672ac706902c1cc45a26abd91db
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: rejected
reason: Changed file has no atom/materialization link and no routed follow-up reference.
# ISO 8601 timestamp
created_at: '2026-11-18T12:44:03.556603+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-18T12:44:03.556603+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence materialization of task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cli-help-speaks-the-declared-evidence-workflow, materialization-cli-tests-exercise-the-real-command-surface, materialization-closeout-gates-operator-manual, materialization-deskops-ui-view-registration, materialization-host-queue-config, materialization-registro-de-comandos-declara-atoms-citations-como-mutante, materialization-rg-tests-test-cli-grammar

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict rejected: Changed file has no atom/materialization link and no routed follow-up reference.

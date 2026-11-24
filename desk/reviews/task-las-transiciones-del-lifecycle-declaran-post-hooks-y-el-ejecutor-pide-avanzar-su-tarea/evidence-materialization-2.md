---
sldb:
  by: agent
  at: '2026-11-24T18:12:57Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-las-transiciones-del-lifecycle-declaran-post-hooks-y-el-ejecutor-pide-avanzar-su-tarea-evidence-materialization-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-cc32-deskops-lifecycle

  materialization-cc35a-runtime-scion

  materialization-cc37-deskops-lifecycle

  materialization-closeout-gates-operator-manual

  materialization-closeout-graph-lifecycle-transitions

  materialization-forced-advance-never-closes

  materialization-post-hooks-doctor-seeds

  materialization-post-hooks-runner

  materialization-post-hooks-tests

  materialization-scion-autonomy-tests'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-las-transiciones-del-lifecycle-declaran-post-hooks-y-el-ejecutor-pide-avanzar-su-tarea@sha256:438ba828fd4aec3fd65505d4853eaa803085facf600aae8472167f8bcafb0208
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 3a5e6da61a42f47d6d83e7d6af13489577f34fdac985fc5ddff32eba82cbbfc9
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-cc32-deskops-lifecycle

  materialization-cc35a-runtime-scion

  materialization-cc37-deskops-lifecycle

  materialization-closeout-gates-operator-manual

  materialization-closeout-graph-lifecycle-transitions

  materialization-forced-advance-never-closes

  materialization-post-hooks-doctor-seeds

  materialization-post-hooks-runner

  materialization-post-hooks-tests

  materialization-scion-autonomy-tests'
# ISO 8601 timestamp
created_at: '2026-11-17T23:04:31.407831+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T23:04:31.407831+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-las-transiciones-del-lifecycle-declaran-post-hooks-y-el-ejecutor-pide-avanzar-su-tarea

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-cc32-deskops-lifecycle, materialization-cc35a-runtime-scion, materialization-cc37-deskops-lifecycle, materialization-closeout-gates-operator-manual, materialization-closeout-graph-lifecycle-transitions, materialization-forced-advance-never-closes, materialization-post-hooks-doctor-seeds, materialization-post-hooks-runner, materialization-post-hooks-tests, materialization-scion-autonomy-tests

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-cc32-deskops-lifecycle
materialization-cc35a-runtime-scion
materialization-cc37-deskops-lifecycle
materialization-closeout-gates-operator-manual
materialization-closeout-graph-lifecycle-transitions
materialization-forced-advance-never-closes
materialization-post-hooks-doctor-seeds
materialization-post-hooks-runner
materialization-post-hooks-tests
materialization-scion-autonomy-tests

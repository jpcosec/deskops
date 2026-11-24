---
sldb:
  by: agent
  at: '2026-11-24T17:58:09Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise-evidence-materialization-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: materialization
# kind evidence only: what the producer verified, one item per line
value: 'materialization-closeout-gates-changelog

  materialization-closeout-gates-operator-manual

  materialization-cola-sigue-tras-retry-docs-operator-manual-md

  materialization-dispatch-deskops-dispatch-py

  materialization-dispatch-docs-operator-manual-md

  materialization-dispatch-paralelo-deskops-dispatch-py

  materialization-dispatch-paralelo-docs-operator-manual-md

  materialization-dispatch-paralelo-tests-test-dispatch-py

  materialization-dispatch-tests-test-dispatch-py

  materialization-merge-driver-docs-operator-manual-md

  materialization-retry-exit-codes-operator-manual

  materialization-workflow-docs-operator-manual-md'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise@sha256:6fd5df542b50378fa4888010376274038e2c5a7aa632f2b5b860fe8ffd69c399
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 6698795a94271d3ec92e118c3d5061d11a8398ab98992e4092c4d204109fc819
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: materialization materialization-closeout-gates-changelog

  materialization-closeout-gates-operator-manual

  materialization-cola-sigue-tras-retry-docs-operator-manual-md

  materialization-dispatch-deskops-dispatch-py

  materialization-dispatch-docs-operator-manual-md

  materialization-dispatch-paralelo-deskops-dispatch-py

  materialization-dispatch-paralelo-docs-operator-manual-md

  materialization-dispatch-paralelo-tests-test-dispatch-py

  materialization-dispatch-tests-test-dispatch-py

  materialization-merge-driver-docs-operator-manual-md

  materialization-retry-exit-codes-operator-manual

  materialization-workflow-docs-operator-manual-md'
# ISO 8601 timestamp
created_at: '2026-11-20T18:18:14.663098+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-20T18:18:14.663098+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence materialization of task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked materialization: materialization-closeout-gates-changelog, materialization-closeout-gates-operator-manual, materialization-cola-sigue-tras-retry-docs-operator-manual-md, materialization-dispatch-deskops-dispatch-py, materialization-dispatch-docs-operator-manual-md, materialization-dispatch-paralelo-deskops-dispatch-py, materialization-dispatch-paralelo-docs-operator-manual-md, materialization-dispatch-paralelo-tests-test-dispatch-py, materialization-dispatch-tests-test-dispatch-py, materialization-merge-driver-docs-operator-manual-md, materialization-retry-exit-codes-operator-manual, materialization-workflow-docs-operator-manual-md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: materialization materialization-closeout-gates-changelog
materialization-closeout-gates-operator-manual
materialization-cola-sigue-tras-retry-docs-operator-manual-md
materialization-dispatch-deskops-dispatch-py
materialization-dispatch-docs-operator-manual-md
materialization-dispatch-paralelo-deskops-dispatch-py
materialization-dispatch-paralelo-docs-operator-manual-md
materialization-dispatch-paralelo-tests-test-dispatch-py
materialization-dispatch-tests-test-dispatch-py
materialization-merge-driver-docs-operator-manual-md
materialization-retry-exit-codes-operator-manual
materialization-workflow-docs-operator-manual-md

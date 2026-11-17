---
sldb:
  by: agent
  at: '2026-11-17T02:31:34Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-deskops-workspace-documental-ws32-node-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: node
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: ''
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: desk/drawer/plans/workspace-documental/dag.yaml#node:WS32
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/node-workspace-documental/context-review/deskops-workspace-documental/WS32/2b1103cd938e033e324866e2489ae2af3b38959864fad0cdde67a08fdebdca51/attempt-1
input_sha256: 2b1103cd938e033e324866e2489ae2af3b38959864fad0cdde67a08fdebdca51
output_sha256: e67ba9d28fb0f6d44c721001218074486e046e29acdcd6b6c8cbe1d0c0e81e81
# pending | accepted | rejected | incomplete
verdict: pending
reason: ''
# ISO 8601 timestamp
created_at: '2026-11-17T02:31:31.765622+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: ''
disposed_by: ''
# e.g. workspace:desk
tags:
- workspace:desk
---

# Node review of WS32

## Summary

_Summarize what was reviewed and the evidence this receipt records._

node review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/node-workspace-documental/context-review/deskops-workspace-documental/WS32/2b1103cd938e033e324866e2489ae2af3b38959864fad0cdde67a08fdebdca51/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

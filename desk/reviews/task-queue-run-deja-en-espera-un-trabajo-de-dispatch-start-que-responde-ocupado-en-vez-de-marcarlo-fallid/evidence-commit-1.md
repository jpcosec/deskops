---
sldb:
  by: agent
  at: '2026-11-23T19:38:10Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid-evidence-commit-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: commit
# kind evidence only: what the producer verified, one item per line
value: '00ec6562a296469669c78b886048b1761c27c8e0

  e893a6313190df132fe381215e08506c57de3137'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid@sha256:a9d1a90b4a4ef385713717fb22eb454dbd6dc611d0bb254c47ac1c4889ae110e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 62d425d35082059bf385a795f795186ec339aaed49c5387887c2fd5304b88b4b
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: commit 00ec6562a296469669c78b886048b1761c27c8e0

  e893a6313190df132fe381215e08506c57de3137'
# ISO 8601 timestamp
created_at: '2026-11-19T13:28:28.686277+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T13:28:28.686277+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Closeout evidence commit of task-queue-run-deja-en-espera-un-trabajo-de-dispatch-start-que-responde-ocupado-en-vez-de-marcarlo-fallid

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked commit: 00ec6562a296469669c78b886048b1761c27c8e0, e893a6313190df132fe381215e08506c57de3137

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: commit 00ec6562a296469669c78b886048b1761c27c8e0
e893a6313190df132fe381215e08506c57de3137

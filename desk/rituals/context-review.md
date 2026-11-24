---
sldb:
  by: agent
  at: '2026-11-24T02:16:54Z'
  authority: generated
  via: save_document_payload
# ritual-xxx
id: ritual-context-review
# Ordered prose steps; not document references
steps:
- '1. Map the multilevel DAG: root, packages, leaves and dependency edges. Start with
  the question at the current node; review every node and its edges, not only the
  root.'
- '2. Build the reviewed input with deskops review preflight <task> (TaskDoc-only)
  or deskops review bundle <task> (cold bundle); for a plan node use deskops review
  node <plan> <node-id>. The builder saves input.md as an explicit concatenation of
  FILE:<path> headers and UTF-8 texts in documented order and hashes the exact saved
  bytes with SHA-256. Evidence directory: runs/subagents/<run-dir>/context-review/<key>/<sha>/attempt-<n>/.'
- 3. Each attempt is a new ephemeral reviewer process launched by deskops review with
  the isolation flags of its RuntimeProfileDoc. The default engine is the runtime-pi-deepseek-flash
  profile under desk/runtimes/; --engine <profile> picks another RuntimeProfileDoc.
  Do not run the reviewer by hand. The command, profile and reason for cheap selection
  are recorded in the run evidence and the receipt. No --continue or --resume.
- '4. Instruct the non-executing reviewer to restate the objective and scope, enumerate
  ambiguities and produce a detailed dry-run: which supplied sources it would read,
  proposed edits, dependency/interface implications, commands it would run later and
  expected validation outcomes. It may name commands but must not run them, inspect
  unsupplied sources or edit files.'
- 5. deskops review writes the reviewer output and a receipt (ReviewDoc) under desk/reviews/<task>/.
  Compare it with owner intent, including missing guardrails and required textual
  corrections, then record the disposition with deskops review dispose <review-id>
  --verdict accepted|rejected --reason <why>. A word such as APTO is never sufficient.
  Transport/quota/unavailable-model failures are recorded as technical (verdict incomplete)
  and kept separate from comprehension findings; retry an available cheap model with
  explicit reason (--force --reason when the input already has a good attempt), without
  expert rescue.
- 6. Use misunderstandings as feedback on the brief. Correct its text; split oversized
  or ambiguous nodes recursively into coherent children and explicit dependency edges.
  Review root, packages and all leaves, plus contracts across edges. Do not execute
  while ambiguity remains unresolved.
- 7. Retry the revised explicit input in a new process, with no prior review or oral
  fixes injected. A new input or changed dependency contract invalidates affected
  reviews, including dependent nodes whose supplied contract changed; unrelated typos
  do not revoke every review. Preserve previous attempts for traceability.
- '8. Before Executor dispatch, run two separate cheap roles under this protocol:
  deskops review preflight <task> (TaskDoc-only reformulation) and deskops review
  bundle <task> (cold-bundle coverage with TaskDoc, routed instructions/rituals, bound
  pills, linked atoms/files and validation targets supplied explicitly). The coordinator
  disposes both receipts with deskops review dispose before dispatch; deskops review
  status <task> shows whether each is accepted for the current input.'
- 9. Only reviewed ready leaves may enter the execution ritual. Expert council review
  of design, an Executor implementation and a fresh independent Tester are separate
  gates; none substitutes for cheap comprehension or human product decisions.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- topic:rituals
- topic:context-review
---

# Cheap recursive zero-context brief review

## Purpose

_Explain why this ritual exists._

Test whether a cheap isolated reviewer understands the written question before planning, promotion or execution. Durable rule: [source atom](../atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md). This ritual is a documentary gate; it adds no lifecycle state or runtime enforcement.

## Trigger

_State when this ritual should start._

Run while drafting or revising a plan, root, package or leaf, before promotion or execution and again when its explicit input or dependency contract changes.

## Preconditions

_List the conditions that must hold before running the ritual._

- The coordinator names the node, exact versioned brief, explicit dependencies/interfaces and expected intent. Large nodes can still be drafts; they need not be promoted to receive review.
- The supplied context is minimal: exact brief plus only necessary explicitly supplied references, with a documented order and paths. No chat history, previous outputs, oral corrections, persistent memory or automatically loaded context/skills.
- A cheap available provider/model is selected with a recorded reason and profile. Do not claim global minimum price without measurement; do not replace a failed cheap reviewer with an expert to obtain approval.

## Validation

_List the checks that prove the ritual was performed correctly._

- Every required root/package/leaf review has exact input/hash, provider/model/profile and selection reason, command/isolation evidence, reformulation, ambiguities, detailed non-executing dry-run, coordinator comparison and required changes.
- The coordinator compares understanding with intent rather than accepting a verdict token; no unresolved ambiguity remains before execution.
- Each attempt used a new process without history, memory, automatic skills/context or reviewer tools. TaskDoc-only and cold-bundle evidence remain separate.
- Changed node inputs and dependency contracts invalidate the affected reviews; review coverage is explicit by node/revision, never inferred from council approval or plan structure.

## Failure Modes

_List common mistakes this ritual prevents._

- Asking an expert council to compensate for an unclear brief, or treating APTO/structural PASS as comprehension or execution authorization.
- Reviewing only the root or whole large DAG and claiming every descendant passed.
- Letting a reviewer execute the dry-run or loading implicit chat history, skills, memory or previous corrections.
- Retrying in the same session, fabricating node evidence, or marking pending reviews approved.
- Confusing transport/quota failures with ambiguous intent, or replacing cheap review with execution/testing.

## Completion

_Describe what completion looks like._

For the reviewed node/version, the coordinator has accepted a faithful reformulation and detailed dry-run with no unresolved ambiguity; all required descendant and interface reviews are traceable. This proves brief comprehension only. Promotion, execution, independent testing, product decisions and closeout retain their own gates.

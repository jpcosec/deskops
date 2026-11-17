---
sldb:
  by: agent
  at: '2026-11-17T22:32:42Z'
  authority: generated
  via: save_document_payload
id: atom-automatic-routines-vs-llm-tasks
title: Deterministic checks are not LLM tasks
five_wh_one_plus: how
tags:
- system:deskops
- topic:automation
- topic:workflow
---

# Deterministic checks are not LLM tasks

## Answer

Actions that require semantic judgment belong to LLM/subagent tasks. Deterministic checks over known inputs, such as running touched-surface tests, closeout validation, or phase end-to-end checks, belong to tests, CI, or CLI gates. The routine and hook models of the primitive layer stay retired. What exists now are post-hooks declared on the lifecycle transitions (`attributes.hooks` of a `RelationDoc`, run by `deskops advance task` after it persists the transition): deterministic commands, not tasks for a model.

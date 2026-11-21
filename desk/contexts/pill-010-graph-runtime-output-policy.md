---
sldb:
  by: agent
  at: '2026-11-21T20:41:48Z'
  authority: generated
  via: save_document_payload
# pill-xxx
id: pill-010
# e.g., language:python, library:pydantic
tags:
- system:deskops
- system:sldb
- pill-type:guardrail
- topic:runtime
- topic:drift-control
---

# Guardrail: generated graph output is runtime state

## What

_Define the context or guardrail this pill carries._

Generated graph snapshots and query indexes are runtime artifacts unless a task explicitly promotes a fixture or contract example into versioned test data.

## Why

_Explain why this context matters for safe execution._

Graph outputs can become large, noisy, and stale. Keeping generated outputs in runtime prevents the repository from confusing source knowledge with derived graph projections.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task writes deskops graph snapshot JSON, generated indexes, query results, or self-reflection reports.

## Where

_Name the files, surfaces, or scope this pill applies to._

Generated outputs go to `.sldb_cache/` (ignored by `.gitignore`), the derived root of the sldb store layout (sldb decision c420809c); deskops code takes it from `deskops.graph.paths.DERIVED_ROOT`. Do not write derived outputs under the old `.sldb/runtime/`. Versioned fixtures belong under tests or contracts only when they prove behavior.

## How

_Describe the correct way to apply this guidance._

Separate source specs/adapters from generated graph outputs. Add or update ignore rules when a new runtime path is introduced. Keep small golden fixtures only for tests.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not commit full generated graph snapshots as documentation. Do not use generated graph output as the only source of relation truth.

---
sldb:
  by: agent
  at: '2026-11-17T23:04:03Z'
  authority: generated
  via: create_document
id: materialization-post-hooks-runner
title: post-hooks runner
source_atoms:
- atom-automatic-routines-vs-llm-tasks
target_kind: code
target_identity: deskops/lifecycle_hooks.py
validation:
- pytest -q tests/test_lifecycle_graph.py
tags:
- system:deskops
- topic:lifecycle
---

# post-hooks runner

## Intent

Corre los post-hooks declarados en una transicion del lifecycle como comandos deterministas, con tope de tiempo y log por avance

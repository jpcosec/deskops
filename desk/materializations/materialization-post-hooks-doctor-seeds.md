---
sldb:
  by: agent
  at: '2026-11-17T23:04:10Z'
  authority: generated
  via: create_document
id: materialization-post-hooks-doctor-seeds
title: post-hooks doctor seeds
source_atoms:
- atom-automatic-routines-vs-llm-tasks
target_kind: code
target_identity: deskops/doctor_findings.py
validation:
- pytest -q tests/test_lifecycle_graph.py
tags:
- system:deskops
- topic:lifecycle
---

# post-hooks doctor seeds

## Intent

La comparacion de semillas gestionadas no cuenta attributes.hooks, que pertenece al desk, como deriva

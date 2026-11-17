---
sldb:
  by: agent
  at: '2026-11-17T23:04:17Z'
  authority: generated
  via: create_document
id: materialization-post-hooks-tests
title: post-hooks tests
source_atoms:
- atom-automatic-routines-vs-llm-tasks
target_kind: test
target_identity: tests/test_lifecycle_graph.py
validation:
- pytest -q tests/test_lifecycle_graph.py
tags:
- system:deskops
- topic:lifecycle
---

# post-hooks tests

## Intent

Prueba con comandos reales del sistema que advance corre los post-hooks en orden y que un fallo devuelve la tarea al estado previo

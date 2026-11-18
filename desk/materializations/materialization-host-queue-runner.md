---
sldb:
  by: agent
  at: '2026-11-18T12:45:07Z'
  authority: generated
  via: create_document
id: materialization-host-queue-runner
title: host queue runner
source_atoms:
- atom-automatic-routines-vs-llm-tasks
target_kind: code
target_identity: deskops/queue.py
validation:
- pytest -q tests/test_queue.py
tags:
- system:deskops
- topic:lifecycle
---

# host queue runner

## Intent

La cola del host ejecuta de a uno, con gates de memoria, los trabajos que encolan los post-hooks

---
sldb:
  by: agent
  at: '2026-11-18T07:40:49Z'
  authority: generated
  via: create_document
id: materialization-host-queue-config
title: host queue config
source_atoms:
- atom-automatic-routines-vs-llm-tasks
target_kind: code
target_identity: deskops/config.py
validation:
- pytest -q tests/test_queue.py
tags:
- system:deskops
- topic:lifecycle
---

# host queue config

## Intent

DeskConfig declara los tipos de trabajo de la cola del host (queue_jobs) y sus gates de memoria

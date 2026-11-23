---
sldb:
  by: agent
  at: '2026-11-23T00:11:12Z'
  authority: generated
  via: create_document
id: materialization-queue-deskops-queue-py
title: queue deskops-queue-py
source_atoms:
- atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola
target_kind: code
target_identity: deskops/queue.py
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_queue_cli.py tests/test_command_registry.py
  tests/test_output_goldens.py tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# queue deskops-queue-py

## Intent

materializa en deskops/queue.py el atom atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola

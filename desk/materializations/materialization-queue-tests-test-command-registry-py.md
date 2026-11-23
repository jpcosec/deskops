---
sldb:
  by: agent
  at: '2026-11-23T00:12:30Z'
  authority: generated
  via: create_document
id: materialization-queue-tests-test-command-registry-py
title: queue tests-test_command_registry-py
source_atoms:
- atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola
target_kind: test
target_identity: tests/test_command_registry.py
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_queue_cli.py tests/test_command_registry.py
  tests/test_output_goldens.py tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# queue tests-test_command_registry-py

## Intent

materializa en tests/test_command_registry.py el atom atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola

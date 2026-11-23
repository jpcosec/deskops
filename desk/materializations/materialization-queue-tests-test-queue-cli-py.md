---
sldb:
  by: agent
  at: '2026-11-23T00:12:41Z'
  authority: generated
  via: create_document
id: materialization-queue-tests-test-queue-cli-py
title: queue tests-test_queue_cli-py
source_atoms:
- atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola
target_kind: test
target_identity: tests/test_queue_cli.py
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_queue_cli.py tests/test_command_registry.py
  tests/test_output_goldens.py tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# queue tests-test_queue_cli-py

## Intent

materializa en tests/test_queue_cli.py el atom atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola

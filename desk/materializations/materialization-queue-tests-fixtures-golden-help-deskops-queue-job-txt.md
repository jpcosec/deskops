---
sldb:
  by: agent
  at: '2026-11-23T00:11:45Z'
  authority: generated
  via: create_document
id: materialization-queue-tests-fixtures-golden-help-deskops-queue-job-txt
title: queue tests-fixtures-golden-help-deskops_queue_job-txt
source_atoms:
- atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_queue_job.txt
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_queue_cli.py tests/test_command_registry.py
  tests/test_output_goldens.py tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# queue tests-fixtures-golden-help-deskops_queue_job-txt

## Intent

materializa en tests/fixtures/golden/help/deskops_queue_job.txt el atom atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola

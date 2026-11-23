---
sldb:
  by: agent
  at: '2026-11-23T00:11:23Z'
  authority: generated
  via: create_document
id: materialization-queue-docs-operator-manual-md
title: queue docs-operator-manual-md
source_atoms:
- atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola
target_kind: docs
target_identity: docs/operator-manual.md
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_queue_cli.py tests/test_command_registry.py
  tests/test_output_goldens.py tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# queue docs-operator-manual-md

## Intent

materializa en docs/operator-manual.md el atom atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola

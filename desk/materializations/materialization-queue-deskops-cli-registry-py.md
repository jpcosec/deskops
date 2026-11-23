---
sldb:
  by: agent
  at: '2026-11-23T00:10:50Z'
  authority: generated
  via: create_document
id: materialization-queue-deskops-cli-registry-py
title: queue deskops-cli-registry-py
source_atoms:
- atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola
target_kind: code
target_identity: deskops/cli/registry.py
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_queue_cli.py tests/test_command_registry.py
  tests/test_output_goldens.py tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# queue deskops-cli-registry-py

## Intent

materializa en deskops/cli/registry.py el atom atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola

---
sldb:
  by: agent
  at: '2026-11-23T00:11:01Z'
  authority: generated
  via: create_document
id: materialization-queue-deskops-data-templates-config-json
title: queue deskops-data-templates-config-json
source_atoms:
- atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola
target_kind: code
target_identity: deskops/data/templates/config.json
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_queue_cli.py tests/test_command_registry.py
  tests/test_output_goldens.py tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# queue deskops-data-templates-config-json

## Intent

materializa en deskops/data/templates/config.json el atom atom-deskops-queue-job-set-edita-los-trabajos-de-la-cola

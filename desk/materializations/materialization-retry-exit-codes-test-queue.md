---
sldb:
  by: agent
  at: '2026-11-19T13:28:10Z'
  authority: generated
  via: create_document
id: materialization-retry-exit-codes-test-queue
title: retry exit codes test_queue
source_atoms:
- atom-queue-run-deja-en-pending-un-trabajo-cuyo-codigo-de-salida-esta-en-retry-exit-codes
target_kind: test
target_identity: tests/test_queue.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# retry exit codes test_queue

## Intent

materializa en tests/test_queue.py el atom atom-queue-run-deja-en-pending-un-trabajo-cuyo-codigo-de-salida-esta-en-retry-exit-codes

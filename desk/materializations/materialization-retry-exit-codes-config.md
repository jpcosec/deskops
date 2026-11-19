---
sldb:
  by: agent
  at: '2026-11-19T13:28:01Z'
  authority: generated
  via: create_document
id: materialization-retry-exit-codes-config
title: retry exit codes config
source_atoms:
- atom-queue-run-deja-en-pending-un-trabajo-cuyo-codigo-de-salida-esta-en-retry-exit-codes
target_kind: code
target_identity: deskops/config.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# retry exit codes config

## Intent

materializa en deskops/config.py el atom atom-queue-run-deja-en-pending-un-trabajo-cuyo-codigo-de-salida-esta-en-retry-exit-codes

---
sldb:
  by: agent
  at: '2026-11-19T13:28:19Z'
  authority: generated
  via: create_document
id: materialization-retry-exit-codes-operator-manual
title: retry exit codes operator-manual
source_atoms:
- atom-queue-run-deja-en-pending-un-trabajo-cuyo-codigo-de-salida-esta-en-retry-exit-codes
target_kind: docs
target_identity: docs/operator-manual.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# retry exit codes operator-manual

## Intent

materializa en docs/operator-manual.md el atom atom-queue-run-deja-en-pending-un-trabajo-cuyo-codigo-de-salida-esta-en-retry-exit-codes

---
sldb:
  by: agent
  at: '2026-11-20T01:47:34Z'
  authority: generated
  via: create_document
id: materialization-cola-sigue-tras-retry-deskops-queue-py
title: cola sigue tras retry deskops-queue-py
source_atoms:
- atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien
target_kind: code
target_identity: deskops/queue.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# cola sigue tras retry deskops-queue-py

## Intent

materializa en deskops/queue.py el atom atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien

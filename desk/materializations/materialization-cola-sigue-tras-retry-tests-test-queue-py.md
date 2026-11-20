---
sldb:
  by: agent
  at: '2026-11-20T01:47:51Z'
  authority: generated
  via: create_document
id: materialization-cola-sigue-tras-retry-tests-test-queue-py
title: cola sigue tras retry tests-test_queue-py
source_atoms:
- atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien
target_kind: test
target_identity: tests/test_queue.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# cola sigue tras retry tests-test_queue-py

## Intent

materializa en tests/test_queue.py el atom atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien

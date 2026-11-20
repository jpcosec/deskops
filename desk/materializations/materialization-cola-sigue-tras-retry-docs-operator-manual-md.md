---
sldb:
  by: agent
  at: '2026-11-20T01:47:42Z'
  authority: generated
  via: create_document
id: materialization-cola-sigue-tras-retry-docs-operator-manual-md
title: cola sigue tras retry docs-operator-manual-md
source_atoms:
- atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien
target_kind: docs
target_identity: docs/operator-manual.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py
tags:
- system:deskops
- topic:queue
---

# cola sigue tras retry docs-operator-manual-md

## Intent

materializa en docs/operator-manual.md el atom atom-queue-run-all-saltea-en-esa-corrida-el-trabajo-que-quedo-en-espera-por-retry-y-sigue-con-los-siguien

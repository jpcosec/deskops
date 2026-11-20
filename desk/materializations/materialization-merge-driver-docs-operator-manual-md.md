---
sldb:
  by: agent
  at: '2026-11-20T09:23:03Z'
  authority: generated
  via: create_document
id: materialization-merge-driver-docs-operator-manual-md
title: merge-driver docs-operator-manual-md
source_atoms:
- atom-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk
target_kind: docs
target_identity: docs/operator-manual.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_merge_driver_install.py
tags:
- system:deskops
- topic:merge-driver
---

# merge-driver docs-operator-manual-md

## Intent

materializa en docs/operator-manual.md el atom atom-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk

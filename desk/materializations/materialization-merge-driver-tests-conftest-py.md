---
sldb:
  by: agent
  at: '2026-11-20T09:23:12Z'
  authority: generated
  via: create_document
id: materialization-merge-driver-tests-conftest-py
title: merge-driver tests-conftest-py
source_atoms:
- atom-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk
target_kind: test
target_identity: tests/conftest.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_merge_driver_install.py
tags:
- system:deskops
- topic:merge-driver
---

# merge-driver tests-conftest-py

## Intent

materializa en tests/conftest.py el atom atom-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk

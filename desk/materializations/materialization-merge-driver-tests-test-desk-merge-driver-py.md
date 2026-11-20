---
sldb:
  by: agent
  at: '2026-11-20T09:23:20Z'
  authority: generated
  via: create_document
id: materialization-merge-driver-tests-test-desk-merge-driver-py
title: merge-driver tests-test_desk_merge_driver-py
source_atoms:
- atom-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk
target_kind: test
target_identity: tests/test_desk_merge_driver.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_merge_driver_install.py
tags:
- system:deskops
- topic:merge-driver
---

# merge-driver tests-test_desk_merge_driver-py

## Intent

materializa en tests/test_desk_merge_driver.py el atom atom-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk

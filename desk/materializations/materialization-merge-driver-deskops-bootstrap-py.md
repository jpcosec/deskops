---
sldb:
  by: agent
  at: '2026-11-20T09:22:46Z'
  authority: generated
  via: create_document
id: materialization-merge-driver-deskops-bootstrap-py
title: merge-driver deskops-bootstrap-py
source_atoms:
- atom-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk
target_kind: code
target_identity: deskops/bootstrap.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_merge_driver_install.py
tags:
- system:deskops
- topic:merge-driver
---

# merge-driver deskops-bootstrap-py

## Intent

materializa en deskops/bootstrap.py el atom atom-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk

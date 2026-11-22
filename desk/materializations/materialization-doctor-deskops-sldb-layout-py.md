---
sldb:
  by: agent
  at: '2026-11-22T07:46:45Z'
  authority: generated
  via: create_document
id: materialization-doctor-deskops-sldb-layout-py
title: doctor deskops-sldb_layout-py
source_atoms:
- atom-doctor-e-init-reportan-el-layout-viejo-de-sldb-con-el-remedio-migrate-layout
target_kind: code
target_identity: deskops/sldb_layout.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_sldb_layout.py
  tests/test_doctor_alerts.py tests/test_gitignore_policy.py
tags:
- system:deskops
- topic:doctor
---

# doctor deskops-sldb_layout-py

## Intent

materializa en deskops/sldb_layout.py el atom atom-doctor-e-init-reportan-el-layout-viejo-de-sldb-con-el-remedio-migrate-layout

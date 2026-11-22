---
sldb:
  by: agent
  at: '2026-11-22T07:46:12Z'
  authority: generated
  via: create_document
id: materialization-doctor-readme-md
title: doctor README-md
source_atoms:
- atom-doctor-e-init-reportan-el-layout-viejo-de-sldb-con-el-remedio-migrate-layout
target_kind: docs
target_identity: README.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_sldb_layout.py
  tests/test_doctor_alerts.py tests/test_gitignore_policy.py
tags:
- system:deskops
- topic:doctor
---

# doctor README-md

## Intent

materializa en README.md el atom atom-doctor-e-init-reportan-el-layout-viejo-de-sldb-con-el-remedio-migrate-layout

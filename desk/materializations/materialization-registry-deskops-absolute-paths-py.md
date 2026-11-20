---
sldb:
  by: agent
  at: '2026-11-20T12:15:52Z'
  authority: generated
  via: create_document
id: materialization-registry-deskops-absolute-paths-py
title: registry deskops-absolute_paths-py
source_atoms:
- atom-build-neighbours-de-absolute-paths-resuelve-el-registro-con-resolve-registered-root
target_kind: code
target_identity: deskops/absolute_paths.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_absolute_paths.py
tags:
- system:deskops
- topic:registry
---

# registry deskops-absolute_paths-py

## Intent

materializa en deskops/absolute_paths.py el atom atom-build-neighbours-de-absolute-paths-resuelve-el-registro-con-resolve-registered-root

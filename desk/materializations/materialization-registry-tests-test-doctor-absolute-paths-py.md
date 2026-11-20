---
sldb:
  by: agent
  at: '2026-11-20T12:16:02Z'
  authority: generated
  via: create_document
id: materialization-registry-tests-test-doctor-absolute-paths-py
title: registry tests-test_doctor_absolute_paths-py
source_atoms:
- atom-build-neighbours-de-absolute-paths-resuelve-el-registro-con-resolve-registered-root
target_kind: test
target_identity: tests/test_doctor_absolute_paths.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_absolute_paths.py
tags:
- system:deskops
- topic:registry
---

# registry tests-test_doctor_absolute_paths-py

## Intent

materializa en tests/test_doctor_absolute_paths.py el atom atom-build-neighbours-de-absolute-paths-resuelve-el-registro-con-resolve-registered-root

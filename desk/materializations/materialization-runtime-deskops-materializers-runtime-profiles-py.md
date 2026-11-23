---
sldb:
  by: agent
  at: '2026-11-23T09:10:18Z'
  authority: generated
  via: create_document
id: materialization-runtime-deskops-materializers-runtime-profiles-py
title: runtime deskops-materializers-runtime_profiles-py
source_atoms:
- atom-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-deriva-el-alias-de-model
target_kind: code
target_identity: deskops/materializers/runtime_profiles.py
validation:
- 'pytest -q tests/test_runtime_profiles.py tests/test_scion_runtime.py tests/test_output_goldens.py:
  65 passed en worktree limpio de 89777a0e'
tags:
- system:deskops
- topic:runtime
---

# runtime deskops-materializers-runtime_profiles-py

## Intent

materializa en deskops/materializers/runtime_profiles.py el atom atom-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-deriva-el-alias-de-model

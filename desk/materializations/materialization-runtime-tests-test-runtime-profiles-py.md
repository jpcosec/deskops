---
sldb:
  by: agent
  at: '2026-11-23T09:10:34Z'
  authority: generated
  via: create_document
id: materialization-runtime-tests-test-runtime-profiles-py
title: runtime tests-test_runtime_profiles-py
source_atoms:
- atom-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-deriva-el-alias-de-model
target_kind: test
target_identity: tests/test_runtime_profiles.py
validation:
- 'pytest -q tests/test_runtime_profiles.py tests/test_scion_runtime.py tests/test_output_goldens.py:
  65 passed en worktree limpio de 89777a0e'
tags:
- system:deskops
- topic:runtime
---

# runtime tests-test_runtime_profiles-py

## Intent

materializa en tests/test_runtime_profiles.py el atom atom-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-deriva-el-alias-de-model

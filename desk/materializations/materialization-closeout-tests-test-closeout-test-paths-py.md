---
sldb:
  by: agent
  at: '2026-11-23T20:01:00Z'
  authority: generated
  via: create_document
id: materialization-closeout-tests-test-closeout-test-paths-py
title: closeout tests-test_closeout_test_paths-py
source_atoms:
- atom-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript
target_kind: test
target_identity: tests/test_closeout_test_paths.py
validation:
- 'pytest -n 3 tests/test_closeout_test_paths.py tests/test_closeout_gates.py tests/test_closeout_resolved_by.py
  en worktree limpio de 8c836050: 75 passed'
tags:
- system:deskops
- topic:closeout
---

# closeout tests-test_closeout_test_paths-py

## Intent

materializa en tests/test_closeout_test_paths.py el atom atom-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript

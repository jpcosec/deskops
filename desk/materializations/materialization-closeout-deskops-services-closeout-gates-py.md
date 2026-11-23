---
sldb:
  by: agent
  at: '2026-11-23T20:00:45Z'
  authority: generated
  via: create_document
id: materialization-closeout-deskops-services-closeout-gates-py
title: closeout deskops-services-closeout_gates-py
source_atoms:
- atom-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript
target_kind: code
target_identity: deskops/services/closeout_gates.py
validation:
- 'pytest -n 3 tests/test_closeout_test_paths.py tests/test_closeout_gates.py tests/test_closeout_resolved_by.py
  en worktree limpio de 8c836050: 75 passed'
tags:
- system:deskops
- topic:closeout
---

# closeout deskops-services-closeout_gates-py

## Intent

materializa en deskops/services/closeout_gates.py el atom atom-el-gate-de-tests-del-closeout-acepta-archivos-de-test-de-typescript

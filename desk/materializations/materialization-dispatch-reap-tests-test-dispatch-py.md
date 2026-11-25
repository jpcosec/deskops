---
sldb:
  by: agent
  at: '2026-11-25T03:15:26Z'
  authority: generated
  via: create_document
id: materialization-dispatch-reap-tests-test-dispatch-py
title: dispatch-reap tests-test_dispatch-py
source_atoms:
- atom-el-reap-encola-el-tester-tras-integrar-un-ejecutor
target_kind: test
target_identity: tests/test_dispatch.py
validation:
- pytest -q tests/test_dispatch.py
tags:
- system:deskops
- topic:dispatch-reap
---

# dispatch-reap tests-test_dispatch-py

## Intent

materializa en tests/test_dispatch.py el atom atom-el-reap-encola-el-tester-tras-integrar-un-ejecutor

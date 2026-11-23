---
sldb:
  by: agent
  at: '2026-11-23T10:32:34Z'
  authority: generated
  via: create_document
id: materialization-closeout-tests-test-closeout-py
title: closeout tests-test_closeout-py
source_atoms:
- atom-el-commit-de-cierre-stagea-solo-lo-que-escribio-el-cierre-en-sldb
target_kind: test
target_identity: tests/test_closeout.py
validation:
- 'pytest -n 4 tests/test_closeout*.py tests/test_transaction.py: 236 passed en worktree
  limpio de f629463d'
tags:
- system:deskops
- topic:closeout
---

# closeout tests-test_closeout-py

## Intent

materializa en tests/test_closeout.py el atom atom-el-commit-de-cierre-stagea-solo-lo-que-escribio-el-cierre-en-sldb

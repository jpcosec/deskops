---
sldb:
  by: agent
  at: '2026-11-25T21:15:15Z'
  authority: generated
  via: create_document
id: materialization-closeout-node-tests-tests-test-closeout-test-paths-py
title: closeout-node-tests tests-test_closeout_test_paths-py
source_atoms:
- atom-el-gate-de-tests-del-closeout-acepta-pruebas-de-node
target_kind: test
target_identity: tests/test_closeout_test_paths.py
validation:
- pytest -q tests/test_closeout_test_paths.py
tags:
- system:deskops
- topic:closeout-node-tests
---

# closeout-node-tests tests-test_closeout_test_paths-py

## Intent

materializa en tests/test_closeout_test_paths.py el atom atom-el-gate-de-tests-del-closeout-acepta-pruebas-de-node

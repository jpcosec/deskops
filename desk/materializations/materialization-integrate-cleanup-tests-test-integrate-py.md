---
sldb:
  by: agent
  at: '2026-11-25T05:06:18Z'
  authority: generated
  via: create_document
id: materialization-integrate-cleanup-tests-test-integrate-py
title: integrate-cleanup tests-test_integrate-py
source_atoms:
- atom-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-ya-presentes-en-origin
target_kind: test
target_identity: tests/test_integrate.py
validation:
- PYTHONPATH=. pytest -q tests/ sobre los tests de integrate tocados
tags:
- system:deskops
- topic:integrate-cleanup
---

# integrate-cleanup tests-test_integrate-py

## Intent

materializa en tests/test_integrate.py el atom atom-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-ya-presentes-en-origin

---
sldb:
  by: agent
  at: '2026-11-21T04:34:10Z'
  authority: generated
  via: create_document
id: materialization-integrate-tests-test-integrate-py
title: integrate tests-test_integrate-py
source_atoms:
- atom-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota
target_kind: test
target_identity: tests/test_integrate.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py
tags:
- system:deskops
- topic:integrate
---

# integrate tests-test_integrate-py

## Intent

materializa en tests/test_integrate.py el atom atom-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota

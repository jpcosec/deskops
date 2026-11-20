---
sldb:
  by: agent
  at: '2026-11-20T11:05:24Z'
  authority: generated
  via: create_document
id: materialization-tip-extendido-tests-test-integrate-py
title: tip extendido tests-test_integrate-py
source_atoms:
- atom-integrate-extiende-el-tip-a-head-cuando-despues-del-closeout-solo-hay-commits-de-desk
target_kind: test
target_identity: tests/test_integrate.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py
tags:
- system:deskops
- topic:integrate
---

# tip extendido tests-test_integrate-py

## Intent

materializa en tests/test_integrate.py el atom atom-integrate-extiende-el-tip-a-head-cuando-despues-del-closeout-solo-hay-commits-de-desk

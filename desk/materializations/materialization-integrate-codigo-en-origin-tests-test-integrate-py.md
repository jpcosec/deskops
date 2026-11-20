---
sldb:
  by: agent
  at: '2026-11-20T05:48:12Z'
  authority: generated
  via: create_document
id: materialization-integrate-codigo-en-origin-tests-test-integrate-py
title: integrate codigo en origin tests-test_integrate-py
source_atoms:
- atom-integrate-saltea-el-push-del-sha-de-codigo-cuando-ya-es-ancestro-de-origin
target_kind: test
target_identity: tests/test_integrate.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py
tags:
- system:deskops
- topic:integrate
---

# integrate codigo en origin tests-test_integrate-py

## Intent

materializa en tests/test_integrate.py el atom atom-integrate-saltea-el-push-del-sha-de-codigo-cuando-ya-es-ancestro-de-origin

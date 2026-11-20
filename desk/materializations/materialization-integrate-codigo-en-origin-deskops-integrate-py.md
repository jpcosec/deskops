---
sldb:
  by: agent
  at: '2026-11-20T05:48:04Z'
  authority: generated
  via: create_document
id: materialization-integrate-codigo-en-origin-deskops-integrate-py
title: integrate codigo en origin deskops-integrate-py
source_atoms:
- atom-integrate-saltea-el-push-del-sha-de-codigo-cuando-ya-es-ancestro-de-origin
target_kind: code
target_identity: deskops/integrate.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py
tags:
- system:deskops
- topic:integrate
---

# integrate codigo en origin deskops-integrate-py

## Intent

materializa en deskops/integrate.py el atom atom-integrate-saltea-el-push-del-sha-de-codigo-cuando-ya-es-ancestro-de-origin

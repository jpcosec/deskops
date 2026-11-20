---
sldb:
  by: agent
  at: '2026-11-20T11:05:15Z'
  authority: generated
  via: create_document
id: materialization-tip-extendido-deskops-integrate-py
title: tip extendido deskops-integrate-py
source_atoms:
- atom-integrate-extiende-el-tip-a-head-cuando-despues-del-closeout-solo-hay-commits-de-desk
target_kind: code
target_identity: deskops/integrate.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py
tags:
- system:deskops
- topic:integrate
---

# tip extendido deskops-integrate-py

## Intent

materializa en deskops/integrate.py el atom atom-integrate-extiende-el-tip-a-head-cuando-despues-del-closeout-solo-hay-commits-de-desk

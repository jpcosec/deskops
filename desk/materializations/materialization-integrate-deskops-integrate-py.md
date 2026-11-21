---
sldb:
  by: agent
  at: '2026-11-21T04:34:00Z'
  authority: generated
  via: create_document
id: materialization-integrate-deskops-integrate-py
title: integrate deskops-integrate-py
source_atoms:
- atom-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota
target_kind: code
target_identity: deskops/integrate.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py
tags:
- system:deskops
- topic:integrate
---

# integrate deskops-integrate-py

## Intent

materializa en deskops/integrate.py el atom atom-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota

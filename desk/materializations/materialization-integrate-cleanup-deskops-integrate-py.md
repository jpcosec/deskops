---
sldb:
  by: agent
  at: '2026-11-25T05:06:06Z'
  authority: generated
  via: create_document
id: materialization-integrate-cleanup-deskops-integrate-py
title: integrate-cleanup deskops-integrate-py
source_atoms:
- atom-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-ya-presentes-en-origin
target_kind: code
target_identity: deskops/integrate.py
validation:
- PYTHONPATH=. pytest -q tests/ sobre los tests de integrate tocados
tags:
- system:deskops
- topic:integrate-cleanup
---

# integrate-cleanup deskops-integrate-py

## Intent

materializa en deskops/integrate.py el atom atom-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-ya-presentes-en-origin

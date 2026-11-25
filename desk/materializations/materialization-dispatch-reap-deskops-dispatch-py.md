---
sldb:
  by: agent
  at: '2026-11-25T03:15:13Z'
  authority: generated
  via: create_document
id: materialization-dispatch-reap-deskops-dispatch-py
title: dispatch-reap deskops-dispatch-py
source_atoms:
- atom-el-reap-encola-el-tester-tras-integrar-un-ejecutor
target_kind: code
target_identity: deskops/dispatch.py
validation:
- pytest -q tests/test_dispatch.py
tags:
- system:deskops
- topic:dispatch-reap
---

# dispatch-reap deskops-dispatch-py

## Intent

materializa en deskops/dispatch.py el atom atom-el-reap-encola-el-tester-tras-integrar-un-ejecutor

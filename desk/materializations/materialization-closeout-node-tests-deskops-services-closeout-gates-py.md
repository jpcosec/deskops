---
sldb:
  by: agent
  at: '2026-11-25T21:14:35Z'
  authority: generated
  via: create_document
id: materialization-closeout-node-tests-deskops-services-closeout-gates-py
title: closeout-node-tests deskops-services-closeout_gates-py
source_atoms:
- atom-el-gate-de-tests-del-closeout-acepta-pruebas-de-node
target_kind: code
target_identity: deskops/services/closeout_gates.py
validation:
- pytest -q tests/test_closeout_test_paths.py
tags:
- system:deskops
- topic:closeout-node-tests
---

# closeout-node-tests deskops-services-closeout_gates-py

## Intent

materializa en deskops/services/closeout_gates.py el atom atom-el-gate-de-tests-del-closeout-acepta-pruebas-de-node

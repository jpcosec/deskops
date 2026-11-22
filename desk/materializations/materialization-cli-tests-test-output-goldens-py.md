---
sldb:
  by: agent
  at: '2026-11-22T09:28:15Z'
  authority: generated
  via: create_document
id: materialization-cli-tests-test-output-goldens-py
title: cli tests-test_output_goldens-py
source_atoms:
- atom-el-golden-de-help-de-deskops-drawer-refleja-la-descripcion-nueva-de-drawer-remove
target_kind: test
target_identity: tests/test_output_goldens.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
tags:
- system:deskops
- topic:cli
---

# cli tests-test_output_goldens-py

## Intent

materializa en tests/test_output_goldens.py el atom atom-el-golden-de-help-de-deskops-drawer-refleja-la-descripcion-nueva-de-drawer-remove

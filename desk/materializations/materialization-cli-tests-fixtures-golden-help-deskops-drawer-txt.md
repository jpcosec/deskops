---
sldb:
  by: agent
  at: '2026-11-22T09:26:50Z'
  authority: generated
  via: create_document
id: materialization-cli-tests-fixtures-golden-help-deskops-drawer-txt
title: cli tests-fixtures-golden-help-deskops_drawer-txt
source_atoms:
- atom-el-golden-de-help-de-deskops-drawer-refleja-la-descripcion-nueva-de-drawer-remove
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_drawer.txt
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
tags:
- system:deskops
- topic:cli
---

# cli tests-fixtures-golden-help-deskops_drawer-txt

## Intent

materializa en tests/fixtures/golden/help/deskops_drawer.txt el atom atom-el-golden-de-help-de-deskops-drawer-refleja-la-descripcion-nueva-de-drawer-remove

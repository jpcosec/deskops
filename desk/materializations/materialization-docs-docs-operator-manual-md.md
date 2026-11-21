---
sldb:
  by: agent
  at: '2026-11-21T20:28:36Z'
  authority: generated
  via: create_document
id: materialization-docs-docs-operator-manual-md
title: docs docs-operator-manual-md
source_atoms:
- atom-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal
target_kind: docs
target_identity: docs/operator-manual.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_skill_cli_drift.py
  tests/test_operator_manual.py
tags:
- system:deskops
- topic:docs
---

# docs docs-operator-manual-md

## Intent

materializa en docs/operator-manual.md el atom atom-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal

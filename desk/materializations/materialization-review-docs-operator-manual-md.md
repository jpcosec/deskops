---
sldb:
  by: agent
  at: '2026-11-21T08:40:10Z'
  authority: generated
  via: create_document
id: materialization-review-docs-operator-manual-md
title: review docs-operator-manual-md
source_atoms:
- atom-review-status-muestra-incomplete-para-un-recibo-dispuesto-como-incomplete
target_kind: docs
target_identity: docs/operator-manual.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_review_command.py
tags:
- system:deskops
- topic:review
---

# review docs-operator-manual-md

## Intent

materializa en docs/operator-manual.md el atom atom-review-status-muestra-incomplete-para-un-recibo-dispuesto-como-incomplete

---
sldb:
  by: agent
  at: '2026-11-21T08:40:21Z'
  authority: generated
  via: create_document
id: materialization-review-tests-test-review-command-py
title: review tests-test_review_command-py
source_atoms:
- atom-review-status-muestra-incomplete-para-un-recibo-dispuesto-como-incomplete
target_kind: test
target_identity: tests/test_review_command.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_review_command.py
tags:
- system:deskops
- topic:review
---

# review tests-test_review_command-py

## Intent

materializa en tests/test_review_command.py el atom atom-review-status-muestra-incomplete-para-un-recibo-dispuesto-como-incomplete

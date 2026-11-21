---
sldb:
  by: agent
  at: '2026-11-21T08:40:00Z'
  authority: generated
  via: create_document
id: materialization-review-deskops-services-review-py
title: review deskops-services-review-py
source_atoms:
- atom-review-status-muestra-incomplete-para-un-recibo-dispuesto-como-incomplete
target_kind: code
target_identity: deskops/services/review.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_review_command.py
tags:
- system:deskops
- topic:review
---

# review deskops-services-review-py

## Intent

materializa en deskops/services/review.py el atom atom-review-status-muestra-incomplete-para-un-recibo-dispuesto-como-incomplete

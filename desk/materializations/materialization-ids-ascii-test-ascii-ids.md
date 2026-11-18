---
sldb:
  by: agent
  at: '2026-11-18T21:26:54Z'
  authority: generated
  via: create_document
id: materialization-ids-ascii-test-ascii-ids
title: ids ascii test_ascii_ids
source_atoms:
- atom-los-ids-que-deskops-deriva-de-un-título-se-pliegan-a-ascii-y-los-ids-existentes-con-tilde-siguen-val
target_kind: test
target_identity: tests/test_ascii_ids.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_ascii_ids.py
tags:
- system:deskops
- topic:ids
---

# ids ascii test_ascii_ids

## Intent

materializa en tests/test_ascii_ids.py el atom atom-los-ids-que-deskops-deriva-de-un-título-se-pliegan-a-ascii-y-los-ids-existentes-con-tilde-siguen-val

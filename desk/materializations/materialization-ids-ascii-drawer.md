---
sldb:
  by: agent
  at: '2026-11-18T21:26:45Z'
  authority: generated
  via: create_document
id: materialization-ids-ascii-drawer
title: ids ascii drawer
source_atoms:
- atom-los-ids-que-deskops-deriva-de-un-título-se-pliegan-a-ascii-y-los-ids-existentes-con-tilde-siguen-val
target_kind: code
target_identity: deskops/services/drawer.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_ascii_ids.py
tags:
- system:deskops
- topic:ids
---

# ids ascii drawer

## Intent

materializa en deskops/services/drawer.py el atom atom-los-ids-que-deskops-deriva-de-un-título-se-pliegan-a-ascii-y-los-ids-existentes-con-tilde-siguen-val

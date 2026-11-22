---
sldb:
  by: agent
  at: '2026-11-22T20:03:19Z'
  authority: generated
  via: create_document
id: materialization-tags-deskops-atom-tags-py
title: tags deskops-atom_tags-py
source_atoms:
- atom-deskops-declara-el-namespace-de-tags-host
target_kind: code
target_identity: deskops/atom_tags.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_atom_tags.py tests/test_domain_tree.py
tags:
- system:deskops
- topic:tags
---

# tags deskops-atom_tags-py

## Intent

materializa en deskops/atom_tags.py el atom atom-deskops-declara-el-namespace-de-tags-host

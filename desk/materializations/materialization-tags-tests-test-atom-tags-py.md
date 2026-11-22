---
sldb:
  by: agent
  at: '2026-11-22T20:04:13Z'
  authority: generated
  via: create_document
id: materialization-tags-tests-test-atom-tags-py
title: tags tests-test_atom_tags-py
source_atoms:
- atom-deskops-declara-el-namespace-de-tags-host
target_kind: test
target_identity: tests/test_atom_tags.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_atom_tags.py tests/test_domain_tree.py
tags:
- system:deskops
- topic:tags
---

# tags tests-test_atom_tags-py

## Intent

materializa en tests/test_atom_tags.py el atom atom-deskops-declara-el-namespace-de-tags-host

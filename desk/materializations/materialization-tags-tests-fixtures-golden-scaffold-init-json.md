---
sldb:
  by: agent
  at: '2026-11-22T20:03:51Z'
  authority: generated
  via: create_document
id: materialization-tags-tests-fixtures-golden-scaffold-init-json
title: tags tests-fixtures-golden-scaffold-init-json
source_atoms:
- atom-deskops-declara-el-namespace-de-tags-host
target_kind: test
target_identity: tests/fixtures/golden/scaffold/init.json
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_atom_tags.py tests/test_domain_tree.py
tags:
- system:deskops
- topic:tags
---

# tags tests-fixtures-golden-scaffold-init-json

## Intent

materializa en tests/fixtures/golden/scaffold/init.json el atom atom-deskops-declara-el-namespace-de-tags-host

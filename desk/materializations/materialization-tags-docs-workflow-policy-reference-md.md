---
sldb:
  by: agent
  at: '2026-11-22T20:03:40Z'
  authority: generated
  via: create_document
id: materialization-tags-docs-workflow-policy-reference-md
title: tags docs-workflow-policy-reference-md
source_atoms:
- atom-deskops-declara-el-namespace-de-tags-host
target_kind: docs
target_identity: docs/workflow-policy-reference.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_atom_tags.py tests/test_domain_tree.py
tags:
- system:deskops
- topic:tags
---

# tags docs-workflow-policy-reference-md

## Intent

materializa en docs/workflow-policy-reference.md el atom atom-deskops-declara-el-namespace-de-tags-host

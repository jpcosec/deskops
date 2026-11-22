---
sldb:
  by: agent
  at: '2026-11-22T20:03:29Z'
  authority: generated
  via: create_document
id: materialization-tags-deskops-data-templates-atoms-tag-namespaces-yaml
title: tags deskops-data-templates-atoms-tag-namespaces-yaml
source_atoms:
- atom-deskops-declara-el-namespace-de-tags-host
target_kind: code
target_identity: deskops/data/templates/atoms/tag-namespaces.yaml
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_atom_tags.py tests/test_domain_tree.py
tags:
- system:deskops
- topic:tags
---

# tags deskops-data-templates-atoms-tag-namespaces-yaml

## Intent

materializa en deskops/data/templates/atoms/tag-namespaces.yaml el atom atom-deskops-declara-el-namespace-de-tags-host

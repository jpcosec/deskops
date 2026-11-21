---
sldb:
  by: agent
  at: '2026-11-21T17:22:46Z'
  authority: generated
  via: create_document
id: materialization-init-deskops-bootstrap-py
title: init deskops-bootstrap-py
source_atoms:
- atom-deskops-init-agrega-deskops-log-al-gitignore-del-repo
target_kind: code
target_identity: deskops/bootstrap.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_gitignore_policy.py
  tests/test_runtime_initializer.py
tags:
- system:deskops
- topic:init
---

# init deskops-bootstrap-py

## Intent

materializa en deskops/bootstrap.py el atom atom-deskops-init-agrega-deskops-log-al-gitignore-del-repo

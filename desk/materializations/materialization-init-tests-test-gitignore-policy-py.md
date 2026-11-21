---
sldb:
  by: agent
  at: '2026-11-21T17:22:56Z'
  authority: generated
  via: create_document
id: materialization-init-tests-test-gitignore-policy-py
title: init tests-test_gitignore_policy-py
source_atoms:
- atom-deskops-init-agrega-deskops-log-al-gitignore-del-repo
target_kind: test
target_identity: tests/test_gitignore_policy.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_gitignore_policy.py
  tests/test_runtime_initializer.py
tags:
- system:deskops
- topic:init
---

# init tests-test_gitignore_policy-py

## Intent

materializa en tests/test_gitignore_policy.py el atom atom-deskops-init-agrega-deskops-log-al-gitignore-del-repo

---
sldb:
  by: agent
  at: '2026-11-21T18:35:12Z'
  authority: generated
  via: create_document
id: materialization-cli-tests-test-cli-py
title: cli tests-test_cli-py
source_atoms:
- atom-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict
target_kind: test
target_identity: tests/test_cli.py
validation:
- 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_cli.py '
tags:
- system:deskops
- topic:cli
---

# cli tests-test_cli-py

## Intent

materializa en tests/test_cli.py el atom atom-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict

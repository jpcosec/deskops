---
sldb:
  by: agent
  at: '2026-11-21T18:35:01Z'
  authority: generated
  via: create_document
id: materialization-cli-deskops-cli-parse-input-py
title: cli deskops-cli-parse_input-py
source_atoms:
- atom-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict
target_kind: code
target_identity: deskops/cli/parse_input.py
validation:
- 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_cli.py '
tags:
- system:deskops
- topic:cli
---

# cli deskops-cli-parse_input-py

## Intent

materializa en deskops/cli/parse_input.py el atom atom-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict

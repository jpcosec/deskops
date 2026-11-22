---
sldb:
  by: agent
  at: '2026-11-22T04:57:39Z'
  authority: generated
  via: create_document
id: materialization-drawer-deskops-services-drawer-py
title: drawer deskops-services-drawer-py
source_atoms:
- atom-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-y-entradas-no-md-por-stem-y-registra-reas
target_kind: code
target_identity: deskops/services/drawer.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_inbox_promote_cli_gaps.py
  tests/test_retire_cli.py tests/test_add_task_from_drawer.py tests/test_cli_help_examples.py
tags:
- system:deskops
- topic:drawer
---

# drawer deskops-services-drawer-py

## Intent

materializa en deskops/services/drawer.py el atom atom-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-y-entradas-no-md-por-stem-y-registra-reas

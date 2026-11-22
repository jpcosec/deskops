---
sldb:
  by: agent
  at: '2026-11-22T04:58:10Z'
  authority: generated
  via: create_document
id: materialization-drawer-tests-test-inbox-promote-cli-gaps-py
title: drawer tests-test_inbox_promote_cli_gaps-py
source_atoms:
- atom-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-y-entradas-no-md-por-stem-y-registra-reas
target_kind: test
target_identity: tests/test_inbox_promote_cli_gaps.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_inbox_promote_cli_gaps.py
  tests/test_retire_cli.py tests/test_add_task_from_drawer.py tests/test_cli_help_examples.py
tags:
- system:deskops
- topic:drawer
---

# drawer tests-test_inbox_promote_cli_gaps-py

## Intent

materializa en tests/test_inbox_promote_cli_gaps.py el atom atom-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-y-entradas-no-md-por-stem-y-registra-reas

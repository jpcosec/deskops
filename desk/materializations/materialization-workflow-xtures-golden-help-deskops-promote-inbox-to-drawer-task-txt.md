---
sldb:
  by: agent
  at: '2026-11-20T15:18:12Z'
  authority: generated
  via: create_document
id: materialization-workflow-xtures-golden-help-deskops-promote-inbox-to-drawer-task-txt
title: workflow xtures-golden-help-deskops_promote_inbox-to-drawer-task-txt
source_atoms:
- atom-una-nota-del-inbox-no-va-al-drawer-la-skill-el-ritual-drawer-triage-la-ayuda-de-promote-y-los-docs-l
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_promote_inbox-to-drawer-task.txt
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_cli_help_goldens.py
tags:
- system:deskops
- topic:workflow
---

# workflow xtures-golden-help-deskops_promote_inbox-to-drawer-task-txt

## Intent

materializa en tests/fixtures/golden/help/deskops_promote_inbox-to-drawer-task.txt el atom atom-una-nota-del-inbox-no-va-al-drawer-la-skill-el-ritual-drawer-triage-la-ayuda-de-promote-y-los-docs-l

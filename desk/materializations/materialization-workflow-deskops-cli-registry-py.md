---
sldb:
  by: agent
  at: '2026-11-20T15:17:40Z'
  authority: generated
  via: create_document
id: materialization-workflow-deskops-cli-registry-py
title: workflow deskops-cli-registry-py
source_atoms:
- atom-una-nota-del-inbox-no-va-al-drawer-la-skill-el-ritual-drawer-triage-la-ayuda-de-promote-y-los-docs-l
target_kind: code
target_identity: deskops/cli/registry.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_cli_help_goldens.py
tags:
- system:deskops
- topic:workflow
---

# workflow deskops-cli-registry-py

## Intent

materializa en deskops/cli/registry.py el atom atom-una-nota-del-inbox-no-va-al-drawer-la-skill-el-ritual-drawer-triage-la-ayuda-de-promote-y-los-docs-l

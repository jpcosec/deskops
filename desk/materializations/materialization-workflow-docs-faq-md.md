---
sldb:
  by: agent
  at: '2026-11-20T15:13:35Z'
  authority: generated
  via: create_document
id: materialization-workflow-docs-faq-md
title: workflow docs-faq-md
source_atoms:
- atom-una-nota-del-inbox-no-va-al-drawer-la-skill-el-ritual-drawer-triage-la-ayuda-de-promote-y-los-docs-l
target_kind: docs
target_identity: docs/faq.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_cli_help_goldens.py
tags:
- system:deskops
- topic:workflow
---

# workflow docs-faq-md

## Intent

materializa en docs/faq.md el atom atom-una-nota-del-inbox-no-va-al-drawer-la-skill-el-ritual-drawer-triage-la-ayuda-de-promote-y-los-docs-l

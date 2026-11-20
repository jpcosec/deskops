---
sldb:
  by: agent
  at: '2026-11-20T15:17:13Z'
  authority: generated
  via: create_document
id: materialization-workflow-claude-skills-deskops-workflow-skill-md
title: workflow -claude-skills-deskops-workflow-SKILL-md
source_atoms:
- atom-una-nota-del-inbox-no-va-al-drawer-la-skill-el-ritual-drawer-triage-la-ayuda-de-promote-y-los-docs-l
target_kind: docs
target_identity: .claude/skills/deskops-workflow/SKILL.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_cli_help_goldens.py
tags:
- system:deskops
- topic:workflow
---

# workflow -claude-skills-deskops-workflow-SKILL-md

## Intent

materializa en .claude/skills/deskops-workflow/SKILL.md el atom atom-una-nota-del-inbox-no-va-al-drawer-la-skill-el-ritual-drawer-triage-la-ayuda-de-promote-y-los-docs-l

---
sldb:
  by: agent
  at: '2026-11-21T20:28:25Z'
  authority: generated
  via: create_document
id: materialization-docs-opencode-skills-use-deskops-skill-md
title: docs -opencode-skills-use-deskops-SKILL-md
source_atoms:
- atom-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal
target_kind: docs
target_identity: .opencode/skills/use-deskops/SKILL.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_skill_cli_drift.py
  tests/test_operator_manual.py
tags:
- system:deskops
- topic:docs
---

# docs -opencode-skills-use-deskops-SKILL-md

## Intent

materializa en .opencode/skills/use-deskops/SKILL.md el atom atom-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal

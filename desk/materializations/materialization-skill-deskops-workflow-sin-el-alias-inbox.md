---
sldb:
  by: agent
  at: '2026-11-17T01:11:41Z'
  authority: generated
  via: create_document
id: materialization-skill-deskops-workflow-sin-el-alias-inbox
title: Skill deskops-workflow sin el alias inbox
source_atoms:
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
target_kind: doc
target_identity: .claude/skills/deskops-workflow/SKILL.md
validation:
- pytest -q tests/test_skill_cli_drift.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---

# Skill deskops-workflow sin el alias inbox

## Intent

la skill documenta deskops message send para registrar huecos

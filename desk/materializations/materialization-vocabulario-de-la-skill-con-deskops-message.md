---
sldb:
  by: agent
  at: '2026-11-17T01:11:59Z'
  authority: generated
  via: create_document
id: materialization-vocabulario-de-la-skill-con-deskops-message
title: Vocabulario de la skill con deskops message
source_atoms:
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
target_kind: doc
target_identity: .claude/skills/deskops-workflow/references/vocabulary.md
validation:
- pytest -q tests/test_skill_cli_drift.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---

# Vocabulario de la skill con deskops message

## Intent

el vocabulario nombra deskops message para el inbox

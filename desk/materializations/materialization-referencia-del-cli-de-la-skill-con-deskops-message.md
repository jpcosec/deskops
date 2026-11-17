---
sldb:
  by: agent
  at: '2026-11-17T01:11:50Z'
  authority: generated
  via: create_document
id: materialization-referencia-del-cli-de-la-skill-con-deskops-message
title: Referencia del CLI de la skill con deskops message
source_atoms:
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
target_kind: doc
target_identity: .claude/skills/deskops-workflow/references/deskops-cli.md
validation:
- pytest -q tests/test_skill_cli_drift.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---

# Referencia del CLI de la skill con deskops message

## Intent

la referencia del CLI usa deskops message send|list|read|ack

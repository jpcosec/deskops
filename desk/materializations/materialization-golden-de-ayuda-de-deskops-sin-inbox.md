---
sldb:
  by: agent
  at: '2026-11-17T01:12:08Z'
  authority: generated
  via: create_document
id: materialization-golden-de-ayuda-de-deskops-sin-inbox
title: Golden de ayuda de deskops sin inbox
source_atoms:
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
target_kind: test
target_identity: tests/fixtures/golden/help/deskops.txt
validation:
- pytest -q tests/test_output_goldens.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---

# Golden de ayuda de deskops sin inbox

## Intent

la ayuda de deskops no lista el comando inbox

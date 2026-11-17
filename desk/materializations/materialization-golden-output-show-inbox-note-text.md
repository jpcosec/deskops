---
sldb:
  by: agent
  at: '2026-11-17T13:32:58Z'
  authority: generated
  via: create_document
id: materialization-golden-output-show-inbox-note-text
title: Golden output/show_inbox-note.text
source_atoms:
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
target_kind: test
target_identity: tests/fixtures/golden/output/show_inbox-note.text
validation:
- pytest -q tests/test_output_goldens.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---

# Golden output/show_inbox-note.text

## Intent

golden de deskops con el campo ack_reason de la nota del inbox

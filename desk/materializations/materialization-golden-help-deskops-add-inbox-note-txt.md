---
sldb:
  by: agent
  at: '2026-11-17T13:31:58Z'
  authority: generated
  via: create_document
id: materialization-golden-help-deskops-add-inbox-note-txt
title: Golden help/deskops_add_inbox-note.txt
source_atoms:
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_add_inbox-note.txt
validation:
- pytest -q tests/test_output_goldens.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---

# Golden help/deskops_add_inbox-note.txt

## Intent

golden de deskops con el campo ack_reason de la nota del inbox

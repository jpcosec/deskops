---
sldb:
  by: agent
  at: '2026-11-17T13:32:06Z'
  authority: generated
  via: create_document
id: materialization-golden-help-deskops-message-ack-txt
title: Golden help/deskops_message_ack.txt
source_atoms:
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_message_ack.txt
validation:
- pytest -q tests/test_output_goldens.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---

# Golden help/deskops_message_ack.txt

## Intent

golden de deskops con el campo ack_reason de la nota del inbox

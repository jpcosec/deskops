---
sldb:
  by: agent
  at: '2026-11-17T01:12:24Z'
  authority: generated
  via: create_document
id: materialization-tests-de-entrega-de-deskops-message
title: Tests de entrega de deskops message
source_atoms:
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
target_kind: test
target_identity: tests/test_message_delivery.py
validation:
- pytest -q tests/test_message_delivery.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---

# Tests de entrega de deskops message

## Intent

verifica la entrega de message send --to a otro desk

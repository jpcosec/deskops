---
sldb:
  by: agent
  at: '2026-11-17T01:12:16Z'
  authority: generated
  via: create_document
id: materialization-tests-del-cli-de-deskops-message
title: Tests del CLI de deskops message
source_atoms:
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
target_kind: test
target_identity: tests/test_message_cli.py
validation:
- pytest -q tests/test_message_cli.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---

# Tests del CLI de deskops message

## Intent

verifica message send|list|read|ack y que deskops inbox ya no es un comando

---
sldb:
  by: agent
  at: '2026-11-17T13:31:50Z'
  authority: generated
  via: create_document
id: materialization-modelo-de-nota-del-inbox-con-ack-reason
title: Modelo de nota del inbox con ack_reason
source_atoms:
- atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk
target_kind: code
target_identity: deskops/models/inbox.py
validation:
- pytest -q tests/test_message_cli.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-deskops-message-es-el-unico-comando-de-mensajeria-del-desk.md
---

# Modelo de nota del inbox con ack_reason

## Intent

la nota del inbox guarda el porque de su ack en ack_reason

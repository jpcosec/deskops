---
sldb:
  by: agent
  at: '2026-11-20T23:09:05Z'
  authority: generated
  via: create_document
id: materialization-messages-deskops-cli-commands-message-py
title: messages deskops-cli-commands-message-py
source_atoms:
- atom-se-borro-el-camino-legacy-de-deskops-message-sin-subcomando-es-un-error-de-uso
target_kind: code
target_identity: deskops/cli/commands/message.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
tags:
- system:deskops
- topic:messages
---

# messages deskops-cli-commands-message-py

## Intent

materializa en deskops/cli/commands/message.py el atom atom-se-borro-el-camino-legacy-de-deskops-message-sin-subcomando-es-un-error-de-uso

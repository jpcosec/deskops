---
sldb:
  by: agent
  at: '2026-11-20T23:09:25Z'
  authority: generated
  via: create_document
id: materialization-messages-tests-test-inbox-promote-cli-gaps-py
title: messages tests-test_inbox_promote_cli_gaps-py
source_atoms:
- atom-se-borro-el-camino-legacy-de-deskops-message-sin-subcomando-es-un-error-de-uso
target_kind: test
target_identity: tests/test_inbox_promote_cli_gaps.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
tags:
- system:deskops
- topic:messages
---

# messages tests-test_inbox_promote_cli_gaps-py

## Intent

materializa en tests/test_inbox_promote_cli_gaps.py el atom atom-se-borro-el-camino-legacy-de-deskops-message-sin-subcomando-es-un-error-de-uso

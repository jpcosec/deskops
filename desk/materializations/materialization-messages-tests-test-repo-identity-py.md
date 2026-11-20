---
sldb:
  by: agent
  at: '2026-11-20T23:09:45Z'
  authority: generated
  via: create_document
id: materialization-messages-tests-test-repo-identity-py
title: messages tests-test_repo_identity-py
source_atoms:
- atom-se-borro-el-camino-legacy-de-deskops-message-sin-subcomando-es-un-error-de-uso
target_kind: test
target_identity: tests/test_repo_identity.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
tags:
- system:deskops
- topic:messages
---

# messages tests-test_repo_identity-py

## Intent

materializa en tests/test_repo_identity.py el atom atom-se-borro-el-camino-legacy-de-deskops-message-sin-subcomando-es-un-error-de-uso

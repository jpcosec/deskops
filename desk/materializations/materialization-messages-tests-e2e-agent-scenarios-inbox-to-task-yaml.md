---
sldb:
  by: agent
  at: '2026-11-20T23:09:15Z'
  authority: generated
  via: create_document
id: materialization-messages-tests-e2e-agent-scenarios-inbox-to-task-yaml
title: messages tests-e2e_agent-scenarios-inbox-to-task-yaml
source_atoms:
- atom-se-borro-el-camino-legacy-de-deskops-message-sin-subcomando-es-un-error-de-uso
target_kind: test
target_identity: tests/e2e_agent/scenarios/inbox-to-task.yaml
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
tags:
- system:deskops
- topic:messages
---

# messages tests-e2e_agent-scenarios-inbox-to-task-yaml

## Intent

materializa en tests/e2e_agent/scenarios/inbox-to-task.yaml el atom atom-se-borro-el-camino-legacy-de-deskops-message-sin-subcomando-es-un-error-de-uso

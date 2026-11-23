---
sldb:
  by: agent
  at: '2026-11-23T11:17:17Z'
  authority: generated
  via: create_document
id: materialization-identity-deskops-cli-registry-py
title: identity deskops-cli-registry-py
source_atoms:
- atom-al-llegar-una-nota-al-inbox-deskops-despierta-a-la-identidad-scion-del-desk-si-su-config-lo-pide
target_kind: code
target_identity: deskops/cli/registry.py
validation:
- 'pytest -n 4 tests/test_message_delivery.py tests/test_message_cli.py tests/test_config.py
  tests/test_output_goldens.py tests/test_queue.py con PYTHONPATH al worktree limpio
  de 465b442b: verdes; la unica falla (test_command_registry, repo whoami) es de init-id
  intento 1, en arreglo'
tags:
- system:deskops
- topic:identity
---

# identity deskops-cli-registry-py

## Intent

materializa en deskops/cli/registry.py el atom atom-al-llegar-una-nota-al-inbox-deskops-despierta-a-la-identidad-scion-del-desk-si-su-config-lo-pide

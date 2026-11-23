---
sldb:
  by: agent
  at: '2026-11-23T14:59:16Z'
  authority: generated
  via: create_document
id: materialization-ownership-deskops-cli-commands-repo-py
title: ownership deskops-cli-commands-repo-py
source_atoms:
- atom-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-y-deskops-owner-responde-el-dueno
target_kind: code
target_identity: deskops/cli/commands/repo.py
validation:
- 'pytest -n 3 tests/test_message_ecosystem_registry.py tests/test_config.py tests/test_cli.py
  tests/test_cli_grammar.py tests/test_message_cli.py tests/test_command_registry.py
  tests/test_repo_identity.py tests/test_model_contract_snapshot.py tests/test_output_goldens.py
  con PYTHONPATH al worktree limpio de 05ac75a9: 166 passed; doctor sin errores de
  RepositoryDoc'
tags:
- system:deskops
- topic:ownership
---

# ownership deskops-cli-commands-repo-py

## Intent

materializa en deskops/cli/commands/repo.py el atom atom-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-y-deskops-owner-responde-el-dueno

---
sldb:
  by: agent
  at: '2026-11-23T15:01:44Z'
  authority: generated
  via: create_document
id: materialization-ownership-tests-test-cli-py
title: ownership tests-test_cli-py
source_atoms:
- atom-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-y-deskops-owner-responde-el-dueno
target_kind: test
target_identity: tests/test_cli.py
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

# ownership tests-test_cli-py

## Intent

materializa en tests/test_cli.py el atom atom-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-y-deskops-owner-responde-el-dueno

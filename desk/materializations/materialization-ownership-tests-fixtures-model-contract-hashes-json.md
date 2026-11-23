---
sldb:
  by: agent
  at: '2026-11-23T15:01:31Z'
  authority: generated
  via: create_document
id: materialization-ownership-tests-fixtures-model-contract-hashes-json
title: ownership tests-fixtures-model_contract_hashes-json
source_atoms:
- atom-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-y-deskops-owner-responde-el-dueno
target_kind: test
target_identity: tests/fixtures/model_contract_hashes.json
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

# ownership tests-fixtures-model_contract_hashes-json

## Intent

materializa en tests/fixtures/model_contract_hashes.json el atom atom-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-y-deskops-owner-responde-el-dueno

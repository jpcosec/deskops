---
sldb:
  by: agent
  at: '2026-11-23T15:00:30Z'
  authority: generated
  via: create_document
id: materialization-ownership-tests-fixtures-golden-help-deskops-owner-txt
title: ownership tests-fixtures-golden-help-deskops_owner-txt
source_atoms:
- atom-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-y-deskops-owner-responde-el-dueno
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_owner.txt
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

# ownership tests-fixtures-golden-help-deskops_owner-txt

## Intent

materializa en tests/fixtures/golden/help/deskops_owner.txt el atom atom-la-ficha-de-repo-del-registro-declara-owns-paths-y-owns-topics-y-deskops-owner-responde-el-dueno

---
sldb:
  by: agent
  at: '2026-11-23T12:34:33Z'
  authority: generated
  via: create_document
id: materialization-identity-tests-test-command-registry-py
title: identity tests-test_command_registry-py
source_atoms:
- atom-deskops-init-id-fija-la-project-identity-repo-whoami-set-la-cambia-por-cli-y-repo-register-avisa
target_kind: test
target_identity: tests/test_command_registry.py
validation:
- 'pytest -n 2 tests/test_repo_identity.py tests/test_command_registry.py tests/test_scaffold_golden.py
  tests/test_output_goldens.py tests/test_registry_robustness.py con PYTHONPATH al
  worktree limpio de 91626206: 33 passed'
tags:
- system:deskops
- topic:identity
---

# identity tests-test_command_registry-py

## Intent

materializa en tests/test_command_registry.py el atom atom-deskops-init-id-fija-la-project-identity-repo-whoami-set-la-cambia-por-cli-y-repo-register-avisa

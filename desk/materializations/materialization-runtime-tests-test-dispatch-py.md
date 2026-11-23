---
sldb:
  by: agent
  at: '2026-11-23T13:17:25Z'
  authority: generated
  via: create_document
id: materialization-runtime-tests-test-dispatch-py
title: runtime tests-test_dispatch-py
source_atoms:
- atom-runtime-template-de-scion-escribe-image-resources-volumes-kubernetes-y-telemetry-en-scion-env-yaml-y
target_kind: test
target_identity: tests/test_dispatch.py
validation:
- 'pytest -n 3 tests/test_scion_runtime.py tests/test_dispatch.py tests/test_output_goldens.py
  tests/test_runtime_profiles.py tests/test_command_registry.py tests/test_role_runtime_artifacts.py
  con PYTHONPATH al worktree limpio de 1858aca9: 125 passed'
tags:
- system:deskops
- topic:runtime
---

# runtime tests-test_dispatch-py

## Intent

materializa en tests/test_dispatch.py el atom atom-runtime-template-de-scion-escribe-image-resources-volumes-kubernetes-y-telemetry-en-scion-env-yaml-y

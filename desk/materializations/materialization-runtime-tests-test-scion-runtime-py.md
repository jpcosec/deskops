---
sldb:
  by: agent
  at: '2026-11-22T08:16:03Z'
  authority: generated
  via: create_document
id: materialization-runtime-tests-test-scion-runtime-py
title: runtime tests-test_scion_runtime-py
source_atoms:
- atom-los-contenedores-de-scion-traen-pytest-xdist-y-la-suite-completa-corre-con-n-4
target_kind: test
target_identity: tests/test_scion_runtime.py
validation:
- 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py '
tags:
- system:deskops
- topic:runtime
---

# runtime tests-test_scion_runtime-py

## Intent

materializa en tests/test_scion_runtime.py el atom atom-los-contenedores-de-scion-traen-pytest-xdist-y-la-suite-completa-corre-con-n-4

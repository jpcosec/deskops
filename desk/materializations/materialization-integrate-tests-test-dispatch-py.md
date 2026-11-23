---
sldb:
  by: agent
  at: '2026-11-23T01:56:43Z'
  authority: generated
  via: create_document
id: materialization-integrate-tests-test-dispatch-py
title: integrate tests-test_dispatch-py
source_atoms:
- atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada
target_kind: test
target_identity: tests/test_dispatch.py
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_config.py tests/test_dispatch.py
  tests/test_integrate.py
tags:
- system:deskops
- topic:integrate
---

# integrate tests-test_dispatch-py

## Intent

materializa en tests/test_dispatch.py el atom atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada

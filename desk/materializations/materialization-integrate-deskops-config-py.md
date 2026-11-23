---
sldb:
  by: agent
  at: '2026-11-23T01:56:08Z'
  authority: generated
  via: create_document
id: materialization-integrate-deskops-config-py
title: integrate deskops-config-py
source_atoms:
- atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada
target_kind: code
target_identity: deskops/config.py
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_config.py tests/test_dispatch.py
  tests/test_integrate.py
tags:
- system:deskops
- topic:integrate
---

# integrate deskops-config-py

## Intent

materializa en deskops/config.py el atom atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada

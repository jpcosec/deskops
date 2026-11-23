---
sldb:
  by: agent
  at: '2026-11-23T01:56:19Z'
  authority: generated
  via: create_document
id: materialization-integrate-deskops-dispatch-py
title: integrate deskops-dispatch-py
source_atoms:
- atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada
target_kind: code
target_identity: deskops/dispatch.py
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_config.py tests/test_dispatch.py
  tests/test_integrate.py
tags:
- system:deskops
- topic:integrate
---

# integrate deskops-dispatch-py

## Intent

materializa en deskops/dispatch.py el atom atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada

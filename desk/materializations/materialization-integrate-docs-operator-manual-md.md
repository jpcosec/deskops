---
sldb:
  by: agent
  at: '2026-11-23T01:56:32Z'
  authority: generated
  via: create_document
id: materialization-integrate-docs-operator-manual-md
title: integrate docs-operator-manual-md
source_atoms:
- atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada
target_kind: docs
target_identity: docs/operator-manual.md
validation:
- TMPDIR=/dev/shm python -m pytest -q tests/test_config.py tests/test_dispatch.py
  tests/test_integrate.py
tags:
- system:deskops
- topic:integrate
---

# integrate docs-operator-manual-md

## Intent

materializa en docs/operator-manual.md el atom atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada

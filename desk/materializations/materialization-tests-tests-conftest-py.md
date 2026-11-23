---
sldb:
  by: agent
  at: '2026-11-23T16:12:28Z'
  authority: generated
  via: create_document
id: materialization-tests-tests-conftest-py
title: tests tests-conftest-py
source_atoms:
- atom-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-gracias-a-una-fixture-autouse-que-limpia
target_kind: test
target_identity: tests/conftest.py
validation:
- 'systemd-run --user --scope -p MemoryMax=2G pytest -p no:xdist tests en worktree
  limpio de 196f3cb9: sin OOM, 1376 passed, 3 failed solo por PATH sin el venv (pytest
  127); esos 3 pasan con PATH del venv bajo el mismo tope'
tags:
- system:deskops
- topic:tests
---

# tests tests-conftest-py

## Intent

materializa en tests/conftest.py el atom atom-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-gracias-a-una-fixture-autouse-que-limpia

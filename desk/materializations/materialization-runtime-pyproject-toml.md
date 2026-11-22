---
sldb:
  by: agent
  at: '2026-11-22T08:15:52Z'
  authority: generated
  via: create_document
id: materialization-runtime-pyproject-toml
title: runtime pyproject-toml
source_atoms:
- atom-los-contenedores-de-scion-traen-pytest-xdist-y-la-suite-completa-corre-con-n-4
target_kind: code
target_identity: pyproject.toml
validation:
- 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py '
tags:
- system:deskops
- topic:runtime
---

# runtime pyproject-toml

## Intent

materializa en pyproject.toml el atom atom-los-contenedores-de-scion-traen-pytest-xdist-y-la-suite-completa-corre-con-n-4

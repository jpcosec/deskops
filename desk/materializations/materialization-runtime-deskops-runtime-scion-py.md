---
sldb:
  by: agent
  at: '2026-11-22T08:15:42Z'
  authority: generated
  via: create_document
id: materialization-runtime-deskops-runtime-scion-py
title: runtime deskops-runtime-scion-py
source_atoms:
- atom-los-contenedores-de-scion-traen-pytest-xdist-y-la-suite-completa-corre-con-n-4
target_kind: code
target_identity: deskops/runtime/scion.py
validation:
- 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py '
tags:
- system:deskops
- topic:runtime
---

# runtime deskops-runtime-scion-py

## Intent

materializa en deskops/runtime/scion.py el atom atom-los-contenedores-de-scion-traen-pytest-xdist-y-la-suite-completa-corre-con-n-4

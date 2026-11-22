---
sldb:
  by: agent
  at: '2026-11-22T19:19:16Z'
  authority: generated
  via: create_document
id: materialization-dispatch-deskops-runtime-scion-py
title: dispatch deskops-runtime-scion-py
source_atoms:
- atom-cada-intento-de-dispatch-tiene-su-propio-rundoc-con-intencion-y-confirmacion-separadas
target_kind: code
target_identity: deskops/runtime/scion.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py tests/test_closeout.py
tags:
- system:deskops
- topic:dispatch
---

# dispatch deskops-runtime-scion-py

## Intent

materializa en deskops/runtime/scion.py el atom atom-cada-intento-de-dispatch-tiene-su-propio-rundoc-con-intencion-y-confirmacion-separadas

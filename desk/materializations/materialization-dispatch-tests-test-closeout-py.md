---
sldb:
  by: agent
  at: '2026-11-22T19:19:48Z'
  authority: generated
  via: create_document
id: materialization-dispatch-tests-test-closeout-py
title: dispatch tests-test_closeout-py
source_atoms:
- atom-cada-intento-de-dispatch-tiene-su-propio-rundoc-con-intencion-y-confirmacion-separadas
target_kind: test
target_identity: tests/test_closeout.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py tests/test_closeout.py
tags:
- system:deskops
- topic:dispatch
---

# dispatch tests-test_closeout-py

## Intent

materializa en tests/test_closeout.py el atom atom-cada-intento-de-dispatch-tiene-su-propio-rundoc-con-intencion-y-confirmacion-separadas

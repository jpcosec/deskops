---
sldb:
  by: agent
  at: '2026-11-22T19:19:37Z'
  authority: generated
  via: create_document
id: materialization-dispatch-tests-fixtures-model-contract-hashes-json
title: dispatch tests-fixtures-model_contract_hashes-json
source_atoms:
- atom-cada-intento-de-dispatch-tiene-su-propio-rundoc-con-intencion-y-confirmacion-separadas
target_kind: test
target_identity: tests/fixtures/model_contract_hashes.json
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py tests/test_closeout.py
tags:
- system:deskops
- topic:dispatch
---

# dispatch tests-fixtures-model_contract_hashes-json

## Intent

materializa en tests/fixtures/model_contract_hashes.json el atom atom-cada-intento-de-dispatch-tiene-su-propio-rundoc-con-intencion-y-confirmacion-separadas

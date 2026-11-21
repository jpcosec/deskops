---
sldb:
  by: agent
  at: '2026-11-21T12:04:22Z'
  authority: generated
  via: create_document
id: materialization-models-tests-test-model-contract-snapshot-py
title: models tests-test_model_contract_snapshot-py
source_atoms:
- atom-el-snapshot-de-contratos-de-modelo-acepta-el-cambio-solo-de-descripcion-de-ruledoc
target_kind: test
target_identity: tests/test_model_contract_snapshot.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py
tags:
- system:deskops
- topic:models
---

# models tests-test_model_contract_snapshot-py

## Intent

materializa en tests/test_model_contract_snapshot.py el atom atom-el-snapshot-de-contratos-de-modelo-acepta-el-cambio-solo-de-descripcion-de-ruledoc

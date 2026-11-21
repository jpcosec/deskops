---
sldb:
  by: agent
  at: '2026-11-21T12:03:04Z'
  authority: generated
  via: create_document
id: materialization-models-tests-fixtures-model-contract-hashes-json
title: models tests-fixtures-model_contract_hashes-json
source_atoms:
- atom-el-snapshot-de-contratos-de-modelo-acepta-el-cambio-solo-de-descripcion-de-ruledoc
target_kind: test
target_identity: tests/fixtures/model_contract_hashes.json
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py
tags:
- system:deskops
- topic:models
---

# models tests-fixtures-model_contract_hashes-json

## Intent

materializa en tests/fixtures/model_contract_hashes.json el atom atom-el-snapshot-de-contratos-de-modelo-acepta-el-cambio-solo-de-descripcion-de-ruledoc

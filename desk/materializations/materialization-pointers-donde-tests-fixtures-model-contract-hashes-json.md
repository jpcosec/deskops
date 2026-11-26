---
sldb:
  by: agent
  at: '2026-11-26T03:24:40Z'
  authority: generated
  via: create_document
id: materialization-pointers-donde-tests-fixtures-model-contract-hashes-json
title: pointers-donde tests-fixtures-model_contract_hashes-json
source_atoms:
- atom-atomos-pills-y-tareas-guardan-el-donde-como-punteros
target_kind: test
target_identity: tests/fixtures/model_contract_hashes.json
validation:
- pytest -q tests/test_where_pointers.py tests/test_model_contract_snapshot.py tests/test_output_goldens.py
  tests/test_view_goldens.py
tags:
- system:deskops
- topic:pointers-donde
---

# pointers-donde tests-fixtures-model_contract_hashes-json

## Intent

materializa en tests/fixtures/model_contract_hashes.json el atom atom-atomos-pills-y-tareas-guardan-el-donde-como-punteros

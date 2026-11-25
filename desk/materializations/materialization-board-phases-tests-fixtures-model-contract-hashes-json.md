---
sldb:
  by: agent
  at: '2026-11-25T12:38:23Z'
  authority: generated
  via: create_document
id: materialization-board-phases-tests-fixtures-model-contract-hashes-json
title: board-phases tests-fixtures-model_contract_hashes-json
source_atoms:
- atom-el-board-declara-las-fases-del-dag
target_kind: test
target_identity: tests/fixtures/model_contract_hashes.json
validation:
- pytest -q tests/test_board_phases.py tests/test_model_contract_snapshot.py
tags:
- system:deskops
- topic:board-phases
---

# board-phases tests-fixtures-model_contract_hashes-json

## Intent

materializa en tests/fixtures/model_contract_hashes.json el atom atom-el-board-declara-las-fases-del-dag

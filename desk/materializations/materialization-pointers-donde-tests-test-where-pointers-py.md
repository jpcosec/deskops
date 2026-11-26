---
sldb:
  by: agent
  at: '2026-11-26T03:25:10Z'
  authority: generated
  via: create_document
id: materialization-pointers-donde-tests-test-where-pointers-py
title: pointers-donde tests-test_where_pointers-py
source_atoms:
- atom-atomos-pills-y-tareas-guardan-el-donde-como-punteros
target_kind: test
target_identity: tests/test_where_pointers.py
validation:
- pytest -q tests/test_where_pointers.py tests/test_model_contract_snapshot.py tests/test_output_goldens.py
  tests/test_view_goldens.py
tags:
- system:deskops
- topic:pointers-donde
---

# pointers-donde tests-test_where_pointers-py

## Intent

materializa en tests/test_where_pointers.py el atom atom-atomos-pills-y-tareas-guardan-el-donde-como-punteros

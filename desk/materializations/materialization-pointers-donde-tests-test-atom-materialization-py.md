---
sldb:
  by: agent
  at: '2026-11-26T03:24:55Z'
  authority: generated
  via: create_document
id: materialization-pointers-donde-tests-test-atom-materialization-py
title: pointers-donde tests-test_atom_materialization-py
source_atoms:
- atom-atomos-pills-y-tareas-guardan-el-donde-como-punteros
target_kind: test
target_identity: tests/test_atom_materialization.py
validation:
- pytest -q tests/test_where_pointers.py tests/test_model_contract_snapshot.py tests/test_output_goldens.py
  tests/test_view_goldens.py
tags:
- system:deskops
- topic:pointers-donde
---

# pointers-donde tests-test_atom_materialization-py

## Intent

materializa en tests/test_atom_materialization.py el atom atom-atomos-pills-y-tareas-guardan-el-donde-como-punteros

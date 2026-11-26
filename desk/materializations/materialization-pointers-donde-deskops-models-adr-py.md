---
sldb:
  by: agent
  at: '2026-11-26T03:24:10Z'
  authority: generated
  via: create_document
id: materialization-pointers-donde-deskops-models-adr-py
title: pointers-donde deskops-models-adr-py
source_atoms:
- atom-atomos-pills-y-tareas-guardan-el-donde-como-punteros
target_kind: code
target_identity: deskops/models/adr.py
validation:
- pytest -q tests/test_where_pointers.py tests/test_model_contract_snapshot.py tests/test_output_goldens.py
  tests/test_view_goldens.py
tags:
- system:deskops
- topic:pointers-donde
---

# pointers-donde deskops-models-adr-py

## Intent

materializa en deskops/models/adr.py el atom atom-atomos-pills-y-tareas-guardan-el-donde-como-punteros

---
sldb:
  by: agent
  at: '2026-11-24T20:14:53Z'
  authority: generated
  via: create_document
id: materialization-tags-deskops-tag-migration-py
title: tags deskops-tag_migration-py
source_atoms:
- atom-un-solo-vocabulario-de-tags-semanticos-en-deskops-resuelto-por-el-store-semantico-de-sldb
target_kind: code
target_identity: deskops/tag_migration.py
validation:
- 'main limpio: pytest test_tag_vocabulary, test_cli_grammar, test_command_registry,
  test_domain_tree y test_specs 27 passed; sldb find board.tareas 50 = tareas del
  desk, board.tareas.ui 1; tester PASA'
tags:
- system:deskops
- topic:tags
---

# tags deskops-tag_migration-py

## Intent

materializa en deskops/tag_migration.py el atom atom-un-solo-vocabulario-de-tags-semanticos-en-deskops-resuelto-por-el-store-semantico-de-sldb

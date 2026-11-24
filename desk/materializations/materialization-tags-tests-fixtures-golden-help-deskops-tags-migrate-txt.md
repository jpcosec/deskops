---
sldb:
  by: agent
  at: '2026-11-24T20:16:06Z'
  authority: generated
  via: create_document
id: materialization-tags-tests-fixtures-golden-help-deskops-tags-migrate-txt
title: tags tests-fixtures-golden-help-deskops_tags_migrate-txt
source_atoms:
- atom-un-solo-vocabulario-de-tags-semanticos-en-deskops-resuelto-por-el-store-semantico-de-sldb
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_tags_migrate.txt
validation:
- 'main limpio: pytest test_tag_vocabulary, test_cli_grammar, test_command_registry,
  test_domain_tree y test_specs 27 passed; sldb find board.tareas 50 = tareas del
  desk, board.tareas.ui 1; tester PASA'
tags:
- system:deskops
- topic:tags
---

# tags tests-fixtures-golden-help-deskops_tags_migrate-txt

## Intent

materializa en tests/fixtures/golden/help/deskops_tags_migrate.txt el atom atom-un-solo-vocabulario-de-tags-semanticos-en-deskops-resuelto-por-el-store-semantico-de-sldb

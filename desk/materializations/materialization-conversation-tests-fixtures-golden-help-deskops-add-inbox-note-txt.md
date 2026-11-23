---
sldb:
  by: agent
  at: '2026-11-23T18:55:38Z'
  authority: generated
  via: create_document
id: materialization-conversation-tests-fixtures-golden-help-deskops-add-inbox-note-txt
title: conversation tests-fixtures-golden-help-deskops_add_inbox-note-txt
source_atoms:
- atom-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-message-send-y-list-atoms-aceptan-conv
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_add_inbox-note.txt
validation:
- 'worktree limpio de main con 3db148a0 y 44e71c26: pytest -n 3 tests/test_atoms_cli.py
  tests/test_message_cli.py tests/test_model_contract_snapshot.py tests/test_output_goldens.py
  tests/test_message_delivery.py 43 passed; deskops doctor sin errores de AtomDoc
  ni InboxNoteDoc'
tags:
- system:deskops
- topic:conversation
---

# conversation tests-fixtures-golden-help-deskops_add_inbox-note-txt

## Intent

materializa en tests/fixtures/golden/help/deskops_add_inbox-note.txt el atom atom-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-message-send-y-list-atoms-aceptan-conv

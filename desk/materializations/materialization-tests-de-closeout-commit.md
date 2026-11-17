---
sldb:
  by: agent
  at: '2026-11-17T02:03:48Z'
  authority: generated
  via: create_document
id: materialization-tests-de-closeout-commit
title: Tests de closeout commit
source_atoms:
- atom-code-changes-close-with-tests-and-commit
target_kind: test
target_identity: tests/test_closeout.py
validation:
- pytest -q tests/test_closeout.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-code-changes-close-with-tests-and-commit.md
---

# Tests de closeout commit

## Intent

verifica closeout commit, incluido que no amienda un commit citado como evidencia de commit

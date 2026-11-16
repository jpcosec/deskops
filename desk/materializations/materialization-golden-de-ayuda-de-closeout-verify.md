---
sldb:
  by: agent
  at: '2026-11-16T23:31:53Z'
  authority: generated
  via: create_document
id: materialization-golden-de-ayuda-de-closeout-verify
title: Golden de ayuda de closeout verify
source_atoms:
- atom-code-changes-close-with-tests-and-commit
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_closeout_verify.txt
validation:
- pytest -q tests/test_output_goldens.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-code-changes-close-with-tests-and-commit.md
---

# Golden de ayuda de closeout verify

## Intent

golden de la ayuda de deskops closeout verify, con --run-dir

---
sldb:
  by: agent
  at: '2026-11-17T07:52:14Z'
  authority: generated
  via: create_document
id: materialization-golden-de-ayuda-de-closeout
title: Golden de ayuda de closeout
source_atoms:
- atom-code-changes-close-with-tests-and-commit
target_kind: test
target_identity: tests/fixtures/golden/help/deskops_closeout.txt
validation:
- pytest -q tests/test_output_goldens.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-code-changes-close-with-tests-and-commit.md
---

# Golden de ayuda de closeout

## Intent

golden de la ayuda de deskops closeout, con verify descrito como escritor de recibos sin commit

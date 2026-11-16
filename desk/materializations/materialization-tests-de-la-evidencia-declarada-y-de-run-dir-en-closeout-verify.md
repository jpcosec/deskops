---
sldb:
  by: agent
  at: '2026-11-16T23:31:44Z'
  authority: generated
  via: create_document
id: materialization-tests-de-la-evidencia-declarada-y-de-run-dir-en-closeout-verify
title: Tests de la evidencia declarada y de run-dir en closeout verify
source_atoms:
- atom-code-changes-close-with-tests-and-commit
target_kind: test
target_identity: tests/test_closeout_declared_evidence.py
validation:
- pytest -q tests/test_closeout_declared_evidence.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-code-changes-close-with-tests-and-commit.md
---

# Tests de la evidencia declarada y de run-dir en closeout verify

## Intent

verifica que closeout verify reporta la evidencia declarada y, con --run-dir, la evidencia de run-dir que exige closeout commit
